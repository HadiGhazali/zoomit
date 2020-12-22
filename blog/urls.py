from django.urls import path, re_path
from .views import PostArchive, PostSingle, CategorySingle, CategoryArchive

urlpatterns = [
    # path('', home, name='posts_archive'),
    path('posts/', PostArchive.as_view(), name='posts_archive'),
    path('posts/<slug:slug>', PostSingle.as_view(), name='post_single_2'),
    # path('posts/<slug:pk>', single, name='post_single'),
    path('categories/', CategoryArchive.as_view(), name='categories_archive'),
    path('categories/<slug:slug>/', CategorySingle.as_view(), name='category_single'),
]
