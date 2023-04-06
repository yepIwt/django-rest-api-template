from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from . import serializers
import datetime
import jwt


def welcome(request):
    return HttpResponse("<h1>Welcome's Page!</h1>")


class RegisterView(APIView):
    def post(self, request) -> Response:
        serializer = serializers.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    
    permission_classes = (permissions.AllowAny,)

    def post(self, request) -> Response:
        serializer = serializers.LoginSerializer(
            data=self.request.data,
            context={'request': self.request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        payload = {
			"id": user.id,
			"exp": datetime.datetime.utcnow() + datetime.timedelta(days=60),
			"iat": datetime.datetime.utcnow()
		}
        
        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()
        response.set_cookie(key="jwt", value=token, httponly=True)
        response.data = {
			"jwt": token
		}
        
        return response
