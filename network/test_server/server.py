#!/usr/bin/env python
# -*- coding: utf-8 -*-

import BaseHTTPServer # HTTPサーバ
import CGIHTTPServer # CGI機能付HTTPサーバ
import cgitb # CGIのためのデバッグ用ライブラリ
import logging

# ログを出力するための自作ハンドラー
class LoggingHandler(CGIHTTPServer.CGIHTTPRequestHandler):
    # ファイル出力するロガーの準備
    __logger = logging.getLogger('httpd')
    fh = logging.FileHandler('log.txt')
    format = logging.Formatter('%(message)s')
    fh.setFormatter(format)
    __logger.addHandler(fh)
    __logger.setLevel(logging.DEBUG) # Debug以上のログレベルで指定されたログを出力
    
    def log_message(self, format, *args):
        # デフォルトの出力機能
        CGIHTTPServer.CGIHTTPRequestHandler.log_message(self, format, *args)
        # 独自のファイル出力機能
        self.__logger.info('%s - - [%s] %s' % (
            self.client_address[0], self.log_date_time_string(), format%args))
        self.__logger.info('%s' % (self.headers))
        #for line in self.rfile:
        #    self.__logger.info('%s' % (line))

if '__main__' == __name__:
    # CGIのデバッグ機能を有効にする
    cgitb.enable()
    
    server = BaseHTTPServer.HTTPServer # ベースとなるHTTPサーバモジュールを用意
    handler = LoggingHandler # リクエストがあったときにCGIとして処理するモジュールを用意 (ログ出力付き)
    server_address = ('', 8000) # サーバのポート番号を指定
    
    httpd = server(server_address, handler) # すべてを合体
    try:
        httpd.serve_forever() # サーバを実行
    except KeyboardInterrupt:
        httpd.socket.close() # キー操作で終了されたら、ソケットを閉じる
