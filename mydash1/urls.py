from django.urls import path,include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dev', views.index, name='index1'),
    path('admin/', admin.site.urls),
]