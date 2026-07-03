from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import Bounty
from .serializers import RegisterSerializer, BountySerializer
from .permissions import IsOwner
from .signals import get_bounty_list_cache_key, invalidate_bounty_cache


# ---------------------------------------------------------------------------
# 1. User Registration
# ---------------------------------------------------------------------------

class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Registers a new user account.
    """
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'message': 'User registered successfully.',
                'username': user.username,
            },
            status=status.HTTP_201_CREATED,
        )


# ---------------------------------------------------------------------------
# 2 & 3. JWT Login / Refresh
# ---------------------------------------------------------------------------
# These simply reuse SimpleJWT's built-in views. They are wired up in urls.py:
#
#   /api/auth/login/    -> TokenObtainPairView
#   /api/auth/refresh/  -> TokenRefreshView
#
# Kept here as named aliases for clarity / potential customization.

class LoginView(TokenObtainPairView):
    """
    POST /api/auth/login/
    Returns access and refresh JWT tokens for valid credentials.
    """
    permission_classes = [permissions.AllowAny]


class RefreshView(TokenRefreshView):
    """
    POST /api/auth/refresh/
    Returns a new access token given a valid refresh token.
    """
    permission_classes = [permissions.AllowAny]


# ---------------------------------------------------------------------------
# 4. Bounty List / Create
# ---------------------------------------------------------------------------

class BountyListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/bounties/  - list current user's bounties (cached 60s)
    POST /api/bounties/  - create a new bounty owned by the current user
    """
    serializer_class = BountySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only ever return bounties belonging to the requesting user.
        return Bounty.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        cache_key = get_bounty_list_cache_key(request.user.id)
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return Response(cached_response)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60)
        return response

    def perform_create(self, serializer):
        # Owner is always taken from the authenticated request, never
        # accepted from the client payload.
        serializer.save(owner=self.request.user)
        invalidate_bounty_cache(self.request.user.id)


# ---------------------------------------------------------------------------
# 5. Bounty Retrieve / Update / Delete
# ---------------------------------------------------------------------------

class BountyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/bounties/<id>/
    PUT    /api/bounties/<id>/
    PATCH  /api/bounties/<id>/
    DELETE /api/bounties/<id>/
    """
    serializer_class = BountySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Bounty.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)
        invalidate_bounty_cache(self.request.user.id)

    def perform_destroy(self, instance):
        owner_id = instance.owner_id
        instance.delete()
        invalidate_bounty_cache(owner_id)

