from django.shortcuts import render
from django.core.files import File
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView
from .models import Forum, Thread, Post, UserProfile
from django.http import HttpResponse
from django.views import View


# Create your views here.
