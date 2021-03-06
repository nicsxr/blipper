from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Q, Count
from account.models import Account
from main.models import Post
from main.forms import PostForm, PostUpdateForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage


posts_per_page = 7

def home_view(request):
    context = {
    }
    users = Account.objects.annotate(count=Count('followers')).order_by('-count')[:3]
    context['top_users'] = users
    page_num = request.GET.get('page',1)
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

        try:
            page = Paginator(posts, posts_per_page).page(page_num)
        except EmptyPage:
            page = Paginator(posts, posts_per_page).page(1)
        
        context['posts'] = page
    
    else:
        posts = Post.objects.all().order_by('-date_posted')
        try:
            page = Paginator(posts, posts_per_page).page(page_num)
        except EmptyPage:
            page = Paginator(posts, posts_per_page).page(1)
        context['posts'] = page
    return render(request, 'home.html', context)


def profile_view(request, id):
    context={
    }
    page_num = request.GET.get('page',1)
    try:
        user = Account.objects.get(id=id)
        posts = Post.objects.filter(poster=user)
        context['user_profile'] = user
        try:
            page = Paginator(posts, posts_per_page).page(page_num)
        except EmptyPage:
            page = Paginator(posts, posts_per_page).page(1)
        context['posts'] = page
        context['posts_count'] = posts.count()
    except ObjectDoesNotExist:
        messages.warning(request, 'Account not found!')
        return redirect('/')
    
    return render(request, 'home.html', context)

@login_required
def post_update_view(request, id):

    try:
        post = Post.objects.get(id=id)
    except ObjectDoesNotExist:
        messages.warning(request, 'Post does not exist.')
        return redirect('/')

    if post.poster != request.user:
        messages.warning(request, 'Post does not belong to you!')
        return redirect('/')
    

    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)
        if 'delete' in request.POST:
            post.delete()

            messages.warning(request, 'Post DELETED succesfully!')
            return redirect('/')
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated succesfully!')
            return redirect('/')
        else:
            messages.warning(request, 'Something went wrong!')
            return redirect('/')

    else:
        form = PostUpdateForm(instance=post)
    context = {
        'form': form,
    }
    return render(request, 'postUpdate.html', context)

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
    print(request)
    if request.method == 'POST':
        try:
            user = request.user
            followee = Account.objects.get(id=id)

            if followee in user.following.all():
                return HttpResponseBadRequest()

            user.following.add(followee)
            followee.followers.add(user)
            return HttpResponse(followee.followers.count())
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()

def search_user(request, name):
    if request.method == 'POST':
        try:
            user = Account.objects.get(username__iexact=name)

            #check if I follow him
            if request.user.is_authenticated:
                i_follow = user in request.user.following.all()
            else:
                i_follow = False

            context = JsonResponse({
                'id': user.id,
                'username': user.username,
                'followers': user.followers.all().count(),
                'following': user.following.all().count(),
                'i_follow': i_follow
            })
            return context
        except ObjectDoesNotExist:
            return HttpResponseBadRequest()
        