from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Categoria, TipoCategoria

Usuario = get_user_model()


class CategoriaModelTest(TestCase):
    """Testes para o modelo Categoria."""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_criar_categoria(self):
        """Testa criação de categoria com campos obrigatórios."""
        categoria = Categoria.objects.create(
            nome='Alimentação',
            tipo=TipoCategoria.DESPESA,
            usuario=self.usuario
        )
        self.assertEqual(categoria.nome, 'Alimentação')
        self.assertEqual(categoria.tipo, TipoCategoria.DESPESA)
        self.assertEqual(categoria.usuario, self.usuario)
        self.assertIsNotNone(categoria.criada_em)

    def test_str_representation(self):
        """Testa a representação em string da categoria."""
        categoria = Categoria.objects.create(
            nome='Salário',
            tipo=TipoCategoria.RECEITA,
            usuario=self.usuario
        )
        self.assertEqual(str(categoria), 'Salário (Receita)')

    def test_unique_constraint(self):
        """Testa constraint de unicidade (nome + tipo + usuario)."""
        Categoria.objects.create(
            nome='Alimentação',
            tipo=TipoCategoria.DESPESA,
            usuario=self.usuario
        )
        with self.assertRaises(Exception):
            Categoria.objects.create(
                nome='Alimentação',
                tipo=TipoCategoria.DESPESA,
                usuario=self.usuario
            )

    def test_mesmo_nome_tipos_diferentes(self):
        """Testa que mesmo nome com tipos diferentes é permitido."""
        Categoria.objects.create(
            nome='Alimentação',
            tipo=TipoCategoria.DESPESA,
            usuario=self.usuario
        )
        categoria = Categoria.objects.create(
            nome='Alimentação',
            tipo=TipoCategoria.RECEITA,
            usuario=self.usuario
        )
        self.assertEqual(categoria.tipo, TipoCategoria.RECEITA)


class CategoriaAPITest(APITestCase):
    """Testes para a API de Categorias."""

    def setUp(self):
        self.client = APIClient()
        self.usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.outro_usuario = Usuario.objects.create_user(
            username='outrouser',
            email='outro@example.com',
            password='testpass123'
        )

        # Obtém tokens JWT
        response = self.client.post('/api/usuarios/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_criar_categoria_autenticado(self):
        """Testa criação de categoria por usuário autenticado."""
        response = self.client.post('/api/categorias/', {
            'nome': 'Alimentação',
            'tipo': 'despesa'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nome'], 'Alimentação')
        self.assertEqual(response.data['tipo'], 'despesa')
        self.assertEqual(response.data['usuario'], self.usuario.id)

    def test_criar_categoria_sem_autenticacao(self):
        """Testa que usuário não autenticado não pode criar categoria."""
        self.client.credentials()  # Remove autenticação
        response = self.client.post('/api/categorias/', {
            'nome': 'Alimentação',
            'tipo': 'despesa'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listar_apenas_proprias_categorias(self):
        """Testa que cada usuário vê apenas suas próprias categorias."""
        # Cria categorias para o usuário principal
        Categoria.objects.create(
            nome='Alimentação', tipo=TipoCategoria.DESPESA, usuario=self.usuario
        )
        Categoria.objects.create(
            nome='Salário', tipo=TipoCategoria.RECEITA, usuario=self.usuario
        )
        # Cria categoria para outro usuário
        Categoria.objects.create(
            nome='Investimento', tipo=TipoCategoria.RECEITA, usuario=self.outro_usuario
        )

        response = self.client.get('/api/categorias/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Apenas 2 do usuário atual

    def test_categoria_duplicada_mesmo_usuario(self):
        """Testa rejeição de categoria duplicada para o mesmo usuário."""
        self.client.post('/api/categorias/', {
            'nome': 'Alimentação',
            'tipo': 'despesa'
        })
        response = self.client.post('/api/categorias/', {
            'nome': 'Alimentação',
            'tipo': 'despesa'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_categoria_mesmo_nome_tipo_diferente(self):
        """Testa que mesmo nome com tipo diferente é permitido."""
        self.client.post('/api/categorias/', {
            'nome': 'Alimentação',
            'tipo': 'despesa'
        })
        response = self.client.post('/api/categorias/', {
            'nome': 'Alimentação',
            'tipo': 'receita'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_atualizar_categoria(self):
        """Testa atualização de categoria."""
        response = self.client.post('/api/categorias/', {
            'nome': 'Alimentação',
            'tipo': 'despesa'
        })
        categoria_id = response.data['id']

        response = self.client.patch(f'/api/categorias/{categoria_id}/', {
            'nome': 'Alimentação Saudável'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], 'Alimentação Saudável')

    def test_excluir_categoria(self):
        """Testa exclusão de categoria."""
        response = self.client.post('/api/categorias/', {
            'nome': 'Alimentação',
            'tipo': 'despesa'
        })
        categoria_id = response.data['id']

        response = self.client.delete(f'/api/categorias/{categoria_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_nao_pode_manipular_categoria_de_outro_usuario(self):
        """Testa que usuário não pode acessar categoria de outro usuário."""
        categoria_outro = Categoria.objects.create(
            nome='Investimento',
            tipo=TipoCategoria.RECEITA,
            usuario=self.outro_usuario
        )

        response = self.client.get(f'/api/categorias/{categoria_outro.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_criar_categoria_sem_tipo_usar_default(self):
        """Testa que o tipo padrão é 'despesa' quando não informado."""
        response = self.client.post('/api/categorias/', {
            'nome': 'Padrão'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['tipo'], 'despesa')