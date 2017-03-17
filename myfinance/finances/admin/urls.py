from django.conf.urls import url

from .views import (
    AdminMainView, AdminUserListView, AdminEditUserView, AdminDeleteUserView, AdminSearchUserView
)

urlpatterns = [
    url(r'^$', AdminMainView.as_view(), name='main'),
    url(r'^users/$', AdminUserListView.as_view(), name='user_list'),
    url(r'^delete/$', AdminDeleteUserView.as_view(), name='delete_user'),
    url(r'^edit/$', AdminEditUserView.as_view(), name='edit_user'),
    url(r'^search/$', AdminSearchUserView.as_view(), name='search_user'),
]