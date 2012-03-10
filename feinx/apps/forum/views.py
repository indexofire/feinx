# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
#from django.core.urlresolvers import reverse
from feincms.content.application.models import app_reverse
from apps.forum.forms import EditPostForm, NewPostForm
from apps.forum.models import Topic, Forum, Post
from apps.initial.utils import cache_result


@cache_result
def forums():
    return Forum.objects.select_related().all()

def forum_index(request, tpl="forum/forum_index.html"):
    topics = Topic.objects.select_related().values(
        'id',
        'subject',
        'posted_by',
        'num_views',
        'num_replies',
        'created_on',
        'forum__slug',
        'forum__name',
        'posted_by__username',
        #'posted_by__user__name',
        #'posted_by__avatar',
    )[:getattr(settings, 'LATEST_TOPIC_NUMBER', 10)]
    ctx = {
        'topics': topics,
        'forums': forums(),
    }
    return render(request, tpl, ctx)

def forum_forum(request, forum_slug, tpl="forum/forum_forum.html"):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topics = Topic.objects.select_related().filter(forum__slug=forum_slug). \
        order_by('-sticky', '-last_reply_on').values(
            'id',
            'subject',
            'posted_by',
            'num_views',
            'num_replies',
            'created_on',
            'forum__slug',
            'forum__name',
            'posted_by__username',
            #'posted_by__name',
            #'posted_by__avatar',
        )
    ctx = {
        'forums': forums(),
        'forum': forum,
        'topics': topics,
    }
    return render(request, tpl, ctx)

def forum_topic(request, topic_id, tpl="forum/forum_topic.html"):
    """
    Display a topic and its replies.
    """
    topic = get_object_or_404(Topic.objects.select_related(), pk=topic_id)
    #if not topic.forum.has_access(request.user):
    #    return HttpResponseForbidden()
    Topic.objects.filter(pk=topic_id).update(num_views=F('num_views') + 1)
    threads = topic.post_set.order_by('created_on').select_related()
    ctx = {
        'topic': topic,
        'posts': threads,
        'replies': threads[1:],
        'thread': threads[0],
        'forum': topic.forum,
        'forums': forums(),
    }
    return render(request, tpl, ctx)

def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return HttpResponseRedirect(post.get_absolute_url_ext())

def markitup_preview(request, template_name="forum/markitup_preview.html"):
    return render_to_response(template_name, {'message': request.POST['data']}, RequestContext(request))

@login_required
def forum_post_thread(request, forum_id=None, topic_id=None,
    form_class=NewPostForm, tpl='forum/forum_post_thread.html'):
    """add a new threads which need sign in as a member by default"""
    qpost = topic = forum = first_post = preview = None
    show_subject_fld = True
    post_type = _(u'topic')
    if forum_id:
        forum = get_object_or_404(Forum, pk=forum_id)
    if topic_id:
        post_type = _(u'reply')
        topic = get_object_or_404(Topic, pk=topic_id)
        forum = topic.forum
        topic.num_replies += 1
        #first_post = topic.post_set.order_by('created_on').select_related()[0]
        show_subject_fld = False
    if request.method == "POST":
        if topic is not None: topic.save()
        form = form_class(request.POST, user=request.user, forum=forum,
            topic=topic, ip=request.META['REMOTE_ADDR'])
        preview = request.POST.get('preview', '')
        if form.is_valid() and request.POST.get('submit', ''):
            post = form.save()
            if topic:
                #return HttpResponseRedirect(post.get_absolute_url_ext())
                return HttpResponseRedirect(app_reverse('forum-topic', 'forum.urls', kwargs={'topic_id': topic.pk,}))
            else:
                #return HttpResponseRedirect(reverse("forum-forum", args=[forum.slug]))
                return HttpResponseRedirect(app_reverse("forum-forum", "forum.urls", args=[forum.slug]))
    else:
        initial={}
        qid = request.GET.get('qid', '')
        if qid:
            qpost = get_object_or_404(Post, id=qid)
            initial['message'] = "[quote=%s]%s[/quote]" % (qpost.posted_by.username, qpost.message)
        form = form_class(initial=initial)
    extend_context = {
        'forums': forums(),
        'forum': forum,
        'form': form,
        'topic': topic,
        #'first_post': first_post,
        'post_type': post_type,
        'preview': preview,
        'show_subject_fld': show_subject_fld,
    }
    #extend_context['unpublished_attachments'] = request.user.attachment_set.all().filter(activated=False)
    extend_context['is_new_post'] = True
    return render_to_response(tpl, extend_context, RequestContext(request))

@login_required
def edit_post(request, post_id, form_class=EditPostForm, template_name="forum/forum_post.html"):
    forums = Forum.objects.select_related().all()
    preview = None
    post_type = _('topic')
    edit_post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = form_class(instance=edit_post, user=request.user, data=request.POST)
        preview = request.POST.get('preview', '')
        if form.is_valid() and request.POST.get('submit', ''):
            edit_post = form.save()
            return HttpResponseRedirect('../')
    else:
        form = form_class(instance=edit_post)
    extend_context = {
        'forums': forums,
        'form': form,
        'post': edit_post,
        'topic':edit_post.topic,
        'forum':edit_post.topic.forum,
        'post_type':post_type,
        'preview':preview,
    }
    #extend_context['unpublished_attachments'] = request.user.attachment_set.all().filter(activated=False)
    extend_context['show_subject_fld'] = edit_post.topic_post
    return render_to_response(template_name, extend_context, RequestContext(request))

@login_required
def user_topics(request, user_id, template_name='forum/user_topics.html'):
    view_user = User.objects.get(pk=user_id)
    topics = view_user.topic_set.order_by('-created_on').select_related()
    extend_context = {
        'topics': topics,
        'view_user': view_user,
    }
    return render_to_response(template_name, extend_context, RequestContext(request))

@login_required
def user_posts(request, user_id, template_name='forum/user_posts.html'):
    view_user = User.objects.get(pk=user_id)
    posts = view_user.post_set.order_by('-created_on').select_related()
    extend_context = {
        'posts': posts,
        'view_user': view_user,
    }
    return render_to_response(template_name, extend_context, RequestContext(request))





from django.views.generic import ListView, DetailView


class ForumIndexView(ListView):
    """
    Index Page of Forum
    """


class TopicDetailView(DetailView):
    """
    Topic View
    """
    qs = Topic.objects.all()
