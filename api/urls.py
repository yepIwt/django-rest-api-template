from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.welcome, name="swagger"),
    path('register', views.RegisterView.as_view(), name="registration"),
]