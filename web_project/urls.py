from django.http import HttpResponse
from web_project import api_router
from django.contrib import admin
from django.urls import path,include
from .views import ping, home_view

urlpatterns = [
    path('',home_view,name='home_view' ),
    path('ping/',ping,name='ping'),
    path("admin/", admin.site.urls),
    path("api/",include(api_router.urlpatterns))
]
