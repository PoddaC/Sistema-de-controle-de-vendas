# Sistema de Controle de Vendas

Sistema de gerenciamento de vendas via terminal, desenvolvido em Python com banco de dados SQLite. O projeto nasceu como exercício prático para consolidar conceitos de modelagem relacional, manipulação de banco de dados e estruturação de código em Python.

## Funcionalidades

- Cadastro de produtos com nome, preço e estoque
- Registro de vendas com múltiplos itens por transação
- Controle automático de estoque a cada venda realizada
- Validação de entradas do usuário para evitar erros de execução
- Histórico completo de vendas com detalhamento por item

## Tecnologias

- Python 3
- SQLite3 (embutido no Python, sem instalação adicional)
- Módulo `datetime` (embutido no Python)

## Estrutura do banco de dados

Três tabelas relacionadas entre si:

- `tb_Produtos` — produtos cadastrados no sistema
- `tb_Vendas` — cabeçalho de cada venda (data e valor total)
- `tb_ItensVenda` — itens vinculados a cada venda, com chaves estrangeiras para as duas tabelas acima

## Como rodar

O projeto não tem dependências externas. Basta ter o Python 3 instalado.

```bash
git clone https://github.com/PoddaC/Sistema-de-controle-de-vendas.git
cd Sistema-de-controle-de-vendas
python sistema_vendas.py
```

O banco de dados é criado automaticamente na primeira execução.

## Autor

Pedro Lucca Ciuffo Podda — estudante de Ciência de Dados no Instituto Infnet  
[LinkedIn](https://www.linkedin.com/in/pedro-podda-ba9257298/) | [GitHub](https://github.com/PoddaC)
