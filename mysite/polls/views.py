from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, UserChoice


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    login_url = "/accounts/login/"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    login_url = "/accounts/login/"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(LoginRequiredMixin, generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    login_url = "/accounts/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["userchoice"] = UserChoice.objects.filter(
            choice__question=context["question"]
        ).filter(user=self.request.user)
        if len(context["userchoice"]) == 1:
            context["userchoice"] = context["userchoice"][0].choice
        return context


@login_required(login_url="/accounts/login/")
def vote_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        user_before_userchoices = UserChoice.objects.filter(
            choice__question=question
        ).filter(user=request.user)
        if len(user_before_userchoices) == 1:
            user_before_userchoices[0].choice.votes -= 1
            user_before_userchoices[0].choice.save()
            user_before_userchoices.delete()
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        UserChoice.objects.create(user=request.user, choice=selected_choice)
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
