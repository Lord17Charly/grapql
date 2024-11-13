import graphene
import graphql_jwt

import users.schema
import header.schema
import linksHeader.schema
import skills.schema
import archievements.schema
import languajes.schema
import interests.schema
import education.schema
import work_experiencie.schema
import work_exp_archivements.schema

class Query(users.schema.Query,
            header.schema.Query,
            linksHeader.schema.Query,
            skills.schema.Query,
            archievements.schema.Query,
            languajes.schema.Query,
            interests.schema.Query,
            education.schema.Query,
            work_experiencie.schema.Query,
            work_exp_archivements.schema.Query,
            graphene.ObjectType):
    pass
class Mutation(header.schema.Mutation,
                linksHeader.schema.Mutation,
                users.schema.Mutation,
                skills.schema.Mutation,
                archievements.schema.Mutation,
                languajes.schema.Mutation,
                interests.schema.Mutation,
                education.schema.Mutation,
                work_experiencie.schema.Mutation,
                work_exp_archivements.schema.Mutation,
                graphene.ObjectType):

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
