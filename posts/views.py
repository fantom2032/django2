import logging
from typing import Literal

from django.views import View
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse

from posts.models import Posts, Images, Categories, PostReaction


logger = logging.getLogger()


class BasePostView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        posts: QuerySet[Posts] = Posts.objects.all()
        return render(
            request=request, template_name="posts.html", 
            context={
                "posts": posts,
                "user": is_active
            }
        )


class PostsView(View):
    """Posts controller with all methods."""

    def get(self, request: HttpRequest) -> HttpResponse:
        is_active = request.user.is_active
        categories = Categories.objects.all()
        if not categories:
            return HttpResponse(
                content="<h1>Something went wrong</h1>"
            )
        if not is_active:
            return redirect(to="login")
        return render(
            request=request, template_name="post_form.html",
            context={"categories": categories}
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        images = request.FILES.getlist("images")
        post = Posts.objects.create(
            user=request.user,
            title=request.POST.get("title"),
            description=request.POST.get("description")
        )
        post.categories.set(request.POST.getlist("categories"))
        imgs = [Images(image=img, post=post) for img in images]
        Images.objects.bulk_create(imgs)
        # for img in images:
        #     Images.objects.create(
        #         image=img,
        #         post=post
        #     )
        return redirect(to="base")


class ShowDeletePostView(View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            post = None
        author = False
        if request.user == post.user:
            author = True
        return render(
            request=request, template_name="pk_post.html",
            context={
                "post": post,
                "author": author
            }
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            pass
        if request.user != post.user:
            return HttpResponse(
                "<h1>У тебя здесь нет власти</h1>"
            )
        post.delete()
        return redirect(to="base")


class LikesView(View):
    def post(
        self, request: HttpRequest, 
        pk: int, action: Literal["like", "dislike"]
    ):
        client = request.user
        if not client.is_active:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        
        try:
            post = Posts.objects.get(pk=pk)
        except Posts.DoesNotExist:
            return JsonResponse({"error": "Post not found"}, status=404)
        
        reaction, created = PostReaction.objects.get_or_create(
            user=client, post=post
        )
        
        if not created and reaction.reaction == action:
            return JsonResponse({"error": "Already reacted"}, status=400)
        
        if not created:
            if reaction.reaction == "like":
                post.likes -= 1
            elif reaction.reaction == "dislike":
                post.dislikes -= 1
            reaction.reaction = action
        else:
            reaction.reaction = action

        if action == "like":
            post.likes += 1
        elif action == "dislike":
            post.dislikes += 1
        
        reaction.save()
        post.save(update_fields=["likes", "dislikes"])
        
        return JsonResponse({
            "likes": post.likes,
            "dislikes": post.dislikes
        }) 