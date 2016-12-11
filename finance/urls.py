from django.conf.urls import url

from .views import \
    MainPageView, AccountView, AddChargeView, \
    AccountInsertView, AccountStatisticsView, LoginView, RegisterView, \
    ProfileUpdateView, ProfileView, LogoutView, UserSearchView, PublicProfileView

urlpatterns = [
    url(r'^$', MainPageView.as_view(), name='main'),
    url(r'^insert/$', AccountInsertView.as_view(), name='insert'),
    url(r'^charges/(?P<number>\d+)/$', AccountView.as_view(), name='account'),
    url(r'^charges/(?P<number>\d+)/add/$', AddChargeView.as_view(), name='add_charge'),
    url(r'^charges/(?P<number>\d+)/statistics/$', AccountStatisticsView.as_view(), name='statistics'),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^profile/$', ProfileView.as_view(), name="profile"),
    url(r'^update/$', ProfileUpdateView.as_view(), name="update"),
    url(r'^usersearch/$', UserSearchView.as_view(), name="usersearch"),
    url(r'^users/(?P<username>[\w.@+-]+)/$', PublicProfileView.as_view(), name='public_profile')
]
