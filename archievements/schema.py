import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from archievements.models import Archievement

class ArchievementType(DjangoObjectType):
    class Meta:
        model = Archievement

class Query(graphene.ObjectType):
    archivements = graphene.List(ArchievementType)
    def resolve_archivements(self, info):
        return Archievement.objects.all()

class CreateArchievement(graphene.Mutation):
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        posted_by = graphene.Int()
        class Arguments:
            title = graphene.String(required=True)
            description = graphene.String(required=True)
        def mutate(self, info,title,description):
            user = info.context.user
            if user.is_anonymous:
                raise GraphQLError('Login to create a archievement')
            archievement = Archievement.objects.create(
                title=title,
                description=description,
                posted_by=user
            )
            return CreateArchievement(
                title=archievement.title,
                description=archievement.description,
                posted_by=archievement.posted_by
            )
class Mutation(graphene.ObjectType):
    create_archievement = CreateArchievement.Field()
