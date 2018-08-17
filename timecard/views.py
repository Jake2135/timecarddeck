from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, Response

class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/login/'
    template_name = 'timecard/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('pub_date')[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login/'
    model = Question
    template_name = 'timecard/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(LoginRequiredMixin, generic.DetailView):
    login_url = '/login/'
    model = Question
    template_name = 'timecard/results.html'

@login_required(login_url='/login/')
def vote(request, question_id):
    username = request.user.username
    question = get_object_or_404(Question, pk=question_id)
    now = timezone.now()
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        card = Response(time=now,question_id=question_id,user=username)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'timecard/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        card.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('timecard:results', args=(question_id,)))
