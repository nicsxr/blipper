from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Q
from account.models import Account
from main.models import Post
from main.forms import PostForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home_view(request):
    context = {
    }
    if request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            poster = request.user
            content = form.cleaned_data.get('content')
            post = Post(poster=poster, content=content)
            post.save()
            return redirect('home')
        else:
            messages.warning(request, 'Post must be at least 1 character and not more than 255 characters.')
            context['post_form'] = form
            return redirect('home')

    if request.user.is_authenticated:
        form = PostForm()
        context['post_form'] = form
        followers = (Q(request.user.following.all()) | Q(request.user))
        if len(followers) > 3:
            posts = Post.objects.filter(poster__in=followers).order_by('-date_posted')
        else:
            posts = Post.objects.all().order_by('-date_posted')
        context['posts'] = posts
    else:
        posts = Post.objects.all().order_by('-date_posted')
        context['posts'] = posts
    return render(request, 'home.html', context)


def profile_view(request, id):
    context={

    }
    try:
        user = Account.objects.get(id=id)
        posts = Post.objects.filter(poster=user)
        context['user'] = user
        context['posts'] = posts
    except ObjectDoesNotExist:
        messages.warning(request, 'Account not found!')
        return redirect('/')
    
    return render(request, 'profile.html', context)


# API CALLS
@login_required(login_url='/account/login/')
def like_post(request, id):
    # cotext= {}
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=id)
            if request.user in post.likers.all():
                messages.warning(request, 'Already liked!')
                return HttpResponseForbidden()
            post.likers.add(request.user)
            post.likes += 1
            post.save()
            return JsonResponse({
                'likes': post.likes
            })
        except ObjectDoesNotExist:
            messages.warning(request, 'Post doesnot exist!')
            return redirect('/')
    return HttpResponseForbidden()

@login_required(login_url='/account/login/')
def follow_user(request, id):
    if request.method == 'POST':
        try:
            user = request.user
            followee = Account.objects.get(id=id)

            if followee in user.following.all():
                return HttpResponseBadRequest()

            user.following.add(followee)
            followee.followers.add(user)
            return HttpResponse('Success')
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()

def search_user(request, name):
    if request.method == 'POST':
        try:
            user = Account.objects.get(username=name)
            return JsonResponse({
                'id': user.id,
                'username': user.username,
                'followers': user.followers.all().count(),
                'following': user.following.all().count(),
                'i_follow': user in request.user.following.all()
            })
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()