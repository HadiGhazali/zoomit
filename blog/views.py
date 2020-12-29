from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404, HttpResponseRedirect
from random import sample
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, FormView
from datetime import datetime
from django.db import models
from django.views.generic.edit import ModelFormMixin, FormMixin, BaseFormView
import json
from datetime import datetime, timedelta

from .models import Post, Category, Comment, CommentLike, UrlHit, HitCount
from .forms import CommentForm, PostForm


class PostArchive(ListView):
    model = Post
    queryset = Post.objects.filter(draft=True, publish_time__lte=timezone.now())
    paginate_by = 10

    success_url = ''
    template_name = 'blog/post.html'

    def get_random_obj(self):
        rand_post_list = []
        rand_num_list = sample(range(len(self.queryset)), 3)
        for i in rand_num_list:
            rand_post_list.append(self.queryset[i])
        return rand_post_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pop_post = Post.objects.order_by('url_hit__hits')[::-1][:5]
        context['pop_post'] = pop_post
        context['rand_post_list'] = self.get_random_obj()
        pop_daily_post = Post.objects.order_by('url_hit__daily_hits')[::-1][:5]
        context['pop_daily_post'] = pop_daily_post
        return context


class PostSingle(DetailView):
    model = Post
    template_name = 'blog/post_single.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hit = hit_count(self.request, UrlHit)
        context['hit'] = hit
        last_10_comment = get_comments_of_post(self.request, 0, 10)
        older_comment = get_comments_of_post(self.request, 10, 20)
        context['last_comment'] = last_10_comment
        context['older_comment'] = older_comment
        pop_post = Post.objects.order_by('url_hit__hits')[::-1][:5]
        context['pop_post'] = pop_post
        related_posts = get_related_post(self.request)
        context['related_posts'] = related_posts
        daily_hit = calculate_daily_hit(self.request)
        context['daily_hit'] = daily_hit
        comment_form = CommentForm()
        context['form'] = comment_form
        last_five_post = Post.objects.all()[:5]
        context['last_posts'] = last_five_post
        return context


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
    new_comment = Comment.objects.create(author=user, post_id=data['post_id'], content=data['content'])
    response = {'comment_id': new_comment.id, 'content': new_comment.content, 'author': new_comment.author.email}
    return HttpResponse(json.dumps(response), status=201)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_post_slug(request):
    path_url = request.path
    post_slug = str(path_url)
    post_slug = post_slug.split('/')
    post_slug = post_slug[2]
    return post_slug


def hit_count(request, obj):
    if not request.session.session_key:
        request.session.save()
    s_key = request.session.session_key
    ip = get_client_ip(request)
    path_url = request.path
    post_slug = get_post_slug(request)
    try:
        post = Post.objects.get(slug=post_slug)
    except Post.DoesNotExist:
        return 'post does not exits'
    url, url_created = obj.objects.get_or_create(url=path_url, post=post)
    if url_created or (ip and request.path not in request.session):
        if request.user.id:
            track, created = HitCount.objects.get_or_create(url_hit=url, ip=ip, session=s_key, user=request.user)
        else:
            track, created = HitCount.objects.get_or_create(url_hit=url, ip=ip, session=s_key)
        if created:
            url.increase()
            request.session[ip] = ip
            request.session[request.path] = request.path
    updating_date_of_obj(url, ip, s_key)
    return url.hits


def get_day():
    return timezone.now()


def updating_date_of_obj(url, ip, s_key):
    obj = HitCount.objects.get(url_hit=url, ip=ip, session=s_key)
    obj.updating_date()


def calculate_daily_hit(request):
    slug = get_post_slug(request)
    today = get_day()
    object_hit_daily = HitCount.objects.filter(update_date__gte=today - timedelta(days=1),
                                               url_hit__post__slug=slug).count()
    url_hit_obj = UrlHit.objects.get(url=request.path)
    url_hit_obj.set_daily_hits(object_hit_daily)
    return object_hit_daily


class AddPostView(FormView):
    form_class = PostForm
    success_url = '../posts'
    template_name = 'blog/add_post.html'

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        post = form.save(commit=False)
        user = self.request.user
        post.author = user
        post.save()
        return HttpResponseRedirect(self.get_success_url())


def get_related_post(request):
    slug = get_post_slug(request)
    this_post = Post.objects.select_related('category').get(slug=slug)
    if this_post.category:
        related_posts = this_post.category.posts.filter(~Q(slug=slug))
    else:
        related_posts = None
    return related_posts


def get_comments_of_post(request, num1, num2):
    slug = get_post_slug(request)
    post = Post.objects.get(slug=slug)
    comments = post.comments.all()[num1:num2]
    return comments
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
