from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import Choice, Question, UserChoice, UserQuestion


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


@login_required(login_url="/accounts/login/")
def make_view(request):
    if request.method == "POST":
        question = Question.objects.create(
            question_text=request.POST["question_text"], pub_date=timezone.now()
        )
        Choice(question=question, choice_text=request.POST["choice_text1"]).save()
        Choice(question=question, choice_text=request.POST["choice_text2"]).save()
        Choice(question=question, choice_text=request.POST["choice_text3"]).save()
        UserQuestion(user=request.user, question=question).save()
        return HttpResponseRedirect(reverse("polls:index"))
    return render(request, "polls/make.html")


@login_required(login_url="/accounts/login/")
def delete_view(request):
    question = Question.objects.get(id=request.POST["delete_want_question"])
    userquestion = UserQuestion.objects.get(question=question)
    if userquestion.user == request.user:
        question.delete()
    return HttpResponseRedirect(reverse("polls:index"))
