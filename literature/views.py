from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View

from home.forms import CommentForm, CommentReplyForm
from home.models import Comment
from .forms import BookSearchForm
from .models import Author, Book, Publisher, Translator, Category, Field, Nationality, Profession
from orders.forms import AddCartForm


class AuthorsView(View):
    template_name = 'literature/authors.html'
    form_class = ''

    def get(self, request):
        authors = Author.objects.all()

        search = request.GET.get('search')
        field_of_writing = request.GET.get('field_of_writing')
        profession = request.GET.get('profession')
        nationality = request.GET.get('nationality')

        top_authors = authors

        print(field_of_writing)

        if search:
            authors = authors.filter(full_name__icontains=search)

        if field_of_writing:
            authors = authors.filter(field_of_writing__id=field_of_writing)

        if profession:
            authors = authors.filter(profession__id=profession)

        if nationality:
            authors = authors.filter(nationality__id=nationality)

        fields = Field.objects.all()
        nationalities = Nationality.objects.all()
        professions = Profession.objects.all()

        context = {
            'authors': authors,
            'fields': fields,
            'nationalities': nationalities,
            'professions': professions,
            'top_authors': top_authors
        }

        return render(request, self.template_name, context)


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

        top_publisher = publishers

        search = request.GET.get('search')

        if search:
            publishers = publishers.filter(name__icontains=search)




        context = {'publishers': publishers, 'top_publisher':top_publisher}

        return render(request, self.template_name, context)


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
        top_translators = translators

        search = request.GET.get('search')

        if search:
            translators = translators.filter(name__icontains=search)

        context = {'translators': translators, 'top_translators':top_translators}

        return render(request, template_name=self.template_name, context=context)


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

        rate = request.GET.get('rate')
        print(rate)
        category = request.GET.getlist('category')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        publisher = request.GET.getlist('publisher')
        author = request.GET.getlist('author')
        search = request.GET.get('search')
        sort_by = request.GET.get('sort_by')

        if rate:
            books = books.filter(rate__gte=int(rate))

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
                Q(title__icontains=search) | Q(author__full_name__icontains=search)
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
    form_class_add_cart = AddCartForm

    def get(self, request, book_id):
        form = self.form_class()
        form_reply = self.form_class_reply()
        form_add_cart = self.form_class_add_cart()

        book = get_object_or_404(Book, id=book_id)

        comments = Comment.objects.filter(
            content_type=ContentType.objects.get(model='book', app_label='literature'),
            object_id=book.id,
            is_reply=False,
        )

        categories = book.category.all()
        related_books = Book.objects.filter(category__in=categories).exclude(id=book.id)

        context = {
            'form': form,
            'form_reply': form_reply,
            'form_add_cart': form_add_cart,
            'book': book,
            'comments': comments,
            'model_name': 'book',
            'app_label': 'literature',
            'related_books': related_books,
        }

        return render(request, self.template_name, context)
