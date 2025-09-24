import ddddocr#导入识别验证码的包
import os#删除文件

def get_url(s):
    # 实例化一个ocr对象
    element = s.query_selector("#codeImg")
    photograph = "element_screenshot.png"
    element.screenshot(path=photograph)
    ocr = ddddocr.DdddOcr()

    # 图像文件路径
    img_path = photograph

    # 读取图像文件并转换为二进制数据
    with open(img_path, 'rb') as f:
        img_bytes = f.read()
    os.remove(photograph)

    # 识别验证码
    result = ocr.classification(img_bytes)

    return result