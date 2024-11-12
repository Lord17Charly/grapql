import graphene
from graphene_django import DjangoObjectType
from .models import Education
from users.schema import UserType
from django.db.models import Q

class EducationType(DjangoObjectType):
    class Meta:
        model = Education

class Query(graphene.ObjectType):
    degrees = graphene.List(EducationType, search=graphene.String())

    def resolve_degrees(self, info, search=None, **kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')
        print (user)
        if (search=="*"):
            filter = (
                Q(posted_by=user)
            )
            return Education.objects.filter(filter)[:10]
        else:
            filter = (
                Q(posted_by=user) & Q(degree__icontains=search)
            )
            return Education.objects.filter(filter)

class ClassEducation(graphene.Mutation):
    idEducation = graphene.Int()
    degree = graphene.String()
    university = graphene.String()
    start_data = graphene.String()
    end_data = graphene.String()
    posted_by = graphene.Field(UserType)

    def mutate(self,info,idEducation,degree,university,start_data,
        end_data):
        user= info.context.user or None
        print(user)

        currenEducation = Education.objects.filter(id=idEducation).first()
        print(currenEducation)
