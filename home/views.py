from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


class HomeView(View):
    template_name = ''
    form_class = ''

    def get(self, reqeust):
        return HttpResponse('Welcome')

    def post(self, request):
        pass
