from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from .views import PostArchive, PostSingle, CategorySingle, CategoryArchive, like_comment, create_comment, \
    AddPostView, get_category_ajax
from .api import post_list, post_detail, comment_detail, comment_list, PostList, PostListMixin, PostDetailMixin, \
    PostListGeneric, PostViewSet

from rest_framework.urlpatterns import format_suffix_patterns

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    # path('', home, name='posts_archive'),
    path('posts/', PostArchive.as_view(), name='posts_archive'),
    path('posts/<slug:slug>', PostSingle.as_view(), name='post_single_2'),
    # path('posts/<slug:pk>', single, name='post_single'),
    path('categories/', CategoryArchive.as_view(), name='categories_archive'),
    path('add_post/', AddPostView.as_view(), name='add_post'),
    path('categories/<slug:slug>/', CategorySingle.as_view(), name='category_single'),
    path('like_comment/', like_comment, name='like_comment'),
    path('create_comment/', create_comment, name='create_comment'),
    # path('get_category_ajax/', get_category_ajax, name='get_category'),
    # path('json/posts/', PostViewSet.as_view({'get': 'list',
    #                                          'post': 'create'}), name='post_list'),
    # path('json/posts/<int:pk>', PostViewSet.as_view({'get': 'retrieve',
    #                                                  'put': 'update',
    #                                                  'delete': 'destroy'}), name='post_detail'),
    path('json/', include(router.urls)),
    path('json/comments/', comment_list, name='comment_list'),
    path('json/comments/<int:pk>', comment_detail, name='comment_detail')
]


