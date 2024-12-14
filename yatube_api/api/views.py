from rest_framework import permissions, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Comment, Follow, Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer, FollowSerializer, GroupSerializer, PostSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author')
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        group_id = self.request.data.get('group')
        if group_id:
            try:
                group = Group.objects.get(id=group_id)
                serializer.save(author=self.request.user, group=group)
            except Group.DoesNotExist:
                raise ValidationError('Группа с таким ID не существует')
        else:
            serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        search_query = self.request.query_params.get('search')
        return Follow.objects.filter(
            user=self.request.user,
            following__username__icontains=search_query if search_query else ''
        )

    def perform_create(self, serializer):
        if self.request.user == serializer.validated_data['following']:
            raise ValidationError('Нельзя подписаться на самого себя')

        if Follow.objects.filter(
            user=self.request.user,
            following=serializer.validated_data['following']
        ).exists():
            raise ValidationError('Вы уже подписаны на этого пользователя')

        serializer.save(user=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.AllowAny]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author')
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    ]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user, post_id=post_id)
