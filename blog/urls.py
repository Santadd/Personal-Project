from django.urls import path
from blog.views import (PostListView, PostDetailView, PostCreateView, 
                        PostUpdateView, PostDeleteView, UserPostListView)

urlpatterns = [
    path('blog_posts/', view=PostListView.as_view(), name='blog-posts'),
    path('view_posts/', view=UserPostListView.as_view(), name='blog-userposts'),
    path('post/<int:pk>/', view=PostDetailView.as_view(), name='blog-detail'),
    path('post/update/<int:pk>/', view=PostUpdateView.as_view(), name='blog-update'),
    path('post/delete/<int:pk>/', view=PostDeleteView.as_view(), name='blog-delete'),
    path('post/new/', view=PostCreateView.as_view(), name='blog-newpost')
]
