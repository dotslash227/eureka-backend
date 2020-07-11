import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Category, Profile, Club
from clubs.models import JoinRequest

# Start of Types
class CategoryType(DjangoObjectType):
    # Category Type
    class Meta:
        model = Category

class UserProfileType(DjangoObjectType):
    # GraphQL Type for user's profile
    class Meta:
        model = Profile
        fields = ("user",)

class UserType(DjangoObjectType):
    # GraphQl type for user
    class Meta:
        model = User       

class ClubType(DjangoObjectType):
    # GraphQL Type for the club
    class Meta:
        model = Club

class JoinClubType(DjangoObjectType):
    status = graphene.String(args={"userId":graphene.Int()})
    
    class Meta:
        model = Club

    def resolve_status(self, info, **args):        
        user_id = args.get("userId")        
        user = User.objects.get(pk=user_id)        
        members = self.members.all()
        if user in members:
            return "Already a Member"
        else:            
            try:
                join = JoinRequest.objects.get(club=self, sender=user)
            except:
                return "ok"                
            else:
                return "Pending Request"
        

# End of Types


# Start of Queries

class Query(object):
    all_categories = graphene.List(CategoryType)
    all_clubs = graphene.List(ClubType)
    clubs_bycategory = graphene.List(JoinClubType, categoryId=graphene.Int(required=False), name=graphene.String(required=False))
    clubs_byuserid = graphene.List(ClubType, userId=graphene.Int(required=True))

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()
    def resolve_all_clubs(self, info, **kwargs):
        return Club.objects.all()
    def resolve_clubs_byuserid(self, info, **kwargs):
        user_id = kwargs.get("userId")
        user = User.objects.get(pk=user_id)        
        return Club.objects.filter(members=user)        
    def resolve_clubs_bycategory(self, info, **kwargs):
        category_id = kwargs.get("categoryId") if kwargs.get("categoryId") else None
        name = kwargs.get("name") if kwargs.get("name") else None
        category = Category.objects.get(pk=category_id) if category_id else None        
        if name and category:                        
            return Club.objects.filter(category=category, name__icontains=name)
        if name and not category:            
            return Club.objects.filter(name__icontains=name)
        if category and not name:            
            return Club.objects.filter(category=category)        

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


# Mutation for letting a user creating a new class
# Only but required Parameters that have to be passed by the app: Name of club, category id, user id of creator
class CreateClubMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        category_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        description = graphene.String(required=True)
        max_players = graphene.Int(required=True)

    club = graphene.Field(ClubType)

    def mutate(self, info, name, category_id, user_id, description, max_players):
        user = User.objects.get(pk=user_id)
        category = Category.objects.get(pk=category_id)
        try:
            # Check if the club with the same name exists or not in the same category or not
            club = Club.objects.get(name__iexact=name, category=category)
        except:
            # If no club exists, then create a new club
            new_club = Club.objects.create(name=name, category=category, creator=user, description=description, max_players=max_players)
            return CreateClubMutation(club=new_club)
        else:
            raise Exception("Two clubs in the same category cannot have the same name")

class Mutation(graphene.ObjectType):
    new_category = CategoryMutation.Field()
    login = LoginMutation.Field()
    signup = SignupMutation.Field()
    create_club = CreateClubMutation.Field()
# End of Mutations