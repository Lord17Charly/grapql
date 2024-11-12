import graphene
from graphene_django import DjangoObjectType
from graphql.pyutils import description
from header.models import Header
from users.schema import UserType
from graphql import GraphQLError
from linksHeader.models  import LinksHeader
from linksHeader.schema  import CreateLinksHeader, linksHeaderType
from header.schema import Header


class LinkInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    icon = graphene.String(required=True)
    link = graphene.String(required=True)

class HeaderType(DjangoObjectType):
    links = graphene.List(linksHeaderType)
    class Meta:
        model = Header
        fields = '__all__'

    def resolve_links(self,info):
        return self.link_header.all()

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
    links = graphene.List(linksHeaderType)
    class Arguments:
        idHeader = graphene.Int()
        title = graphene.String(required=True)
        profile_img = graphene.String()
        about = graphene.String()
        links = graphene.List(LinkInput)

    def mutate(self, info, idHeader, title, profile_img, about, links):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to update your')

        header = Header.objects.filter(posted_by=user).first()
        if header:
            header.title = title
            header.profile_img = profile_img
            header.about = about
            header.save()
        else:
            header = Header.objects.create(
                title=title,
                profile_img=profile_img,
                about=about,
                posted_by=user
            )

        if links:
            for link in links:
                LinksHeader.objects.create(
                    header=header,
                    title=link.title,
                    icon=link.icon,
                    link=link.link,
                )
        return UpdateHeader(
            idHeader=header.id,
            title=header.title,
            profile_img=header.profile_img,
            about=header.about,
            posted_by=user,
            links=header.link_header.all()
        )
class Mutation(graphene.ObjectType):
    update_header = UpdateHeader.Field()
