#!/bin/sh
#/etc/iproute2/rt_tablesに追記
#200 gate1
#201 gate2


IP0=*.*.*.* # eth0のIPアドレス
IP1=*.*.*.* # eth1のIPアドレス

IF0=eth0
IF1=eth1
GATEWAY0=*.*.*.* # IP1,IF1のゲートウェイアドレス
GATEWAY1=*.*.*.* # IP2,IF2のゲートウェイアドレス
IP0_NET=*.*.*.*/* # IP1,GATEWAY1のネットワークアドレス
IP1_NET=*.*.*.*/* # IP2,GATEWAY2のネットワークアドレス
TABLE0_NAME=* # /etc/iproute2/rt_tablesに追記したルートテーブル名1
TABLE1_NAME=* # /etc/iproute2/rt_tablesに追記したルートテーブル名2


ip route add $IP0_NET dev $IF0 src $IP0 table $TABLE0_NAME
ip route add default via $GATEWAY0 table $TABLE0_NAME
ip rule add from $IP0 table $TABLE0_NAME
ip route add default via $GATEWAY0 metric 15

ip route add $IP1_NET dev $IF1 src $IP1 table $TABLE1_NAME
ip route add default via $GATEWAY1 table $TABLE1_NAME
ip rule add from $IP1 table $TABLE1_NAME
ip route add default via $GATEWAY1 metric 10
