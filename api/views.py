from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from . import serializers
import datetime
import jwt
from api.models import User

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


class GetUser(APIView):
    def get(self, request):

        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        if not request.data.get("id"):
            request.data.update({"id": payload['id']})
        
        user = User.objects.filter(id=request.data["id"]).first()
        if not user:
            return Response({})
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)
