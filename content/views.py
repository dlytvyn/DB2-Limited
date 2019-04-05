from django.shortcuts import render, redirect, reverse
from .forms import PostForm, CommentForm
from .models import Posts, Likes, Comments


def add_comment_view(request, id):
    form = CommentForm(request.POST or None)
    post = Posts.objects.get(id=id)
    if form.is_valid():
        form.save(request, post)
    return redirect(reverse('account:one_post', kwargs={'id': post.id}))


def add_post_view(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        user = form.save(request, commit=False)
        if request.FILES:
            user.photo = request.FILES['photo']
        user.save()
        return redirect('account_page')
    return render(request, 'content/add_post.html', {'form': form})


def one_post_view(request, id):
    post = Posts.objects.get(id=id)
    form = CommentForm()
    return render(request, "content/one_post.html", {'post': post,
                                                     'form': form})


def like_view(request, id):
    post = Posts.objects.get(id=id)
    if not Likes.objects.filter(post_id=post.id, user_id=request.user.id).first():
        Likes(post=post, user=request.user).save()
    return redirect(reverse('account_page'))


def liked_view(request, id):
    post = Posts.objects.get(id=id)
    like = Likes.objects.filter(post=post, user=request.user)
    if like:
        like.delete()
    return redirect(reverse('account_page'))
