import graphene
from graphene_django import DjangoObjectType
from .models import WorkEperiencies
from graphql import GraphQLError
from work_exp_archivements.models import WorkExperienciesArchivements
from work_exp_archivements.schema import workExpArchType


class WorkExpArchInput(graphene.InputObjectType):
    description = graphene.String(required=True)

class WorkEperienciesType(DjangoObjectType):
    archivements = graphene.List(workExpArchType)

    class Meta:
        model = WorkEperiencies
        fields = '__all__'

    def resolve_archivements(self, info):
        # Retorna solo los logros relacionados con esta instancia de `WorkEperiencies`
        return self.archivements.filter(work_experiencies=self)
class Query(graphene.ObjectType):
    work_experiencies = graphene.List(WorkEperienciesType)

    def resolve_work_experiencies(self, info):
        return WorkEperiencies.objects.all()

class CreateWorkEperiencies(graphene.Mutation):
    idWorkEperiencies = graphene.Int()
    company = graphene.String()
    location = graphene.String()
    start_date = graphene.String()
    end_date = graphene.String()
    archivements = graphene.List(workExpArchType)

    class Arguments:
        idWorkEperiencies = graphene.Int()
        company = graphene.String(required=True)
        location = graphene.String(required=True)
        start_date = graphene.String(required=True)
        end_date = graphene.String(required=True)
        archivements = graphene.List(WorkExpArchInput)

    def mutate(self, info, idWorkEperiencies, company, location, start_date, end_date, archivements):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Log in to create a work experience")

        # Crear o actualizar `WorkEperiencies`
        work_experiencies = WorkEperiencies.objects.create(
            company=company,
            location=location,
            start_date=start_date,
            end_date=end_date,
            posted_by=user
        )


        if archivements:
            for archivement in archivements:
                created_archivement = WorkExperienciesArchivements.objects.create(
                    work_experiencies=work_experiencies,
                    description=archivement.description,
                )
                created_archivements.append(created_archivement)

        return CreateWorkEperiencies(
            idWorkEperiencies=work_experiencies.id,
            company=work_experiencies.company,
            location=work_experiencies.location,
            start_date=work_experiencies.start_date,
            end_date=work_experiencies.end_date,
            archivements=created_archivements
        )

class Mutation(graphene.ObjectType):
    create_work_experiencies = CreateWorkEperiencies.Field()
