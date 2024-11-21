import json
from django.test import TestCase
from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth import get_user_model
from languajes.models import Languages
from mixer.backend.django import mixer

class LanguagesTestCase(GraphQLTestCase):
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

        # Crear un lenguaje para las pruebas
        self.language = mixer.blend(
            Languages,
            name="Spanish",
            posted_by=self.user
        )

    def test_query_language_by_id(self):
        QUERY_LANGUAGE_BY_ID = '''
        query GetLanguageById($idLanguage: Int!) {
            languagesById(idLanguage: $idLanguage) {
                name
                postedBy {
                    username
                }
            }
        }
        '''
        variables = {"idLanguage": self.language.id}

        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": QUERY_LANGUAGE_BY_ID,
                "variables": variables
            }),
            content_type="application/json",
            **self.headers
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)

        self.assertEqual(content['data']['languagesById']['name'], "Spanish")
        self.assertEqual(content['data']['languagesById']['postedBy']['username'], "testuser")

    def test_query_language_by_id_unauthenticated(self):
        QUERY_LANGUAGE_BY_ID = '''
        query GetLanguageById($idLanguage: Int!) {
            languagesById(idLanguage: $idLanguage) {
                name
                postedBy {
                    username
                }
            }
        }
        '''
        variables = {"idLanguage": self.language.id}

        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": QUERY_LANGUAGE_BY_ID,
                "variables": variables
            }),
            content_type="application/json"
        )

        content = json.loads(response.content)
        self.assertResponseHasErrors(response)
        self.assertEqual(content['errors'][0]['message'], 'Login to see your languages')

    def test_create_language(self):
        CREATE_LANGUAGE_MUTATION = '''
        mutation CreateLanguage($name: String!) {
            createLanguages(name: $name) {
                name
                postedBy {
                    username
                }
            }
        }
        '''
        variables = {"name": "French"}

        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": CREATE_LANGUAGE_MUTATION,
                "variables": variables
            }),
            content_type="application/json",
            **self.headers
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['createLanguages']['name'], "French")

    def test_update_language(self):
        UPDATE_LANGUAGE_MUTATION = '''
        mutation UpdateLanguage($idLanguage: Int!, $name: String!) {
            updateLanguages(idLanguage: $idLanguage, name: $name) {
                idLanguage
                name
            }
        }
        '''
        variables = {
            "idLanguage": self.language.id,
            "name": "German"
        }

        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": UPDATE_LANGUAGE_MUTATION,
                "variables": variables
            }),
            content_type="application/json",
            **self.headers
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['updateLanguages']['name'], "German")

    def test_delete_language(self):
        DELETE_LANGUAGE_MUTATION = '''
        mutation DeleteLanguage($idLanguage: Int!) {
            deleteLanguages(idLanguage: $idLanguage) {
                success
            }
        }
        '''
        variables = {"idLanguage": self.language.id}

        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": DELETE_LANGUAGE_MUTATION,
                "variables": variables
            }),
            content_type="application/json",
            **self.headers
        )

        content = json.loads(response.content)
        self.assertResponseNoErrors(response)
        self.assertTrue(content['data']['deleteLanguages']['success'])
