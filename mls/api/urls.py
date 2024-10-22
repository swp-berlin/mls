from django.urls import path

from .v1 import router as router_v1

app_name = 'api'

urlpatterns = [
    path('v1/', router_v1.urls),
]
