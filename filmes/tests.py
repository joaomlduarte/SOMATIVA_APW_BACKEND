from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Favorito, Filme


class FilmesTests(APITestCase):
    def setUp(self):
        self.usuario = User.objects.create_user('maria', 'maria@email.com', 'Filmes@2026')

    def test_catalogo_tem_no_minimo_10_filmes(self):
        self.assertGreaterEqual(Filme.objects.count(), 10)

    def test_catalogo_exige_login(self):
        resposta = self.client.get('/api/filmes/')

        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lista_filmes_com_todos_os_campos(self):
        self.client.force_authenticate(self.usuario)

        resposta = self.client.get('/api/filmes/')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), Filme.objects.count())
        for campo in ['id', 'titulo', 'sinopse', 'genero', 'ano_lancamento', 'imagem']:
            self.assertIn(campo, resposta.data[0])

    def test_consulta_um_filme(self):
        self.client.force_authenticate(self.usuario)
        filme = Filme.objects.first()

        resposta = self.client.get(f'/api/filmes/{filme.id}/')

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta.data['titulo'], filme.titulo)


class FavoritosTests(APITestCase):
    url = '/api/favoritos/'

    def setUp(self):
        self.maria = User.objects.create_user('maria', 'maria@email.com', 'Filmes@2026')
        self.joao = User.objects.create_user('joao', 'joao@email.com', 'Filmes@2026')
        self.filme = Filme.objects.first()
        self.client.force_authenticate(self.maria)

    def test_favoritos_exigem_login(self):
        self.client.force_authenticate(None)

        self.assertEqual(self.client.get(self.url).status_code, status.HTTP_401_UNAUTHORIZED)
        resposta = self.client.post(self.url, {'filme_id': self.filme.id}, format='json')
        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_adiciona_favorito_para_o_usuario_logado(self):
        resposta = self.client.post(self.url, {'filme_id': self.filme.id}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resposta.data['filme']['titulo'], self.filme.titulo)
        self.assertTrue(Favorito.objects.filter(usuario=self.maria, filme=self.filme).exists())

    def test_ignora_usuario_enviado_pelo_frontend(self):
        self.client.post(
            self.url, {'filme_id': self.filme.id, 'usuario': self.joao.id}, format='json'
        )

        self.assertTrue(Favorito.objects.filter(usuario=self.maria).exists())
        self.assertFalse(Favorito.objects.filter(usuario=self.joao).exists())

    def test_nao_permite_favoritar_o_mesmo_filme_duas_vezes(self):
        self.client.post(self.url, {'filme_id': self.filme.id}, format='json')

        resposta = self.client.post(self.url, {'filme_id': self.filme.id}, format='json')

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Favorito.objects.filter(usuario=self.maria).count(), 1)

    def test_lista_apenas_os_favoritos_do_proprio_usuario(self):
        outro_filme = Filme.objects.last()
        Favorito.objects.create(usuario=self.maria, filme=self.filme)
        Favorito.objects.create(usuario=self.joao, filme=outro_filme)

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)
        self.assertEqual(resposta.data[0]['filme']['id'], self.filme.id)

    def test_remove_favorito(self):
        favorito = Favorito.objects.create(usuario=self.maria, filme=self.filme)

        resposta = self.client.delete(f'{self.url}{favorito.id}/')

        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Favorito.objects.filter(id=favorito.id).exists())

    def test_nao_remove_favorito_de_outro_usuario(self):
        favorito_do_joao = Favorito.objects.create(usuario=self.joao, filme=self.filme)

        resposta = self.client.delete(f'{self.url}{favorito_do_joao.id}/')

        self.assertEqual(resposta.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Favorito.objects.filter(id=favorito_do_joao.id).exists())
