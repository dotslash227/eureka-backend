import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from quizzers.models import Club
from .models import Quiz, Question, Option

# Start of DjangoModel Query Typeqs
class QuizType(DjangoObjectType):
    class Meta:
        model =  Quiz

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question

class OptionType(DjangoObjectType):
    class Meta:
        model = Option
# End of Query Types