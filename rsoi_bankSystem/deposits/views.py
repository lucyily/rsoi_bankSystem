from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import TemplateView, View, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Contract, Deposit
from bankSystem import models


class DepositListView(ListView):
    model = Deposit
    paginate_by = 20  # if pagination is desired


class DepositDetailView(DetailView):
    model = Deposit


class Index(TemplateView):
    login_url = "/login/"
    template_name = 'deposits/index.html'


class ContractCreate(CreateView):
	model = Contract
	fields = ['deposite', 'sum']

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.start = timezone.now()
		self.object.end = timezone.now() + self.object.deposite.term  
		self.object.customer = models.Customer.objects.get(user=self.request.user)
		self.object.save()
		return HttpResponse("deposit-list")