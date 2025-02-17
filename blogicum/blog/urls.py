from django.urls import path

from blog.views import (add_comment, category_posts, comment_edit,
                        comment_delete, index, post_delete, post_detail,
                        post_edit, profile_edit, PostCreateView, ProfileView)


app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('posts/<int:post_id>/', post_detail, name='post_detail'),
    path('/posts/<int:post_id>/edit/', post_edit, name='edit_post'),
    path('/posts/<int:post_id>/delete/', post_delete, name='delete_post'),

    path('posts/<int:post_id>/comment/', add_comment, name='add_comment'),
    path(
        '/posts/<int:post_id>/edit_comment/<int:comment_id>',
        comment_edit,
        name='edit_comment',
    ),
    path(
        '/posts/<int:post_id>/delete_comment/<comment_id>',
        comment_delete,
        name='delete_comment',
    ),
    path(
        'category/<slug:category_slug>/',
        category_posts,
        name='category_posts',
    ),
    path('profile/<str:username>', ProfileView.as_view(), name='profile'),
    path('profile/edit/', profile_edit, name='edit_profile'),
    path('create_post/', PostCreateView.as_view(), name='create_post'),
]
