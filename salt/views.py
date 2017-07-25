# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from salt.models import *
from salt.SaltAPI import *
import json
import re
# Create your views here.

def index(request):
    project_list = Projects.objects.all()
    return render(request, 'project.html', locals())

def hostkey(request):
    s = Salt_api()
    key = s.ListKey()
    for i in key[0]:
        Hosts.objects.create(host_key=i)
    return HttpResponse('OK')

def projecthost(request):
    project = request.GET.get('project')
    p = Projects.objects.get(project_name=project)
    hlist = Projects_to_Host.objects.filter(pid=p.pk)
    l =[]
    for i in hlist:
        host = {}
        host['name'] = i.hid.host_key
        host['id'] = i.hid.pk
        l.append(host)
    return HttpResponse(json.dumps(l))

def get_service(request):
    hostid = request.GET.get('hostid')
    Pname = request.GET.get('project')
    user_re = request.GET.get('match')
    print hostid, Pname
    s = Salt_api()
    host = Hosts.objects.get(pk=hostid)
    filter_re = Projects.objects.get(project_name = Pname).filter_re
    #print Projects_to_Host.objects.filter(pid = Projects.objects.get(project_name=Pname)).values(host.host_key)
    data = s.Salt_CMD(fun='service.get_all', tgt=host.host_key)
    l1 = [i for i in data['return'][0][host.host_key] if re.match(filter_re, i)]
    if user_re:
        l1 = [i for i in l1 if re.match(user_re, i)]
    service_list = [{host.host_key: l1}]
    #return HttpResponse(json.dumps(service_list))
    return render(request, 'services_list.html', locals())


def status(request):
    hostkey = request.GET.get('host')
    service = request.GET.get('service')
    s = Salt_api()
    data = s.Salt_CMD(fun='service.status', tgt=hostkey, arg=service)
    print data
    return HttpResponse(json.dumps(data['return'][0][hostkey]))

def turn(request):
    host=request.GET.get('host')
    action='service.'+request.GET.get('action')
    service=request.GET.get('service')
    salt=Salt_api()
    if salt.status == 0:
        #salt_host_key = Host.objects.get(host_name=host).salt_key_name
        data = salt.Salt_CMD(fun=action.lower(),tgt=host,arg=service)
        return HttpResponse(json.dumps(data['return'][0][host]))

def code_manager(request):
    action = request.GET.get('action')
    project_name = request.GET.get('project')
    cmd_data = Projects.objects.get(project_name=project_name).update_cmd
    print cmd_data
    if cmd_data:
        cmd = json.loads(cmd_data)[action]
        salt=Salt_api()
        if action == 'pull':
            arg="su -c '%s' deploy" %cmd
            data = salt.Salt_CMD(fun='cmd.run',tgt='admin-staging.stargt.com.my',arg=arg)
        else:
            data = salt.Salt_CMD(fun='cmd.run',tgt='admin-staging.stargt.com.my',arg=cmd)
        return HttpResponse(json.dumps(data['return'][0]['admin-staging.stargt.com.my']))
    else:
        return HttpResponse(json.dumps('你没请我吃饭,所以此项目暂时无法进行代码管理.'))
