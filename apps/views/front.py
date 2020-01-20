# django
from django.shortcuts import render
from django.views.generic import TemplateView


class Front(TemplateView):

    template_name = "front.html"
