yum -y localinstall http://repo.zabbix.com/zabbix/2.4/rhel/6/x86_64/zabbix-release-2.4-1.el6.noarch.rpm
yum -y install zabbix-agent zabbix-sender


ZABBIX_SERVER='**.**.**.**'
ZABBIX_INT='eth**'

sed -i -e '
/^Server=/ s/=.*/='$ZABBIX_SERVER'/
/^ServerActive=/ s/=.*/='$ZABBIX_SERVER'/
/^Hostname=/ s/=.*/='$(uname -n)'/
/# ListenIP=/ a ListenIP=127.0.0.1,'$(ip -o -4 addr show $ZABBIX_INT primary | awk '{print $4}' | sed 's/\/.*//')'
' /etc/zabbix/zabbix_agentd.conf

service zabbix-agent start
chkconfig zabbix-agent on
