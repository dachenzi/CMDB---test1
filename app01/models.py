from django.db import models

# Create your models here.


class Host(models.Model):
    '''
    存放主机信息
    '''
    hostname = models.CharField(max_length=32)
    hostip = models.GenericIPAddressField(max_length=32)
    diskinfo = models.ForeignKey('Disk')
    meminfo = models.ForeignKey('Mem')
    cpu = models.ForeignKey('Cpu')


class Cpu(models.Model):
    '''
    存放主机CPU相关信息
    '''
    cpu_name = models.CharField(max_length=64)
    cpu_count = models.IntegerField()

class Mem(models.Model):
    '''
    存放主机内存相关信息
    '''
    memtotal = models.CharField(max_length=32)
    memfree = models.CharField(max_length=32)
    mempercent = models.CharField(max_length=32)

class Disk(models.Model):
    '''
    存放主机磁盘相关信息
    '''
    disksize = models.CharField(max_length=32)
    diskused = models.CharField(max_length=32)
    diskaval = models.CharField(max_length=32)
    diskuse = models.CharField(max_length=32)