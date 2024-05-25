#!/bin/bash

echo "操作系统信息:"
uname -a
echo
lsb_release -a
echo
cat /etc/os-release
echo

echo "系统架构:"
uname -m
echo

echo "内核版本:"
uname -r
echo

echo "CPU详细信息:"
lscpu
echo
#cat /proc/cpuinfo
#echo

echo "内存使用情况:"
free -h
echo

echo "磁盘使用情况:"
df -h
echo

echo "分区信息:"
lsblk
echo
fdisk -l
echo

echo "温度信息:"
if command -v sensors &> /dev/null
then
    sensors
else
    echo "lm-sensors 未安装。请使用您的包管理器安装 lm-sensors。"
fi
echo

echo "网络接口及IP地址:"
ip addr
echo

echo "路由表:"
ip route
echo

echo "系统启动时间:"
uptime
echo

#echo "系统加载信息:"
#dmesg | tail -n 20
#echo

#echo "系统日志:"
#journalctl -n 20

