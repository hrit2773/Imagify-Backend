from django.http import HttpResponse
from .api_router import url_patterns
from django.contrib import admin
from django.urls import path,include
from .views import ping, home_view
urlpatterns = [
    path("",home_view,name='home_view' ),
    path('ping/',ping,name='ping'),
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("api/",include(url_patterns))
]