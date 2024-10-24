from django.urls import path

from .router import router
from .views import ExtractView, EmbeddingView

urlpatterns = [
    path('extract/<path:filename>', ExtractView.as_view(), name='extract'),
    path('embedding/<path:filename>', EmbeddingView.as_view(), name='embedding'),
    path('', router.urls),
]
