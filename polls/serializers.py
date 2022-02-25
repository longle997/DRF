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
		# i don't want when user create poll, they can choose created_by field
		read_only_fields = ['poll']


	def create(self, validated_data):
		# self.context.get("poll") was sent from ChoiseList view
		poll = self.context.get("poll")
		# add field created_by to validated data
		validated_data.update({"poll": poll})
		return Choise.objects.create(**validated_data)

'''
>>> from polls.serializers import PollSerializer
>>> from polls.models import Poll
>>> poll_serializer = PollSerializer(data={'question': 'who are you?', 'created_by': 1})
>>> poll_serializer.save()
>>> <Poll: who are you?>
'''
class PollSerializer(serializers.ModelSerializer):
	# refer to related_name='choise', if we wanna have choise field in our poll object, need to add this LOC
	choise = ChoiseSerializer(many=True, read_only=True, required=False)

	class Meta:
		model = Poll
		fields = '__all__'
		# i don't want when user create poll, they can choose created_by field
		read_only_fields = ['created_by']


	def create(self, validated_data):
		# get user data from request
		user = None

		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user

		# add field created_by to validated data
		validated_data.update({"created_by": user})
		return Poll.objects.create(**validated_data)


class CreatePollSerializer(serializers.ModelSerializer):

	class Meta:
		model = Poll
		fields = ['question']

	def create(self, validated_data):
		user_ids = validated_data.pop('user_id')
		instance = super().create(validated_data)
		instance.users.add(user)
		return instance


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
		# to check token of user, go to shell => import User model => get any user instance => user_instance.auth_token
		# token is asigned for a specific user, in the next request, we can append that token in header of request as alternative of username and password
		Token.objects.create(user=user)
		return user
