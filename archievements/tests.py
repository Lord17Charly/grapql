from django.contrib.auth import get_user_model
from graphene_django.utils.testing import GraphQLTestCase
from mixer.backend.django import mixer
import json
from archievements.models import Archievement
from archievements.schema import schema

CREATE_ARCHIEVEMENT_MUTATION = '''
mutation CreateArchievement($title: String!, $description: String!) {
  createArchievement(title: $title, description: $description) {
    title
    description
    postedBy
  }
}
'''

UPDATE_ARCHIEVEMENT_MUTATION = '''
mutation UpdateArchievement($idArchivements: Int!, $title: String!, $description: String!) {
  updateArchievement(idArchivements: $idArchivements, title: $title, description: $description) {
    idArchivements
    title
    description
  }
}
'''

DELETE_ARCHIEVEMENT_MUTATION = '''
mutation DeleteArchievement($idArchivements: Int!) {
  deleteArchievement(idArchivements: $idArchivements) {
    success
  }
}
'''

ARCHIEVEMENT_QUERY = '''
{
  archivements {
    id
    title
    description
  }
}
'''

ARCHIEVEMENT_BY_ID_QUERY = '''
query ArchievementById($id: Int!) {
  archivementsById(id: $id) {
    id
    title
    description
  }
}
'''

class ArchievementTestCase(GraphQLTestCase):
    GRAPHQL_URL = "/graphql/"
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password")

        self.archievement = mixer.blend(Archievement, title="Test Archievement", description="Test Description", posted_by=self.user)

        response_token = self.query(
            '''
            mutation TokenAuth($username: String!, $password: String!) {
                tokenAuth(username: $username, password: $password) {
                    token
                }
            }
            ''',
            variables={'username': 'testuser', 'password': 'password'}
        )
        content_token = json.loads(response_token.content)
        self.token = content_token['data']['tokenAuth']['token']
        self.headers = {"HTTP_AUTHORIZATION": f"JWT {self.token}"}

    def test_create_archievement(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": CREATE_ARCHIEVEMENT_MUTATION,
                "variables": {
                    "title": "New Archievement",
                    "description": "New Description"
                }
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert content['data']['createArchievement']['title'] == "New Archievement"
        assert content['data']['createArchievement']['description'] == "New Description"

    def test_update_archievement(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": UPDATE_ARCHIEVEMENT_MUTATION,
                "variables": {
                    "idArchivements": self.archievement.id,
                    "title": "Updated Archievement",
                    "description": "Updated Description"
                }
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert content['data']['updateArchievement']['title'] == "Updated Archievement"
        assert content['data']['updateArchievement']['description'] == "Updated Description"

    def test_delete_archievement(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": DELETE_ARCHIEVEMENT_MUTATION,
                "variables": {
                    "idArchivements": self.archievement.id
                }
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert content['data']['deleteArchievement']['success'] is True
        with self.assertRaises(Archievement.DoesNotExist):
            Archievement.objects.get(id=self.archievement.id)

    def test_query_archivements(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": ARCHIEVEMENT_QUERY
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert content['data']['archivements'][0]['title'] == "Test Archievement"
        assert content['data']['archivements'][0]['description'] == "Test Description"

    def test_query_archivement_by_id(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": ARCHIEVEMENT_BY_ID_QUERY,
                "variables": {
                    "id": self.archievement.id
                }
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert content['data']['archivementsById']['title'] == "Test Archievement"
        assert content['data']['archivementsById']['description'] == "Test Description"
