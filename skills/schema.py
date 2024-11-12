from django.urls.conf import URLPattern
import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Skill


class skillsType(DjangoObjectType):
    class Meta:
        model = Skill

class Query(graphene.ObjectType):
    skills = graphene.List(skillsType)

    def resolve_skills(self, info):
        return Skill.objects.all()

class CreateSkill(graphene.Mutation):
    name = graphene.String(required=True)
    posted_by = graphene.Int()

    class Arguments:
        name = graphene.String(required=True)


    def  mutate(self, info,name):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to create a skill')
        skill = Skill.objects.create(
            name=name,
            posted_by=user
        )
        return CreateSkill(
            name=skill.name,
            posted_by=skill.posted_by
        )

class Mutation(graphene.ObjectType):
   create_skill = CreateSkill.Field()
