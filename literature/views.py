from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View

from home.forms import CommentForm, CommentReplyForm
from home.models import Comment
from .forms import BookSearchForm
from .models import Author, Book, Publisher, Translator, Category


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


class TranslatorsView(View):
    template_name = 'literature/translators.html'
    form_class = ''

    def get(self, request):
        translators = Translator.objects.all()
        return render(request, template_name=self.template_name, context={'translators': translators})


class TranslatorDetailView(View):
    template_name = 'literature/translator_detail.html'
    form_class = CommentForm
    form_class_reply = CommentReplyForm

    def get(self, request, translator_id):
        form = self.form_class()
        form_reply = self.form_class_reply()

        translator = get_object_or_404(Translator, id=translator_id)

        comments = Comment.objects.filter(
            content_type=ContentType.objects.get(model='translator', app_label='literature'),
            object_id=translator.id,
            is_reply=False,
        )

        context = {
            'form': form,
            'form_reply': form_reply,
            'translator': translator,
            'comments': comments,
            'model_name': 'translator',
            'app_label': 'literature'
        }

        return render(request, self.template_name, context)


class BooksView(View):
    template_name = 'literature/books.html'

    def get(self, request):
        books = Book.objects.all()

        category = request.GET.getlist('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        publisher = request.GET.getlist('publisher')
        author = request.GET.getlist('author')
        search = request.GET.get('search')
        sort_by = request.GET.get('sort_by')

        if category:
            books = books.filter(category__id__in=category)

        if min_price:
            books = books.filter(price__gte=min_price)

        if max_price:
            books = books.filter(price__lte=max_price)

        if publisher:
            books = books.filter(publisher__id__in=publisher)

        if author:
            books = books.filter(author__id__in=author)

        if search:
            books = books.filter(
                Q(title__icontains=search) | Q(author__name__icontains=search)
            )

        # if sort_by == 'popularity':
        #     books = books.order_by('-popularity')
        if sort_by == 'name':
            books = books.order_by('title')
        elif sort_by == 'newest':
            books = books.order_by('-publication_date')
        elif sort_by == 'oldest':
            books = books.order_by('publication_date')
        elif sort_by == 'cheap':
            books = books.order_by('price')
        elif sort_by == 'expensive':
            books = books.order_by('-price')


        context = {
            'books': books,
            'categories': Category.objects.all(),
            'publishers': Publisher.objects.all(),
            'authors': Author.objects.all(),
            'selected_categories': category,
            'selected_publishers': publisher,
            'selected_authors': author,
            'min_price': min_price or '',
            'max_price': max_price or '',
            'sort_by': sort_by or '',
        }

        return render(request, self.template_name, context)


class BookDetailView(View):
    template_name = 'literature/book_detail.html'
    form_class = CommentForm
    form_class_reply = CommentReplyForm

    def get(self, request, book_id):
        form = self.form_class()
        form_reply = self.form_class_reply()

        book = get_object_or_404(Book, id=book_id)

        comments = Comment.objects.filter(
            content_type=ContentType.objects.get(model='book', app_label='literature'),
            object_id=book.id,
            is_reply=False,
        )
        for i in book.author.all():
            print(i)
        context = {
            'form': form,
            'form_reply': form_reply,
            'book': book,
            'comments': comments,
            'model_name': 'book',
            'app_label': 'literature'
        }

        return render(request, self.template_name, context)
