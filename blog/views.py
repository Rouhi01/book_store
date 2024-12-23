from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.views import View

from home.forms import CommentForm, CommentReplyForm
from home.models import Comment
from .models import Blog


class BlogsView(View):
    template_name = 'blog/blogs.html'
    form_class = ''

    def get(self, request):
        blogs = Blog.objects.all()
        context = {
            'blogs': blogs
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
            'app_label': 'blog'
        }
        return render(request, self.template_name, context)

