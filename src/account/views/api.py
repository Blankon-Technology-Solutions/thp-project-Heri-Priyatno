from django.contrib import messages
from django.contrib.auth import login, logout
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import User
from account.serializers import UserSerializer, LoginSerializer, RegisterSerializer


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            messages.warning(request, "Invalid username, password")
            return Response({
                "error": "invalid username password"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = serializer.validated_data
            login(request, user)
            # messages.success(request, "Log in success")
            # _, token = AuthToken.objects.create(user)
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                # "token":token
            })


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = User.objects.filter(email=request.data['email'])
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # _, token = AuthToken.objects.create(user)
        # login(request, user)  # if you readily want to login the user after register
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            # "token":token
        })


@api_view(["POST"])
def logout_api(request):
    logout(request)
    return Response({
        "logout": "success"
    })

