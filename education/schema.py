import graphene
from graphene_django import DjangoObjectType
from .models import Education
from graphql_jwt.decorators import login_required
from users.schema import UserType
from django.db.models import Q

class EducationType(DjangoObjectType):
    class Meta:
        model = Education

class Query(graphene.ObjectType):
    degress = graphene.List(EducationType,search=graphene.String())
    degreeById = graphene.Field(EducationType,idEducation=graphene.Int())
    # get all education
    def resolve_degress(self,info,search=None, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Log in to see your education')
        print(user)

        if search:
            filter= (
                Q(posted_by=user)
            )
            return Education.objects.filter(filter)[:10]
        else:
            filter= (
                Q(posted_by=user) & Q(degree__icontains=search)
            )
        return Education.objects.filter(filter)

    # get by id
    def resolve_degreeById(self,info,idEducation, **Kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Log in to see your education')
        print(user)
        filter = (
            Q(posted_by=user) & Q(id=idEducation)
        )
        return Education.objects.filter(filter).first()
class CreateEducation(graphene.Mutation):
    idEducation = graphene.Int()
    degree = graphene.String()
    university = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    posted_by = graphene.Field(UserType)

    class Arguments:
        idEducation = graphene.Int()
        degree = graphene.String()
        university = graphene.String()
        start_date = graphene.Date()
        end_date = graphene.Date()

    def mutate(self,info,idEducation,degree,university,start_date,end_date):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Log in to add education')
        print(user)

        currentEducation = Education.objects.filter(id=idEducation).first()
        print(currentEducation)
        education = Education(
            degree=degree,
            university=university,
            start_date=start_date,
            end_date=end_date,
            posted_by=user
        )
        if currentEducation:
            education.pk = currentEducation.id
        education.save()
        return CreateEducation(
            idEducation=education.pk,
            degree=education.degree,
            university=education.university,
            start_date=education.start_date,
            end_date=education.end_date,
            posted_by=education.posted_by
        )

class DeleteEducation(graphene.Mutation):
    idEducation = graphene.Int()

    class Arguments:
        idEducation = graphene.Int()

    def mutate(self,info,idEducation):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Log in to delete education')
        print(user)

        currentEducation = Education.objects.filter(id= idEducation).first()
        print(currentEducation)

        if not currentEducation:
            raise Exception('Education not found')
        currentEducation.delete()

        return DeleteEducation(idEducation=idEducation)
class Mutation(graphene.ObjectType):
    create_education = CreateEducation.Field()
    delete_education = DeleteEducation.Field()
