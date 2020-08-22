from django.urls import path, re_path
from myapp import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    #path(r'detail/<int:top_no>', views.detail, name='detail'),
    re_path(r'(?P<top_no>\d+)/', views.detail, {}, name='detail'),
    path(r'courses/', views.courses, name='courses'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'order_response/', views.place_order, name='place_order'),
    path(r'courses/<int:course_id>', views.coursedetail, name='course_detail'),
    path(r'login', views.user_login, name='login'),
    path(r'logout', views.user_logout, name='logout'),
    path(r'myaccount', views.myaccount, name='myaccount'),
    path(r'register', views.register, name='register'),
    # path(r'reset-password/', PasswordResetView.as_view(), name='reset_password'),
    # path(r'reset-password/done/', PasswordResetDoneView.as_view, name='password_reset_done'),
    # path(r'password_reset_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view,
    #      name='password_reset_confirm')
]
