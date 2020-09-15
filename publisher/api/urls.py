from django.urls         import path
from publisher.api.views import (
	api_create_publisher_view,
	api_detail_publisher_view,
	api_update_publisher_view,
	api_delete_publisher_view,
	APIPublisherListView
)

app_name = 'publisher'

urlpatterns = [
	path('create',      api_create_publisher_view,      name="create"),
	path('<pk>',        api_detail_publisher_view,      name="detail"),
	path('<pk>/update', api_update_publisher_view,      name="update"),
	path('<pk>/delete', api_delete_publisher_view,      name="delete"),
	path('',            APIPublisherListView.as_view(), name="list"),
]