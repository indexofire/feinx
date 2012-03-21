# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models import F
from django.views.generic import View, CreateView, DetailView
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from feincms.content.application.models import app_reverse
from feinx.apps.forum.forms import EditPostForm, NewPostForm
from feinx.apps.forum.models import Forum, Topic, Reply
from feinx.utils.cache import cache_result

@cache_result
def forums():
    return Forum.objects.select_related().all()

class ForumIndexView(View):
    """
    Index page of forum.
    """
    template_name = 'forum/forum_index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['topics'] = Topic.objects.select_related().values(
            'id',
            'subject',
            'author',
            'view_num',
            'reply_num',
            'created',
            'forum__id',
            'forum__name',
            'author__username',
        )[:getattr(settings, 'LATEST_TOPIC_NUMBER', 10)]
        context['forums'] = forums()
        return render(request, self.template_name, context)

class ForumForumView(View):
    """
    Each forum categories view
    """
    template_name = 'forum/forum_forum.html'

    #def get_queryset(self):
    #    forum = get_object_or_404(Forum, slug__iexact=self.args[0])

    def get(self, request, *args, **kwargs):
        context = {}
        context['topics'] = Topic.objects.filter(forum__id=kwargs['forum_id']).select_related().order_by('-sticky').values(
            'id',
            'subject',
            'author',
            'view_num',
            'reply_num',
            'created',
            'forum__id',
            'forum__name',
            'author__username',
        )
        context['forums'] = forums()
        context['forum_id'] = kwargs['forum_id']
        return render(request, self.template_name, context)

class ForumTopicView(View):
    """
    Display all threads of each topic.
    """

    template_name = 'forum/forum_topic.html'

    def get(self, request, *args, **kwargs):
        topic = get_object_or_404(Topic.objects.select_related().values(
            'id',
            'author__username',
            'content',
            'forum',
            'forum__id',
            ), pk=kwargs['topic_id'])        
        Topic.objects.filter(pk=kwargs['topic_id']).update(view_num=F('view_num') + 1)
        #t = get_object_or_404(Topic, pk=kwargs['topic_id'])
        forum = topic['forum']
        forum_id = topic['id']
        replies = t.reply_set.order_by('created').select_related()
        context = {
            'topic': topic,
            'posts': replies,
            'replies': replies,
            'thread': topic,
            'forum': forum,
            'forums': forums(),
        }
        return render(request, self.template_name, context)


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


class ForumPostView(CreateView):
    """
    Post new topic or reply view.
    """
    template_name = 'forum/forum_post.html'
    forum = None
    topic = None

    def get_form_kwargs(self):

        if self.kwargs['forum_id']:
            forum = get_object_or_404(Forum, pk=self.kwargs['forum_id'])
        elif self.kwargs['topic_id']:
            topic = get_object_or_404(Topic, pk=self.kwargs['topic_id'])
            topic.update(num_replies=F('num_replies') + 1)
            #forum = topic.forum
        self.forum = forum
        self.topic = topic

    def get_context_data(self, **kwargs):
        context = super(ForumPostView, self).get_context_data(**kwargs)
        context['forum'] = self.forum
        context['topic'] = self.topic

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
                return HttpResponseRedirect(app_reverse('forum-topic', 'feinx.apps.forum.urls', kwargs={'topic_id': topic.pk,}))
            else:
                #return HttpResponseRedirect(reverse("forum-forum", args=[forum.slug]))
                return HttpResponseRedirect(app_reverse('forum-forum', 'feinx.apps.forum.urls', args=[forum.slug]))
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

class ForumDeleteView(View):
    """
    Delete a post.
    """
    pass


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

class TopicDetailView(DetailView):
    """
    Topic View
    """
    qs = Topic.objects.all()
