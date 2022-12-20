from django_filters import FilterSet
from .models import Comments
 
class PostFilter(FilterSet):
    class Meta:
        model = Comments
        fields = {
            'Announcement': ['exact'],
        }