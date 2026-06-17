from rest_framework import permissions


class IsOwnerCategoria(permissions.BasePermission):
    """
    Permissão customizada que permite acesso apenas ao usuário
    proprietário da categoria.
    """

    def has_object_permission(self, request, view, obj):
        """
        Verifica se o usuário autenticado é o dono da categoria.
        """
        return obj.usuario == request.user