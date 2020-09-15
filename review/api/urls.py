from django.urls      import path
from review.api.views import (
	api_create_review_view,
	api_detail_review_view,
	api_update_review_view,
	api_delete_review_view,
	APIReviewListView
)

app_name = 'review'

urlpatterns = [
	path('create',      api_create_review_view,      name="create"),
	path('<pk>',        api_detail_review_view,      name="detail"),
	path('<pk>/update', api_update_review_view,      name="update"),
	path('<pk>/delete', api_delete_review_view,      name="delete"),
	path('',            APIReviewListView.as_view(), name="list"),
]