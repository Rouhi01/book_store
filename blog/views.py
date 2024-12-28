from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render
from django.views import View

from home.forms import CommentForm, CommentReplyForm
from home.models import Comment
from .models import Blog, Tag
from literature.models import Category


class BlogsView(View):
    template_name = 'blog/blogs.html'
    form_class = ''

    def get(self, request):
        blogs = Blog.objects.all()
        latest_blogs = blogs
        tags = Tag.objects.all()
        categories = Category.objects.all()

        category = request.GET.get('category')
        tag = request.GET.get('tag')
        search = request.GET.get('search')



        if category:
            blogs = blogs.filter(category__id=category)

        if tag:
            blogs = blogs.filter(tag__id=tag)

        if search:
            blogs = blogs.filter(
                Q(title__icontains=search) |
                Q(user__profile__first_name__icontains=search) |
                Q(user__profile__last_name__icontains=search)
            )

        context = {
            'latest_blogs': latest_blogs,
            'blogs': blogs,
            'tags': tags,
            'categories': categories
        }
        return render(request, self.template_name, context)


class BlogDetailView(View):
    template_name = 'blog/blog_detail.html'
    form_class = CommentForm
    form_class_reply = CommentReplyForm

    def get(self, request, blog_id, slug):
        form = self.form_class()
        form_reply = self.form_class_reply()

        blog = Blog.objects.get(id=blog_id, slug=slug)

        related_blogs = Blog.objects.filter(
            Q(tag__in=blog.tag.all()) |
            Q(category__name__exact=blog.category.name) |
            Q(user__id=blog.user.id)
        )[:4]

        comments = Comment.objects.filter(
            content_type=ContentType.objects.get(model='blog', app_label='blog'),
            object_id=blog.id,
            is_reply=False,
        )

        context = {
            'form': form,
            'form_reply': form_reply,
            'blog': blog,
            'comments': comments,
            'model_name': 'blog',
            'app_label': 'blog',
            'related_blogs': related_blogs
        }
        return render(request, self.template_name, context)

