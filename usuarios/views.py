from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Usuario
from .serializers import (
    UsuarioRegisterSerializer,
    UsuarioPerfilSerializer,
    UsuarioUpdateSerializer,
    UsuarioChangePasswordSerializer,
    UsuarioLoginSerializer
)


class UsuarioViewSet(viewsets.ViewSet):
    """
    ViewSet para gerenciar operações de usuário.
    """

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='cadastro')
    def cadastro(self, request):
        """
        Endpoint para cadastro de novo usuário.
        POST /api/usuarios/cadastro/
        """
        serializer = UsuarioRegisterSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.save()
            # Gera tokens JWT para o novo usuário
            refresh = RefreshToken.for_user(usuario)
            return Response({
                'message': 'Usuário cadastrado com sucesso',
            'usuario': UsuarioPerfilSerializer(usuario).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny], url_path='login')
    def login(self, request):
        """
        Endpoint para login de usuário.
        POST /api/usuarios/login/
        """
        serializer = UsuarioLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            usuario = authenticate(username=username, password=password)
            if usuario is not None:
                refresh = RefreshToken.for_user(usuario)
                return Response({
                    'message': 'Login realizado com sucesso',
                    'usuario': UsuarioPerfilSerializer(usuario).data,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }, status=status.HTTP_200_OK)
            return Response({
                'error': 'Credenciais inválidas'
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'patch', 'delete'], permission_classes=[IsAuthenticated], url_path='perfil')
    def perfil(self, request):
        """
        Endpoint para consultar, editar e excluir perfil do usuário autenticado.
        GET /api/usuarios/perfil/ - Consultar perfil
        PATCH /api/usuarios/perfil/ - Editar perfil
        DELETE /api/usuarios/perfil/ - Excluir conta
        """
        usuario = request.user

        if request.method == 'GET':
            serializer = UsuarioPerfilSerializer(usuario)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            serializer = UsuarioUpdateSerializer(usuario, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Perfil atualizado com sucesso',
                    'usuario': UsuarioPerfilSerializer(usuario).data
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            usuario.delete()
            return Response({
                'message': 'Conta excluída com sucesso'
            }, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated], url_path='trocar-senha')
    def trocar_senha(self, request):
        """
        Endpoint para alterar a senha do usuário autenticado.
        PATCH /api/usuarios/trocar-senha/
        """
        usuario = request.user
        serializer = UsuarioChangePasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            usuario.set_password(serializer.validated_data['new_password'])
            usuario.save()
            return Response({
                'message': 'Senha alterada com sucesso'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

