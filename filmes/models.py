from django.conf import settings
from django.db import models


class Filme(models.Model):
    titulo = models.CharField(max_length=200, unique=True)
    sinopse = models.TextField()
    genero = models.CharField(max_length=50)
    ano_lancamento = models.PositiveIntegerField()
    imagem = models.FileField(upload_to='posters/')

    class Meta:
        ordering = ['titulo']

    def __str__(self):
        return self.titulo


class Favorito(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoritos'
    )
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='favoritado_por')
    data_favoritado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_favoritado']
        constraints = [
            # Regra de negócio: o mesmo usuário não pode favoritar o mesmo filme duas vezes
            models.UniqueConstraint(fields=['usuario', 'filme'], name='favorito_unico_por_usuario'),
        ]

    def __str__(self):
        return f'{self.usuario} - {self.filme}'
