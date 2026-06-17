from rest_framework import permissions


class IsOwnerTransacao(permissions.BasePermission):
    """
    Permissão customizada que permite acesso apenas ao usuário
    proprietário da transação.
    """

    def has_object_permission(self, request, view, obj):
        """
        Verifica se o usuário autenticado é o dono da transação.
        """
        return obj.usuario == request.user