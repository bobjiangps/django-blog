from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponse, StreamingHttpResponse
from wsgiref.util import FileWrapper
from django.utils import timezone
from .models import Post, Visitor, Category, Tag
from .forms import PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as d_login, logout as d_logout
from django.db import connection
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from utils.geoip_helper import GeoIpHelper
from bobjiang.settings import BASE_DIR, RECORD_VISITOR
from django.contrib.auth.decorators import permission_required, login_required
# import markdown
import os
import mimetypes


def top_viewed_posts(request, amount=5):
    record_visit(request)
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        # posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visiable__name='public').order_by('views').reverse()
        new_posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visiable__name='public').order_by('published_date').reverse()
    else:
        # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('views').reverse()
        new_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
    # for the posts which set to top
    posts = Post.objects.filter(id__in=[104, 61, 68, 78, 203]).order_by("views").reverse()

    top_viewed_tag_sql = """
        SELECT sum(bp.views) as sum_view, bt.name FROM `blog_post` as bp 
        left join `blog_visiable` as bv on bp.visiable_id = bv.id 
        left join `blog_post_tag` as bpt on bpt.post_id = bp.id 
        left join `blog_tag` as bt on bpt.tag_id = bt.id 
        where bv.name = 'public' 
        group by bpt.tag_id 
        order by sum_view desc 
        limit 6 
    """
    with connection.cursor() as cursor:
        cursor.execute(top_viewed_tag_sql)
        rows = cursor.fetchall()
        top_viewed_tags = [r[1] for r in rows]
    return render(request, 'blog/main.html', {'posts': posts[:amount], 'new_posts': new_posts[:amount], 'top_tags': top_viewed_tags})


def post_list(request):
    record_visit(request)
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        # posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visiable__name='public').order_by('published_date').reverse()
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visiable__name='public').order_by('views').reverse()
    else:
        # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('views').reverse()
    return pagination(request, posts)


def post_list_sort(request, sort_type):
    record_visit(request)
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        if sort_type == 'date':
            posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visiable__name='public').order_by('published_date').reverse()
        elif sort_type == 'view':
            posts = Post.objects.filter(published_date__lte=timezone.now()).filter(visiable__name='public').order_by('views').reverse()
    else:
        if sort_type == 'date':
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date').reverse()
        elif sort_type == 'view':
            posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('views').reverse()
    return pagination(request, posts)


def post_detail(request, post_id):
    record_visit(request)
    post = get_object_or_404(Post, pk=post_id)
    if post.visiable.name == "private" and request.user.is_authenticated == False:
        return render(request, 'error/403.html')
    post.comments = post.comment_set.all().filter().order_by('-created_time')
    post.increase_views()
    # post.text = markdown.markdown(post.text, extensions=['markdown.extensions.extra','markdown.extensions.codehilite','markdown.extensions.toc'])
    post_prev = Post.objects.filter(visiable__name='public').filter(id__lt=post_id).order_by('-id').first()
    post_next = Post.objects.filter(visiable__name='public').filter(id__gt=post_id).order_by('id').first()
    return render(request, 'blog/post_detail.html', {'post': post, 'post_prev': post_prev, 'post_next': post_next})


@permission_required('blog.change_post', raise_exception=True)
def post_edit(request, post_id):
    record_visit(request)
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            try:
                post.author = request.user
            except ValueError:
                # return HttpResponse('<h1>please login first</h1>')
                return render(request, 'error/403.html')
            post.save()
            form.save_m2m()
            return redirect(post_detail, post_id=post.id)
    else:
        users = [u.username for u in User.objects.all()]
        login_user = request.user.username
        if login_user not in users:
            # return render(request, 'blog/unauthenticated.html')
            return render(request, 'error/403.html')
        else:
            form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@permission_required('blog.add_post', raise_exception=True)
def create_new(request):
    record_visit(request)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            try:
                post.author = request.user
            except ValueError:
                # return HttpResponse('<h1>please login first</h1>')
                return render(request, 'error/403.html')
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect(post_detail, post_id=post.id)
    else:
        users = [u.username for u in User.objects.all()]
        login_user = request.user.username
        if login_user not in users:
            # return render(request, 'blog/unauthenticated.html')
            return render(request, 'error/403.html')
        else:
            form = PostForm()
    return render(request, 'blog/create_new.html', {'form': form})


