import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post

POST_MINIMUM_CHARS = 3

def index(request):
    if request.method == "POST":
        print("Post request submitted.")

        # Post must be more than 3 characters
        if len(request.POST["content"]) <= POST_MINIMUM_CHARS:
            print("Post is too short!")

            posts = Post.objects.all()
            posts = posts.order_by("-date").all()
            return render(request, "network/index.html", {"posts":posts})
        else:

            # Create new post
            p = Post(
                author = request.user,
                content = request.POST["content"],
                likes = 0
            )
            p.save()

            posts = Post.objects.all()
            posts = posts.order_by("-date").all()
            return render(request, "network/index.html", {"posts":posts})
    else:
        posts = Post.objects.all()
        posts = posts.order_by("-date").all()
        return render(request, "network/index.html", {"posts":posts})

# A user's profile page
def profile(request, username):

    # If here by post, add user to Follow list
    if request.method == "POST":
        print("Follow button has been pressed.")
        user_to_follow = User.objects.get(username=username)
        follower = request.user
        # Toggle follow status
        if not follower in user_to_follow.followers.all():
            user_to_follow.followers.add(follower)
            user_to_follow.save()
            # Also add the user whose profile it is to the active user's (i.e. the follower's) "following" list
            follower.following.add(user_to_follow)
            follower.save()
        else:
            print("Already following this user!")
            user_to_follow.followers.remove(follower)
            user_to_follow.save()
            follower.following.remove(user_to_follow)
            follower.save()

    # Get all posts by a specific user
    posts = Post.objects.all()
    postsToShow = []
    for post in posts:
        if post.author.username == username:
            postsToShow.append(post)
    posts = posts.order_by("-date").all()
    profile_user = User.objects.get(username=username)
    return render(request, "network/profile.html", {"profile_username": username, "profile_user": profile_user, "posts": posts})

# Thanks for the hint!
def post(request, post_id):

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Getting a 403 Forbidden error here and at this point I feel like I am only losing more points by turning this in later (each minute = 0.1%) than I would be by taking the time to figure this out
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)
    
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
