from django.views.generic.base import TemplateView
from django.shortcuts import render

from .models import Magazine

# Create your views here.
class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['magazines'] = Magazine.objects.all()
        return context


class AboutView(TemplateView):
    template_name = "main/about.html"


class GalleryView(TemplateView):
    template_name = "main/gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['magazines'] = Magazine.objects.all()
        return context
