from django.db import models
from django.conf import settings


class TipoCategoria(models.TextChoices):
    """Enum para tipos de categoria."""
    RECEITA = 'receita', 'Receita'
    DESPESA = 'despesa', 'Despesa'


class Categoria(models.Model):
    """
    Modelo de Categoria para organizar transações financeiras.

    Cada categoria pertence a um único usuário e possui um tipo
    (receita ou despesa) para classificação das transações.
    """
    nome = models.CharField('Nome', max_length=100)
    tipo = models.CharField(
        'Tipo',
        max_length=10,
        choices=TipoCategoria.choices,
        default=TipoCategoria.DESPESA,
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='categorias',
        verbose_name='Usuário',
    )
    criada_em = models.DateTimeField('Criada em', auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']
        constraints = [
            models.UniqueConstraint(
                fields=['nome', 'tipo', 'usuario'],
                name='unique_categoria_por_usuario_e_tipo'
            )
        ]

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"