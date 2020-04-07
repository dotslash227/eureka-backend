import graphene
import quizzers.schema

class Query(
    quizzers.schema.Query,
    graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(
    quizzers.schema.Mutation,
    graphene.ObjectType
    ):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)