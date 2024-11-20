from graphene_django.utils.testing import GraphQLTestCase
from mixer.backend.django import mixer
import json
from django.contrib.auth import get_user_model
from header.models import Header
from linksHeader.models import LinksHeader
from users.schema import UserType
from header.schema import schema


UPDATE_HEADER_MUTATION = '''
mutation UpdateHeader($idHeader: Int!, $title: String!, $profileImg: String, $about: String, $links: [LinkInput]) {
  updateHeader(idHeader: $idHeader, title: $title, profileImg: $profileImg, about: $about, links: $links) {
    idHeader
    title
    profileImg
    about
    links {
      title
      icon
      link
    }
  }
}
'''

HEADER_QUERY = '''
{
  headers {
    id
    title
    profileImg
    about
    links {
      title
      icon
      link
    }
  }
}
'''

class HeaderTestCase(GraphQLTestCase):
    GRAPHQL_URL = "/graphql/"
    GRAPHQL_SCHEMA = schema

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password")

        self.header = mixer.blend(Header, title="Initial Header", profile_img="initial.jpg", about="Initial about", posted_by=self.user)
        self.link1 = mixer.blend(LinksHeader, header=self.header, title="Link 1", icon="icon1.png", link="https://link1.com")

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

    def test_update_header(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": UPDATE_HEADER_MUTATION,
                "variables": {
                    "idHeader": self.header.id,
                    "title": "Updated Header",
                    "profileImg": "updated.jpg",
                    "about": "Updated about",
                    "links": [
                        {"title": "New Link", "icon": "icon2.png", "link": "https://newlink.com"}
                    ]
                }
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert content['data']['updateHeader']['title'] == "Updated Header"
        assert content['data']['updateHeader']['profileImg'] == "updated.jpg"
        assert content['data']['updateHeader']['about'] == "Updated about"
        assert len(content['data']['updateHeader']['links']) == 2
        assert content['data']['updateHeader']['links'][1]['title'] == "New Link"

    def test_query_header(self):
        response = self.client.post(
            self.GRAPHQL_URL,
            data=json.dumps({
                "query": HEADER_QUERY
            }),
            content_type="application/json",
            **self.headers
        )
        content = json.loads(response.content)

        self.assertResponseNoErrors(response)

        assert content['data']['headers']['title'] == "Initial Header"
        assert len(content['data']['headers']['links']) == 1
        assert content['data']['headers']['links'][0]['title'] == "Link 1"
