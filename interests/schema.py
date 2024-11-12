import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Interest


class InterestType(DjangoObjectType):
    class Meta:
        model = Interest

class Query(graphene.ObjectType):
    interests = graphene.List(InterestType)
    def resolve_interests(self, info):
        return Interest.objects.all()

class CreateInterest(graphene.Mutation):
        name = graphene.String(required=True)
        icon = graphene.String(required=True)
        posted_by = graphene.Int()
        class Arguments:
            name = graphene.String(required=True)
            icon = graphene.String(required=True)
        def mutate(self, info,name,icon):
            user = info.context.user
            if user.is_anonymous:
                raise GraphQLError('Login to create a interest')
            interest = Interest.objects.create(
                name=name,
                icon=icon,
                posted_by=user
            )
            return CreateInterest(
                name=interest.name,
                icon=interest.icon,
                posted_by=interest.posted_by
            )
class Mutation(graphene.ObjectType):
    create_interest = CreateInterest.Field()
