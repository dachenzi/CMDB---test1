#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# OS: CentOS 6.7
# Version: 2.7.6
# Description: 收集系统相关信息
# Time: 2017/10/09
# Auth: Dahlhin

from subprocess import Popen,PIPE
import socket
import requests
import json

def getcpuinfo():
    p = Popen(['cat','/proc/cpuinfo'],stdout=PIPE,stderr=PIPE)
    info,err = p.communicate()
    if not err:
        info = info.split('\n')
        cpu_count = 0
        cpu_name = ''
        for line in info:
            if line.startswith('processor'):
                cpu_count += 1
            if cpu_name:
                pass
            else:
                if line.startswith('model name'):
                    cpu_name = line.split(':')[1].split()
                    cpu_name = ' '.join(cpu_name)
        return (cpu_count,cpu_name)

def getloadavg():
    p = Popen(['uptime'],stdout=PIPE,stderr=PIPE)
    loadavg,err = p.communicate()
    if not err:
        loadavg = loadavg.split(',')[3].split(':')[1].replace(' ','')
    return loadavg

def getcpupercent():
    p = Popen(['top','-bin1'],stdout=PIPE,stderr=PIPE)
    info,err = p.communicate()
    if not err:
        cpu_percent = info.split('\n')[2].split()[1].split('%')[0]
    return cpu_percent

def getmeminfo():
    p = Popen(['cat','/proc/meminfo'],stdout=PIPE,stderr=PIPE)
    info,err = p.communicate()
    if not err:
        info = info.split('\n')
        for line in info:
            if line.startswith('MemTotal'):
               MemTotal = int(line.split()[1])
            if line.startswith('MemFree'):
               MemFree = int(line.split()[1])
    Mempercent = '%.02f' % (float(MemFree)/float(MemTotal)  * 100 ) + '%'
    MemTotal = str(MemTotal/1024) + 'M'
    MemFree = str(MemFree/1024) + 'M'
    return (MemTotal,MemFree,Mempercent)

def getdiskinfo():
    p = Popen(['df','-h'],stdout=PIPE,stderr=PIPE)
    info = p.stdout
    if not p.stderr.read():
        for line in info:
            if line.endswith('/\n'):
                disksize = line.split()[0]
                diskused = line.split()[1]
                diskaval = line.split()[2]
                diskuse = line.split()[3]
    return (disksize,diskused,diskaval,diskuse)

def hostinfo():
    hostname = socket.gethostname()
    p = Popen(['ifconfig','eth0'],stdout=PIPE)
    for line in p.stdout:
        if line.strip().startswith('inet addr:'):
            hostip = line.split()[1].split(':')[1]
    return (hostname,hostip)

if __name__ == '__main__':
    cpu_count,cpu_name = getcpuinfo()
    cpu_percent = getcpupercent()
    loadavg = getloadavg()
    MemTotal,MemFree,Mempercent = getmeminfo()
    disksize,diskused,diskaval,diskuse = getdiskinfo()
    hostname,hostip = hostinfo()
    data = {
    'cpu':
    {'cpu_count': cpu_count, 'cpu_name': cpu_name, 'cpu_percent': cpu_percent, 'loadavg':loadavg},
    'mem':
    {'MemTotal': MemTotal, 'MemFree': MemFree, 'Mempercent': Mempercent},
    'disk':
    {'disksize': disksize, 'diskused': diskused, 'diskaval': diskaval, 'diskuse': diskuse},
    'host':
    {'hostname': hostname, 'hostip': hostip}
    }
    r = requests.post('http://10.10.12.174:8888/show_data/',data=json.dumps(data))
    print(json.dumps(data))



