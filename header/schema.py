import graphene
from graphene_django import DjangoObjectType
from graphql.pyutils import description
from header.models import Header
from users.schema import UserType
from graphql import GraphQLError

class HeaderType(DjangoObjectType):
    class Meta:
        model = Header

class Query(graphene.ObjectType):
    headers = graphene.Field(HeaderType)

    def resolve_headers(self, info):
        return Header.objects.filter(posted_by=info.context.user).first()

class UpdateHeader(graphene.Mutation):
    idHeader = graphene.Int()
    title = graphene.String(required=True)
    profile_img = graphene.String()
    about = graphene.String()
    posted_by = graphene.Field(UserType)

    class Arguments:
        idHeader = graphene.Int()
        title = graphene.String(required=True)
        profile_img = graphene.String()
        about = graphene.String()

    def mutate(self, info, idHeader, title, profile_img, about):
        user = info.context.user
        # Verificar si el usuario está autenticado
        if user.is_anonymous:
            raise GraphQLError('Login to update your header')

        # Buscar el Header asociado al usuario
        header = Header.objects.filter(posted_by=user).first()

        if header:
            # Si existe un header, lo actualizamos
            header.title = title
            header.profile_img = profile_img
            header.about = about
            header.save()
        else:
            # Si no existe un header, lo creamos
            header = Header.objects.create(
                title=title,
                profile_img=profile_img,
                about=about,
                posted_by=user
            )
        return UpdateHeader(
            idHeader=header.id,
            title=header.title,
            profile_img=header.profile_img,
            about=header.about,
            posted_by=user
        )
class Mutation(graphene.ObjectType):
    update_header = UpdateHeader.Field()
