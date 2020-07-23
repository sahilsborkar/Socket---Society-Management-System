from django.urls import path, re_path
from . import views
from .views import PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('soclist', views.soclist, name='blog-soclist'),
    re_path(r'^sochome/(?P<oid>[0-9]+)/$', views.sochome, name='blog-sochome'),
    path('society/<int:society_id>/post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('society/<int:society_id>/post/new/', PostCreateView.as_view(), name='post-create'),
    path('society/<int:society_id>/post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('society/<int:society_id>/post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete')
]