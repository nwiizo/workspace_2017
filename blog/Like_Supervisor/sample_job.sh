#!/bin/bash
sleep 20
NOWTIME=`date -u +"%Y/%m/%d %I:%M:%S"`
DF=`df -h -i`
echo "${NOWTIME}"
echo -e "$n"
echo -e "${DF}"
