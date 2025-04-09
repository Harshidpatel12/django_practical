from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ask/', views.ask_question, name='ask_question'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('answer/<int:pk>/like/', views.like_answer, name='like_answer'),
] 