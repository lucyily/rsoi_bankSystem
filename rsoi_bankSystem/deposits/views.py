from django.shortcuts import render
from django.views.generic import TemplateView, View, DetailView
from django.views.generic.list import ListView
from .models import Deposit


class DepositListView(ListView):
    model = Deposit
    paginate_by = 20  # if pagination is desired


class DepositDetailView(DetailView):
    model = Deposit


class Index(TemplateView):
    login_url = "/login/"
    template_name = 'deposits/index.html'