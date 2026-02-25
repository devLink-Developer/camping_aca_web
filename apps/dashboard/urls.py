from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('messages/', views.dashboard_messages, name='messages'),
    path('statistics/', views.dashboard_statistics, name='statistics'),
    path('chatbot/statistics/', views.chatbot_statistics, name='chatbot_statistics'),
    path('chatbot/clients/', views.chatbot_clients, name='chatbot_clients'),
    path('chatbot/clients/<str:phone>/messages/', views.chatbot_client_messages, name='chatbot_client_messages'),
    path('chatbot/clients/<str:phone>/messages/json/', views.chatbot_client_messages_json, name='chatbot_client_messages_json'),
    path('settings/', views.dashboard_settings, name='settings'),
    path('services/', views.manage_services, name='manage_services'),
    path('gallery/', views.manage_gallery, name='manage_gallery'),
    path('prices/', views.manage_prices, name='manage_prices'),
    path('faqs/', views.manage_faqs, name='manage_faqs'),
    path('news/', views.manage_news, name='manage_news'),
]
