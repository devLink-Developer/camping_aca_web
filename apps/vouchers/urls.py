from django.urls import path
from . import views

app_name = 'vouchers'

urlpatterns = [
    path('', views.voucher_list, name='list'),
    path('create/', views.voucher_create, name='create'),
    path('scanner/', views.voucher_scanner, name='scanner'),
    path('<uuid:voucher_code>/', views.voucher_detail, name='detail'),
    path('api/validate/', views.voucher_validate, name='validate'),
    path('api/use/', views.voucher_use, name='use'),
]
