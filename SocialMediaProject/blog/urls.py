from django.urls import path
from . import views
from .views import (PostCreateView,PostUpdateView,PostListView,PostDetailView,PostDeleteView,UserPostListView)

urlpatterns=[
    path('',PostListView.as_view(),name='blog-home'),
    path('about/',views.about,name='blog-about'),
    path('post/new/',PostCreateView.as_view(),name="post-create"),
    path('post/<int:pk>/update',PostUpdateView.as_view(),name="post-update"),
    path('post/<int:pk>/delete',PostDeleteView.as_view(),name="post-delete"),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name="post-detail"),
    path('user/<str:username>',UserPostListView.as_view(),name="user-posts"),
    path('blog-python/',views.blog_python_view,name="blog-python"),
    path('latest-posts/',views.latestlistview,name="latest-posts"),
    path('questions-post/',views.questionsview,name='questions-post'),
    path('comments/<int:pk>',views.comments,name="comments"),
]