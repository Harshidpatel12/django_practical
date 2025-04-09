from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import JsonResponse
from .models import User, Question, Answer, Like
from .forms import AnswerForm

def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'quora/home.html', {'questions': questions})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('quora:home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'quora/login.html')

def logout_view(request):
    logout(request)
    return redirect('quora:home')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('quora:register')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('quora:register')
            
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('quora:home')
        
    return render(request, 'quora/register.html')

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    user_likes = Like.objects.filter(user=request.user, answer__in=answers).values_list('answer_id', flat=True) if request.user.is_authenticated else []
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('quora:question_detail', pk=pk)
    else:
        form = AnswerForm()
        
    return render(request, 'quora/question_detail.html', {
        'question': question,
        'answers': answers,
        'form': form,
        'user_likes': user_likes
    })

@login_required
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    like, created = Like.objects.get_or_create(user=request.user, answer=answer)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
        
    return JsonResponse({
        'liked': liked,
        'likes_count': answer.likes.count()
    })
