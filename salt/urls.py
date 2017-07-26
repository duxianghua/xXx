from django.conf.urls import url
from salt.views import *

urlpatterns = [
	url(r'^$', index, name='index'),
	url(r'^hostkey', hostkey),
	url(r'^projecthost', projecthost),
	url(r'^get_service', get_service),
	url(r'^status', status),
	url(r'^turn', turn),
	url(r'^code', code_manager),
]