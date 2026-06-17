from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'criado_em')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'criado_em')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Metadados', {'fields': ('criado_em', 'atualizado_em')}),
    )
    readonly_fields = ('criado_em', 'atualizado_em')
