from django.core.validators import RegexValidator
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse


class Profession(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Field(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'


class Nationality(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Nationality'
        verbose_name_plural = 'Nationalities'

    def __str__(self):
        return self.name


class Author(models.Model):
    field_of_writing = models.ManyToManyField(Field, related_name='fauthors')
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_death = models.DateField(blank=True, null=True)
    picture = models.ImageField(upload_to='authors/', blank=True, null=True)
    comment = GenericRelation('home.Comment')
    biography = models.TextField(blank=True)
    nationality = models.ManyToManyField(Nationality, related_name='nauthors')
    profession = models.ManyToManyField(Profession, related_name='pauthors')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('literature:author_detail', args=[self.id])


class Translator(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    picture = models.ImageField(upload_to='translator_picture/', blank=True, null=True)
    comment = GenericRelation('home.Comment')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('literature:translator_detail', args=[self.id])


class Publisher(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    picture = models.ImageField(upload_to='publisher_picture/', blank=True, null=True)
    date_establishment = models.DateField(blank=True, null=True)
    comment = GenericRelation('home.Comment')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('literature:publisher_detail', args=[self.id])


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BookImage(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='bimages')
    image = models.ImageField(upload_to='book_images/')
    caption = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'Image for {self.book.title}'


BOOK_FORMAT_CHOICES = [
    ('paperback', 'چاپی'),
    ('ebook', 'کتاب الکترونیکی'),
    ('audiobook', 'کتاب صوتی'),
]


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Cateogry'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ManyToManyField(Author, related_name='abooks')
    translator = models.ManyToManyField(Translator, related_name='tbooks', blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, related_name='pbooks', null=True, blank=True)
    comment = GenericRelation('home.Comment')

    title = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    publication_date = models.DateField(blank=True, null=True)
    format = models.CharField(max_length=50, choices=BOOK_FORMAT_CHOICES)
    cover_image = models.ImageField(upload_to='cover_images/')
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, related_name='lbooks', null=True)
    pages = models.PositiveIntegerField(blank=True, null=True)
    isbn = models.CharField(
        max_length=17,
        unique=True,
        validators=[RegexValidator(regex=r'^\d{3}-\d{1,5}-\d{1,7}-\d{1,7}-\d{1}$', message="فرمت شابک معتبر نیست")]
    )
    category = models.ManyToManyField(Category, related_name='cbook')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('literature:book_detail', args=[self.id])




