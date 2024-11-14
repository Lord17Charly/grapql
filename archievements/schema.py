import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from archievements.models import Archievement
from django.db.models import Q

from education.schema import EducationType

class ArchievementType(DjangoObjectType):
    class Meta:
        model = Archievement

class Query(graphene.ObjectType):
    archivementsBy = graphene.List(EducationType,idArchivement= graphene.Int())
    archivements = graphene.List(ArchievementType)
    def resolve_archivements(self, info):
        return Archievement.objects.all()

    def resolve_archivementesById(self,info,idArchivement, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Log in to see your archievements')
        print(user)
        filter=(
            Q(posted_by=user) & Q(id=idArchivement)
        )
        return Archievement.object.filter(filter).first()

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
            raise GraphQLError('Login to update your archievements')
        archievement = Archievement.objects.get(id=idArchivements)
        if archievement.posted_by != user:
            raise GraphQLError('Not authorized to update this archievement')
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
    success = graphene.Boolean()

    class Arguments:
        idArchivements = graphene.Int(required=True)

    def mutate(self, info, idArchivements):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to delete your archievements')
        archievement = Archievement.objects.get(id=idArchivements)
        if not archievement:
            raise GraphQLError('Not authorized to delete this archievement')

        archievement.delete()
        return DeleteArchievement(success=True)

class Mutation(graphene.ObjectType):
    create_archievement = CreateArchievement.Field()
    update_archievement = UpdateArchivement.Field()
    delete_archievemnt = DeleteArchievement.Field()
