from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.welcome, name="Swagger"),
    path('register', views.RegisterView.as_view(), name="Registration"),
    path('login', views.LoginView.as_view(), name="Login"),

    path('users/get', views.GetUser.as_view(), name="GetUser")
]