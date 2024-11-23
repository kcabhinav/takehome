from django.urls import path
from .views import RegisterView, LoginView, ReferralListView, ListUsersView

urlpatterns = [
    path('', ListUsersView.as_view(), name='users'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('referrals/<int:user_id>/', ReferralListView.as_view(), name='referrals'),
]