def archives(request):
    # Post.objects.filter(visiable__name='public').annotate(total_comments=Count('comment')).order_by("-total_comments")
    record_visit(request)
    all_category = []
    all_tag = []
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        date_list = Post.objects.filter(visiable__name='public').dates('published_date', 'month', order='DESC')
        category_by_post_view = Category.objects.annotate(blog_views=Count('post__views')).filter(post__visiable__name='public').order_by('-blog_views')
        tag_by_post_view = Tag.objects.annotate(blog_views=Sum('post__views')).filter(post__visiable__name='public').order_by('-blog_views')
        for c in category_by_post_view:
            all_category.append(c.name)
        for t in tag_by_post_view:
            all_tag.append(t.name)
    else:
        date_list = Post.objects.dates('published_date', 'month', order='DESC')
        category_by_post_view = Category.objects.annotate(blog_views=Count('post__views')).order_by('-blog_views')
        tag_by_post_view = Tag.objects.annotate(blog_views=Sum('post__views')).order_by('-blog_views')
        for c in category_by_post_view:
            all_category.append(c.name)
        for t in tag_by_post_view:
            all_tag.append(t.name)
    return render(request, 'blog/archives.html', context={'date_list': date_list, 'category_list': all_category, 'tag_list': all_tag})


def archives_date(request, year, month):
    record_visit(request)
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        posts = Post.objects.filter(visiable__name='public').filter(published_date__year=year, published_date__month=month).order_by('views').reverse()
    else:
        posts = Post.objects.filter(published_date__year=year, published_date__month=month).order_by('views').reverse()
    return pagination(request, posts)


def archives_date_sort(request, year, month, sort_type):
    record_visit(request)
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        if sort_type == 'date':
            posts = Post.objects.filter(visiable__name='public').filter(published_date__year=year, published_date__month=month).order_by('published_date').reverse()
        elif sort_type == 'view':
            posts = Post.objects.filter(visiable__name='public').filter(published_date__year=year, published_date__month=month).order_by('views').reverse()
    else:
        if sort_type == 'date':
            posts = Post.objects.filter(published_date__year=year, published_date__month=month).order_by('published_date').reverse()
        elif sort_type == 'view':
            posts = Post.objects.filter(published_date__year=year, published_date__month=month).order_by('views').reverse()
    return pagination(request, posts)


def archives_category(request, category_name):
    record_visit(request)
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        posts = Post.objects.filter(visiable__name='public').filter(published_date__lte=timezone.now()).filter(category__name=category_name).order_by('views').reverse()
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(category__name=category_name).order_by('views').reverse()
    return pagination(request, posts)


def archives_category_sort(request, category_name, sort_type):
    record_visit(request)
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        if sort_type == 'date':
            posts = Post.objects.filter(visiable__name='public').filter(published_date__lte=timezone.now()).filter(category__name=category_name).order_by('published_date').reverse()
        elif sort_type == 'view':
            posts = Post.objects.filter(visiable__name='public').filter(published_date__lte=timezone.now()).filter(category__name=category_name).order_by('views').reverse()
    else:
        if sort_type == 'date':
            posts = Post.objects.filter(published_date__lte=timezone.now()).filter(category__name=category_name).order_by('published_date').reverse()
        elif sort_type == 'view':
            posts = Post.objects.filter(published_date__lte=timezone.now()).filter(category__name=category_name).order_by('views').reverse()
    return pagination(request, posts)


def archives_tag(request, tag_name):
    record_visit(request)
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        posts = Post.objects.filter(visiable__name='public').filter(published_date__lte=timezone.now()).filter(tag__name=tag_name).order_by('views').reverse()
    else:
        posts = Post.objects.filter(published_date__lte=timezone.now()).filter(tag__name=tag_name).order_by('views').reverse()
    return pagination(request, posts)


