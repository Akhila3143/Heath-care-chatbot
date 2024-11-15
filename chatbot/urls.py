from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='chatbot-home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('chatbot-interface/', views.chatbot_interface, name='chatbot-interface'),
    path('get-response/', views.get_response, name='get_response'),
    path('services/', views.services, name='services'),
    path('about-us/', views.about_us, name='about_us'),
    path('faq/', views.faq, name='faq'),
]
