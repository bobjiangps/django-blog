from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from blog.models import Post
from blog.views import post_detail
from .models import Comment
from .forms import CommentForm

def post_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']
            comment = Comment(name=name, email=email, content=content)
            comment.post = post
            comment.save()
            print("valid in if")
            return redirect(post_detail,post_id=post_id)
        else:
            print("not valid")
            
    print("not post method")
    post.comments = post.comment_set.all().filter().order_by('-created_time')
    return render(request, 'blog/post_detail.html', {'post': post})
