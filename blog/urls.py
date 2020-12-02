from django.urls import path, re_path
from .views import home, single, categories_archive, category_single

urlpatterns = [
    path('posts/', home, name='posts_archive'),
    path('posts/<slug:pk>', single, name='post_single'),
    path('categories/', categories_archive, name='categories_archive'),
    path('categories/<slug:pk>/', category_single, name='category_single'),
]
