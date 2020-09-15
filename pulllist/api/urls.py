from django.urls        import path
from pulllist.api.views import (
	api_detail_pull_list_series_view,
	APIPullListSeriesListView,
	api_unsub_series_pulllist_view,
	api_sub_series_pulllist_view,
	api_add_comic_pulllist_view,
	api_remove_comic_pulllist_view,
	api_update_subbed_series_pulllist_view,
	APIPullListComicsListView
)

app_name = 'pulllist'

urlpatterns = [
	path('series/<pk>',        api_detail_pull_list_series_view,       name="series"),
	path('series',             APIPullListSeriesListView.as_view(),    name="series_list"),
	path('series/unsubscribe', api_unsub_series_pulllist_view,         name="unsubscribe"),
	path('series/subscribe',   api_sub_series_pulllist_view,           name="subscribe"),
	path('series/update',      api_update_subbed_series_pulllist_view, name="update-series"),
	path('comics/add',         api_add_comic_pulllist_view,            name="add_comic"),
	path('comics/remove',      api_remove_comic_pulllist_view,         name="remove_comic"),
	path('comics',             APIPullListComicsListView.as_view(),    name="comics_list")
]