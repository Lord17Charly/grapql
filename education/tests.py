from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
import json
from education.models import Education
from education.schema import schema

CREATE_EDUCATION_MUTATION = '''
mutation CreateEducation($degree: String!, $university: String!, $startDate: Date!, $endDate: Date!) {
  createEducation(degree: $degree, university: $university, startDate: $startDate, endDate: $endDate) {
    idEducation
    degree
    university
    startDate
    endDate
  }
}
'''

EDUCATION_QUERY = '''
{
  degress {
    id
    degree
    university
    startDate
    endDate
  }
}
'''

class EducationTestCase(GraphQLTestCase):
    GRAPHQL_URL = "/graphql/"
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password")
        self.education1 = mixer.blend(
            Education,
            degree="Bachelor's in Computer Science",
            university="Test University",
            start_date="2020-01-01",
            end_date="2024-01-01",
            posted_by=self.user
        )
        self.education2 = mixer.blend(
            Education,
            degree="Master's in Data Science",
            university="Test University",
            start_date="2025-01-01",
            end_date="2027-01-01",
            posted_by=self.user
        )
        response_token = self.query(
            '''
            mutation TokenAuth($username: String!, $password: String!) {
                tokenAuth(username: $username, password: $password) {
                    token
                }
            }
            ''',
            variables={"username": "testuser", "password": "password"}
        )
        content_token = json.loads(response_token.content)
        self.token = content_token['data']['tokenAuth']['token']
        self.headers = {"HTTP_AUTHORIZATION": f"JWT {self.token}"}

    def test_create_education(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": CREATE_EDUCATION_MUTATION,
                "variables": {
                    "degree": "PhD in Artificial Intelligence",
                    "university": "AI University",
                    "startDate": "2028-01-01",
                    "endDate": "2032-01-01"
                }
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert content['data']['createEducation']['degree'] == "PhD in Artificial Intelligence"
        assert content['data']['createEducation']['university'] == "AI University"

    def test_query_education(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({"query": EDUCATION_QUERY}),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert len(content['data']['degress']) == 2
        assert content['data']['degress'][0]['degree'] == "Bachelor's in Computer Science"
        assert content['data']['degress'][1]['degree'] == "Master's in Data Science"
