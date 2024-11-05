from datetime import datetime
from typing import List

# Classe para representar uma categoria de produtos
class Categoria:
    def __init__(self, nome: str):
        self.nome = nome  # Atributo para armazenar o nome da categoria

# Classe para representar um produto
class Produto:
    def __init__(self, nome: str, categoria: Categoria, preco: float, quantidade: int, localizacao: str):
        self.nome = nome  # Nome do produto
        self.categoria = categoria  # Categoria à qual o produto pertence
        self.preco = preco  # Preço do produto
        self.quantidade = quantidade  # Quantidade disponível em estoque
        self.localizacao = localizacao  # Localização do produto no estoque

# Classe para registrar movimentações (entradas e saídas) de produtos
class Movimentacao:
    def __init__(self, produto: Produto, quantidade: int, tipo: str):
        self.produto = produto  # Produto relacionado à movimentação
        self.quantidade = quantidade  # Quantidade movimentada
        self.tipo = tipo  # Tipo da movimentação: 'entrada' ou 'saida'
        self.data = datetime.now()  # Data e hora da movimentação

# Classe para gerenciar o sistema de estoque
class SistemaEstoque:
    def __init__(self):
        self.produtos = []  # Lista para armazenar produtos
        self.categorias = []  # Lista para armazenar categorias
        self.movimentacoes = []  # Lista para armazenar movimentações

    # Método para cadastrar uma nova categoria
    def cadastrar_categoria(self, nome: str) -> Categoria:
        categoria = Categoria(nome)  # Cria uma nova instância de Categoria
        self.categorias.append(categoria)  # Adiciona a categoria à lista de categorias
        return categoria  # Retorna a categoria cadastrada

    # Método para cadastrar um novo produto
    def cadastrar_produto(self, nome: str, categoria: Categoria, preco: float, quantidade: int, localizacao: str) -> Produto:
        produto = Produto(nome, categoria, preco, quantidade, localizacao)  # Cria uma nova instância de Produto
        self.produtos.append(produto)  # Adiciona o produto à lista de produtos
        return produto  # Retorna o produto cadastrado

    # Método para consultar produtos pelo nome
    def consultar_produto(self, nome: str) -> List[Produto]:
        # Retorna uma lista de produtos que correspondem ao nome consultado (case insensitive)
        return [produto for produto in self.produtos if produto.nome.lower() == nome.lower()]

    # Método para registrar a entrada de um produto
    def registrar_entrada(self, nome_produto: str, quantidade: int):
        produto = self.buscar_produto_por_nome(nome_produto)  # Busca o produto pelo nome
        if produto:  # Se o produto for encontrado
            produto.quantidade += quantidade  # Atualiza a quantidade do produto
            movimentacao = Movimentacao(produto, quantidade, 'entrada')  # Cria uma movimentação de entrada
            self.movimentacoes.append(movimentacao)  # Adiciona a movimentação à lista
            print(f"Entrada registrada: {quantidade} unidades de {produto.nome}")  # Mensagem de sucesso
        else:
            print("Produto não encontrado.")  # Mensagem de erro

    # Método para registrar a saída de um produto
    def registrar_saida(self, nome_produto: str, quantidade: int):
        produto = self.buscar_produto_por_nome(nome_produto)  # Busca o produto pelo nome
        if produto:  # Se o produto for encontrado
            if produto.quantidade >= quantidade:  # Verifica se há quantidade suficiente
                produto.quantidade -= quantidade  # Atualiza a quantidade do produto
                movimentacao = Movimentacao(produto, quantidade, 'saida')  # Cria uma movimentação de saída
                self.movimentacoes.append(movimentacao)  # Adiciona a movimentação à lista
                print(f"Saída registrada: {quantidade} unidades de {produto.nome}")  # Mensagem de sucesso
            else:
                print("Quantidade em estoque insuficiente.")  # Mensagem de erro
        else:
            print("Produto não encontrado.")  # Mensagem de erro

    # Método para buscar um produto pelo nome
    def buscar_produto_por_nome(self, nome: str) -> Produto:
        for produto in self.produtos:  # Percorre a lista de produtos
            if produto.nome.lower() == nome.lower():  # Compara nomes (case insensitive)
                return produto  # Retorna o produto encontrado
        return None  # Retorna None se não encontrar o produto

    # Método para gerar um relatório de estoque
    def gerar_relatorio_estoque(self):
        print("Relatório de Estoque:")  # Cabeçalho do relatório
        for produto in self.produtos:  # Percorre a lista de produtos
            # Imprime o nome, quantidade e localização do produto
            print(f"{produto.nome} - Quantidade em estoque: {produto.quantidade} - Localização: {produto.localizacao}")

    # Método para gerar um relatório de movimentações
    def gerar_relatorio_movimentacoes(self):
        print("Relatório de Movimentações:")  # Cabeçalho do relatório
        for mov in self.movimentacoes:  # Percorre a lista de movimentações
            # Imprime o tipo, quantidade e nome do produto, juntamente com a data da movimentação
            print(f"{mov.tipo.capitalize()} de {mov.quantidade} unidades do produto {mov.produto.nome} em {mov.data.strftime('%Y-%m-%d %H:%M:%S')}")

