from django.urls import path

from . import views

app_name = "quora"

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("ask/", views.ask_question, name="ask_question"),
    path("question/<int:pk>/", views.question_detail, name="question_detail"),
    path("answer/<int:answer_id>/like/", views.like_answer, name="like_answer"),
]
