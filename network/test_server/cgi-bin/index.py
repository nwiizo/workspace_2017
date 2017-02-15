#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import os

# HTTPヘッダーを表示する関数
def show_header():
    print 'Content-type: text/html'
    print

# POSTデータをファイルに追記    
def write_post_comments(name, comments):
    fp = open('data.txt','a')
    # 名前とコメントを縦線で合体させて保存する
    # もし本文中に改行があれば、<br>に置き換える
    fp.write(name + '|' + comments.replace('\n', '<br>') + '\n')
    fp.close()

# HTMLの最初の部分を表示
def show_html_header():
    # HTMLヘッダーを表示
    print '<html><head><title>Hello, World!</title>'
    print '<meta charset="UTF-8"></head>'
    # body開始
    print '<body>'
    # 入力フォームも表示
    print '<form action="index.py" method="post">'
    print '<h1>BBS</h1>'
    print '<table border="0">'
    print '<tr><td align="right"><b>Name: </b></td><td><input type="text" name="name" size="30" maxlength="20"></td></tr>'
    print '<tr><td align="right"><b>Comments: </b></td><td><textarea name="comments" rows="4" cols="40"></textarea></td></tr>'
    print '<tr><td></td><td><input type="submit" value="submit"></td></tr>'
    print '</table>'
    print '</form>'

# BBSの記事を表示
def show_bbs_items():
    # ファイルを開いて、一行ずつ表示する
    fp = open('data.txt', 'r')
    item_list = []
    for line in fp:
        line = line.strip()
        if '' == line:
            continue
        splitted_line = line.split('|') # 縦線で文字列を分割
        print '<div class="item" style="margin: 10px; padding: 5px; border: 1px solid #000000;">'
        print '    <div class="name">Name: ' + splitted_line[0] + '</div>'
        print '    <div class="comments">Comments: ' + splitted_line[1] + '</div>'
        print '</div>'
    fp.close

# HTMLの最後の部分を表示
def show_html_footer():
    print '</body></html>'

# ここからプログラムが始まります
if '__main__' == __name__:
    # パラメータを読み込みます
    form = cgi.FieldStorage()
    
    # もしPOSTメソッドによるアクセスだったら
    if 'POST' == os.environ['REQUEST_METHOD']:
        # フォーム情報にnameとcommentsがあるか確認
        if form.has_key('name') and form.has_key('comments'):
            write_post_comments(form.getvalue('name'),
                                form.getvalue('comments'))
    
    # HTTPヘッダーを表示
    show_header()

    # HTMLを表示
    show_html_header()
    show_bbs_items()
    show_html_footer()
