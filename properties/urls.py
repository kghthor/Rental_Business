# properties/urls.py
from django.urls import path
from .views import (
    property_list, property_create, property_detail, property_update, property_delete,
    interested_in_property, like_property
)

urlpatterns = [
    path('', property_list, name='property_list'),
    path('new/', property_create, name='property_create'),
    path('<int:pk>/', property_detail, name='property_detail'),
    path('<int:pk>/edit/', property_update, name='property_update'),
    path('<int:pk>/delete/', property_delete, name='property_delete'),
    path('<int:pk>/interested/', interested_in_property, name='interested_in_property'),
    path('<int:pk>/like/', like_property, name='like_property'),
]
