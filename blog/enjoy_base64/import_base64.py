#! /usr/bin/env python
# -*- coding:utf-8 -*-

import base64

data = "motouchi"

print(("data:{}").format(data))
# base 64でencode
enc_data = base64.encodestring(data.encode("utf8")).decode("ascii")
# そんなデータを出力
print(("encode data:{}").format(enc_data))
# decodeするよ
dec_data = base64.decodestring(enc_data.encode("ascii")).decode("utf8")
# そんなデータを出力
print (("decode data:{}").format(dec_data))
