from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from .forms import AnswerForm
from .models import User, Question, Answer, Like


def home(request):
    return render(request, "quora/home.html", {"questions": Question.objects.all()})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("quora:home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "quora/login.html")


def logout_view(request):
    logout(request)
    return redirect("quora:home")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("quora:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("quora:register")

        user = User.objects.create_user(
            username=username, email=email, password=password1
        )
        login(request, user)
        return redirect("quora:home")

    return render(request, "quora/register.html")


@login_required
def ask_question(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            question = Question.objects.create(
                title=title, content=content, author=request.user
            )
            return redirect("quora:question_detail", pk=question.pk)
    return render(request, "quora/ask_question.html")


def question_detail(request, pk):
    if not Question.objects.filter(pk=pk).exists():
        return HttpResponseNotFound("Question not found")

    question = Question.objects.get(pk=pk)
    answers = Answer.objects.filter(question=question)

    if request.user.is_authenticated:
        user_likes = Like.objects.filter(
            user=request.user, answer__in=answers
        ).values_list("answer_id", flat=True)
    else:
        user_likes = []

    if request.method == "POST" and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect("quora:question_detail", pk=pk)
    else:
        form = AnswerForm()

    return render(
        request,
        "quora/question_detail.html",
        {
            "question": question,
            "answers": answers,
            "form": form,
            "user_likes": user_likes,
        },
    )


@login_required
def like_answer(request, answer_id):
    if not Answer.objects.filter(id=answer_id).exists():
        return HttpResponseNotFound("Answer not found")

    answer = Answer.objects.get(id=answer_id)
    like_qs = Like.objects.filter(user=request.user, answer=answer)

    if like_qs.exists():
        like_qs.delete()
        liked = False
    else:
        Like.objects.create(user=request.user, answer=answer)
        liked = True

    return JsonResponse({"liked": liked, "likes_count": answer.likes.count()})
