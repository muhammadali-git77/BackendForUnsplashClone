from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from . import settings
from api.views import PostViewSet, UserUpdateView,download_image

router = DefaultRouter()
router.register(r'images', PostViewSet, basename='photo')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('dj_rest_auth.urls')),
    path('api/v1/auth/registration/', include('dj_rest_auth.registration.urls')), 
    path('api/v1/userdatas/', UserUpdateView.as_view(), name="userdatas"),
    path('api/v1/', include(router.urls)),
    path('download/<int:photo_id>/', download_image, name='download_image'),
]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
