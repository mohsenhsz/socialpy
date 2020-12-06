from django.urls import path
from . import views


urlpatterns = [
    path('', views.AllPosts, name='index'),
    path('<int:post_id>/<int:year>/<int:month>/<int:day>/<slug:slug>/',views.PostDetails, name='post_details'),
    path('create_post/<int:user_id>/', views.CreatePost, name='create_post'),
    path('delete_post/<int:user_id>/<int:post_id>/', views.DeletePost, name='delete_post'),
    path('edit_post/<int:user_id>/<int:post_id>/', views.EditPost, name='edit_post'),
    path('<int:post_id>/<int:comment_id>/', views.ReplyComment, name='reply_comment'),
    path('<int:post_id>/', views.LikePost, name='like'),
    path('dislike/<int:post_id>/', views.DislikePost, name='dislike'),
]
