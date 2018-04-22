from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import TemplateView, View, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Contract, Deposit, BankAccount, ChartOfAccounts, Transaction
from bankSystem import models


class DepositListView(ListView):
    model = Deposit
    paginate_by = 20  # if pagination is desired


class DepositDetailView(DetailView):
    model = Deposit


class Index(TemplateView):
    login_url = "/login"
    template_name = 'deposits/index.html'


class NextDay(TemplateView):
    login_url = "/login"
    template_name = 'deposits/index.html'


class ContractCreate(CreateView):
	model = Contract
	fields = ['deposite', 'sum']

	@staticmethod
	def _create_cashbox():
		code_number = "1010"
		code = ChartOfAccounts.objects.get(number=code_number)
		cashbox = BankAccount.objects.get_or_create(
			code = code,
			defaults = {
				"code": ChartOfAccounts.objects.get(number=code_number),
				"number": code_number+"0"*9,
			}
		)
		return cashbox[0]

	@staticmethod
	def _create_bank_fund():
		code_number = "7327"
		code = ChartOfAccounts.objects.get(number="7327")
		bank_fund = BankAccount.objects.get_or_create(
			code = code,
			defaults = {
				"code": ChartOfAccounts.objects.get(number="7327"),
				"number": code_number+"0"*9,
			}
		)
		if bank_fund[1]:
			print("created")
		return bank_fund[0]

	@staticmethod
	def _create_customer_acc():
		code_number = "3014"
		code = ChartOfAccounts.objects.get(number=code_number)
		customer_acc = BankAccount.objects.get_or_create(
			code = code,
			defaults = {
				"code": ChartOfAccounts.objects.get(number=code_number),
				"number": code_number+"0"*9,
			}
		)
		return customer_acc[0]

	def create_transaction(self, source, target, sum):
		transaction = Transaction(source_acc=source, target_acc=target, sum=sum)
		transaction.save()

	def _transaction_chain(self, contract: Contract):
		"""Цепочка транзакций при заключении новго договора"""
		cashbox_acc = self._create_cashbox()
		cashbox_acc.debits += contract.sum
		cashbox_acc.save()
		bank_fund_acc = self._create_bank_fund()
		customer_acc = BankAccount(
			code = ChartOfAccounts.objects.get(number="3014"), 
			contract=contract)
		customer_acc.save() 
		self.create_transaction(cashbox_acc, customer_acc, contract.sum)
		self.create_transaction(customer_acc, bank_fund_acc, contract.sum)

	def form_valid(self, form):
		if form.is_valid():
			deposite = form.cleaned_data["deposite"]
			sum = form.cleaned_data["sum"]
			self.contract = Contract()
			self.contract.deposite = deposite 
			self.contract.sum = sum
			self.contract.start = timezone.now()
			self.contract.end = timezone.now() + self.contract.deposite.term  
			self.contract.customer = models.Customer.objects.get(user=self.request.user)
			self.contract.save()
			self._transaction_chain(self.contract)
			return HttpResponse("deposit-list")