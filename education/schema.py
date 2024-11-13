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
class Mutation(graphene.ObjectType):
    create_education = CreateEducation.Field()
