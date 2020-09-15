from django.contrib          import admin
from django.urls             import path, include
from django.contrib.auth     import views as auth_views
from django.conf             import settings
from django.conf.urls.static import static
from comic.api.views         import APIComicNewReleasesListView, APIComicNewReleasesCoversListView
from personal.views          import home_screen_view
from account.views           import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    must_authenticate_view,
)

urlpatterns = [
    # Stock URLs
    path('', include('frontend.urls')),
    path('', home_screen_view, name="home"),
    path('admin/', admin.site.urls),

    # Account URLs
    path('login/',             login_view,              name="login"),
    path('logout/',            logout_view,             name="logout"),
    path('must_authenticate/', must_authenticate_view,  name="must_authenticate"),
    path('register/',          registration_view,       name="register"),
    path('accounts/',           account_view,            name="account"),
    path('accounts/', include('django.contrib.auth.urls')),

    # Password reset URLs
    path('password_change/done/',   auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),       name='password_change_done'),
    path('password_change/',        auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),                name='password_change'),
    path('password_reset/done/',    auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),     name='password_reset_done'),
    path('reset/done/',             auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),                                                           name='password_reset_confirm'),
    path('password_reset/',         auth_views.PasswordResetView.as_view(),                                                                  name='password_reset'),

    # REST Framework API URLs
    path('api/comics/',      include('comic.api.urls',      'comic_api')),
    path('api/publishers/',  include('publisher.api.urls',  'publisher_api')),
    path('api/series/',      include('series.api.urls',     'series_api')),
    path('api/creators/',    include('creator.api.urls',    'creator_api')),
    path('api/accounts/',    include('account.api.urls',    'account_api')),
    path('api/reviews/',     include('review.api.urls',     'review_api')),
    path('api/collections/', include('collection.api.urls', 'collection_api')),
    path('api/pull_lists/',  include('pulllist.api.urls',   'pull_list_api')),
    path('api/new_releases', APIComicNewReleasesListView.as_view(), name="new_releases_list"),
    path('api/new_releases/covers', APIComicNewReleasesCoversListView.as_view(), name="new_releases__covers_list")
]
