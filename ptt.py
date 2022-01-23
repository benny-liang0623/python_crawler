import requests
from bs4 import BeautifulSoup
import shutil
import os
import time
from fake_useragent import UserAgent

os.mkdir("img")

url = "https://www.ptt.cc/bbs/Beauty/index.html"

while True:
    ua = UserAgent()
    header = {'user-agent':ua.random,'cookie': 'over18=1;'}
    rq = requests.get(url , headers=header)
    bsrq = BeautifulSoup(rq.text)

    title_url = bsrq.select(".title a")
    title_url_list = []
    for i in title_url:
        if "大尺碼" in i.text:
            continue
        else:
            title_url_list.append(i["href"])

    for new_url in title_url_list:
        picture_url_list = []
        new_rq = requests.get("https://www.ptt.cc"+new_url , headers=header)
        new_bsrq = BeautifulSoup(new_rq.text)
        picture_url = new_bsrq.select(".richcontent img")
        for p_url in picture_url:
            picture_url_list.append(p_url["src"])
        for download_picture in picture_url_list:
            try:
                fname = download_picture.split("/")[6].split("?")[0]
                print(fname)
                res2 = requests.get(download_picture, stream=True)
                pics = open("img//"+fname, 'wb') #將取得的圖檔名稱寫入電腦資料夾，w=write、b=binary、r=read
                shutil.copyfileobj(res2.raw, pics) #raw原始資料
                pics.close()
                time.sleep(0.5)
            except:
                continue

    page_num = bsrq.select(".btn.wide")
    if page_num == []:
        break
    else:
        url="https://www.ptt.cc"+page_num[1]["href"]
        print(url)
        time.sleep(1)