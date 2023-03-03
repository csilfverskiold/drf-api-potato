from django.db.models import Count
from rest_framework import generics, filters
from drf_api_potato.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer


class ProfileList(generics.ListAPIView):  # Create
    """
    List of all profiles
    Profile creation is handled by Django signals
    """
    queryset = Profile.objects.annotate(
        recipes_count=Count('owner__recipe', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):  # Read/Update
    """
    Retrieve or update a profile (if user logged in)
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
