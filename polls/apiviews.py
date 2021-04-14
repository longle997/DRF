from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404

from .models import Poll, Choise, Vote
from .serializers import PollSerializer, ChoiseSerializer, VoteSerializer, UserSerializer
from rest_framework import generics, status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

'''
# APIView is the most basic class that you usually override when defining your REST view
class PollList(APIView):
	# override the get method, using method as HTTP request
	def get(self, request):
		polls = Poll.objects.all()[:20]
		data = PollSerializer(polls, many=True).data
		# response data must be in JSON format
		return Response(data)

class PollDetail(APIView):
	def get(self, request, pk):
		poll = get_object_or_404(Poll, pk=pk)
		data = PollSerializer(poll).data
		return Response(data)
		'''

# Used for read-write endpoints to represent a collection of model instances.
# Provides get and post method handlers.
class PollList(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	# The queryset that should be used for returning objects from this view
	queryset = Poll.objects.all()
	# The serializer class that should be used for validating and deserializing input, and for serializing output
	serializer_class = PollSerializer

class PollDetail(generics.RetrieveDestroyAPIView):
	permission_classes = (IsAuthenticated,)
	queryset = Poll.objects.all()
	serializer_class = PollSerializer

	def destroy(self, request, *args, **kwargs):
		poll = Poll.objects.get(pk=self.kwargs['pk'])
		# request.user is current user is create the request, data form request
		# poll.created_by is author of current poll, data from DB
		if not request.user == poll.created_by:
			raise PermissionDenied("You can not delete this poll")
		return super().destroy(request, *args, **kwargs)

class ChoiseList(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	def get_queryset(self):
		# Because in Choise model, it have pool field with ForeignKey to Pool model
		# So one field is automatically add to Choise model intance, which is 'poll_id'
		# from url pattern pk value will be pass to here and refer by "self.kwargs['pk']"
		# From the urls, we pass on pk to ChoiceList. We override the get_queryset method, to filter on choices with this poll_id, and let DRF handle the rest.
		queryset = Choise.objects.filter( poll_id=self.kwargs['pk'] )
		return queryset

	def post(self, request, *args, **kwargs):
		poll = Poll.objects.get(pk=self.kwargs['pk'])
		if not request.user == poll.created_by:
			raise PermissionDenied('You can not create choice for this poll')
		return super().post(request, *args, **kwargs)

	serializer_class = ChoiseSerializer

# generic class base view is good for general usage, but if you wanna make a complex view, you should use APIView
class CreateVote(APIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = VoteSerializer

	def post(self, request, pk, choise_pk):
		# take voted_by value from POST request
		voted_by = request.data.get('voted_by')
		# from urlpattern we collect pk and choise_pk and pass them to here
		data = {'choise': choise_pk, 'poll': pk, 'voted_by': voted_by}
		serializer = VoteSerializer(data=data)
		if serializer.is_valid():
			vote = serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class UserCreate(generics.CreateAPIView):
	# give exemption to UserCreate view for authentication by overriding the global settings
	authentication_classes = ()
	permission_classes = ()
	serializer_class = UserSerializer

class LoginView(APIView):
	permission_classes = ()

	def post(self, request,):
		# get username and password from request
		username = request.data.get('username')
		password = request.data.get('password')
		# check is user exist in DB
		user = authenticate(username=username, password=password)
		if user:
			return Response({'token': user.auth_token.key})
		else:
			return Response({'error': 'Wrong Credentials'}, status=status.HTTP_400_BAD_REQUEST)