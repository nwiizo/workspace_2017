#!/usr/bin/env python3
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    print("先輩の誕生日いつですか?")
    year = int(input("年は?:"))
    month = int(input("月は?:"))
    day = int(input("何日?:"))
    C = year/100
    Y = year%100
    F = int(day) + (26*(int(month)+1)/10) + int(Y) + (int(Y)/4) + 5*C + (C/4)
    X = (F % 7) + 1
    week = ["土","日","月","火","水","木","金"]
    print(week[int(X)]+"曜日です",)
    print(str(year) +"年"+str(month) + "月"+ str(day) +"日は"+ \
           str(week[int(X)])+"曜日でした")
    print("ひょっとして全部覚えてるの??")
    print("いえ、モジュロ演算というのを使って…当たってました?")
    print("ごめん、何曜日か知らないや!!")
