
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:username>", views.profile, name="profile"),

    # I need this in other to make the fetch requests work
    path("posts/<int:post_id>", views.post, name="post")
]
