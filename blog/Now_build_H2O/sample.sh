#!/bin/bash
yum groupinstall "Development Tools"
yum -y install cmake openssl-devel git
yum -y install curl curl-devel libarchive libarchive-devel expat expat-devel zlib zlib-devel openssl cname
yum -y install php-fpm
yum -y install rpmforget
cd ~
git clone --depth=1 https://github.com/h2o/h2o.git
cd h2o
cmake -DWITH_BUNDLED_SSL=off .
make && make install
examples/h2o/h2o.conf << EOS
file.custom-handler:
  extension: .php
  fastcgi.connect:
    host: 127.0.0.1
    port: 9000
    type: tcp
EOS
./h2o -c examples/h2o/h2o.conf