# Inicializando o sistema de estoque
sistema_estoque = SistemaEstoque()

# Cadastrando categorias e produtos iniciais
categoria_eletronicos = sistema_estoque.cadastrar_categoria("Eletrônicos")  # Cadastra a categoria "Eletrônicos"
# Cadastra produtos iniciais na categoria "Eletrônicos"
sistema_estoque.cadastrar_produto("TV LED", categoria_eletronicos, 1500.00, 10, "A1")
sistema_estoque.cadastrar_produto("Smartphone", categoria_eletronicos, 2000.00, 15, "B3")

# Função para cadastrar novos produtos pelo usuário
def cadastrar_produto_usuario():
    # Solicita informações do novo produto ao usuário
    nome = input("Digite o nome do produto: ")
    categoria_nome = input("Digite o nome da categoria: ")
    preco = float(input("Digite o preço do produto: "))
    quantidade = int(input("Digite a quantidade do produto: "))
    localizacao = input("Digite a localização do produto: ")

    # Verifica se a categoria já existe, caso contrário, cria uma nova
    categoria = next((cat for cat in sistema_estoque.categorias if cat.nome.lower() == categoria_nome.lower()), None)
    if not categoria:  # Se a categoria não existir
        categoria = sistema_estoque.cadastrar_categoria(categoria_nome)  # Cria nova categoria

    # Cadastra o novo produto
    produto = sistema_estoque.cadastrar_produto(nome, categoria, preco, quantidade, localizacao)
    print(f"Produto cadastrado: {produto.nome} - Categoria: {categoria.nome}")  # Mensagem de confirmação

# Função para consulta de produtos pelo usuário
def consultar_produto_usuario():
    nome_produto = input("Digite o nome do produto que deseja consultar: ")  # Solicita o nome do produto
    consulta = sistema_estoque.consultar_produto(nome_produto)  # Realiza a consulta
    if consulta:  # Se o produto for encontrado
        print(f"Produto encontrado: {consulta[0].nome} - Quantidade: {consulta[0].quantidade}")  # Exibe informações do produto
    else:
        print("Produto não encontrado.")  # Mensagem de erro

# Função para registrar movimentações de estoque
def movimentar_estoque_usuario():
    # Solicita informações para a movimentação do estoque
    nome_produto = input("Digite o nome do produto para movimentação: ")
    tipo_movimento = input("Digite 'entrada' para entrada de estoque ou 'saída' para saída de estoque: ").strip().lower()
    quantidade = int(input("Digite a quantidade para movimentação: "))

    # Registra a entrada ou saída conforme a escolha do usuário
    if tipo_movimento == 'entrada':
        sistema_estoque.registrar_entrada(nome_produto, quantidade)  # Registra a entrada
        print(f"Entrada de {quantidade} unidades de {nome_produto} registrada com sucesso.")  # Mensagem de confirmação
    elif tipo_movimento == 'saída':
        sistema_estoque.registrar_saida(nome_produto, quantidade)  # Registra a saída
        print(f"Saída de {quantidade} unidades de {nome_produto} registrada com sucesso.")  # Mensagem de confirmação
    else:
        print("Tipo de movimentação inválido.")  # Mensagem de erro

# Função para geração de relatórios pelo usuário
def gerar_relatorio_usuario():
    tipo_relatorio = input("Digite 'estoque' para relatório de estoque ou 'movimentações' para relatório de movimentações: ").strip().lower()
    if tipo_relatorio == 'estoque':
        sistema_estoque.gerar_relatorio_estoque()  # Gera o relatório de estoque
    elif tipo_relatorio == 'movimentações':
        sistema_estoque.gerar_relatorio_movimentacoes()  # Gera o relatório de movimentações
    else:
        print("Tipo de relatório inválido.")  # Mensagem de erro

# Menu para interação com o usuário
while True:
    print("\nEscolha uma opção:")  # Exibe opções do menu
    print("1 - Cadastrar produto")
    print("2 - Consultar produto")
    print("3 - Movimentar estoque")
    print("4 - Gerar relatório")
    print("0 - Sair")
    
    opcao = input("Digite o número da opção desejada: ").strip()  # Solicita a opção do usuário
    
    if opcao == "1":
        cadastrar_produto_usuario()  # Chama a função para cadastrar produto
    elif opcao == "2":
        consultar_produto_usuario()  # Chama a função para consultar produto
    elif opcao == "3":
        movimentar_estoque_usuario()  # Chama a função para movimentar estoque
    elif opcao == "4":
        gerar_relatorio_usuario()  # Chama a função para gerar relatórios
    elif opcao == "0":
        print("Saindo do sistema.")  # Mensagem de saída
        break  # Encerra o loop
    else:
        print("Opção inválida. Tente novamente.")  # Mensagem de erro
