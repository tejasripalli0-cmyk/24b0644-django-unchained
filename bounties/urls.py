from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    RefreshView,
    BountyListCreateView,
    BountyDetailView,
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/refresh/', RefreshView.as_view(), name='auth-refresh'),

    path('bounties/', BountyListCreateView.as_view(), name='bounty-list-create'),
    path('bounties/<int:pk>/', BountyDetailView.as_view(), name='bounty-detail'),
]

