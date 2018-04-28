from django.shortcuts import render, redirect
from datetime import datetime
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import TemplateView, View, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Contract, Deposit, BankAccount, ChartOfAccounts, Transaction, Interest
from bankSystem import models


class DepositListView(ListView):
    model = Deposit
    paginate_by = 20  # if pagination is desired


class DepositDetailView(DetailView):
    model = Deposit


class Index(TemplateView):
    login_url = "/login"
    template_name = 'deposits/index.html'

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
    return bank_fund[0]

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


def create_transaction(source, target, sum):
    transaction = Transaction(source_acc=source, target_acc=target, sum=sum)
    transaction.save()


def calculate_interest(contract: Contract):
    interests = Interest.objects.filter(value__lte = contract.sum)
    interest = max(interests, key=lambda i: i.rate)
    return interest.rate


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
        code = ChartOfAccounts.objects.get(number=code_number)
        bank_fund = BankAccount.objects.get_or_create(
            code = code,
            defaults = {
                "code": ChartOfAccounts.objects.get(number=code_number),
                "number": code_number+"0"*9,
            }
        )
        return bank_fund[0]

    @staticmethod
    def _create_customer_acc(contract):
        code_number = "3014"
        code = ChartOfAccounts.objects.get(number=code_number)
        customer_acc = BankAccount.objects.get_or_create(
            code = code,
            contract = contract,
            defaults = {
                "code": ChartOfAccounts.objects.get(number=code_number),
                "number": code_number+"0"*9,
                "contract":  contract,
            }
        )
        return customer_acc[0]

    @staticmethod
    def _create_interest_acc(contract):
        code_number = "3471" #для срочных вкладов
        code = ChartOfAccounts.objects.get(number=code_number)
        customer_acc = BankAccount.objects.get_or_create(
            code = code,
            contract = contract,
            defaults = {
                "code": ChartOfAccounts.objects.get(number=code_number),
                "number": code_number+"0"*9,
                "contract":  contract,
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

def next_day(request):
    for contract in Contract.objects.filter(end__gte = datetime.now()):
        daily_interest = calculate_interest(contract)/100/365
        daily_payment = round(daily_interest*contract.sum, 4)
        cashbox_acc = _create_cashbox()
        bank_fund_acc = _create_bank_fund()
        user_acc = ContractCreate._create_customer_acc(contract=contract)
        interest_acc = ContractCreate._create_interest_acc(contract=contract)
        create_transaction(bank_fund_acc, interest_acc, daily_payment)
        create_transaction(interest_acc, cashbox_acc, daily_payment)
        cashbox_acc.credits += daily_payment
        cashbox_acc.save()
        print("hi")
    return HttpResponse("pizdec")
