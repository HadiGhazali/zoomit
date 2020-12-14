from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from .models import Post, Category
from .forms import CommentForm


def home(request):
    author = request.GET.get('author', None)
    posts = Post.objects.all()
    if author:
        posts = posts.filter(author__username=author)
    categories = Category.objects.all()
    context = {
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'blog/post.html', context)


def single(request, pk):
    try:
        post = Post.objects.select_related('post_setting', 'category', 'author').get(slug=pk)
    except Post.DoesNotExist:
        raise Http404('post not found')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
        else:
            pass
    else:
        form = CommentForm()
    context = {
        'form': form,
        'post': post,
        'category': post.category,
        'setting': post.post_setting,
        'author': post.author,
        'comments': post.comments.filter(is_confirmed=True),
        'related_posts': post.category.posts.filter(~Q(slug=pk))}
    return render(request, 'blog/post_single.html', context)


def category_single(request, pk):
    try:
        category = Category.objects.get(slug=pk)
    except Category.DoesNotExist:
        raise Http404('Category not found')
    posts = Post.objects.filter(category=category)

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'blog/category_single.html', context)


def categories_archive(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'blog/category_archive.html', context)


