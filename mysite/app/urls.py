
from django.urls import path
from .views import AnnouncementList, AnnouncemenDetailView, AnnounceUpdateView, AnnounceCreate, AnnouncementDelete, AnnounceComment

urlpatterns = [
    path('', AnnouncementList.as_view()),
    path('announce_create', AnnounceCreate.as_view()),
    path('<int:pk>', AnnouncemenDetailView.as_view()),
    path('<int:pk>/edit', AnnounceUpdateView.as_view()),
    path('<int:pk>/delete', AnnouncementDelete.as_view()),
    path('<int:pk>/comments', AnnounceComment.as_view()),
]