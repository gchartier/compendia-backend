from django.urls       import path
from creator.api.views import (
	api_create_creator_view,
	api_detail_creator_view,
	api_update_creator_view,
	api_delete_creator_view,
	APICreatorListView
)

app_name = 'creator'

urlpatterns = [
	path('create',      api_create_creator_view,      name="create"),
	path('<pk>',        api_detail_creator_view,      name="detail"),
	path('<pk>/update', api_update_creator_view,      name="update"),
	path('<pk>/delete', api_delete_creator_view,      name="delete"),
	path('',            APICreatorListView.as_view(), name="list"),
]