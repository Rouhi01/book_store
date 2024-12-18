from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import ContentType
from home.models import Like


class HomeView(View):
    template_name = 'home/home.html'
    form_class = ''

    def get(self, reqeust):
        return render(reqeust, template_name=self.template_name)

    def post(self, request):
        pass


class LikeView(LoginRequiredMixin, View):

    def get(self, request, model_name, object_id):
        content_type = ContentType.objects.get(model=model_name.lower())
        model = content_type.model_class()
        object = get_object_or_404(model, id=object_id)

        like = Like.objects.filter(
            user=request.user,
            content_type=ContentType.objects.get(model=model_name.lower()),
            object_id=object.id
        )

        if like.exists():
            Like.objects.get(
                user=request.user,
                content_type=ContentType.objects.get(model=model_name.lower()),
                object_id=object.id
            ).delete()
            messages.error(request, 'پست توسط شما دیسلایک شد', 'danger')
        else:
            Like.objects.create(
                user=request.user,
                content_type=ContentType.objects.get(model=model_name.lower()),
                object_id=object.id
            )
            messages.success(request, 'پست توسط شما لایک شد', 'success')

        return redirect(object.get_absolute_url())



