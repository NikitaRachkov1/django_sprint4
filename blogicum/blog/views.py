from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.views import View

from .forms import (CommentForm, CustomUserCreationForm,
                    PostForm, ProfileEditForm)
from .models import Post, Category, Comment

POSTS_LIMIT = 10


class PostCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(
            request,
            'blog/create.html',
            {'form': form},
        )

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(
                'blog:profile',
                username=request.user.username,
            )
        return render(
            request,
            'blog/create.html',
            {'form': form}
        )


class ProfileView(View):
    def get(self, request, username=None):
        if not username:
            username = request.user.username
        user_profile = get_object_or_404(User, username=username)

        if request.user == user_profile:
            posts = user_profile.posts.all()
        else:
            posts = user_profile.posts.filter(pub_date__lte=timezone.now())

        paginator = Paginator(posts, POSTS_LIMIT)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request,
            'blog/profile.html',
            {
                'profile': user_profile,
                'page_obj': page_obj,
            },
        )


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(
            request,
            'registration/registration_form.html',
            {'form': form}
        )

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(
            request,
            'registration/registration_form.html',
            {'form': form}
        )


@login_required
def add_comment(request, post_id):
    post_obj = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post_obj
            comment.save()
            return redirect(
                'blog:post_detail',
                post_id=post_id,
            )


@login_required
def comment_edit(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden('Нельзя редактировать чужой коммент!')

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(
                'blog:post_detail',
                post_id=post_id,
            )
    else:
        form = CommentForm(instance=comment)

    return render(
        request,
        'blog/comment.html',
        {'form': form, 'comment': comment}
    )


@login_required
def comment_delete(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.author != request.user:
        return HttpResponseForbidden('Вы не можете удалять чужой коммент!')

    comment.delete()
    return redirect(
        'blog:post_detail',
        post_id=post_id,
    )


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if not category.is_published:
        raise Http404("В данной категории нет постов")

    posts_in_category = Post.objects.published().filter(category=category)

    paginator = Paginator(posts_in_category, POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/category.html',
        context={
            'category': category,
            'page_obj': page_obj,
        }
    )


def index(request):
    posts = Post.objects.published()

    paginator = Paginator(posts, POSTS_LIMIT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/index.html',
        context={
            'page_obj': page_obj,
            'title': 'Лента записей',
        }
    )


def post_detail(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        is_published=True,
        pub_date__lte=timezone.now(),
        category__is_published=True
    )
    comments = post.comments.all()
    print(comments, len(comments))

    form = CommentForm()

    return render(
        request,
        'blog/detail.html',
        context={
            'post': post,
            'title': 'Пост',
            'form': form,
            'comments': comments,
        },
    )


@login_required
def profile_edit(request):
    user_obj = get_object_or_404(User, username=request.user.username)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            return redirect(
                'blog:profile',
                username=user_obj.username,
            )
    else:
        form = ProfileEditForm(instance=user_obj)

    return render(
        request,
        'blog/user.html',
        {'form': form}
    )


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden('Вы не можете редактировать чужой пост!')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(
                'blog:post_detail',
                post_id=post_id,
            )
    else:
        form = PostForm(instance=post)

    return render(
        request,
        'blog/create.html',
        {'form': form}
    )


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.author != request.user:
        return HttpResponseForbidden('Вы не можете удалять чужой пост!')

    post.delete()
    return redirect(
        'blog:profile',
        username=request.user.username,
    )
