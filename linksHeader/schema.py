from django.db.models import fields
from django.urls.conf import URLPattern
import graphene
from graphene_django import DjangoObjectType
from header.models import Header
from linksHeader.models import LinksHeader
from graphql import GraphQLError

class linksHeaderType(DjangoObjectType):
    class Meta:
        model = LinksHeader
        fields= '__all__'

class Query(graphene.ObjectType):
    linksHeaders = graphene.List(linksHeaderType)

    def resolve_linksHeaders(self, info):
        return LinksHeader.objects.all()


class CreateLinksHeader(graphene.Mutation):

        title = graphene.String(required=True)
        icon = graphene.String()
        link = graphene.String()
        header = graphene.Int()
        class Arguments:
            title = graphene.String(required=True)
            icon = graphene.String()
            link = graphene.String()
            header = graphene.Int()

        def mutate(self, info, title, icon, link, header):
            user = info.context.user
            if user.is_anonymous:
                raise GraphQLError('Login to create a link')

            header = Header.objects.get(id=header)
            linkHeader = LinksHeader.objects.create(
                title=title,
                icon=icon,
                link=link,
                header=header
            )
            return CreateLinksHeader(
                title = linkHeader.title,
                icon = linkHeader.icon,
                link = linkHeader.link,
                header = linkHeader.header
            )

class Mutation(graphene.ObjectType):
    create_linksHeader = CreateLinksHeader.Field()
