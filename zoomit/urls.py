from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from account.api import UserViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('account.urls')),
                  path('api/', include(router.urls)),
                  path('', include('blog.urls')),

                  path('api-auth/', include('rest_framework.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
