from django.shortcuts import render, redirect
from datetime import datetime, date
from django.utils import timezone
from django.http import HttpResponse
from django.views.generic import TemplateView, View, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Contract, Deposit, BankAccount, ChartOfAccounts, Transaction, Interest
from bankSystem import models


class DepositListView(ListView):
    model = Deposit
    paginate_by = 10  # if pagination is desired


class DepositDetailView(DetailView):
    model = Deposit

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rates'] = Interest.objects.filter(deposit=self.get_object())
        return context


class Index(TemplateView):
    login_url = "/login"
    template_name = 'deposits/index.html'


def create_bank_fund():
    code_number = "7327"
    code = ChartOfAccounts.objects.get_or_create(
        number=code_number,
        defaults = {
            "number": code_number,
            "name": "Фонд банковского развития",
            "type": "Passive"
        }
    )[0]
    bank_fund = BankAccount.objects.get_or_create(
        code = code,
        defaults = {
            "code": ChartOfAccounts.objects.get(number=code_number),
            "number": code_number+"0"*9,
            "credits": 10**11
        }
    )
    return bank_fund[0]


def create_cashbox():
    code_number = "1010"
    code = ChartOfAccounts.objects.get_or_create(
        number=code_number,
        defaults = {
            "number": code_number,
            "name": "Касса",
            "type": "Active"
        }
    )[0]
    cashbox = BankAccount.objects.get_or_create(
        code = code,
        defaults = {
            "code": ChartOfAccounts.objects.get(number=code_number),
            "number": code_number+"0"*9,
        }
    )
    return cashbox[0]


def create_customer_acc(contract):
    code_number = "3014"
    code = ChartOfAccounts.objects.get_or_create(
        number=code_number,
        defaults = {
            "number": code_number,
            "name": "Текущий счет клиента",
            "type": "Active"
        }
    )[0]
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

def create_interest_acc(contract):
    code_number = "3471" #для срочных вкладов
    code = ChartOfAccounts.objects.get_or_create(
        number=code_number,
        defaults = {
            "number": code_number,
            "name": "Процентный счет клиента",
            "type": "Active"
        }
    )[0]
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


def create_transaction(source, target, sum):
    transaction = Transaction(source_acc=source, target_acc=target, sum=sum)
    transaction.save()


class ContractCreate(CreateView):
    model = Contract
    fields = ['deposite', 'sum']

    def create_transaction(self, source, target, sum):
        transaction = Transaction(source_acc=source, target_acc=target, sum=sum)
        transaction.save()

    def _transaction_chain(self, contract: Contract):
        """Цепочка транзакций при заключении новго договора"""
        cashbox_acc = create_cashbox()
        cashbox_acc.debits += contract.sum
        cashbox_acc.save()
        bank_fund_acc = create_bank_fund()
        bank_fund_acc.save()
        customer_acc = create_customer_acc(contract)
        customer_acc.save()
        interest_acc = create_interest_acc(contract)
        interest_acc.save()
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
            return redirect('../contract-list/')


class UserContractListView(ListView):
    template_name = 'deposits/user_contract_list.html'

    def get_queryset(self):
        customer = models.Customer.objects.get(user = self.request.user) 
        queryset = Contract.objects.filter(customer=customer)
        return queryset


class ContractTransactionList(DetailView):
    model = Contract

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interest_sum'] = BankAccount.objects.filter(contract=self.object, code__number="3471").first().credits
        return context
    
def next_day(request):
    if request.method == "POST":
        last_day = None
        try:
            with open("last_next_day", "r") as f:
                last_day = f.readline().strip()
        except:
            with open("last_next_day", "w") as f:
                f.close()
        if last_day == str(date.today()):
            return HttpResponse("Сегодня вы уже делали процедуру: Следующий банковский день ")
        for contract in Contract.objects.filter(end__gte = datetime.now()):
            daily_interest = contract.interest/100/365
            daily_payment = round(daily_interest*contract.sum, 4)
            cashbox_acc = create_cashbox()
            bank_fund_acc = create_bank_fund()
            user_acc = create_customer_acc(contract=contract)
            interest_acc = create_interest_acc(contract=contract)
            create_transaction(bank_fund_acc, interest_acc, daily_payment)
            create_transaction(interest_acc, cashbox_acc, daily_payment)
            cashbox_acc.credits += daily_payment
            cashbox_acc.save()
            with open("last_next_day", "w") as f:
                f.write(str(date.today()))
        return HttpResponse("Процедура отработала нормально")
