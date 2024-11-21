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

    def resolve_interest_by_id(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to view interest')
        return Interest.objects.get(id=id).first()

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
class UpdateInterest(graphene.Mutation):
    idInterest = graphene.Int(required=True)
    name = graphene.String(required=True)
    icon = graphene.String(required=True)

    class Arguments:
        idInterest = graphene.Int(required=True)
        name = graphene.String(required=True)
        icon = graphene.String(required=True)

    def mutate(self, info, idInterest, name, icon):
        user = info.context.user
        interest = Interest.objects.get(id=idInterest)
        if interest.posted_by != user:
            raise GraphQLError('Not permitted to update this interest')
        interest.name = name
        interest.icon = icon
        interest.save()
        return UpdateInterest(
            idInterest=interest.id,
            name=interest.name,
            icon=interest.icon
        )

class DeleteInterest(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        idInterest = graphene.Int(required=True)

    def mutate(self, info, idInterest):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to delete interest')
        interest = Interest.objects.get(id=idInterest)
        if interest.posted_by != user:
            raise GraphQLError('Not permitted to delete this interest')
        interest.delete()
        return DeleteInterest(success=True)

class Mutation(graphene.ObjectType):
    create_interest = CreateInterest.Field()
    update_interest = UpdateInterest.Field()
    delete_interest = DeleteInterest.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
