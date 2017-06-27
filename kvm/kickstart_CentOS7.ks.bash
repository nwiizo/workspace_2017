#!/bin/bash

cat <<EOS> /tmp/centos7.ks.cfg
#version=RHEL7
install
cdrom
text
cmdline
skipx
lang en_US.UTF-8
keyboard --vckeymap=jp106 --xlayouts=jp
timezone Asia/Tokyo --isUtc --nontp
network --activate --bootproto=dhcp --noipv6
zerombr
bootloader --location=mbr
clearpart --all --initlabel
part / --fstype=xfs --grow --size=1 --asprimary --label=root
rootpw --plaintext <password>
auth --enableshadow --passalgo=sha512
selinux --disabled
firewall --disabled
firstboot --disabled
reboot
%packages
%end
EOS
