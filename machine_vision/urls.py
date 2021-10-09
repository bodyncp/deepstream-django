"""machine_vision URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.views import static
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include
from stark.service.v1 import site
from vision.views import account,data_api
from vision.views import download

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^stark/', site.urls),
    url(r'^rbac/', include(('rbac.urls', 'rbac'), namespace='rbac')),
    url(r'^login/', account.login, name='login'),
    url(r'^index/', account.index, name='index'),
    url(r'^logout/', account.logout, name='logout'),
    url(r'^download/$', download.download_file, name='download_file'),
    url(r'^customer/data/display/$', account.data_display, name='data_display'),
    url(r'^customer/data/display/api', data_api.data_display_api, name='data_display_api'),
    url(r'^customer/point_url/api/v1/get/', data_api.request_url_api, name='data_url_api'),

    url(r'^stark/vision/userinfoextent/reset/password/(?P<pk>\d+)/(?P<user>\w+)/', account.reset_password,
        name='reset_password_one'),
    url(r'^stark/vision/userinfoextent/change/(?P<pk>\d+)/(?P<user>\w+)/', account.user_edit_one,
        name='user_edit_one'),
# url(r'^stark/registers/person_count_info/(?P<point_name>\w+)/(?P<point_in>\w+)/(?P<point_out>\w+)/(?P<date_time>\w+)', account.person_count_info, name='person_count_adds'),
url(r'^stark/registers/person_count_info/.*', data_api.person_count_info, name='person_count_adds'),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)', static.serve, {'document_root': settings.MEDIA_ROOT}),
]
