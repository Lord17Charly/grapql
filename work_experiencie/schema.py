import graphene
from graphene_django import DjangoObjectType
from .models import WorkEperiencies
from graphql import GraphQLError
from work_exp_archivements.models import WorkExperienciesArchivements
from work_exp_archivements.schema import workExpArchType
from django.db.models import Q


class WorkExpArchInput(graphene.InputObjectType):
    description = graphene.String(required=True)

class WorkEperienciesType(DjangoObjectType):
    archivements = graphene.List(workExpArchType)

    class Meta:
        model = WorkEperiencies
        fields = '__all__'

    def resolve_archivements(self, info):
        return self.archivements.filter(work_experiencies=self)
class Query(graphene.ObjectType):
    work_experiencies = graphene.List(WorkEperienciesType)
    work_experienciesById = graphene.Field(WorkEperienciesType, idWorExp=graphene.Int(required=True))

    def resolve_work_experiencies(self, info):
        return WorkEperiencies.objects.all()

    def resolve_work_experienciesById(self, info, idWorExp,**Kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to see your work experiencies')
        print(user)
        filter=(
                Q(posted_by=user) & Q (id=idWorExp)
            )
        return WorkEperiencies.objects.filter(filter).first()

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

class UpdateWorkEperiencies(graphene.Mutation):
    idWorkEperiencies = graphene.Int()
    company = graphene.String()
    location = graphene.String()
    start_date = graphene.String()
    end_date = graphene.String()
    archivements = graphene.List(workExpArchType)

    class Arguments:
        idWorkEperiencies = graphene.Int(required=True)
        company = graphene.String()
        location = graphene.String()
        start_date = graphene.String()
        end_date = graphene.String()
        archivements = graphene.List(WorkExpArchInput)

    def mutate(self, info, idWorkEperiencies, company=None, location=None, start_date=None, end_date=None, archivements=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to update your work experience')

        work_experience = WorkEperiencies.objects.filter(id=idWorkEperiencies, posted_by=user).first()
        if not work_experience:
            raise GraphQLError('Work experience not found or you do not have permission to edit it')

        if company:
            work_experience.company = company
        if location:
            work_experience.location = location
        if start_date:
            work_experience.start_date = start_date
        if end_date:
            work_experience.end_date = end_date
        work_experience.save()

        if archivements is not None:
            WorkExperienciesArchivements.objects.filter(work_experiencies=work_experience).delete()
            for archivement in archivements:
                WorkExperienciesArchivements.objects.create(
                    work_experiencies=work_experience,
                    description=archivement.description
                )

        return UpdateWorkEperiencies(
            idWorkEperiencies=work_experience.id,
            company=work_experience.company,
            location=work_experience.location,
            start_date=work_experience.start_date,
            end_date=work_experience.end_date,
            archivements=work_experience.archivements.all()
        )


class DeleteWorkEperiencies(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        idWorkEperiencies = graphene.Int(required=True)

    def mutate(self, info, idWorkEperiencies):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('Login to delete your work experience')

        work_experience = WorkEperiencies.objects.filter(id=idWorkEperiencies, posted_by=user).first()
        if not work_experience:
            raise GraphQLError('Work experience not found or you do not have permission to delete it')

        work_experience.delete()
        return DeleteWorkEperiencies(success=True)


class Mutation(graphene.ObjectType):
    create_work_experiencies = CreateWorkEperiencies.Field()
    update_work_experiencies = UpdateWorkEperiencies.Field()
    delete_work_experiencies = DeleteWorkEperiencies.Field()
