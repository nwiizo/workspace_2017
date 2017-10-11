#! /bin/bash
# bitcoind monitor shell
#
SROOT=$(cd $(dirname "$0"); pwd)
cd $SROOT

BITCOIND_RPC="bitcoin-cli "
WANIP=`curl -sL https://ip.btc.com`

HEIGHT=`$BITCOIND_RPC getinfo | grep "blocks" | awk '{print $2}' | awk -F"," '{print $1}'`
CONNS=`$BITCOIND_RPC getinfo | grep "connections" | awk '{print $2}' | awk -F"," '{print $1}'`

SERVICE="bpool.bitcoind.$WANIP"
VALUE="height:$HEIGHT;conn:$CONNS;"
MURL="https://monitor.btc.com/monitor/api/v1/message?service=$SERVICE&value=$VALUE"

if [[ $CONNS -ne 0 ]]; then
  curl --max-time 30 $MURL
  exit 0
fi
