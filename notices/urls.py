from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notice/<str:pk>/', views.notice_detail, name='notice_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_notice, name='add_notice'),
    path('edit/<str:pk>/', views.edit_notice, name='edit_notice'),
    path('delete/<str:pk>/', views.delete_notice, name='delete_notice'),
    path('chatbot-api/', views.chatbot_api, name='chatbot_api'),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
]
