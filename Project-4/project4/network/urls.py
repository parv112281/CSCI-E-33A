
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/create", views.create_post, name="create_post"),
    path("posts/<int:pagenumber>", views.fetch_posts, name="fetch_posts"),
    path("posts/<str:username>/<int:pagenumber>",
         views.fetch_user_posts, name="fetch_user_posts"),
    path("posts/<int:id>/update", views.update_post, name="update_post"),
    path("posts/<int:id>/like", views.like_post, name="like_post"),
    path("user/<str:username>", views.fetch_profile, name="fetch_profile"),
    path("user/<str:username>/follow", views.follow, name="follow"),
    path("user/<str:username>/unfollow", views.unfollow, name="unfollow")
]
