# 👷 CRUD de Operadores

Aplicação web simples para gestão de operadores, construída com **Streamlit** e **SQLite**.

## ✨ Funcionalidades

- ➕ **Criar** novos operadores
- 📋 **Listar** todos os operadores registados
- ✏️ **Editar** operadores existentes
- 🗑️ **Excluir** operadores
- ✅ Campo de **ativo/inativo** por operador
- 📅 Data de nascimento formatada (DD/MM/YYYY)

## 🛠️ Tecnologias

- [Python 3.11+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) — interface web
- [Pandas](https://pandas.pydata.org/) — manipulação de dados
- [SQLite](https://www.sqlite.org/) — base de dados local

## 📁 Estrutura do projeto

CRUD/
├── app.py # Interface Streamlit
├── database.py # Camada de acesso ao SQLite
├── requirements.txt # Dependências
├── .gitignore # Ficheiros ignorados pelo Git
└── README.md # Este ficheiro

## 🚀 Como correr localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/filipevalente486/crud-operadores.git
cd crud-operadores