from django.urls import path
from .import views

app_name = 'polls'
urlpatterns = [

    path('questions/', views.PollList.as_view()),

    path('comments/', views.CommentList.as_view()),

]