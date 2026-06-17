from django.contrib import admin
from .models import Transacao


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Transacao.
    """
    list_display = ('id', 'descricao', 'valor', 'tipo', 'data', 'usuario', 'categoria')
    list_filter = ('tipo', 'data', 'usuario')
    search_fields = ('descricao',)
    ordering = ('-data',)