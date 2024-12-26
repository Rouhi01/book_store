from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import ContentType

from accounts.models import User
from literature.forms import BookSearchForm
from .models import Like, Comment
from .forms import CommentForm, CommentReplyForm, LikeForm
from literature.models import Category, Book, Author, Publisher
from blog.models import Blog


class HomeView(View):
    template_name = 'home/home.html'

    def get(self, reqeust):
        categories = Category.objects.all()
        top_authors = Author.objects.annotate(book_count=Count('abooks')).order_by('-book_count')[:4]
        top_publishers = Publisher.objects.annotate(book_count=Count('pbooks')).order_by('-book_count')[:8]

        post_content_type = ContentType.objects.get(app_label='accounts', model='post')
        top_comments = Comment.objects.exclude(content_type=post_content_type).order_by('-created_at')[:10]

        latest_books = Book.objects.order_by('-created_at')[:6]

        three_articles = Blog.objects.order_by('-created_at')


        context = {
            'categories': categories,
            'top_authors': top_authors,
            'top_publishers': top_publishers,
            'top_comments': top_comments,
            'latest_books': latest_books,
            'three_articles': three_articles

        }
        return render(reqeust, self.template_name, context)

    def post(self, request):
        pass


class LikeView(LoginRequiredMixin, View):
    form_class = LikeForm

    def post(self, request, model_name, object_id):
        form = LikeForm(request.POST)

        content_type = ContentType.objects.get(model=model_name.lower())
        model = content_type.model_class()
        obj = get_object_or_404(model, id=object_id)

        post_data = request.POST.copy()
        post_data['content_id'] = obj.id
        form = LikeForm(post_data)

        if form.is_valid():
            like = Like.objects.filter(
                user=request.user,
                content_type=ContentType.objects.get(model=model_name.lower()),
                object_id=obj.id,
            )
            if like.exists():
                Like.objects.get(
                    user=request.user,
                    content_type=ContentType.objects.get(model=model_name.lower()),
                    object_id=obj.id,
                ).delete()
                messages.error(request, 'پست توسط شما دیسلایک شد', 'danger')
            else:
                Like.objects.create(
                    user=request.user,
                    content_type=ContentType.objects.get(model=model_name.lower()),
                    object_id=obj.id,
                )
                messages.success(request, 'پست توسط شما لایک شد', 'success')

            return redirect(obj.get_absolute_url())
        else:
            print(form.errors)
            messages.error(request, 'خطا', 'danger')
            return redirect(obj.get_absolute_url())


# class LikeCommentView(LoginRequiredMixin, View):
#     form_class = LikeCommentForm
#
#     def post(self, request, model_name, object_id, parent_model_name, parent_object_id):
#         form = self.form_class(request.POST)
#
#         post_data = request.POST.copy()
#         post_data['content_id'] = object_id
#         post_data['parent_content_id'] = parent_object_id
#
#         parent_content_type = ContentType.objects.get(model=parent_model_name.lower())
#         model = parent_content_type.model_class()
#         obj = get_object_or_404(model, id=parent_object_id)
#
#         if form.is_valid():
#
#             like = Like.objects.filter(
#                 user=request.user,
#                 content_type=ContentType.objects.get(model=model_name.lower()),
#                 object_id=object_id,
#                 parent_content_type=parent_content_type.objects.get(model=parent_model_name.lower()),
#                 parent_object_id=parent_object_id,
#             )
#
#             if like.exists():
#                 Like.objects.get(
#                     user=request.user,
#                     content_type=ContentType.objects.get(model=model_name.lower()),
#                     object_id=object_id,
#                     parent_content_type=parent_content_type.objects.get(model=parent_model_name.lower()),
#                     parent_object_id=parent_object_id,
#                 ).delete()
#                 messages.error(request, 'پست توسط شما دیسلایک شد', 'danger')
#             else:
#                 Like.objects.create(
#                     user=request.user,
#                     content_type=ContentType.objects.get(model=model_name.lower()),
#                     object_id=object_id,
#                     parent_content_type=parent_content_type.objects.get(model=parent_model_name.lower()),
#                     parent_object_id=parent_object_id,
#                 )
#                 messages.success(request, 'پست توسط شما لایک شد', 'success')
#             return redirect(obj.get_absolute_url())
#         else:
#             print(form.errors)
#             messages.error(request, 'خطا در لایک یا عدم لایک', 'danger')
#             return redirect(obj.get_absolute_url())


class CommentView(LoginRequiredMixin, View):
    form_class = CommentForm

    @method_decorator(login_required)
    def post(self, request, user_id, model_name, object_id, app_name):
        form = self.form_class(request.POST)

        content_type = ContentType.objects.get(model=model_name, app_label=app_name)
        model = content_type.model_class()
        obj = get_object_or_404(model, id=object_id)
        user = User.objects.get(id=user_id)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.content_type = content_type
            comment.object_id = obj.id
            comment.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد', 'success')
            return redirect(obj.get_absolute_url())


class CommentReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm

    @method_decorator(login_required)
    def post(self, request, user_id, model_name, object_id, comment_id, app_name):
        form = self.form_class(request.POST)

        content_type = ContentType.objects.get(model=model_name, app_label=app_name)
        model = content_type.model_class()
        obj = get_object_or_404(model, id=object_id)
        user = User.objects.get(id=user_id)
        comment = get_object_or_404(Comment, id=comment_id, content_type=content_type, object_id=object_id)

        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = user
            reply.content_type = content_type
            reply.object_id = obj.id
            reply.is_reply = True
            reply.reply = comment
            reply.save()
            messages.success(request, 'ریپلای شما با موفقیت ثبت شد', 'success')
        return redirect(obj.get_absolute_url())
