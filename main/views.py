from django.shortcuts import render, redirect
from account.models import Account, Follow
from main.models import Post, Like
from main.forms import PostForm
from django.core.exceptions import ObjectDoesNotExist

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
            context['post_form'] = form
            return redirect('home')

    if request.user.is_authenticated:
        likes = Like.objects.filter(liker=request.user)
        form = PostForm()
        context['post_form'] = form
        context['likes'] = likes
    posts = Post.objects.all().order_by('-date_posted')
    context['posts'] = posts
    return render(request, 'home.html', context)

def like_post(request, id):
    # cotext= {}
    try:
        post=Post.objects.get(id=id)
        like = Like.objects.get(liker=request.user, post=post)
        return redirect('/')
    except ObjectDoesNotExist:
        #messages.warning(request, 'Obj doesnot exist!')
        post=Post.objects.get(id=id)
        like = Like(liker=request.user, post=post)
        like.save()
        post.likes += 1
        post.save()
        return redirect('/')

    #need to check permission !!!!!!!!!!!!!!1

    # return render(request, '/', context)
    # if request.POST:
    #     return 0

