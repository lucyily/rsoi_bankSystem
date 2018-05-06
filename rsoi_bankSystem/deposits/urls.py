from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('next-day/', views.next_day, name='next-day'),
    path('deposit-list/', views.DepositListView.as_view(), name='deposit-list'),
    path('deposit-list/<slug:pk>/', views.DepositDetailView.as_view(), name='deposit-details'),
    path('create-contract/', views.ContractCreate.as_view(), name='create-contract'),
    path('contract-list/', views.UserContractListView.as_view(), name='contract-list'),
    path('contract-list/<slug:pk>/', views.ContractTransactionList.as_view(), name='contract-details'),
    ]
