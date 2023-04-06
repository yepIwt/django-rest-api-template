from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers

def welcome(request):
    return HttpResponse("<h1>Welcome's Page!</h1>")


class RegisterView(APIView):
    def post(self, request) -> Response:
        serializer = serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)