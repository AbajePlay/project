from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('groups/', groups, name='groups'),
    path('lesson_form/', lesson_form),
    path('students/<group_name>/', students),
    path('marks/<int:lesson_id>/', marks),
    path('logout/', logout_view, name='logout')
]