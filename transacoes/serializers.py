from rest_framework import serializers
from .models import Transacao, TipoTransacao


class TransacaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Transacao.
    """
    usuario_nome = serializers.CharField(
        source='usuario.username', read_only=True
    )
    categoria_nome = serializers.CharField(
        source='categoria.nome', read_only=True
    )

    class Meta:
        model = Transacao
        fields = [
            'id', 'valor', 'tipo', 'descricao', 'data',
            'categoria', 'categoria_nome',
            'usuario', 'usuario_nome',
            'criada_em', 'atualizada_em',
        ]
        read_only_fields = [
            'id', 'usuario', 'usuario_nome',
            'categoria_nome', 'criada_em', 'atualizada_em',
        ]

    def validate_valor(self, value):
        """Garante que o valor seja positivo."""
        if value <= 0:
            raise serializers.ValidationError(
                'O valor da transação deve ser positivo.'
            )
        return value

    def validate(self, data):
        """
        Validações adicionais:
        - Se uma categoria for informada, verifica se pertence ao usuário.
        """
        request = self.context.get('request')
        if request and request.user:
            categoria = data.get('categoria')
            if categoria and categoria.usuario != request.user:
                raise serializers.ValidationError(
                    'A categoria informada não pertence ao usuário autenticado.'
                )
        return data