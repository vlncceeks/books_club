from django.urls import re_path
from . import views

urlpatterns = [
    re_path(
        r'^(?P<user_id>\d+)/profile/$',
        views.user_profile,
        name='user-profile'
    ),

    re_path(
        r'^(?P<user_id>\d+)/books/(?P<status>\w+)/$',
        views.user_books_by_status
    ),

    re_path(
        r'^(?P<user_id>\d+)/events/$',
        views.user_events
    ),

    re_path(
        r'^active/$',
        views.active_users
    ),

    re_path(
        r'^(?P<user_id>\d+)/stats/$',
        views.user_books_stats
    ),
]