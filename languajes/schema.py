import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError

from users.schema import UserType
from .models import Languages
from django.db.models import Q

class LanguagesType(DjangoObjectType):
    class Meta:
        model = Languages
        fields = '__all__'

class Query(graphene.ObjectType):
    languages_by_id = graphene.Field(LanguagesType,idLanguage=graphene.Int())
    def resolve_languages(self, info):
        return Languages.objects.all()

    def resolve_languages_by_id(self,info,idLanguage,**Kwargs):
        user= info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to see your languages')
        print(user)
        filter = (
            Q(posted_by=user) & Q(id=idLanguage)
        )
        return Languages.objects.filter(filter).first()

class CreateLanguages(graphene.Mutation):
    name = graphene.String(required=True)
    posted_by = graphene.Field(UserType)
    class Arguments:
        name = graphene.String(required=True)
    def mutate(self, info,name):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to create a languages')
        language = Languages.objects.create(
            name=name,
            posted_by=user
        )
        return CreateLanguages(
            name=language.name,
            posted_by=language.posted_by
        )

class UpdateLanguages(graphene.Mutation):
        idLanguage = graphene.Int()
        name = graphene.String(required=True)
        class Arguments:
            idLanguage = graphene.Int()
            name = graphene.String(required=True)

        def mutate(self, info , idLanguage,name,**Kwargs):
            user = info.context.user
            if user.is_anonymous:
                raise GraphQLError('Login to update a languages')
            language = Languages.objects.get(id=idLanguage)
            language.name = name
            language.save()

            return UpdateLanguages(
                idLanguage=language.id,
                name=language.name
            )

class Deletelanguages(graphene.Mutation):
        success = graphene.Boolean()

        class Arguments:
            idLanguage = graphene.Int()

        def mutate(self, info , idLanguage):
            user = info.context.user
            if user.is_anonymous:
                raise GraphQLError('Login to delete a languages')
            language = Languages.objects.get(id=idLanguage)
            language.delete()

            return Deletelanguages(success=True)

class Mutation(graphene.ObjectType):
    create_languages = CreateLanguages.Field()
    update_languages = UpdateLanguages.Field()
    delete_languages = Deletelanguages.Field()
