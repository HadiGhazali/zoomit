from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, FormView
from datetime import datetime
from django.db import models
from django.views.generic.edit import ModelFormMixin, FormMixin, BaseFormView
import json

from .models import Post, Category, Comment, CommentLike
from .forms import CommentForm


# class Comments(FormView):
#     form_class = CommentForm
#
#
#
#     def post(self, request, *args, **kwargs):
#         """
#         Handle POST requests: instantiate a form instance with the passed
#         POST variables and then check if it's valid.
#         """
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.post = Post.objects.get(id=request.POST['post_id'])
#             print('____________________________')
#             comment.save()
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#


class PostArchive(ListView):
    model = Post
    queryset = Post.objects.filter(draft=True, publish_time__lte=datetime.now())
    success_url = ''
    template_name = 'blog/post.html'


class PostSingle(DetailView):
    model = Post
    template_name = 'blog/post_single.html'


class CategorySingle(DetailView):
    model = Category
    template_name = 'blog/category_single.html'


class CategoryArchive(ListView):
    model = Category
    queryset = Category.objects.all()
    template_name = 'blog/category_archive.html'


@csrf_exempt
def like_comment(request):
    data = json.loads(request.body)
    user = request.user
    try:
        comment = Comment.objects.get(id=data['comment_id'])
    except Comment.DoesNotExist:
        return HttpResponse('bad request', status=404)
    try:
        comment_like = CommentLike.objects.get(author=user, comment=comment)
        comment_like.condition = data['condition']
        comment_like.save()
    except CommentLike.DoesNotExist:
        CommentLike.objects.create(author=user,
                                   comment=comment,
                                   condition=data['condition'])
    response = {'dislike_count': comment.dislike_count, 'like_count': comment.like_count, 'comment_id': comment.id}
    return HttpResponse(json.dumps(response), status=201)


@csrf_exempt
def create_comment(request):
    data = json.loads(request.body)
    user = request.user
    print(data)
    try:
        post = Post.objects.get(id=data['post_id'])
    except Comment.DoesNotExist:
        return HttpResponse('bad request', status=404)
    new_comment = Comment.objects.create(author=user, post=post, content=data['content'])
    response = {'comment_id': new_comment.id, 'content': new_comment.content, 'author': new_comment.author.email}
    return HttpResponse(json.dumps(response), status=201)
# def home(request):
#     author = request.GET.get('author', None)
#     posts = Post.objects.all()
#     if author:
#         posts = posts.filter(author__email=author)
#     categories = Category.objects.all()
#     context = {
#         'posts': posts,
#         'categories': categories,
#     }
#     return render(request, 'blog/post.html', context)


# def single(request, pk):
#     try:
#         post = Post.objects.select_related('post_setting', 'category', 'author').get(slug=pk)
#     except Post.DoesNotExist:
#         raise Http404('post not found')
#
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.post = post
#             comment.save()
#         else:
#             pass
#     else:
#         form = CommentForm()
#     context = {
#         'form': form,
#         'post': post,
#         'category': post.category,
#         'setting': post.post_setting,
#         'author': post.author,
#         'comments': post.comments.filter(is_confirmed=True),
#         'related_posts': post.category.posts.filter(~Q(slug=pk))}
#     return render(request, 'blog/post_single.html', context)
#


# def category_single(request, pk):
#     try:
#         category = Category.objects.get(slug=pk)
#     except Category.DoesNotExist:
#         raise Http404('Category not found')
#     posts = Post.objects.filter(category=category)
#
#     context = {
#         'posts': posts,
#         'category': category,
#     }
#     return render(request, 'blog/category_single.html', context)

# def categories_archive(request):
#     categories = Category.objects.all()
#     context = {
#         'categories': categories,
#     }
#     return render(request, 'blog/category_archive.html', context)
