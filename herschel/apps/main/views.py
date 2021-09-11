from django.views.generic.base import TemplateView
from django.shortcuts import render
from constance import config

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["join_link"] = config.GET_INVOLVED_LINK
        return context

class GalleryView(TemplateView):
    template_name = "main/gallery.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['magazines'] = Magazine.objects.all()
        return context
