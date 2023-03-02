from rest_framework import generics, permissions
from drf_api_potato.permissions import IsOwnerOrReadOnly
from saves.models import Save
from saves.serializers import SaveSerializer


class SaveList(generics.ListCreateAPIView):
    """
    List saves or create a save/save a recipe if logged in.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = SaveSerializer
    queryset = Save.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SaveDetail(generics.RetrieveDestroyAPIView):
    """
    Retrieve a save or delete it by id if you own it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = SaveSerializer
    queryset = Save.objects.all()
