#!/usr/bin/env python
#-*- coding: utf-8 -*-

from flask import Flask
from flask import request
import MySQLdb


app = Flask(__name__)

@app.route('/')
def kadai_1():
    return "MOTOUCHI FLASK PAGE"


DATABASE = 'mysql://root:*********@127.0.0.1/filmsdb'

@app.route('/db')
def db_save():
    category_name = ['アクション','SF','コメテﾞィ','サスヘﾟンス','時代劇','アニメ']
    title_cat = ""
    connector = MySQLdb.connect(db="filmsdb", user="root", passwd="****",charset="utf8")
    #connector = MySQLdb.connect(db="filmsdb", user="root")
    connector.cursorclass = MySQLdb.cursors.DictCursor
    cursor = connector.cursor()
    cursor.execute("SET NAMES utf8")
    sql = "select * from films_title where category_id = 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        title_cat = title_cat  + str(category_name[row["category_id"]-1]) + ":"\
        + str(row["title"].encode("utf-8")) + "</p>"
    return title_cat
    cursor.close()
    connector.close()
    return "FIN"

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=80)#!/usr/bin/env python
#-*- coding: utf-8 -*-

from flask import Flask
from flask import request
import MySQLdb


app = Flask(__name__)

@app.route('/')
def kadai_1():
    return "MOTOUCHI FLASK PAGE"


DATABASE = 'mysql://root:*********@127.0.0.1/filmsdb'

@app.route('/db')
def db_save():
    category_name = ['アクション','SF','コメテﾞィ','サスヘﾟンス','時代劇','アニメ']
    title_cat = ""
    connector = MySQLdb.connect(db="filmsdb", user="root", passwd="****",charset="utf8")
    #connector = MySQLdb.connect(db="filmsdb", user="root")
    connector.cursorclass = MySQLdb.cursors.DictCursor
    cursor = connector.cursor()
    cursor.execute("SET NAMES utf8")
    sql = "select * from films_title where category_id = 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        title_cat = title_cat  + str(category_name[row["category_id"]-1]) + ":"\
        + str(row["title"].encode("utf-8")) + "</p>"
    return title_cat
    cursor.close()
    connector.close()
    return "FIN"

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0', port=80)
