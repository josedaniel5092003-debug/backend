from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet, SalidaViewSet
from . import views
from .views import ResultadosView

# Router para los ViewSets (usuarios y salidas)
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'salidas', SalidaViewSet)

# URLs finales de la app
urlpatterns = [
    path('', include(router.urls)),  # /api/usuarios/ y /api/salidas/
    path('meses-votados/', views.meses_votados),  # /api/meses-votados/
    path('resultados/', ResultadosView.as_view()),
    path('api/limpiar-todo/', views.limpiar_todo, name='limpiar_todo'),
]
