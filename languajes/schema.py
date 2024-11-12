import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import languages

class languagesType(DjangoObjectType):
    class Meta:
        model = languages

class Query(graphene.ObjectType):
    languages = graphene.List(languagesType)
    def resolve_languages(self, info):
        return languages.objects.all()


class CreateLanguages(graphene.Mutation):
    name = graphene.String(required=True)
    posted_by = graphene.Int()
    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info,name):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to create a languages')
        language = languages.objects.create(
            name=name,
            posted_by=user
        )
        return CreateLanguages(
            name=language.name,
            posted_by=language.posted_by
        )

class Mutation(graphene.ObjectType):
    create_languages = CreateLanguages.Field()
