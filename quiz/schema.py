import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from quizzers.models import Club
from .models import Quiz, Question, Option
from django.utils import timezone

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

# Queries for quizzes
class Query(object):
    quiz_by_clubs = graphene.List(QuizType, clubId=graphene.Int(required=True))
    questions_by_quiz = graphene.List(QuestionType, quizId=graphene.Int(required=True))
    options_by_question = graphene.List(OptionType, questionId=graphene.Int(required=True))

    def resolve_quiz_by_clubs(self, info, **kwargs):
        club_id = kwargs.get("clubId")        
        club = Club.objects.get(pk=club_id)        
        return Quiz.objects.filter(club=club)

    def resolve_questions_by_quiz(self, info, **kwargs):
        quiz_id = kwargs.get("quizId")
        quiz = Club.objects.get(pk=quiz_id)
        return Question.objects.filter(quiz=quiz)

    def resolve_options_by_question(self, info, **kwargs):
        question_id = kwargs.get("questionId")
        question = Question.objects.get(pk=question_id)
        return Option.objects.filter(question=question)

# End of Queries for quizzes