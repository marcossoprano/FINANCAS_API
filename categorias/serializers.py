from rest_framework import serializers
from .models import Categoria, TipoCategoria


class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Categoria.
    """
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Categoria
        fields = [
            'id', 'nome', 'tipo', 'usuario', 'usuario_nome', 'criada_em'
        ]
        read_only_fields = ['id', 'usuario', 'usuario_nome', 'criada_em']

    def validate_nome(self, value):
        """Normaliza o nome: remove espaços extras e capitaliza."""
        nome_limpo = value.strip().title()
        if len(nome_limpo) < 2:
            raise serializers.ValidationError(
                'O nome da categoria deve ter pelo menos 2 caracteres.'
            )
        return nome_limpo

    def validate(self, data):
        """
        Verifica duplicidade manualmente (como camada extra de segurança
        além da constraint do banco) para fornecer mensagem clara ao usuário.
        """
        request = self.context.get('request')
        if request and request.user:
            usuario = request.user
            nome = data.get('nome')
            tipo = data.get('tipo')

            # Verifica se já existe categoria com mesmo nome, tipo e usuário
            queryset = Categoria.objects.filter(
                nome=nome,
                tipo=tipo,
                usuario=usuario
            )

            # Se for atualização, exclui a própria instância da verificação
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)

            if queryset.exists():
                raise serializers.ValidationError(
                    f'Você já possui uma categoria "{nome}" do tipo "{tipo}".'
                )

        return data