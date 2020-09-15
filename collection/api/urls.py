from django.urls          import path
from collection.api.views import (
	api_detail_collection_view,
	api_detail_comic_box_view,
	api_update_comic_box_view,
	api_delete_comic_box_view,
	api_create_comic_box_view,
	APIComicBoxComicsListView,
	APIComicBoxListView,
	api_detail_collected_comic_view,
	api_update_collected_comic_view,
	api_remove_collected_comic_view,
	api_add_collected_comic_view,
	APICollectedComicListView
)

app_name = 'collection'

urlpatterns = [
	# Collection
	path('', api_detail_collection_view, name="collection_detail"),

	# Comic Box
	path('boxes/create',       api_create_comic_box_view,           name="comic_box_create"),
	path('boxes/<pk>',         api_detail_comic_box_view,           name="comic_box_detail"),
	path('boxes/<pk>/update',  api_update_comic_box_view,           name="comic_box_update"),
	path('boxes/<pk>/delete',  api_delete_comic_box_view,           name="comic_box_delete"),
	path('boxes/<pk>/comics',  APIComicBoxComicsListView.as_view(), name="comic_box_comics_list"),
	path('boxes',              APIComicBoxListView.as_view(),       name="comic_box_list"),

	# Collected Comic
	path('comics/<pk>/add',    api_add_collected_comic_view,        name="collected_comic_add"),
	path('comics/<pk>',        api_detail_collected_comic_view,     name="collected_comic_detail"),
	path('comics/<pk>/update', api_update_collected_comic_view,     name="collected_comic_update"),
	path('comics/<pk>/remove', api_remove_collected_comic_view,     name="collected_comic_remove"),
	path('comics',             APICollectedComicListView.as_view(), name="collected_comic_list"),
]