from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from mixer.backend.django import mixer
import json
from django.contrib.auth import get_user_model
from interests.models import Interest
from interests.schema import schema

UPDATE_INTEREST_MUTATION = '''
mutation UpdateInterest($idInterest: Int!, $name: String!, $icon: String!) {
  updateInterest(idInterest: $idInterest, name: $name, icon: $icon) {
    idInterest
    name
    icon
  }
}
'''

CREATE_INTEREST_MUTATION = '''
mutation CreateInterest($name: String!, $icon: String!) {
  createInterest(name: $name, icon: $icon) {
    name
    icon
  }
}
'''

DELETE_INTEREST_MUTATION = '''
mutation DeleteInterest($idInterest: Int!) {
  deleteInterest(idInterest: $idInterest) {
    success
  }
}
'''

INTEREST_QUERY = '''
{
  interests {
    id
    name
    icon
  }
}
'''

INTEREST_BY_ID_QUERY = '''
query InterestById($id: Int!) {
  interestById(id: $id) {
    id
    name
    icon
  }
}
'''

class InterestTestCase(GraphQLTestCase):
    GRAPHQL_URL = "/graphql/"
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password")

        self.interest = mixer.blend(Interest, name="Test Interest", icon="test_icon.png", posted_by=self.user)

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

def test_update_interest(self):
    response = self.client.post(
        self.GRAPHQL_URL,
        data=json.dumps({
            "query": UPDATE_INTEREST_MUTATION,
            "variables": {
                "idInterest": self.interest.id,
                "name": "Updated Interest",
                "icon": "updated_icon.png"
            }
        }),
        content_type="application/json",
        **self.headers
    )
    content = json.loads(response.content)
    self.assertResponseNoErrors(response)
    assert content['data']['updateInterest']['name'] == "Updated Interest"
    assert content['data']['updateInterest']['icon'] == "updated_icon.png"

    def test_create_interest(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": CREATE_INTEREST_MUTATION,
                "variables": {
                    "name": "New Interest",
                    "icon": "new_icon.png"
                }
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert content['data']['createInterest']['name'] == "New Interest"
        assert content['data']['createInterest']['icon'] == "new_icon.png"

    def test_delete_interest(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": DELETE_INTEREST_MUTATION,
                "variables": {
                    "idInterest": self.interest.id
                }
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert content['data']['deleteInterest']['success'] is True
        with self.assertRaises(Interest.DoesNotExist):
            Interest.objects.get(id=self.interest.id)

    def test_query_interests(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": INTEREST_QUERY
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert content['data']['interests'][0]['name'] == "Test Interest"
        assert content['data']['interests'][0]['icon'] == "test_icon.png"

    def test_query_interest_by_id(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": INTEREST_BY_ID_QUERY,
                "variables": {
                    "id": self.interest.id
                }
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert content['data']['interestById']['name'] == "Test Interest"
        assert content['data']['interestById']['icon'] == "test_icon.png"
