from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Usuario


class UsuarioRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para cadastro de novos usuários.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, data):
        """Valida se as senhas coincidem."""
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'As senhas não coincidem.'})
        return data

    def create(self, validated_data):
        """Cria e retorna um novo usuário."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        usuario = Usuario.objects.create_user(**validated_data, password=password)
        return usuario


class UsuarioPerfillSerializer(serializers.ModelSerializer):
    """
    Serializer para consultar o perfil do usuário.
    """
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'criado_em', 'atualizado_em')
        read_only_fields = ('id', 'criado_em', 'atualizado_em')


class UsuarioUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualizar o perfil do usuário.
    """
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email')

    def validate_email(self, value):
        """Valida unicidade do email."""
        user = self.instance
        if Usuario.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError('Este email já está em uso.')
        return value


class UsuarioChangePasswordSerializer(serializers.Serializer):
    """
    Serializer para alteração de senha.
    """
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate_old_password(self, value):
        """Valida se a senha antiga está correta."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('A senha atual está incorreta.')
        return value

    def validate(self, data):
        """Valida se as novas senhas coincidem."""
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({'new_password': 'As senhas não coincidem.'})
        return data


class UsuarioLoginSerializer(serializers.Serializer):
    """
    Serializer para login (apenas validação de credenciais).
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
