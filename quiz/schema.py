import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from quizzers.models import Club
from .models import Quiz, Question, Option, Results
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

class ResultType(DjangoObjectType):
    class Meta:
        model = Results
# End of Query Types

# Queries for quizzes
class Query(object):
    quiz_by_clubs = graphene.List(QuizType, clubId=graphene.Int(required=True))
    questions_by_quiz = graphene.List(QuestionType, quizId=graphene.Int(required=True))
    options_by_question = graphene.List(OptionType, questionId=graphene.Int(required=True))
    new_quizes_by_user = graphene.List(QuizType, userId=graphene.Int(required=True))
    quiz = graphene.Field(QuizType, quizId=graphene.Int(required=True))

    def resolve_quiz(self, info, **kwargs):
        quiz_id = kwargs.get("quizId")        
        return Quiz.objects.get(pk=quiz_id)

    def resolve_quiz_by_clubs(self, info, **kwargs):
        # Method to resolve quiz by clubs query
        club_id = kwargs.get("clubId")        
        club = Club.objects.get(pk=club_id)        
        return Quiz.objects.filter(club=club)

    def resolve_questions_by_quiz(self, info, **kwargs):
        # method to resolve questions in a quiz
        quiz_id = kwargs.get("quizId")
        quiz = Club.objects.get(pk=quiz_id)
        return Question.objects.filter(quiz=quiz)

    def resolve_options_by_question(self, info, **kwargs):
        # method to resolve  options of a quiz
        question_id = kwargs.get("questionId")
        question = Question.objects.get(pk=question_id)
        return Option.objects.filter(question=question)

    def resolve_new_quizes_by_user(self, info, **kwargs):
        # method to resolve upcoming quizzes to be displayed on the main homepage
        user_id = kwargs.get("userId")
        user = User.objects.get(pk=user_id)
        quizes = []
        try:
            user_clubs = Club.objects.filter(members=user)            
        except:
            raise Exception("User not part of clubs")
        else:            
            for club in user_clubs:
                quiz_list = Quiz.objects.filter(club=club)
                for each in quiz_list:
                    print(each)
                    try:
                        result = Results.objects.get(quiz=each, user=user)
                    except:
                        quizes.append(each)                                        

        return quizes

# End of Queries for quizzes

# Start of Mutations for Quizes
class CreateResultMutation(graphene.Mutation):
    class Arguments:
        quiz_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        score = graphene.Float(required=True)
    
    result = graphene.Field(ResultType)

    def mutate(self, info, quiz_id, user_id, score):
        quiz = Quiz.objects.get(pk=quiz_id)
        user = User.objects.get(pk=user_id)        
        results = Results.objects.filter(quiz=quiz, user=user)
        if len(results) > 0:
            raise Exception("User already has taken the quiz")
        else:
            result = Results(quiz=quiz, user=user, score=score)
            result.save()
            return CreateResultMutation(result=result)


class Mutation(graphene.ObjectType):
    create_result_mutation = CreateResultMutation.Field()