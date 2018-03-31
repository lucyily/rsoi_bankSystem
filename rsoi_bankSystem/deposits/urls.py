from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('deposit-list/', views.DepositListView.as_view(), name='deposit-list'),
    path('deposit-list/<slug:pk>/', views.DepositDetailView.as_view(), name='deposit-details')
]