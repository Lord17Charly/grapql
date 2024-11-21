import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from archievements.models import Archievement
from django.db.models import Q

from education.schema import EducationType
from work_exp_archivements import schema

class ArchievementType(DjangoObjectType):
    class Meta:
        model = Archievement

class Query(graphene.ObjectType):
    archivements = graphene.List(ArchievementType)
    archivements_by_id = graphene.Field(ArchievementType, id=graphene.Int(required=True))

    def resolve_archivements(self, info):
        return Archievement.objects.all()

    def resolve_archivements_by_id(self, info, id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Log in to see your archievements') # pragma: no cover.
        return Archievement.objects.filter(posted_by=user,id=id).first()

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
                raise GraphQLError('Login to create a archievement') # pragma: no cover.
            archievement = Archievement.objects.create(
                title=title,
                description=description,
                posted_by=user
            )
            return CreateArchievement(
                title=archievement.title,
                description=archievement.description,
                posted_by=user.id
            )
class UpdateArchivement(graphene.Mutation):
    idArchivements = graphene.Int()
    title = graphene.String(required=True)
    description = graphene.String(required=True)
    posted_by = graphene.Int()


    class Arguments:
        idArchivements = graphene.Int()
        title = graphene.String(required=True)
        description = graphene.String(required=True)

    def mutate(self,info,idArchivements,title=None,description=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to update your archievements') # pragma: no cover.
        archievement = Archievement.objects.get(id=idArchivements)
        if archievement.posted_by != user:
            raise GraphQLError('Not authorized to update this archievement') # pragma: no cover.
        if title:
            archievement.title = title
        if description:
            archievement.description = description
        archievement.save()

        return UpdateArchivement(
            idArchivements= archievement.id,
            title= archievement.title,
            description= archievement.description,
        )

class DeleteArchievement(graphene.Mutation):
    class Arguments:
        id_archivements = graphene.Int(required=True)
    success = graphene.Boolean()
    def mutate(self, info, id_archivements):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to delete your archievements') # pragma: no cover.
        archievement = Archievement.objects.get(pk=id_archivements)
        archievement.delete()
        return DeleteArchievement(success=True)


class Mutation(graphene.ObjectType):
    create_archievement = CreateArchievement.Field()
    update_archievement = UpdateArchivement.Field()
    delete_archievement = DeleteArchievement.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
