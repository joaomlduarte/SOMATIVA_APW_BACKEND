from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CadastroSerializer, LoginSerializer, UsuarioSerializer
from .services import autenticar_por_usuario_ou_email


class CadastroView(generics.CreateAPIView):
    """POST /api/cadastro/ - cria uma nova conta (rota pública)."""

    serializer_class = CadastroSerializer
    authentication_classes = []
    permission_classes = [AllowAny]


class LoginView(APIView):
    """POST /api/login/ - valida usuário/e-mail e senha e devolve o token JWT."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario = autenticar_por_usuario_ou_email(
            serializer.validated_data['usuario'], serializer.validated_data['senha']
        )
        if usuario is None:
            return Response(
                {'detail': 'Usuário/e-mail ou senha inválidos.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(usuario)
        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'usuario': UsuarioSerializer(usuario).data,
            }
        )
