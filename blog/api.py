from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, Http404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .permissions import IsPostAuthorOrReadOnly
from blog.models import Post, Comment, Category
from blog.serializers import PostSerializer, CommentSerializer, CategorySerializer
from rest_framework.parsers import JSONParser
from rest_framework import status, mixins, generics
from rest_framework.views import APIView


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsPostAuthorOrReadOnly]

    @action(detail=True, methods=['get'])
    def comment(self, request, pk=None):
        post = self.get_object()
        comment = post.comments.all()

        page = self.paginate_queryset(comment)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def get_published(self, request):
        posts = Post.objects.filter(draft=False)

        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['POST'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.draft = False
        post.save()
        serializer = self.get_serializer(post)
        return Response(serializer.data)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
