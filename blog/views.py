from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as d_login, logout as d_logout
#import markdown


def post_list(request):
    try:
        login_user = request.user
        if str(login_user) == 'AnonymousUser':
            raise
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    except:
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visiable__name='public').order_by('published_date').reverse()
    return pagination(request,posts)

def post_list_sort(request, sort_type):
    try:
        login_user = request.user
        if str(login_user) == 'AnonymousUser':
            raise
        if sort_type == 'date':
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
        elif sort_type == 'view':
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('views').reverse()
    except:
        if sort_type == 'date':
            posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visiable__name='public').order_by('published_date').reverse()
        elif sort_type == 'view':
            posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visiable__name='public').order_by('views').reverse()
    return pagination(request,posts)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.comments = post.comment_set.all().filter().order_by('-created_time')
    post.increase_views()
    #post.text = markdown.markdown(post.text, extensions=['markdown.extensions.extra','markdown.extensions.codehilite','markdown.extensions.toc'])
    return render(request, 'blog/post_detail.html', {'post': post})

def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            try:
                post.author = request.user
            except ValueError:
                return HttpResponse('<h1>please login first</h1>')
            post.save()
            return redirect(post_detail, post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

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

def archives(request):
    all_category = []
    all_tag = []
    try:
        login_user = request.user
        if str(login_user) == 'AnonymousUser':
            raise
        date_list = Post.objects.dates('published_date', 'month', order='DESC')
        posts = Post.objects.all()
        for p in posts:
            if p.category.name not in all_category:
                all_category.append(p.category.name)
            for t in p.tag.all():
                if t.name not in all_tag:
                    all_tag.append(t.name)
    except:
        date_list = Post.objects.filter(visiable__name='public').dates('published_date', 'month', order='DESC')
        posts = Post.objects.filter(visiable__name='public')
        for p in posts:
            if p.category.name not in all_category:
                all_category.append(p.category.name)
            for t in p.tag.all():
                if t.name not in all_tag:
                    all_tag.append(t.name)
    all_category.sort()
    all_tag.sort()
    return render(request, 'blog/archives.html', context={'date_list': date_list, 'category_list': all_category, 'tag_list': all_tag})

def archives_date(request, year, month):
    try:
        login_user = request.user
        if str(login_user) == 'AnonymousUser':
            raise
        posts = Post.objects.filter(published_date__year=year,published_date__month=month).order_by('published_date').reverse()
    except:
        posts = Post.objects.filter(visiable__name='public').filter(published_date__year=year,published_date__month=month).order_by('published_date').reverse()
    return pagination(request,posts)

def archives_category(request, category_name):
    try:
        login_user = request.user
        if str(login_user) == 'AnonymousUser':
            raise
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(category__name=category_name).order_by('published_date').reverse()
    except:
        posts = Post.objects.filter(visiable__name='public').filter(published_date__lte=timezone.now()).filter(category__name=category_name).order_by('published_date').reverse()
    return pagination(request,posts)

def archives_tag(request, tag_name):
    try:
        login_user = request.user
        if str(login_user) == 'AnonymousUser':
            raise
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(tag__name=tag_name).order_by('published_date').reverse()
    except:
        posts = Post.objects.filter(visiable__name='public').filter(published_date__lte=timezone.now()).filter(tag__name=tag_name).order_by('published_date').reverse()
    return pagination(request,posts)

def pagination(request,filter_posts):
    paginator = Paginator(filter_posts, 5)
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

def about_site_me(request):
    return render(request, 'blog/about.html')

def about_me(request):
    return render(request, 'blog/about_me.html')

def about_site(request):
    return render(request, 'blog/about_site.html')

def do_login(request):
    if request.method == 'GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/') 
        request.session['login_error'] = False
        user = request.user
        if user.is_authenticated:
            return redirect(reverse("post_list"))
        else:
            return render(request, 'blog/login.html')
    elif request.method == "POST":
        userName = request.POST['user-name']
        userPassword = request.POST['user-pw']
        user = authenticate(username=userName, password=userPassword)
        if user is not None: 
            if user.is_active:
                d_login(request, user)
                return redirect(request.session['login_from'])  # go back to page before login
            else:
                request.session['login_error'] = "未激活用户"
                return render(request,'blog/login.html',{'username':userName,'password':userPassword})
        else:
            request.session['login_error'] = "错误的用户名或密码"
            return render(request,'blog/login.html',{'username':userName,'password':userPassword})

def do_logout(request):
    d_logout(request)
    return redirect(reverse('post_list'))
