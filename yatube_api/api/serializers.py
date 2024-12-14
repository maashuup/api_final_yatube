from rest_framework import serializers

from django.contrib.auth import get_user_model

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = [
            'id',
            'text',
            'pub_date',
            'author',
            'image',
            'group',
        ]
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = [
            'id',
            'title',
            'slug',
            'description',
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = [
            'id',
            'author',
            'post',
            'text',
            'created',
        ]
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        fields = ['user', 'following']
        model = Follow
