from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("make/", views.make_view, name="make"),
    path("delete/", views.delete_view, name="delete"),
    path("modification/", views.modification_view, name="modification"),
]
