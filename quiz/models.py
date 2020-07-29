from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from quizzers.models import Club

quiz_types = (
    ("mcq", "MCQ"),
    ("knockout", "Knockout"),
    ("blanks", "Fill In the Blanks"),
    ("written", "Written")
)

class Quiz(models.Model):
    date_created = models.DateField(default=timezone.now)
    date_publish = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False, choices=(
        (True, "Yes"),
        (False, "No")
    ))
    created_by = models.ForeignKey(User, related_name="quiz_creator", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    club = models.ForeignKey(Club, on_delete=models.DO_NOTHING)
    quiz_type = models.CharField(max_length=20, choices=quiz_types)
    quizzers = models.ManyToManyField(User, related_name="quizzers")

    def __str__(self):
        return "Quiz Name: %s of club: %s" % (self.name, self.club.name)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING)
    question = models.CharField(max_length=200)        

    def __str__(self):
        return  self.question

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    option = models.CharField(max_length=200)
    correct = models.BooleanField(default=False, choices=(
        (True, "Yes"),
        (False, "No")
    ))

    def __str__(self):
        return self.option

class Results(models.Model):
    date = models.DateField(default=timezone.now)
    quiz = models.ForeignKey(Quiz, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    score = models.FloatField(default=0.00)

    def __str__(self):
        return "Results for Quiz id: %s and for user id: %s with name : %s" % (self.pk, self.user.id, self.user.username)
