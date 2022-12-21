from django_filters import FilterSet, AllValuesFilter
from .models import Comments
 
class PostFilter(FilterSet):
        
    class Meta:
        model = Comments
        fields = ['Announcement']