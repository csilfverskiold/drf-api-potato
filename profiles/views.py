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
    filter_backends = [
        filters.OrderingFilter  # Attribute sets fields sortable
    ]
    ordering_fields = [
        'recipes_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):  # Read/Update
    """
    Retrieve or update a profile (if user logged in)
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        recipes_count=Count('owner__recipe', distinct=True),
        followers_count=Count('owner__followed', distinct=True),
        following_count=Count('owner__following', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
