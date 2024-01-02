from django.urls import path
from .views import processed_video, upload_video, delete
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('upload/', upload_video, name='upload_video'),
    path('processed/<int:pk>/', processed_video, name='processed_video'),
    path('upload/delete/<int:pk>', delete, name='delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)