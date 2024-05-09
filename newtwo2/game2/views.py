from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from .models import Group


def groups(request):
    groups = Group.objects.all()
    error_message = None  # Определение переменной error_message
    return render(request, 'groups.html', {'groups': groups, 'error_message': error_message})

def students(request, group_name):
    students = Student.objects.filter(group__group=group_name)
    return render(request, 'students.html', {'students':students})


def marks(request, lesson_id=None):
    if lesson_id:
        lesson = Lesson.objects.get(id=lesson_id)
        marks = Mark.objects.filter(lesson=lesson)
    else:
        lesson = None
        marks = None

    if request.method == "POST":
        form = MarkForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.lesson = lesson
            obj.save()
            return redirect('marks', lesson_id=lesson_id)
    else:
        form = MarkForm()

    return render(request, 'marks.html', {'lesson': lesson, 'marks': marks, 'form': form})

def lesson_form(request):
    if request.method == "POST":
        form = LessonForm(request.POST)
        if form.is_valid():
            obj = Lesson(date=form.cleaned_data['date'], group=form.cleaned_data['group'],
                         discipline=form.cleaned_data['discipline'])
            obj.save()
            return redirect(f'/marks/{obj.id}')
    else:
        form = LessonForm()

    return render(request, 'form.html', {'form': form})

def marks(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    marks = Mark.objects.filter(lesson=lesson)
    previous_page = request.META.get('HTTP_REFERER')

    if request.method == "POST":
        form = MarkForm(lesson_id, request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.lesson = lesson
            obj.save()
            return redirect(previous_page) if previous_page else redirect('groups')
    else:
        form = MarkForm(lesson_id)
    return render(request, 'marks.html', {'lesson': lesson, 'marks': marks, 'form': form})

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('groups')
        else:
            error_message = "Неправильное имя пользователя или пароль"
    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('groups')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
