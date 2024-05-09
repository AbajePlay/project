from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import NumericPasswordValidator
from django.utils.translation import gettext_lazy as _

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"
        widgets = {'date': forms.SelectDateWidget()}

class MarkForm(forms.ModelForm):
    def __init__(self, lesson_id, *args, **kwargs):
        super(MarkForm, self).__init__(*args, **kwargs)
        les = Lesson.objects.get(id=lesson_id)
        self.fields['student'] = forms.ModelChoiceField(queryset=Student.objects.filter(group=les.group))

    class Meta:
        model = Mark
        fields = ['mark', 'student']

class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': _("Пароли в обоих полях не совпадают."),
        'password_entirely_numeric': _("Этот пароль полностью состоит из цифр."),
        'password_too_short': _("Пароль слишком короткий. Он должен содержать не менее 8 символов."),
    }

    def clean_password2(self):
        password2 = super().clean_password2()
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8:
            raise forms.ValidationError(
                self.error_messages['password_too_short'],
                code='password_too_short',
            )
        if password1.isdigit():
            raise forms.ValidationError(
                self.error_messages['password_entirely_numeric'],
                code='password_entirely_numeric',
            )
        return password2