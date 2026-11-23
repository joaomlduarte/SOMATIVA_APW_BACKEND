from rest_framework.routers import DefaultRouter

from .views import FavoritoViewSet, FilmeViewSet

router = DefaultRouter()
router.register('filmes', FilmeViewSet, basename='filme')
router.register('favoritos', FavoritoViewSet, basename='favorito')

urlpatterns = router.urls
