import sqlite3
from datetime import datetime

def menu_principal(mensagem, opcoes_validas):
    while True:
        opcao = input(mensagem).strip()
        if opcao in opcoes_validas:
            return opcao
        print("Opcao invalida, tente novamente.\n")

def validar_inteiro(mensagem):
    while True:
        valor = input(mensagem).strip()
        try:
            return int(valor)
        except ValueError:
            print("Digite um numero inteiro.\n")

def ler_float(mensagem):
    while True:
        valor = input(mensagem).strip()
        try:
            return float(valor)
        except ValueError:
            print("Digite um numero valido. Exemplo: 10 ou 10.50\n")

conn = sqlite3.connect("sistema_vendas.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tb_Produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco REAL NOT NULL,
        estoque INTEGER NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tb_Vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        valor_total REAL NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tb_ItensVenda (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER NOT NULL,
        produto_id INTEGER NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unitario REAL NOT NULL,
        FOREIGN KEY (venda_id) REFERENCES tb_Vendas(id),
        FOREIGN KEY (produto_id) REFERENCES tb_Produtos(id)
    )
""")

conn.commit()

def cadastrar_produto():
    print("\nCadastro de Produto")
    nome = input("Nome do produto: ")
    preco = ler_float("Preco do produto: ")
    estoque = validar_inteiro("Quantidade em estoque: ")

    cursor.execute("""
        INSERT INTO tb_Produtos (nome, preco, estoque)
        VALUES (?, ?, ?)
    """, (nome, preco, estoque))

    conn.commit()
    print("Produto cadastrado com sucesso.\n")

def lista_de_produtos():
    print("\nLista de Produtos\n")

    cursor.execute("SELECT id, nome, preco, estoque FROM tb_Produtos")
    produtos = cursor.fetchall()

    if not produtos:
        print("Nenhum produto cadastrado.\n")
        return

    print(f"{'ID':<5}{'Nome':<25}{'Preco':<10}{'Estoque':<10}")
    for p in produtos:
        print(f"{p[0]:<5}{p[1]:<25}{p[2]:<10.2f}{p[3]:<10}")

    print("")

def registrar_venda():
    print("\nRegistrar Venda\n")

    lista_de_produtos()

    itens = []
    valor_total = 0.0

    while True:
        id_raw = input("Digite o ID do produto (0 para finalizar): ").strip()

        if id_raw == "0":
            break

        if not id_raw.isdigit():
            print("Digite apenas numeros.\n")
            continue

        id_produto = int(id_raw)
        quantidade = validar_inteiro("Quantidade: ")

        cursor.execute("""
            SELECT nome, preco, estoque
            FROM tb_Produtos
            WHERE id = ?
        """, (id_produto,))
        produto = cursor.fetchone()

        if produto is None:
            print("Produto nao encontrado.\n")
            continue

        nome, preco, estoque_atual = produto

        if quantidade > estoque_atual:
            print(f"Estoque insuficiente. Estoque atual: {estoque_atual}\n")
            continue

        subtotal = preco * quantidade
        valor_total += subtotal

        itens.append((id_produto, quantidade, preco))

        print(f"Item adicionado: {nome} | Qtd: {quantidade} | Subtotal: {subtotal:.2f}")
        print(f"Total parcial: {valor_total:.2f}\n")

    if not itens:
        print("Venda cancelada.\n")
        return

    data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO tb_Vendas (data, valor_total)
        VALUES (?, ?)
    """, (data_venda, valor_total))

    id_venda = cursor.lastrowid

    for produto_id, quantidade, preco_unitario in itens:
        cursor.execute("""
            INSERT INTO tb_ItensVenda (venda_id, produto_id, quantidade, preco_unitario)
            VALUES (?, ?, ?, ?)
        """, (id_venda, produto_id, quantidade, preco_unitario))

        cursor.execute("""
            UPDATE tb_Produtos
            SET estoque = estoque - ?
            WHERE id = ?
        """, (quantidade, produto_id))

    conn.commit()

    print("\nResumo da Venda")
    print(f"ID da Venda: {id_venda}")
    print(f"Data: {data_venda}")
    print(f"Valor total: {valor_total:.2f}\n")

def lista_de_vendas():
    print("\nLista de Vendas\n")

    cursor.execute("SELECT id, data, valor_total FROM tb_Vendas")
    vendas = cursor.fetchall()

    if not vendas:
        print("Nenhuma venda registrada.\n")
        return

    for v in vendas:
        print(f"ID: {v[0]} | Data: {v[1]} | Total: {v[2]:.2f}")

        cursor.execute("""
            SELECT P.nome, I.quantidade, I.preco_unitario
            FROM tb_ItensVenda I
            JOIN tb_Produtos P ON I.produto_id = P.id
            WHERE venda_id = ?
        """, (v[0],))
        itens = cursor.fetchall()

        for item in itens:
            nome, qtd, preco_unit = item
            subtotal = qtd * preco_unit
            print(f"   Produto: {nome} | Quantidade: {qtd} | Preco: {preco_unit:.2f} | Subtotal: {subtotal:.2f}")

        print("")

def menu():
    while True:
        print("Sistema de Controle de Vendas")
        print("1 - Cadastrar produto")
        print("2 - Lista de produtos")
        print("3 - Registrar venda")
        print("4 - Lista de vendas")
        print("0 - Sair")

        opcao = menu_principal("Escolha: ", ["0", "1", "2", "3", "4"])

        if opcao == "1":
            cadastrar_produto()
        elif opcao == "2":
            lista_de_produtos()
        elif opcao == "3":
            registrar_venda()
        elif opcao == "4":
            lista_de_vendas()
        elif opcao == "0":
            print("Saindo do sistema.")
            break

        input("\nPressione ENTER para continuar...\n")

    conn.close()

menu()
