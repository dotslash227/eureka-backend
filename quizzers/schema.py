import graphene
import json
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Category, Profile


# Start of Types
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category

class UserProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ("user",)

class UserType(DjangoObjectType):
    class Meta:
        model = User        

# End of Types


# Start of Queries

class Query(object):
    all_categories = graphene.List(CategoryType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

# End of Queries Section


# Start of Mutations

# Category Mutation class
class CategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)
    errors = graphene.String()

    def mutate(self, info, name):
        try:
            category = Category.objects.get(name=name)
        except:            
            category = Category.objects.create(name=name)
            return CategoryMutation(category=category)        
        else:
            raise Exception("already exists")

# Mutation for logging in the user
# This mutation returns a profile object, the FE can query the user
# object from this mutation
class LoginMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    profile = graphene.Field(UserProfileType)    

    def mutate(self, info, username, password):        
        user = authenticate(username=username, password=password)        
        if user is None:
            raise Exception("Incorrect username or password")
        else:
            print (user)
            if user.is_active:
                user_profile = Profile.objects.get(user=user)
                return LoginMutation(profile=user_profile)
            else:
                return Exception("User is disabled")

# Mutation for signing up a new user
# This mutation returns a profile object, the FE can query the user
# object from this mutation
class SignupMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        firstName = graphene.String(required=True)
        lastName = graphene.String(required=True)
        email = graphene.String(required=True)

    profile = graphene.Field(UserProfileType)

    def mutate(self, info, username, password, firstName, lastName, email):        
        # Check whether a user with the username already exists or not
        try:
            user = User.objects.get(username=username)
        except:
            # Check if a user with the same email exists or not
            try:
                user = User.objects.get(email=email)     
            except:
                user = User.objects.create(username=username, first_name=firstName, last_name=lastName, email=email)
                user.set_password(password)
                profile = Profile.objects.create(user=user)
                return SignupMutation(profile=profile)
            else:
                raise Exception("User with the same email already exists")            
        else:
            raise Exception("User with the same username already exists")        

class Mutation(graphene.ObjectType):
    new_category = CategoryMutation.Field()
    login = LoginMutation.Field()
    signup = SignupMutation.Field()
# End of Mutations