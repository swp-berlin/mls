from django.urls import path, include

urlpatterns = [
    path('v1/', include('mls.api.v1.urls')),
]
