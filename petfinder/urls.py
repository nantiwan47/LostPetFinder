from django.urls import path
from .views import *

urlpatterns = [
    path('', lost_pet_list, name='home'),
    path('find/', find_list, name='find_list')
]
