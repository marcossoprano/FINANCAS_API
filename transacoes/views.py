from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Transacao
from .serializers import TransacaoSerializer
from .permissions import IsOwnerTransacao


class TransacaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar transações do usuário autenticado.

    list:
    Retorna todas as transações do usuário autenticado.

    create:
    Cria uma nova transação para o usuário autenticado.

    retrieve:
    Retorna os detalhes de uma transação específica.

    update:
    Atualiza todos os campos de uma transação.

    partial_update:
    Atualiza parcialmente uma transação.

    destroy:
    Exclui uma transação.
    """
    serializer_class = TransacaoSerializer
    permission_classes = [IsAuthenticated, IsOwnerTransacao]

    def get_queryset(self):
        """
        Filtra as transações para retornar apenas as do usuário autenticado.
        Suporta filtro por tipo (receita/despesa) via query param.
        """
        queryset = Transacao.objects.filter(usuario=self.request.user)

        tipo = self.request.query_params.get('tipo')
        if tipo in ('receita', 'despesa'):
            queryset = queryset.filter(tipo=tipo)

        return queryset

    def perform_create(self, serializer):
        """
        Atribui automaticamente o usuário autenticado à transação criada.
        """
        serializer.save(usuario=self.request.user)