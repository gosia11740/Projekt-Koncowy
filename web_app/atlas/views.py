from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View

from .models import Hello

class HelloView(View):
    template_name = "templates/base.html"
    def get(self, request):
        return render(request, self.template_name)