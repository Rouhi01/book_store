from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404
from django.views import View

from home.forms import CommentForm, CommentReplyForm
from home.models import Comment
from .models import Author, Book, Publisher


class AuthorsView(View):
    template_name = 'literature/authors.html'
    form_class = ''

    def get(self, request):
        authors = Author.objects.all()
        return render(request, template_name=self.template_name, context={'authors': authors})


class AuthorDetailView(View):
    template_name = 'literature/author_detail.html'
    form_class = CommentForm
    form_class_reply = CommentReplyForm

    def get(self, request, author_id):
        form = self.form_class()
        form_reply = self.form_class_reply()

        author = get_object_or_404(Author, id=author_id)

        comments = Comment.objects.filter(
            content_type=ContentType.objects.get(model='author', app_label='literature'),
            object_id=author.id,
            is_reply=False,
        )

        context = {
            'form': form,
            'form_reply': form_reply,
            'author': author,
            'comments': comments,
            'model_name': 'author',
            'app_name': 'literature'
        }

        return render(request, self.template_name, context)


class PublisherView(View):
    template_name = 'literature/publishers.html'
    form_class = ''

    def get(self, request):
        publishers = Publisher.objects.all()
        return render(request, self.template_name, {'publishers': publishers})


class PublisherDetailView(View):
    template_name = 'literature/publisher_detail.html'
    form_class = CommentForm
    form_class_reply = CommentReplyForm

    def get(self, request, publisher_id):
        form = self.form_class()
        form_reply = self.form_class_reply()

        publisher = get_object_or_404(Publisher, id=publisher_id)

        comments = Comment.objects.filter(
            content_type=ContentType.objects.get(model='publisher', app_label='literature'),
            object_id=publisher.id,
            is_reply=False,
        )

        context = {
            'form': form,
            'form_reply': form_reply,
            'publisher': publisher,
            'comments': comments,
            'model_name': 'publisher',
            'app_label': 'literature'
        }

        return render(request, self.template_name, context)