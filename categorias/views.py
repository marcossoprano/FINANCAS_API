from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Categoria
from .serializers import CategoriaSerializer
from .permissions import IsOwnerCategoria


class CategoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar categorias do usuário autenticado.

    list:
    Retorna todas as categorias do usuário autenticado.

    create:
    Cria uma nova categoria para o usuário autenticado.

    retrieve:
    Retorna os detalhes de uma categoria específica.

    update:
    Atualiza todos os campos de uma categoria.

    partial_update:
    Atualiza parcialmente uma categoria.

    destroy:
    Exclui uma categoria.
    """
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated, IsOwnerCategoria]

    def get_queryset(self):
        """
        Filtra as categorias para retornar apenas as do usuário autenticado.
        """
        return Categoria.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        """
        Atribui automaticamente o usuário autenticado à categoria criada.
        """
        serializer.save(usuario=self.request.user)