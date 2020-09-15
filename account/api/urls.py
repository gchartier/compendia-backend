from django.urls       import path
from account.api.views import (
	api_register_account_view,
	api_account_properties_view,
	api_update_account_view,
	ObtainAuthTokenView,
	does_account_exist_view,
	ChangePasswordView
)

app_name = 'account'

urlpatterns = [
	path('check_if_account_exists/', does_account_exist_view,       name="check_if_account_exists"),
	path('change_password/',         ChangePasswordView.as_view(),  name="change_password"),
	path('register',                 api_register_account_view,     name="register"),
	path('properties',               api_account_properties_view,   name="properties"),
	path('properties/update',        api_update_account_view,       name="update"),
	path('login',                    ObtainAuthTokenView.as_view(), name="login"),
]