from django.urls import path
from review.api.views import APIComicReviewsListView
from comic.api.views import (
    api_detail_comic_view,
    api_update_comic_view,
    api_delete_comic_view,
    api_create_comic_view,
    APIComicListView,
    APIComicNewReleasesListView,
    APIComicNewReleasesCoversListView
)

app_name = 'comic'

urlpatterns = [
    path('<pk>/get', api_detail_comic_view,
         name="detail"),
    path('<pk>/update', api_update_comic_view,
         name="update"),
    path('<pk>/delete', api_delete_comic_view,
         name="delete"),
    path('create', api_create_comic_view,
         name="create"),
    path('', APIComicListView.as_view(),
         name="list"),
    path('new-releases', APIComicNewReleasesListView.as_view(),
         name="new_releases_list"),
    path('new-releases/covers', APIComicNewReleasesCoversListView.as_view(),
         name="new_releases_covers_list"),
    path('<pk>/reviews', APIComicReviewsListView.as_view(),
         name="review_list")
]
