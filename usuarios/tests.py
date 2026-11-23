from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

SENHA_VALIDA = 'Filmes@2026'


class CadastroTests(APITestCase):
    url = '/api/cadastro/'

    def dados_cadastro(self, **alteracoes):
        dados = {
            'username': 'maria',
            'email': 'maria@email.com',
            'senha': SENHA_VALIDA,
            'confirmacao_senha': SENHA_VALIDA,
        }
        dados.update(alteracoes)
        return dados

    def test_cadastra_usuario_com_senha_criptografada(self):
        resposta = self.client.post(self.url, self.dados_cadastro(), format='json')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('senha', resposta.data)
        usuario = User.objects.get(username='maria')
        self.assertNotEqual(usuario.password, SENHA_VALIDA)
        self.assertTrue(usuario.check_password(SENHA_VALIDA))

    def test_recusa_senhas_diferentes(self):
        resposta = self.client.post(
            self.url, self.dados_cadastro(confirmacao_senha='Outra@2026'), format='json'
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirmacao_senha', resposta.data)

    def test_recusa_campos_obrigatorios_vazios(self):
        resposta = self.client.post(self.url, {}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        for campo in ['username', 'email', 'senha', 'confirmacao_senha']:
            self.assertIn(campo, resposta.data)

    def test_recusa_email_ja_cadastrado(self):
        User.objects.create_user('joao', 'maria@email.com', SENHA_VALIDA)

        resposta = self.client.post(self.url, self.dados_cadastro(), format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', resposta.data)

    def test_recusa_senha_fraca(self):
        resposta = self.client.post(
            self.url, self.dados_cadastro(senha='123', confirmacao_senha='123'), format='json'
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('senha', resposta.data)


class LoginTests(APITestCase):
    url = '/api/login/'

    def setUp(self):
        User.objects.create_user('maria', 'maria@email.com', SENHA_VALIDA)

    def test_login_com_nome_de_usuario(self):
        resposta = self.client.post(
            self.url, {'usuario': 'maria', 'senha': SENHA_VALIDA}, format='json'
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertIn('access', resposta.data)
        self.assertEqual(resposta.data['usuario']['username'], 'maria')

    def test_login_com_email(self):
        resposta = self.client.post(
            self.url, {'usuario': 'MARIA@email.com', 'senha': SENHA_VALIDA}, format='json'
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertIn('access', resposta.data)

    def test_recusa_credenciais_invalidas(self):
        resposta = self.client.post(
            self.url, {'usuario': 'maria', 'senha': 'senha-errada'}, format='json'
        )

        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(resposta.data['detail'], 'Usuário/e-mail ou senha inválidos.')

    def test_recusa_campos_vazios(self):
        resposta = self.client.post(self.url, {'usuario': '', 'senha': ''}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
