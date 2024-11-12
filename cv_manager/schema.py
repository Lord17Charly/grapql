import graphene
import graphql_jwt

import users.schema
import header.schema

class Query(users.schema.Query,users.schema.Mutation,header.schema.Query,):
    pass

class Mutation(header.schema.Mutation,users.schema.Mutation,graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
