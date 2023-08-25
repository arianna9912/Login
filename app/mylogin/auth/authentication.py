from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from mylogin.auth.serializer import UserSerializer


class Login(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(username=username, password=password)

        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = UserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh_token': login_serializer.validated_data.get('refresh'),
                    'user': user_serializer.data,
                    'message': 'Inicio de Sesión Exitoso'
                }, status=status.HTTP_200_OK
                )

        user = User.objects.filter(username=username).first()
        if not user: return Response({'error': 'Nombre de usuario incorrecto'}, status=status.HTTP_403_FORBIDDEN)
        if user and not user.is_active: return Response({'error': 'El usuario está inactivo'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'error': 'Contraseña o nombre de usuario incorrecto'}, status=status.HTTP_403_FORBIDDEN)

