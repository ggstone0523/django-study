from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from polls.models import UserChoice
from django.contrib.auth.decorators import login_required
from accounts.tasks import send_mail_view


def login_view(request):
    try:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("polls:index"))

        context = {
            "is_login_failed": False,
            "next": "/polls/",
        }

        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                redirect = request.POST["next"]
                return HttpResponseRedirect(redirect)
            else:
                context["is_login_failed"] = True

        if request.method == "GET":
            context["next"] = request.GET.get("next", "/polls/")

        return render(request, "accounts/login.html", context)
    except:
        return render(request, "accounts/error.html")


@login_required(login_url="/accounts/login/")
def logout_view(request):
    try:
        logout(request)
        return HttpResponseRedirect(reverse("accounts:login"))
    except:
        return render(request, "accounts/error.html")


def make_view(request):
    try:
        context = {}
        if request.method == "POST":
            try:
                User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password"],
                    email=request.POST["email"],
                )
                send_mail_view.delay(
                    request.POST["email"], "Thanks you for make account!"
                )
                return HttpResponseRedirect(reverse("accounts:login"))
            except (IntegrityError):
                context["alert"] = 1

        return render(request, "accounts/make.html", context)
    except:
        return render(request, "accounts/error.html")


@login_required(login_url="/accounts/login/")
def delete_view(request):
    try:
        user_selected_choices = UserChoice.objects.filter(user=request.user)
        for user_selected_choice in user_selected_choices:
            user_selected_choice.choice.votes -= 1
            user_selected_choice.choice.save()
        email = request.user.email
        request.user.delete()
        send_mail_view.delay(email, "Your account is delete!")
        return HttpResponseRedirect(reverse("accounts:login"))
    except:
        return render(request, "accounts/error.html")


@login_required(login_url="/accounts/login/")
def modification_view(request):
    try:
        if request.method == "POST":
            request.user.username = request.POST.get("username", request.user.username)
            if "password" in request.POST:
                request.user.set_password(request.POST["password"])
            request.user.email = request.POST.get("email", request.user.email)
            request.user.save()
            login(request, request.user)
            return HttpResponseRedirect(reverse("accounts:modification"))

        return render(
            request,
            "accounts/modification.html",
            {
                "username": request.user.username,
                "email": request.user.email,
            },
        )
    except:
        return render(request, "accounts/error.html")
