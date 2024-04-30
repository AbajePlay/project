from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    group = models.CharField(max_length=50)

    def __str__(self):
        return self.group

class Student(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    age = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.group.group}'


class Discipline(models.Model):
    discipline = models.CharField(max_length=70)
    lector = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.discipline

class Lesson(models.Model):
    date = models.DateField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)

class Mark(models.Model):
    choise = (('н', 'н'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),)

    mark = models.CharField(max_length=1, choices=choise)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.mark