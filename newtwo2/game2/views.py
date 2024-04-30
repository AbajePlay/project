from django.shortcuts import render, redirect
from .models import *
from .forms import *

def groups(request):
    groups = Group.objects.all()
    return render(request, 'groups.html', {'groups':groups})

def students(request, group_name):
    students = Student.objects.filter(group__group=group_name)
    return render(request, 'students.html', {'students':students})


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
    if request.method == "POST":
        form = MarkForm(lesson_id, request.POST)
        if form.is_valid():
            obj = Mark(mark=form.cleaned_data['mark'], student=form.cleaned_data['student'],
                       lesson=Lesson.objects.get(id=lesson_id))
            obj.save()
    else:
        form = MarkForm(lesson_id)
    return render(request, 'marks.html', {'form':form})