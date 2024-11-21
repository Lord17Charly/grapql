import json
from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from .models import Skill

class SkillTestCase(GraphQLTestCase):
    GRAPHQL_URL = "/graphql/"

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

        # Crear una habilidad para las pruebas
        self.skill = mixer.blend(
            Skill,
            name="JavaScript",
            posted_by=self.user
        )

    def test_query_skill_by_id(self):
        QUERY_SKILL_BY_ID = '''
        query GetSkillById($id: Int!) {
            skillsById(id: $id) {
                name
                postedBy {
                    username
                }
            }
        }
        '''
        variables = {"id": self.skill.id}

        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": QUERY_SKILL_BY_ID,
                "variables": variables
            }),
            content_type="application/json",
            **self.headers
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['skillsById']['name'], "JavaScript")
        self.assertEqual(content['data']['skillsById']['postedBy']['username'], "testuser")


    def test_create_skill(self):
        CREATE_SKILL_MUTATION = '''
        mutation CreateSkill($name: String!) {
            createSkill(name: $name) {
                name
            }
        }
        '''
        variables = {"name": "Python"}

        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": CREATE_SKILL_MUTATION,
                "variables": variables
            }),
            content_type="application/json",
            **self.headers
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['createSkill']['name'], "Python")

    def test_update_skill(self):
        UPDATE_SKILL_MUTATION = '''
        mutation UpdateSkill($idSkill: Int!, $name: String!) {
            updateSkill(idSkill: $idSkill, name: $name) {
                idSkill
                name
            }
        }
        '''
        variables = {
            "idSkill": self.skill.id,
            "name": "Django"
        }

        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": UPDATE_SKILL_MUTATION,
                "variables": variables
            }),
            content_type="application/json",
            **self.headers
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['updateSkill']['name'], "Django")

    def test_delete_skill(self):
        DELETE_SKILL_MUTATION = '''
        mutation DeleteSkill($idSkill: Int!) {
            deleteSkill(idSkill: $idSkill) {
                success
            }
        }
        '''
        variables = {"idSkill": self.skill.id}

        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": DELETE_SKILL_MUTATION,
                "variables": variables
            }),
            content_type="application/json",
            **self.headers
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['deleteSkill']['success'])
