import django_filters

from posts.models import Follow


class FollowFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(
        field_name='following__username',
        lookup_expr='icontains'
    )

    class Meta:
        model = Follow
        fields = ['user', 'following']
