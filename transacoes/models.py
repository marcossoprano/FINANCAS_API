from django.db import models
from django.conf import settings


class TipoTransacao(models.TextChoices):
    """Enum para tipos de transação."""
    RECEITA = 'receita', 'Receita'
    DESPESA = 'despesa', 'Despesa'


class Transacao(models.Model):
    """
    Modelo de Transação Financeira.

    Cada transação pertence a um usuário e pode ser opcionalmente
    associada a uma categoria para organização.
    """
    valor = models.DecimalField('Valor', max_digits=15, decimal_places=2)
    tipo = models.CharField(
        'Tipo',
        max_length=10,
        choices=TipoTransacao.choices,
    )
    descricao = models.TextField('Descrição', blank=True)
    data = models.DateField('Data')
    categoria = models.ForeignKey(
        'categorias.Categoria',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='transacoes',
        verbose_name='Categoria',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transacoes',
        verbose_name='Usuário',
    )
    criada_em = models.DateTimeField('Criada em', auto_now_add=True)
    atualizada_em = models.DateTimeField('Atualizada em', auto_now=True)

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-data', '-criada_em']

    def __str__(self):
        return f"{self.get_tipo_display()} - R$ {self.valor} ({self.data})"