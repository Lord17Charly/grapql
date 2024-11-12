import graphene
import graphql_jwt

import users.schema
import header.schema
import linksHeader.schema
import skills.schema
import archievements.schema
import languajes.schema
import interests.schema

class Query(users.schema.Query,
            header.schema.Query,
            linksHeader.schema.Query,
            skills.schema.Query,
            archievements.schema.Query,
            languajes.schema.Query,
            interests.schema.Query,
            graphene.ObjectType):
    pass
class Mutation(header.schema.Mutation,
                linksHeader.schema.Mutation,
                users.schema.Mutation,
                skills.schema.Mutation,
                archievements.schema.Mutation,
                languajes.schema.Mutation,
                interests.schema.Mutation,
                graphene.ObjectType):

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
schema = graphene.Schema(query=Query, mutation=Mutation)
