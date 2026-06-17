from django.contrib import admin
from .models import Categoria


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Categoria.
    """
    list_display = ['nome', 'tipo', 'usuario', 'criada_em']
    list_filter = ['tipo', 'usuario']
    search_fields = ['nome', 'usuario__username']
    ordering = ['nome']
    readonly_fields = ['criada_em']