from django_filters import FilterSet
from .models import Comments, Announcement
 
class PostFilter(FilterSet):
   
    class Meta:
        model = Comments
        fields = {
            'Announcement': ['exact']
            }
