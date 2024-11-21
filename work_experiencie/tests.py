import json
from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from mixer.backend.django import mixer
from django.contrib.auth import get_user_model
from work_experiencie.models import WorkEperiencies
from work_exp_archivements.models import WorkExperienciesArchivements
from work_experiencie.schema import schema

class WorkExperienciesTestCase(GraphQLTestCase):
    GRAPHQL_URL ="http://localhost:8000/graphql/"
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword"
        )
        response_token = self.query(
            '''
            mutation TokenAuth($username: String!, $password: String!) {
                tokenAuth(username: $username, password: $password) {
                    token
                }
            }
            ''',
            variables={'username': 'testuser', 'password': 'testpassword'}
        )
        content_token = json.loads(response_token.content)
        self.token = content_token['data']['tokenAuth']['token']
        self.headers = {"HTTP_AUTHORIZATION": f"JWT {self.token}"}

        self.work_exp = mixer.blend(
            WorkEperiencies,
            company="Test Company",
            position="Test Position",
            location="Test Location",
            posted_by=self.user
        )
        self.archivement = mixer.blend(
            WorkExperienciesArchivements,
            work_experiencies=self.work_exp,
            description="Test Achievement"
        )

    def test_create_work_experience(self):
        CREATE_WORK_EXP_MUTATION = '''
        mutation CreateWorkExperience(
            $company: String!,
            $position: String!,
            $location: String!,
            $startDate: String!,
            $endDate: String!,
            $archivements: [WorkExpArchInput]
        ) {
            createWorkExperiencies(
                company: $company,
                position: $position,
                location: $location,
                startDate: $startDate,
                endDate: $endDate,
                archivements: $archivements
            ) {
                id
                company
                position
                location
                startDate
                endDate
                archivements {
                    description
                }
            }
        }
        '''

        variables = {
            "company": "New Company",
            "position": "Developer",
            "location": "New City",
            "startDate": "2023-01-01",
            "endDate": "2024-01-01",
            "archivements": [
                {"description": "Achievement 1"},
                {"description": "Achievement 2"}
            ]
        }

        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": CREATE_WORK_EXP_MUTATION,
                "variables": variables
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertNotIn("errors", content, f"GraphQL Errors: {content.get('errors')}")

        data = content['data']['createWorkExperiencies']
        self.assertEqual(data['location'], "New City")
        self.assertEqual(data['position'], "Developer")



    def test_query_work_experience_by_id(self):
        WORK_EXP_QUERY = '''
        query GetWorkExperienceById($idWorExp: Int!) {
            workExperienciesById(idWorExp: $idWorExp) {
                id
                company
                position
                location
                startDate
                endDate
                archivements {
                    description
                }
            }
        }
        '''

        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": WORK_EXP_QUERY,
                "variables": {
                    "idWorExp":self.work_exp.id,
                    "company": "Updated Company",
                    "position": "Updated Position",
                    "location": "Updated Location"
                }
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        print("Query Work Experience Response:", content)

        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['workExperienciesById']['company'], "Test Company")

    def test_update_work_experience(self):
        UPDATE_WORK_EXP_MUTATION = '''
        mutation UpdateWorkExperience(
            $idWorkEperiencies: Int!,
            $company: String,
            $position: String,
            $location: String,
            $startDate: String,
            $endDate: String,
            $archivements: [WorkExpArchInput]
        ) {
            updateWorkExperiencies(  # Cambiado a camelCase
                idWorkEperiencies: $idWorkEperiencies,
                company: $company,
                position: $position,
                location: $location,
                startDate: $startDate,
                endDate: $endDate,
                archivements: $archivements
            ) {
                idWorkEperiencies
                company
                position
                location
                startDate
                endDate
                archivements {
                    description
                }
            }
        }
        '''

        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": UPDATE_WORK_EXP_MUTATION,
                "variables": {
                    "idWorkEperiencies":self.work_exp.id,
                    "company": "Updated Company",
                    "position": "Updated Position",
                    "location": "Updated Location"
                }
            }),
            content_type="application/json",
            **self.headers
        )

        content = json.loads(response.content)

        print("Update Work Experience Response:", content)

        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['updateWorkExperiencies']['company'], "Updated Company")
        self.assertEqual(content['data']['updateWorkExperiencies']['position'], "Updated Position")
