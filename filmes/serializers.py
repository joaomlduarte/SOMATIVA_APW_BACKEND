from rest_framework import serializers

from .models import Favorito, Filme


class FilmeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filme
        fields = ['id', 'titulo', 'sinopse', 'genero', 'ano_lancamento', 'imagem']


class FavoritoSerializer(serializers.ModelSerializer):
    # Leitura: o filme completo. Escrita: só o id do filme em "filme_id".
    filme = FilmeSerializer(read_only=True)
    filme_id = serializers.PrimaryKeyRelatedField(
        source='filme', queryset=Filme.objects.all(), write_only=True
    )

    class Meta:
        model = Favorito
        fields = ['id', 'filme', 'filme_id', 'data_favoritado']

    def validate_filme_id(self, filme):
        usuario = self.context['request'].user
        if Favorito.objects.filter(usuario=usuario, filme=filme).exists():
            raise serializers.ValidationError('Este filme já está nos seus favoritos.')
        return filme
