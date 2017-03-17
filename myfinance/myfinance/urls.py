from django.conf.urls import include, url
from django.contrib import admin
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^admin/', include("finances.admin.urls", namespace='admin')),
    url(r'^', include("finances.urls", namespace='finances')),
    url(r'^api/', include("finances.api.urls", namespace='api')),
    url(r'session_security/', include('session_security.urls')),
    url(r'^api-token-auth/', obtain_jwt_token)
]
