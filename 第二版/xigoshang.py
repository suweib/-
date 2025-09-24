from playwright.sync_api import sync_playwright#导入同步模块
from sjk import readMysql#数据库模块
from yzm import get_url as yzm#验证码识别
from qq import get_html
import time
import asyncio




def main():
    with sync_playwright() as p:  # 同步模块
        result = readMysql()  # 读取数据库信息

        for i in result[1:]:
            username = i[1]
            password = i[0]
            browser = p.firefox.launch(headless=False,args=["--mute-audio"])  # 启动浏览器
            context = browser.new_context()# 创建浏览器上下文
            page = context.new_page()  # 打开新页面



            page.goto('https://bxait.hongmukej.com/user/login', wait_until='domcontentloaded')  # 访问网址
            page.wait_for_timeout(3000)  # 等待3秒
            page.fill('#username', username)  # 输入用户名
            page.fill('#password', password)  # 输入密码
            yzm_1=yzm(page)
            page.fill('#code',yzm_1)
            page.click('.btn')
            page.wait_for_timeout(3000)
            page.reload(wait_until='networkidle')#刷新页面
            if page.url == 'https://bxait.hongmukej.com/user/login':
                while True:  # 添加循环，直到登录成功
                    page.reload(wait_until='networkidle')
                    page.wait_for_timeout(3000)
                    page.fill('#username', username)  # 输入用户名
                    page.fill('#password', password)  # 输入密码
                    yzm_2 = yzm(page)
                    page.fill('#code', yzm_2)
                    page.click('.btn')
                    page.wait_for_timeout(3000)
                    # 检查是否登录成功
                    if page.url != 'https://bxait.hongmukej.com/user/login':
                        page.reload(wait_until='networkidle')
                        break  # 登录成功，退出循环
            time.sleep(5)
            page.wait_for_selector('.user-course .item')
            courses = page.locator('.user-course .item').all()
            initial_page_handle=page.url# 保存当前页面数据，每次循环结束后跳转
            # 循环点击每个高亮元素
            for course in courses:

                course.locator('.img').click()
                page.get_by_text('学习成绩').click()

                prev_class_schedule = None

                while True:
                    time.sleep(3)
                    html_2 = page.content()
                    class_schedule = get_html(html_2)
                    if class_schedule == prev_class_schedule:
                        break
                    prev_class_schedule = class_schedule
                    for course_1 in class_schedule:
                        if course_1['time_1'] <course_1['time_2']:

                            with page.expect_popup()  as new_page_info:
                                page.get_by_text(course_1['name']).first.click()

                            # 获取新标签页
                                time.sleep(2)
                                new_page = new_page_info.value
                                new_page.wait_for_load_state()

                                if new_page:

                                    new_page.locator('.courseplay-video').click()

                                    time.sleep(5)
                                    try:
                                        if new_page.locator('#layui-layer1'):
                                            yzm_3 = yzm(new_page)
                                            new_page.locator('input[placeholder="请输入验证码"]').nth(1).fill(yzm_3)
                                            new_page.get_by_text('开始播放').click()
                                    finally:
                                        time.sleep(10 + int(course_1['time_2']) - int(course_1['time_1']))
                                        new_page.close()




                                else:
                                    time.sleep(1)
                        elif course_1['time_1'] >= course_1['time_2']:
                            continue

                    page.wait_for_timeout(3000)

                    page.get_by_text('下一页').click()





                # highlight_elements = page.locator('.pagebar-bbs .list.page-btn').all()
                # third_last_text = highlight_elements[-3].text_content()
                # print(third_last_text)

                page.goto(initial_page_handle)#回到初始页面



if __name__ == '__main__':
    max_retries = 99
    retry_count = 0
    while True:
        try:
            main()
            # 成功执行后重置重试计数
            retry_count = 0
            time.sleep(10)
        except Exception as e:
            retry_count += 1
            print(f"错误: {e}")
            print(f"重试次数: {retry_count}/{max_retries}")

            if retry_count >= max_retries:
                print("达到最大重试次数，程序退出")

                break

            time.sleep(10)


