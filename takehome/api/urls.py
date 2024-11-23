from django.urls import path
from .views import (
    register,
    # login,
    viewUsers,
    # verify_referral
)


urlpatterns = [
    path('', viewUsers, name='view'),
    path('register/', register, name='register'),
    # path('login/', login, name='login'),
    # path('referral/', verify_referral, name='verify_referral'),
]
