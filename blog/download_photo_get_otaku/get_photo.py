#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import sys
from urllib import request
import os.path
import os
import time
import re 


# url先の画像を保存する関数
def download(url):
    url = "http://www.keyakizaka46.com/"+ url
    headers = {
              "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
                      }
    req = request.Request(url, None, headers)
    img = request.urlopen(req)
    localfile = open(os.path.basename(url), 'wb')
    localfile.write(img.read())
    img.close()
    localfile.close()


# shutterstockの画像検索結果を保存
# アクセス先遷移
#par_url = 'http://www.keyakizaka46.com/mob/news/diarKiji.php?site=k46o&ima=0000&cd=member&ct=17'
#imoはページ数 ctはメンバー数
def page_info(url):
    url = url + "&ima=" + str("0".zfill(4))
    url = url + "&cd=member&ct=" + str("17")
    return url

def main():
    par_url = "http://www.keyakizaka46.com/mob/news/diarKiji.php?site=k46o"

    par_url = page_info(par_url)
# urlアクセス
    res = request.urlopen(par_url)
# beautifulsoupでパース
    soup = BeautifulSoup(res.read(),"html.parser")
# 
    pattern = r"/img"
# ページに存在するimgタグを検索
    for link in soup.find_all('img'):
# 画像URLを取得
        img_url = link.get('src')
        match_img = re.match(pattern,img_url)
        if match_img:
            #print (img_url)
# ローカルに画像をダウンロード
            download(img_url)
#なんとなく待ちましょう
            time.sleep(10)
        else:
            pass

if __name__ == '__main__':
    main()


