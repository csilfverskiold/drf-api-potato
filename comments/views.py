from django.http import Http404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Comment
from .serializers import CommentSerializer
from drf_api_potato.permissions import IsOwnerOrReadOnly


class CommentList(APIView):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(
            comments, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = CommentSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class CommentDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentSerializer

    def get_object(self, pk):  # Method - If comment does not exist
        try:
            comment = Comment.objects.get(pk=pk)
            self.check_object_permissions(self.request, comment)
            return comment
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request, pk):  # Method - Retrieve a comment
        comment = self.get_object(pk)
        serializer = CommentSerializer(
            comment, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request, pk):  # Method - Update a comment
        comment = self.get_object(pk)
        serializer = CommentSerializer(
            comment, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):  # Method - Delete a comment
        comment = self.get_object(pk)
        comment.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
