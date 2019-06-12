from collections import OrderedDict

from django.core import serializers

from django.shortcuts import render
from django.views import generic
from pure_pagination.mixins import PaginationMixin
from .models import Commentary, CommentaryText
from django.http import JsonResponse, HttpResponse

class CommentaryByChapter(PaginationMixin, generic.ListView):
    model = CommentaryText
    template_name = "commentary/index.html"
    context_object_name = "commentaries"
    paginate_by = 20
