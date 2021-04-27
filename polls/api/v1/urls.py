from django.urls import path
from .import views

app_name = 'polls'
urlpatterns = [

    path('questions/', views.PollList.as_view()),

]