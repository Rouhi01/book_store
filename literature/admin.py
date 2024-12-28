from django.contrib import admin
from .models import (Profession,
                     Field,
                     Nationality,
                     Author,
                     Translator,
                     Publisher,
                     Language,
                     BookImage,
                     Book,
                     Category)


@admin.register(Profession)
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Nationality)
class NationalityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name')
    filter_horizontal = ('field_of_writing', 'nationality', 'profession')


@admin.register(Translator)
class TranslatorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)



class BookImageInline(admin.StackedInline):
    model = BookImage
    can_delete = False

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'publication_date', 'format', 'language', 'isbn')
    search_fields = ('title', 'isbn')
    list_filter = ('format', 'language', 'publisher')
    filter_horizontal = ('author', 'translator', 'category')
    autocomplete_fields = ('publisher', 'language')

    inlines = [BookImageInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')