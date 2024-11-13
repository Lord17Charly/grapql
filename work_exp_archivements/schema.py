import graphene
from graphene_django import DjangoObjectType
from graphql.pyutils import description
from .models import WorkExperienciesArchivements
from graphql import GraphQLError
from work_experiencie.models import WorkEperiencies


class workExpArchType(DjangoObjectType):
    class Meta:
        model = WorkExperienciesArchivements
        fields = '__all__'

class Query(graphene.ObjectType):
    work_exp_archivements = graphene.List(workExpArchType)

    def resolve_work_exp_archivements(self, info):
        return WorkExperienciesArchivements.objects.all()

class CreateWorkEperienciesArchivementes(graphene.Mutation):
        description = graphene.String(required=True)
        work_experiencies = graphene.Int()
        class Arguments:
            description = graphene.String(required=True)
            work_experiencies = graphene.Int()

        def mutate(self, info, description, work_experiencies):
            user = info.context.user
            if user.is_anonymous:
                raise GraphQLError('Login to create a work experiencies archivement')

            work_experiencies = WorkEperiencies.objects.get(id=work_experiencies)
            work_exp_archivement = WorkExperienciesArchivements.objects.create(
                description=description,
                work_experiencies=work_experiencies
            )
            return CreateWorkEperienciesArchivementes(
                description = work_exp_archivement.description,
                work_experiencies = work_exp_archivement.work_experiencies
            )
class Mutation(graphene.ObjectType):
    create_work_exp_archivement = CreateWorkEperienciesArchivementes.Field()
