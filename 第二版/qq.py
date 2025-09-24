from bs4 import BeautifulSoup
from transformation import time_to_seconds


def get_html(html_1):
    soup = BeautifulSoup(html_1, 'html.parser')
    ase = soup.find("div", class_="yee-dt-main-wrap")
    course_list = []

    # 假设你想要遍历所有class以"dt-table1-r"开头的tr元素
    rows = ase.find_all("tr", class_=lambda x: x and x.startswith("dt-table1-r"))

    for ases in rows:
        acssce = ases.find("td", style="text-align: left;").text  # 课程名称
        viewingDuration = ases.find_all("td", align="center")[3].text
        videoDuration = ases.find_all("td", align="center")[4].text
        viewingDuration = time_to_seconds(viewingDuration)
        videoDuration = time_to_seconds(videoDuration)
        course_list.append({'name': acssce, 'time_1': viewingDuration, 'time_2': videoDuration})

    return course_list

