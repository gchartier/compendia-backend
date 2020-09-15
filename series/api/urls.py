from django.urls      import path
from series.api.views import (
	api_create_series_view,
	api_detail_series_view,
	api_update_series_view,
	api_delete_series_view,
	APISeriesListView
)

app_name = 'series'

urlpatterns = [
	path('create',      api_create_series_view,      name="create"),
	path('<pk>',        api_detail_series_view,      name="detail"),
	path('<pk>/update', api_update_series_view,      name="update"),
	path('<pk>/delete', api_delete_series_view,      name="delete"),
	path('',            APISeriesListView.as_view(), name="list"),
]