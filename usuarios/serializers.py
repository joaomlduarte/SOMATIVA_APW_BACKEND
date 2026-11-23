from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers


class UsuarioSerializer(serializers.ModelSerializer):
    """Dados públicos do usuário devolvidos ao frontend (sem senha)."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CadastroSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)
    confirmacao_senha = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'senha', 'confirmacao_senha']
        extra_kwargs = {'email': {'required': True, 'allow_blank': False}}

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('Já existe uma conta com este e-mail.')
        return email.lower()

    def validate(self, dados):
        if dados['senha'] != dados['confirmacao_senha']:
            raise serializers.ValidationError({'confirmacao_senha': 'As senhas não conferem.'})

        usuario_temporario = User(username=dados['username'], email=dados['email'])
        try:
            validate_password(dados['senha'], user=usuario_temporario)
        except DjangoValidationError as erro:
            raise serializers.ValidationError({'senha': list(erro.messages)})
        return dados

    def create(self, dados):
        # create_user grava a senha criptografada (hash), nunca em texto puro
        return User.objects.create_user(
            username=dados['username'],
            email=dados['email'],
            password=dados['senha'],
        )


class LoginSerializer(serializers.Serializer):
    """Campo 'usuario' aceita o nome de usuário OU o e-mail."""

    usuario = serializers.CharField()
    senha = serializers.CharField(write_only=True)
