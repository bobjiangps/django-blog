# -*- coding: UTF-8 -*-
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from blog.views import post_detail
from .models import Comment
from .forms import CommentForm

from email.mime.text import MIMEText
import smtplib
import re
import os
import json


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
            reg_comment_at = "@\w*"
            name_re_result = re.findall(reg_comment_at, comment.content)
            if len(name_re_result) > 0:
                print("has @ match result %s " % str(name_re_result))
                email_to_send = []
                for name_at in name_re_result:
                    for c in post.comment_set.all():
                        if c.name == name_at[1:] and c.email not in email_to_send:
                            print("match the name, not send email yet, email is %s" % c.email)
                            send_mail_notification(c.email, your_post=post)
                            email_to_send.append(c.email)
                            # not at - pass
                            # at but not match - admin not receive email - pass
                            # at and match, and has one person match - pass
                            # at and match, and has multiple person match, multiple person has same email - pass
                            # at and match, and has multiple person match, multiple person has different email - not test
                            # multiple at - pass
            send_mail_notification("jbsv43@sina.com", your_post=post, notify_admin=True)
            return redirect(post_detail, post_id=post_id)
        else:
            print("not valid")

    post.comments = post.comment_set.all().filter().order_by('-created_time')
    return render(request, 'blog/post_detail.html', {'post': post})


def send_mail_notification(mail_receiver, your_post, notify_admin=False):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(base_dir, "store.json"), "r") as store_file:
        stored = json.load(store_file)
    if notify_admin:
        subject = "您的文章有了新评论 https://www.byincd.com/bobjiang/article-01" + str(your_post.pk)
    else:
        subject = "您的评论有了新回复 https://www.byincd.com/bobjiang/article-01" + str(your_post.pk)
    content = """请查看新的评论/回复，链接是 <a href='https://www.byincd.com/bobjiang/article-01%s'>https://www.byincd.com/bobjiang/article-01%s</a>.
                  <br>文章标题是: %s <br><br>
                 sent from www.byincd.com""" % (str(your_post.pk), str(your_post.pk), your_post.title)
    msg = MIMEText(content, "html")
    msg["Subject"] = subject
    msg["From"] = stored["email_sender"]
    msg["To"] = mail_receiver
    msg["Cc"] = ""
    smtp = smtplib.SMTP_SSL(stored["smtp_server"])
    smtp.login(stored["email_sender_username"], stored["email_sender_pw"])
    smtp.sendmail(msg["From"], (msg["To"].split(";")) + (msg["Cc"].split(";") if msg["Cc"] is not None else []), msg.as_string())
    smtp.quit()
