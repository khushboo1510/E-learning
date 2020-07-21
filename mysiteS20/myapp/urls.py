from django.urls import path, re_path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    #path(r'detail/<int:top_no>', views.detail, name='detail'),
    re_path(r'(?P<top_no>\d+)/', views.detail, {}, name='detail'),
    path(r'courses/', views.courses, name='courses')
]
