from django.urls import path, include

urlpatterns = [
    path('api/', include('mls.api.urls')),
    path('', include('django.contrib.staticfiles.urls')),
]
