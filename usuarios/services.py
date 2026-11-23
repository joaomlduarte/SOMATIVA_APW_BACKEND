from django.contrib.auth import authenticate
from django.contrib.auth.models import User


def autenticar_por_usuario_ou_email(login, senha):
    """Autentica pelo nome de usuário ou pelo e-mail. Devolve o User ou None."""
    login = login.strip()
    username = login

    if '@' in login:
        conta = User.objects.filter(email__iexact=login).first()
        if conta is None:
            return None
        username = conta.username

    return authenticate(username=username, password=senha)
