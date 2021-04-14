from rest_framework import serializers

from .models import Poll, Choise, Vote
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class VoteSerializer(serializers.ModelSerializer):
	class Meta:
		model = Vote
		fields = '__all__'


class ChoiseSerializer(serializers.ModelSerializer):
	# by setting many=True you tell drf that queryset contains mutiple items (a list of items) so drf needs to serialize each item with serializer class (and serializer.data will be a list)
	# One can add extra fields to a ModelSerializer or override the default fields by declaring fields on the class
	# refer to related_name='votes'
	votes = VoteSerializer(many=True, required=False)

	class Meta:
		model = Choise
		fields = '__all__'

'''
>>> from polls.serializers import PollSerializer
>>> from polls.models import Poll
>>> poll_serializer = PollSerializer(data={'question': 'who are you?', 'created_by': 1})
>>> poll_serializer.save()
>>> <Poll: who are you?>
'''
class PollSerializer(serializers.ModelSerializer):
	# refer to related_name='choise'
	choise = ChoiseSerializer(many=True, read_only=True, required=False)

	class Meta:
		model = Poll
		fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		# when we successfully create a new user, the response message doesn't include password
		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		# check if email or username is blank, also check is email/username already exist in DB
		# actions for email/username are default, we wanna hash the password so we override the create method
		user = User(
			email = validated_data['email'],
			username = validated_data['username']
		)
		# set_password will hashing password for security
		user.set_password(validated_data['password'])
		user.save()
		# create token when new user is created
		# to check token of user, go to shell => import User model => get any user instance => user_instance.get().auth_token
		# token is asigned for a specific user, in the next request, we can append that token in header of request as alternative of username and password
		Token.objects.create(user=user)
		return user
