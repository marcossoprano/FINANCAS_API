from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransacaoViewSet

router = DefaultRouter()
router.register(r'', TransacaoViewSet, basename='transacao')

urlpatterns = [
    path('', include(router.urls)),
]