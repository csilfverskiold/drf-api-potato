from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api_potato.permissions import IsOwnerOrReadOnly
from .models import Recipe
from .serializers import RecipeSerializer


class RecipeList(generics.ListCreateAPIView):  # Create
    """
    List recipes or create a recipe if logged in
    """
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Recipe.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True),
        saves_count=Count('saves', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,  # Sets fields sortable
        filters.SearchFilter,  # Allows text search specific field
        DjangoFilterBackend,  # Allows field filter dropdown
    ]
    filterset_fields = [
        'owner__followed__owner__profile',  # User feed
        'likes__owner__profile',  # Recipes a specific user likes
        'saves__owner__profile',  # Recipes a specific user saved
        'owner__profile',  # Recipes of a specific user
    ]
    search_fields = [
        'owner__username',
        'title',
        'category',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
        'saves__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):  # R/U/D
    """
    Retrieve a recipe and edit or delete it if logged in user owns it
    """
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Recipe.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True),
        saves_count=Count('saves', distinct=True)
    ).order_by('-created_at')
