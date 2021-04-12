from django.urls import path
from .views import polls_list, polls_detail

urlpatterns = [
	# user access to specific url =>  link to corresponding view

    path('polls/', polls_list, name='polls_list'),
    path('polls/<int:pk>/', polls_detail, name='polls_detail')
]