def archives_tag_sort(request, tag_name, sort_type):
    record_visit(request)
    users = [u.username for u in User.objects.all()]
    login_user = request.user.username
    if login_user not in users:
        if sort_type == 'date':
            posts = Post.objects.filter(visiable__name='public').filter(published_date__lte=timezone.now()).filter(tag__name=tag_name).order_by('published_date').reverse()
        elif sort_type == 'view':
            posts = Post.objects.filter(visiable__name='public').filter(published_date__lte=timezone.now()).filter(tag__name=tag_name).order_by('views').reverse()
    else:
        if sort_type == 'date':
            posts = Post.objects.filter(published_date__lte=timezone.now()).filter(tag__name=tag_name).order_by('published_date').reverse()
        elif sort_type == 'view':
            posts = Post.objects.filter(published_date__lte=timezone.now()).filter(tag__name=tag_name).order_by('views').reverse()
    return pagination(request, posts)


def pagination(request,filter_posts):
    paginator = Paginator(filter_posts, 5)
    page = request.GET.get('page', 1)
    try:
        part_posts = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page.
        part_posts = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page of results
        part_posts = paginator.page(paginator.num_pages)
    # return render(request, 'blog/post_list.html', {'posts':posts})
    return render(request, 'blog/post_list.html', {'posts': part_posts})


def about_site_me(request):
    record_visit(request)
    return render(request, 'blog/about.html')


def about_me(request):
    record_visit(request)
    # update_wordcloud()
    return render(request, 'blog/about_me.html')


def update_wordcloud():
    import jieba
    import wordcloud
    import os

    wc_file_name = "./media/wordcloud/aboutme_wordcloud.png"
    if os.path.exists(wc_file_name):
        os.remove(wc_file_name)
    with open("./media/wordcloud/string_source.txt", "r", encoding='UTF-8') as f:
        text = f.read()
    user_define_file = "./media/wordcloud/user_define.txt"
    jieba.load_userdict(user_define_file)
    cut = jieba.cut(text)
    strings = ' '.join(cut)

    w = wordcloud.WordCloud(font_path='./media/wordcloud/simhei.ttf', width=1000, height=700, background_color='white')
    w.generate(strings)
    w.to_file(wc_file_name)


def about_site(request):
    record_visit(request)
    return render(request, 'blog/about_site.html')


@login_required
def about_visitor(request):
    record_visit(request)
    return render(request, 'blog/about_visitor.html')


def do_login(request):
    record_visit(request)
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
                return render(request, 'blog/login.html', {'username': userName, 'password': userPassword})
        else:
            request.session['login_error'] = "错误的用户名或密码"
            return render(request, 'blog/login.html', {'username': userName, 'password': userPassword})


def do_logout(request):
    record_visit(request)
    d_logout(request)
    return redirect(reverse('post_list'))


def show_view_record(request):
    days = request.POST.get('day_period')
    # view_string = "<thead><tr><th scope='col'>#</th><th scope='col'>name1</th><th scope='col'>name2</th><th scope='col'>name3</th></tr></thead>"
    import codecs
    with codecs.open("/home/test/record_view/count_record_views.csv", encoding="utf8") as f:
        data = f.readlines()

    seq_sort = []
    start_flag = False
    start_seq = 0
    end_seq = 0
    for seq, line in enumerate(data):
        if len(line) > 1 and start_flag == False:
            start_seq = seq
            start_flag = True
        elif len(line) <= 1 and start_flag == True:
            end_seq = seq-1
            seq_sort.append((start_seq, end_seq))
            start_flag = False
    seq_sort.reverse()
    seq_sort = seq_sort[:5]

    recorded_post_ids = data[int(seq_sort[0][0]) + 1].strip().split(",")
    temp_head_string = ""
    for number_list in seq_sort:
        temp_head_string += "<th scope='col'>%s</th>" % data[number_list[0]][:10]
    thead_string = "<thead><tr><th scope='col'>%d</th>%s</tr></thead>" % (len(recorded_post_ids), temp_head_string)

    recorded_post_values = [1, 2, 3, 4, 5]
    for num in range(len(seq_sort)):
        title_view_dict = {}
        id_list = data[int(seq_sort[num][0]) + 1].strip().split(",")
        name_list = data[int(seq_sort[num][0]) + 2].strip().split(",")
        views_list = data[int(seq_sort[num][1])].strip().split(",")
        for id_num in range(len(id_list)):
            title_view_dict[id_list[id_num]] = {"title": name_list[id_num], "views": views_list[id_num]}
        recorded_post_values[num] = title_view_dict
    tbody_string = "<tbody></tbody>"
    for post_id in recorded_post_ids:
        temp_tbody_td_string = ""
        for value_id in range(len(recorded_post_values)):
            try:
                temp_tbody_td_string += "<td>%s</td>" % recorded_post_values[value_id][post_id]["views"]
            except:
                temp_tbody_td_string += "<td>no data</td>"
        temp_tbody_string = "<tr><th scope='row'>%s</th>%s</tr>" % (recorded_post_values[0][post_id]["title"],temp_tbody_td_string)
        tbody_string += temp_tbody_string

    view_string = thead_string + tbody_string
    return HttpResponse('{"status":"success", "view_string":"%s"}' % view_string, content_type='application/json')


