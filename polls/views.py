from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Poll
from .serializers import PollSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
def polls_list(request):
	# when we access any engpoint, default request.method is 'GET'
	if request.method == 'GET':
		MAX_OBJECTS = 20
		polls = Poll.objects.all()[:MAX_OBJECTS]
		data = {'result': list(polls.values('question', 'created_by__username', 'pub_date'))}
		return JsonResponse(data)

'''
pass json format data to html file
def polls_list(request):
	MAX_OBJECTS = 20
	polls = Poll.objects.all()[:MAX_OBJECTS]
	# convert from query type to JSON format
	data = PollSerializer(polls, many=True).data
	context = {
		'data': data
	}
	return render(request, 'polls/polls_list.html', context)
'''

def polls_detail(request, pk):
	poll = get_object_or_404(Poll, pk=pk)
	# poll.created_by only return query object with value <User: longle>
	# poll.created_by.username will return a string with value 'longle'
	data = {'result': {
			'question': poll.question,
			'created_by': poll.created_by.username,
			'pub_date': poll.pub_date
		}
	}
	return JsonResponse(data)