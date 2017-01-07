#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import re

def parser(): 
    usage = 'Usage:python <FILE> [-b <bust size>] [-i] [-u <under>] [-t <top>] [--help]'\
            .format(__file__)
    parser = ArgumentParser(usage=usage)
    parser.add_argument('-b','--bust',dest='bust_size',help='you want to know the bust size(A ~ H)infomation ')
    parser.add_argument('-i','--infomation',dest='bust_list',help='infomation' )
    parser.add_argument('-u','--under',dest='under',type=int,help='bust infor' )
    parser.add_argument('-t','--top',dest='top',type=int,help='bust infomation' )
    args = parser.parse_args()
    if args.bust_size:
        return '{}'.format(cup(args.bust_size))
    if args.bust_list:
        return '{}'.format(cup_info(args.bust_list))
    if args.under and args.top:
        return '{}'.format(cup_cal(args.under,args.top))

def default():
    print ('AA')
    return '( ﾟ∀ﾟ)o彡°'
def cup(size):
    if size.upper() == "AA":
        return ('{} cup is very like, Call me ***-****-****').format(size)
    elif size.upper() == 'A':
        return ('{} :Angel').format(size)
    elif size.upper() == 'B':        
        return ('{} :Beautiful' ).format(size)
    elif size.upper() == 'C':        
        return ('{} :Creative').format(size)
    elif size.upper() == 'D':        
        return ('{} :Deluxe').format(size)
    elif size.upper() == 'E':        
        return ('{} :Elegant').format(size)
    elif size.upper() == 'F':
        return ('{} :Fantastic').format(size)
    else:
        return ('{} :女性の敵').format(size)
def cup_info(bust):
    cup = ['AA','A','B','C','D','E','F','G','H']
    diff = [7.5,10.0,12.5,15.0,17.5,20.0,22,5,25.0,27,5]
    return ('The difference between the top and the under is {} cm').format(diff[cup.index(bust.upper())])

def cup_cal(under,top):
    cup = ['AA','A','B','C','D','E','F','G','H']
    diff = [7.5,10.0,12.5,15.0,17.5,20.0,22,5,25.0,27,5]
    op_diff = top - under
    for n in diff:
        if op_diff > n:
            return ('{}{}').format(cup[(diff.index(n))],under)
            break
        else:
            pass
    return 'UNKNOW'

if __name__ == '__main__':
    result = parser()
    print(result)
