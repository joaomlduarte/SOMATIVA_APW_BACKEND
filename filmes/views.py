from rest_framework import mixins, viewsets

from .models import Favorito, Filme
from .serializers import FavoritoSerializer, FilmeSerializer


class FilmeViewSet(viewsets.ReadOnlyModelViewSet):
    """GET /api/filmes/ e GET /api/filmes/{id}/ (exigem login)."""

    queryset = Filme.objects.all()
    serializer_class = FilmeSerializer


class FavoritoViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """GET/POST /api/favoritos/ e DELETE /api/favoritos/{id}/ (exigem login).

    O usuário vem sempre do token JWT (request.user), nunca do corpo da requisição.
    """

    serializer_class = FavoritoSerializer

    def get_queryset(self):
        # Cada usuário só enxerga (e só remove) os próprios favoritos
        return Favorito.objects.filter(usuario=self.request.user).select_related('filme')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
