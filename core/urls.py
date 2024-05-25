from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #path('', views.PropertyListView.as_view(), name='property_list'),
    path('login/',views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
   path('', views.property_list, name='property_list'),
]
