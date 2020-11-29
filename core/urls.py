from django.urls import path
from . import views


urlpatterns = [
    path('', views.AllPosts, name='index'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>',views.PostDetails, name='post_details'),
]
