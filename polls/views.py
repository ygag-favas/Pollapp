from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F
from django.db.models import Sum
from .models import Choice, Question, Comment
from .forms import CommentForm
from django.contrib.auth import get_user_model

User = get_user_model()


class IndexView(generic.ListView):
    template_name = 'polls/index.html'

    def get(self, request):
        """Returns latest question list by given order"""
        p = Question.objects.order_by('order_no')[:5]
        """Returns most popular poll by number of votes"""
        q = Question.objects.annotate(num_votes=Sum('choice__votes')).filter(
            num_votes__isnull=False).order_by('-num_votes')[0]
        return render(request, 'polls/index.html', {'p': p, 'q': q})


class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/account/login/'
    redirect_field_name = 'polls:index'
    model = Question
    template_name = 'polls/detail.html'

    def get(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        if question.is_expired:
            """if question expired show results"""
            return HttpResponseRedirect(reverse('polls:results',
                                                args=(question.id,)))
        else:
            self.update_view_count(request, question_id)
            comments = Comment.objects.filter(question=question_id)
            cf = CommentForm()
            return render(request, 'polls/detail.html', {'question': question,
                                                         'comments': comments,
                                                         'cf': cf, })

    def post(self, request, question_id):
        return self.add_comment(request, question_id)

    def update_view_count(self, request, question_id):
        Question.objects.filter(pk=question_id).update(views=F('views') + 1)

    def add_comment(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        if request.method == 'POST':
            cf = CommentForm(request.POST)
            if cf.is_valid():
                email = request.POST.get('email')
                content = request.POST.get('content')
                comment = Comment.objects.create(question=question, email=email
                                                 , content=content)
                comment.save()

                return HttpResponseRedirect(reverse('polls:detail',
                                                    args=(question_id,)))
            else:
                return render(request, 'polls/detail.html',
                              {'question': question, 'cf': cf})


class ResultsView(LoginRequiredMixin, generic.DetailView):
    login_url = '/account/login/'
    redirect_field_name = 'polls:index'
    model = Question
    template_name = 'polls/results.html'


class VoteView(generic.ListView):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice']
                                                      )
        except (KeyError, Choice.DoesNotExist):

            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()

            return HttpResponseRedirect(reverse('polls:results',
                                                args=(question_id,)))

