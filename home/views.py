from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


class HomeView(View):
    template_name = 'home/home.html'
    form_class = ''

    def get(self, reqeust):
        return render(reqeust, template_name=self.template_name)

    def post(self, request):
        pass
