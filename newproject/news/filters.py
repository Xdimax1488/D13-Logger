from django_filters import FilterSet
from .models import *


class NewsFilter(FilterSet):
    class Meta:
        model = Post
        fields = {'datetime': ['gt'],
                  'text_title': ['icontains'],
                  'author': ['exact']}
