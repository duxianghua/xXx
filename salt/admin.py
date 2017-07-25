# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from salt.models import *
admin.site.register(Hosts)
admin.site.register(Projects)
admin.site.register(Projects_to_Host)