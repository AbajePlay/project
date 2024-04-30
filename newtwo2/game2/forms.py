from django import forms
from .models import *

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"
        widgets = {'date': forms.SelectDateWidget()}

class MarkForm(forms.ModelForm):
    def __init__(self, lesson_id, *args, **kwargs):
        super(MarkForm, self). __init__(*args, **kwargs)
        les = Lesson.objects.get(id=lesson_id)
        self.fields['student'] = forms.ModelChoiceField(queryset=Student.objects.filter(group=les.group))

    class Meta:
        model = Mark
        fields = ['mark', 'student']