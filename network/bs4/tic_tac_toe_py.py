#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import re
import socket
import itertools


def print_board(b):
    print("{0:^3}|{1:^3}|{2:^3}".format(b[0], b[1], b[2]))
    print("---+---+---")
    print("{0:^3}|{1:^3}|{2:^3}".format(b[3], b[4], b[5]))
    print("---+---+---")
    print("{0:^3}|{1:^3}|{2:^3}".format(b[6], b[7], b[8]))


# ['X', '', 'O', 'O', 'X', '', 'X', 'O', 'X']
# ['', 'X', '', '', 'O', '', '', '', '']

"""
一番強い(というか最善手の) AIアルゴリズム

1. 置けば勝てるなら置く
2. 敵が勝ちそうであれば妨害する
3. 優先順位的に真ん中 -> 端 におく
4. それも空いていない場合は 諦めて 適当な場所に置く.
"""

#lines = (
#    (0, 1, 2), (3, 4, 5), (6, 7, 8),
#    (0, 3, 6), (1, 4, 7), (2, 5, 8),
#    (2, 4, 6), (0, 4, 8))

lines = ((0, 1, 2), (3, 4, 5))


# my_hand で勝てるかどうか? 勝てるのであれば置くべき場所を返す
def is_win(board, my_hand):
    for pos in lines:
        for ps in itertools.permutations(pos):
            p = board[ps[0]]
            if p == "" and board[ps[1]] == my_hand and board[ps[2]] == my_hand:
                return ps[0]
    return -1  # わからんw


def is_draw(board):
    rest_board = [x for x, y in enumerate(board) if y == ""]
    if len(rest_board) <= 2:
        if is_win(board, "O") == -1 and is_win(board, "X") == -1:
            return True
    return False


# 今の状態から次にどこに置くかを決定する
def decide_pos(board, my_hand):
    enemy_hand = ""
    if my_hand == "X":
        enemy_hand = "O"
    else:
        enemy_hand = "X"

    # もし勝てるのであれば勝つ
    p = is_win(board, my_hand)
    if p >= 0:
        return p

    # もし負けるのであれば妨害を入れる
    p = is_win(board, enemy_hand)
    if p >= 0:
        return p

    # もし中央が空いていればそこに置く.
    if board[4] == "":
        return 4

    # もし隅が空いていれば隅の適当な場所に置く.
    corner = (0, 2, 6, 8)
    for c in corner:
        if board[c] == "":
            return c

    # それ以外の場合は適当に置く.
    for c in range(9):
        if board[c] == "":
            return c
    return None


def read_board(sc_board):
    """
    t is following input.
     X |   |
    ---+---+---
       |   |
    ---+---+---
       |   |
    """
    board = []
    sc = sc_board.replace("---+---+---", "").split("\n")
    for s in sc:
        if s != "":
            s = map(lambda x: x.strip(), s.split("|"))
            for k in s:
                board.append(k)
    return board


def sock(reip, report):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((reip, report))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s, s.makefile('rw')


def read_until(f, delim='\n'):
    data = ""
    while not data.endswith(delim):
        data += f.read(1)
    return data


def main():
    # HOST = "tic-tac-toe.2016.volgactf.ru"
    # HOST = "95.213.237.93"
    HOST = "95.213.237.91"
    PORT = 45679
    s, f = sock(HOST, PORT)
    print(read_until(f), end="")
    print(read_until(f), end="")
    s.sendall(b'jtwp470\n')
    print(read_until(f, "\n\n"))

    print(read_until(f), end="")  # Round number X.
    print(read_until(f), end="")  # Server vs. k. Current score: 0.5 - 0.5

    # 最初に2行読み込む.
    # もし Round が入っていたら 一度リセット
    # my_hand = "O"
    while True:
        inp = ""
        inp += read_until(f)
        inp += read_until(f)
        if "Round" in inp:
            m = re.match(r"Round number (\d+).", inp.split("\n")[0])
            round_number = int(m.group(1))

            print("Round : %d " % round_number)
            print(inp)
            # 偶数の時は自分は X
            # if round_number % 2 == 0:
            #  my_hand = "O"
            #else:
            #    my_hand = "X"

            #print("my_hand is : " + my_hand)

            inp = ""
            inp += read_until(f)
            inp += read_until(f)

        inp += read_until(f)
        inp += read_until(f)
        inp += read_until(f)
        inp += read_until(f)
        board = read_board(inp)

        my_hand = board[4]
        if my_hand == "" or my_hand == "X":
            my_hand = "X"
        else:
            my_hand = "O"
        print("MY_HAND: %s" % my_hand)
        x = decide_pos(board, my_hand)
        if x is not None:
            s.sendall((str(x) + "\n").encode())
            print("Send: % d" % x)
        print_board(board)

    s.close()
    f.close()


def test():
    ## test_code
    board = ['X', 'X', '',
             '', '', '',
             '', '', '']
    assert decide_pos(board, "X") == 2
    board = ['X', '', 'O',
             'O', 'O', '',
             '', '', '']

    # 妨害を入れる
    assert decide_pos(board, "X") == 5
    board = ['X', 'O', '',
             'O', '', '',
             '', '', '']
    assert decide_pos(board, "X") == 4

    board = ['X', 'O', 'X',
             'O', 'O', 'X',
             'X', 'X', 'O']

    print(decide_pos(board, "X"))

if __name__ == "__main__":
    main()