def record_visit(request):
    if RECORD_VISITOR:
        try:
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                current_ip = request.META.get('HTTP_X_FORWARDED_FOR')
            else:
                current_ip = request.META.get('REMOTE_ADDR')
            if "HTTP_USER_AGENT" in request.META:
                current_agent = request.META["HTTP_USER_AGENT"]
            else:
                current_agent = "no agent key in request"
            current_page = request.get_full_path()
            today = timezone.now()

            visitor_exist = Visitor.objects.filter(ip=str(current_ip), page=current_page, record_date__range=(today.date(), today.date() + timezone.timedelta(days=1)))
            if visitor_exist:
                current_visitor = visitor_exist[0]
                current_visitor.increase_views()
            else:
                current_visitor = Visitor()
                current_visitor.ip = current_ip
                ip_exist = Visitor.objects.filter(ip=str(current_ip)).order_by('-id')
                generate_new_location = True
                if ip_exist:
                    generate_new_location = False
                    temp_visitor = ip_exist[0]
                    if (today - temp_visitor.record_date).days >= 7:
                        generate_new_location = True
                    if temp_visitor.region:
                        current_visitor.region = temp_visitor.region
                if generate_new_location:
                    if current_ip not in ["127.0.0.1", "localhost"]:
                        try:
                            current_visitor.region = GeoIpHelper.get_location(current_ip)
                        except Exception as e:
                            print("error when get location from ipify, message: %s" % str(e))
                current_visitor.agent = current_agent
                current_visitor.page = current_page
                if 'HTTP_REFERER' in request.META.keys():
                    temp_referer = request.META["HTTP_REFERER"]
                    temp_host = request.get_host()
                    if temp_host not in temp_referer.split("/"):
                        current_visitor.referer = temp_referer
                current_visitor.record_date = today
                current_visitor.update_date = today
                current_visitor.views = 1
                current_visitor.save()
        except Exception as e:
            print("get error when record visitor, message: %s" % str(e))
            with open("./record_visitor_error.txt", "a") as f:
                f.write(str(timezone.now()))
                f.write("\n")
                f.write(str(e))
                f.write("\n\n")


def download_bak(request):
    if request.user.is_authenticated:
        bak_file = "other/db_bak/django-blog-v2-latest.sql"
        filename = os.path.basename(bak_file)
        abs_path = os.path.join(BASE_DIR, bak_file)
        if os.path.exists(abs_path):
            chunk_size = 8192
            response = StreamingHttpResponse(FileWrapper(open(abs_path, 'rb'), chunk_size), content_type=mimetypes.guess_type(abs_path)[0])
            response['Content-Length'] = os.path.getsize(abs_path)
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response
        else:
            return HttpResponse('<h1>Cannot find the file</h1>')
    else:
        # return HttpResponse('<h1>please login first</h1>')
        return render(request, 'error/403.html')


def page_not_found(request, exception):
    return render(request, 'error/404.html')


def permission_denied(request, exception):
    return render(request, 'error/403.html')


def internal_error(request):
    return render(request, 'error/500.html')
