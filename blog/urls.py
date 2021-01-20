from django.urls import path, re_path, include
from zoomit.urls import router
from .views import PostArchive, PostSingle, CategorySingle, CategoryArchive, like_comment, create_comment, \
    AddPostView, get_category_ajax
from .api import PostViewSet, CommentViewSet, CategoryViewSet

from rest_framework.urlpatterns import format_suffix_patterns

router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('posts/', PostArchive.as_view(), name='posts_archive'),
    path('posts/<slug:slug>', PostSingle.as_view(), name='post_single_2'),
    path('categories/', CategoryArchive.as_view(), name='categories_archive'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('categories/<slug:slug>/', CategorySingle.as_view(), name='category_single'),
    path('like_comment/', like_comment, name='like_comment'),
    path('create_comment/', create_comment, name='create_comment'),
    path('get_category/', get_category_ajax, name='get_category')
]


