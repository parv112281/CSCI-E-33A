from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.urls import reverse
import json
from math import ceil

from .models import User, Post, Following

POSTS_PER_PAGE = 10


def __construct_posts_response(username, raw_posts, pagenumber):
    posts = []
    for post in raw_posts:
        liked = False
        allow_edit = username == post.user.username
        for liker in post.likers.all():
            if username == liker.username:
                liked = True
                break
        posts.append(post.serialize(liked, allow_edit))

    posts.sort(key=lambda post: post['created_on'], reverse=True)

    num_pages = ceil(len(posts) / POSTS_PER_PAGE)
    start_post_index = (pagenumber - 1) * POSTS_PER_PAGE
    end_post_index = pagenumber * POSTS_PER_PAGE

    if len(posts) <= start_post_index:
        start_post_index = len(posts) - POSTS_PER_PAGE - 1
        end_post_index = len(posts)
    elif len(posts) <= end_post_index:
        end_post_index = len(posts)

    return_posts = posts[start_post_index:end_post_index]

    return JsonResponse(
        {
            "posts": return_posts,
            "num_pages": num_pages
        })


@csrf_exempt
@login_required
def update_post(request, id):
    print('in update_post')
    if request.method == "PUT":
        post = Post.objects.get(id=id)
        data = json.loads(request.body)
        if data.get("message") is not None:
            post.message = data["message"]
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)


@csrf_exempt
@login_required
def like_post(request, id):
    print('in like_post')
    post = Post.objects.get(id=id)
    print(post)
    post.likers.add(request.user)
    post.save()
    print(post)

    return HttpResponse(status=204)


def index(request):
    return render(request, "network/index.html")


def fetch_user_posts(request, username, pagenumber):
    print('in fetch_user_posts')
    user = User.objects.get(username=username)
    user_posts = Post.objects.filter(user=user).all()
    username = None if request.user is None else request.user.username

    return __construct_posts_response(username, user_posts, pagenumber)


def fetch_posts(request, pagenumber):
    print('in fetch_posts')
    username = None if request.user is None else request.user.username

    return __construct_posts_response(username, Post.objects.all(), pagenumber)


def fetch_profile(request, username):
    print('in fetch_profile')
    user = User.objects.get(username=username)
    for f in request.user.follows.all():
        print(f.follower.username)

    return JsonResponse(
        {
            "id": user.id,
            "current_username": request.user.username,
            "is_followed": any(user.username == follow.follows.username
                               for follow in request.user.follows.all()),
            "username": user.username,
            "num_followers": len(user.follower.all()),
            "follows": len(user.follows.all()),
        }
    )


@login_required
def follow(request, username):
    print('in follow')
    user = User.objects.get(username=username)
    following = Following(follows=user, follower=request.user)
    following.save()
    return JsonResponse({"message": "Followed successfully."}, status=201)


@login_required
def unfollow(request, username):
    print('in unfollow')
    user = User.objects.get(username=username)
    following = Following.objects.get(follows=user, follower=request.user)
    following.delete()
    return JsonResponse({"message": "unfollowed successfully."}, status=201)


@csrf_exempt
@login_required
def create_post(request):
    print('in create_post')
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        message = body['message']
        # add post to the db
        post = Post.objects.create(
            user=request.user,
            message=message
        )
        # return response containing id, username, message, the datetime it was created, the number of likes, and wheteher the current user has liked the post
        return JsonResponse(post.serialize(False, True))


def login_view(request):
    print('in login_view')
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
    print('in logout_view')
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    print('in register')
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
