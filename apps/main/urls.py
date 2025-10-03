from django.urls import path
from . import views


urlpatterns = [
    path('category/', views.CategoryListCreateView.as_view(), name='category-list'),
    path('category/<slug:slug>', views.CategoryDetailView.as_view(),
         name='category-detail'),
    path('category/<category_slug:slug>/posts',
         views.post_by_category, name='post-by-category'),

    path('', views.PostListCreateView.as_view(), name='post-list'),
    path('my-posts/', views.MyPostsView.as_view(), name='my-posts'),
    path('popular/', views.popular_posts, name='popular-posts'),
    path('recent/', views.recent_posts, name='recent-posts'),
    path('<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
]
