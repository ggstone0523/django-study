from django.urls import path

from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote_view, name="vote"),
    path("make/", views.make_view, name="make"),
    path("delete/", views.delete_view, name="delete"),
    path("modification/", views.modification_view, name="modification"),
]
