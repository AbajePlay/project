from django.urls import path
from .views import *

urlpatterns = [
    path('', groups),
    path('lesson_form/', lesson_form),
    path('students/<group_name>/', students),
    path('marks/<int:lesson_id>/', marks)
]