import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from .models import Skill
from django.db.models import Q

class SkillType(DjangoObjectType):
    class Meta:
        model = Skill

class Query(graphene.ObjectType):
    skills = graphene.List(SkillType)
    skills_by_id = graphene.Field(SkillType, id=graphene.Int(required=True))

    def resolve_skills(self, info):
        return Skill.objects.all()

    def resolve_skills_by_id(self, info, id, **Kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Log in to see your skills')
        # Se devuelve la skill con el filtro adecuado
        skill = Skill.objects.filter(posted_by=user, id=id).first()
        if not skill:
            raise GraphQLError('Skill not found')
        return skill

class CreateSkill(graphene.Mutation):
    name = graphene.String(required=True)
    posted_by = graphene.Int()

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
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

class UpdateSkill(graphene.Mutation):
    idSkill = graphene.Int(required=True)
    name = graphene.String(required=True)

    class Arguments:
        idSkill = graphene.Int(required=True)
        name = graphene.String(required=True)

    def mutate(self, info, idSkill, name):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to update a skill')
        skill = Skill.objects.get(id=idSkill)
        if skill.posted_by != user:
            raise GraphQLError('Not permitted to update this skill')
        skill.name = name
        skill.save()
        return UpdateSkill(idSkill=skill.id, name=skill.name)

class DeleteSkill(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        idSkill = graphene.Int(required=True)

    def mutate(self, info, idSkill):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to delete a skill')
        skill = Skill.objects.get(id=idSkill)
        if skill.posted_by != user:
            raise GraphQLError('Not permitted to delete this skill')
        skill.delete()
        return DeleteSkill(success=True)

class Mutation(graphene.ObjectType):
   create_skill = CreateSkill.Field()
   update_skill = UpdateSkill.Field()
   delete_skill = DeleteSkill.Field()
