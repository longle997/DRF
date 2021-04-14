from django.urls import path
from .views import polls_list, polls_detail
from .apiviews import PollList, PollDetail, ChoiseList, CreateVote, UserCreate, LoginView
from rest_framework.authtoken import views

urlpatterns = [
	# user access to specific url =>  link to corresponding view

    # path('polls/', polls_list, name='polls_list'),
    # path('polls/<int:pk>/', polls_detail, name='polls_detail')

    path('polls/', PollList.as_view(), name='polls_list'),
    path('polls/<int:pk>/', PollDetail.as_view(), name='polls_detail'),
    # path("choises/", ChoiseList.as_view(), name="choice_list"),
    # path("vote/", CreateVote.as_view(), name="create_vote"),
    path('polls/<int:pk>/choises/', ChoiseList.as_view(), name='choice_list'),
    path("polls/<int:pk>/choises/<int:choise_pk>/vote/", CreateVote.as_view(), name="create_vote"),
    path('users/', UserCreate.as_view(), name='user_create'),
    path('login/', LoginView.as_view(), name='login'),
]