from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'polls'
urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),

    path('polls/<int:question_id>/', views.DetailView.as_view(),
         name='detail'),

    path('polls/<int:pk>/results/', views.ResultsView.as_view(),
         name='results'),

    path('polls/<int:question_id>/vote/', views.VoteView.as_view(),
         name='vote'),

    path('polls/api/', include('polls.api.urls')),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
