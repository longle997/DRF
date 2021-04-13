from rest_framework import serializers

from .models import Poll, Choise, Vote

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