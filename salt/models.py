# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Projects(models.Model):
    project_name = models.CharField(max_length=50,unique=True)
    filter_re = models.CharField(max_length=100, null="Ture", blank='Ture')
    update_cmd = models.CharField(max_length=1000, null="Ture", blank='Ture')
    project_desc = models.TextField(max_length=400,null="Ture",blank='Ture')
    def __str__(self):
        return self.project_name
    class Meta:
        verbose_name = u'项目分组'
        verbose_name_plural = u'项目列表'


class Hosts(models.Model):
    host_key = models.CharField(max_length=50,unique=True)
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.host_key
    class Meta:
        verbose_name = u'主机列表'
        verbose_name_plural = u'主机列表'


class Projects_to_Host(models.Model):
    pid = models.ForeignKey(Projects)
    hid = models.ForeignKey(Hosts)
    def __str__(self):
        return self.pid.project_name +'-'+ self.hid.host_key
    class Meta:
        verbose_name = u'项目主机对应关系表'
        verbose_name_plural = u'项目主机对应关系表'

