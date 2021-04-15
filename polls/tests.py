from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from polls import apiviews
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
# Create your tests here.

class TestPoll(APITestCase):
	def setUp(self):
		# It allows you to create requests with any http method, which you can then pass on to any view method and compare responses.
		self.factory = APIRequestFactory()
		# declare view for test
		self.view = apiviews.PollList.as_view()
		# declare uri for test
		self.uri = '/polls/'
		self.user = self.setup_user()
		self.token = Token.objects.create(user=self.user)
		self.client = APIClient()
		# self.token.save()

	@staticmethod
	def setup_user():
		User = get_user_model()
		return User.objects.create_user(
			'test',
			email = 'testuser@ahihi.com',
			password='test'
		)

	def test_list(self):
		# in this case we test get method with /polls/ uri
		request = self.factory.get(self.uri,
			HTTP_AUTHORIZATION='Token {}'.format(self.token.key))
		# request.user = self.user
		response = self.view(request)
		self.assertEqual(response.status_code, 200,
						 'Expected Response Code 200, received {0} instead.'
						 .format(response.status_code))

	def test_list2(self):
		# simply login with 'login' method
		self.client.login(username="test", password="test")
		# APIClient support us to easier create a get request
		response = self.client.get(self.uri)
		self.assertEqual(response.status_code, 200,
						 'Expected Response Code 200, received {0} instead.'
						 .format(response.status_code))

	def test_create(self):
		self.client.login(username="test", password="test")
		params = {
			"question": "How are you?",
			"created_by": 1
		}
		response = self.client.post(self.uri, params)
		self.assertEqual(response.status_code, 201,
						 'Expected Response Code 201, received {0} instead.'
						 .format(response.status_code))