#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import sys
from urllib import request
import os.path
import os
import re 
import threading
 
# url先の画像を保存する関数
def download(url):
    url = "http://www.keyakizaka46.com"+ url
    headers = {
              "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
                      }
    print(url)
    req = request.Request(url, None, headers)
    img = request.urlopen(req)
    localfile = open(os.path.basename(url), 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()

def download_instance(url,page,n):
    for i in range(n):
        p_s = str(int(page) + i)
        par_url = url + "&id=" + p_s
        print(par_url)
        res = request.urlopen(par_url) # beautifulsoupでパース
        soup = BeautifulSoup(res.read(),"html.parser")
        pattern = r"/files/14/diary/k46/member/moblog/"
# ページに存在するimgタグを検索
        for link in soup.find_all('img'):
# 画像URLを取得
            img_url = link.get('src')
            match_img = re.search(pattern,img_url)
            if match_img:
                #print ("http://www.keyakizaka46.com"+img_url)
# ローカルに画像をダウンロード
                download(img_url)
            else:
                pass

#http://www.keyakizaka46.com/mob/news/diarKijiShw.php?site=k46o&ima=0000&id=(101から始まる記事番号)&cd=member

def main():
    par_url = "http://www.keyakizaka46.com/mob/news/diarKijiShw.php?site=k46o&ima=0000&id="
    page = 101 + int(input("start page:"))
    n = int(input("get page:"))
    t1 = threading.Thread(target=download_instance, name="download_instance", args=(par_url,page,n))
    t1.start()
    t1.join()
    print("end")
if __name__ == '__main__':
    main()
