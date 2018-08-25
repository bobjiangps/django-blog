from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    try:
        login_user = request.user
        if str(login_user) == 'AnonymousUser':
            raise
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    except:
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visiable__name='public').order_by('published_date').reverse()
    paginator = Paginator(posts, 5)
    page = request.GET.get('page',1)
    try:
        part_posts = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer, deliver first page.
        part_posts = paginator.page(1)
    except EmptyPage:
        #if page is out of range, deliver last page of results
        part_posts = paginator.page(paginator.num_pages)
    #return render(request, 'blog/post_list.html', {'posts':posts})
    return render(request, 'blog/post_list.html', {'posts':part_posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.comments = post.comment_set.all().filter().order_by('-created_time')
    post.increase_views()
    return render(request, 'blog/post_detail.html', {'post': post})

def create_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            try:
                post.author = request.user
            except ValueError:
                return HttpResponse('<h1>请先登陆</h1>')
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/create_new.html', {'form': form})

