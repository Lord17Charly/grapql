import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from header.models import Header
from users.schema import UserType

class HeaderType(DjangoObjectType):
    class Meta:
        model = Header

class Query(graphene.ObjectType):
    headers = graphene.Field(HeaderType)

    def resolve_headers(self, info):
        return Header.objects.filter(posted_by=info.context.user).first()

class UpdateHeader(graphene.Mutation):
    header = graphene.Field(HeaderType)

    class Arguments:
        title = graphene.String(required=True)
        profile_img = graphene.String()
        about = graphene.String()

    def mutate(self, info, title, profile_img=None, about=None):
        user = info.context.user
        if not user.is_authenticated:
            raise GraphQLError("User not authenticated.")

        header, created = Header.objects.get_or_create(posted_by=user)

        header.title = title
        if profile_img:
            header.profile_img = profile_img
        if about:
            header.about = about

        header.save()

        return UpdateHeader(header=header)

class Mutation(graphene.ObjectType):
    update_header = UpdateHeader.Field()
