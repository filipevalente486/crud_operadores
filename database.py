import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "operadores.db"


def get_conn():
    """Retorna conexão com o SQLite."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    """Cria a tabela se não existir."""
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS operadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                funcionario_nr TEXT,
                data_nascimento DATE,
                ativo INTEGER DEFAULT 1
            )
        """)
        conn.commit()


# ---------- CREATE ----------
def criar_operador(nome, email, funcionario_nr, data_nascimento, ativo=True):
    with get_conn() as conn:
        cur = conn.execute(
            """INSERT INTO operadores (nome, email, funcionario_nr, data_nascimento, ativo)
               VALUES (?, ?, ?, ?, ?)""",
            (nome, email, funcionario_nr, str(data_nascimento), int(ativo))
        )
        conn.commit()
        return cur.lastrowid


# ---------- READ ----------
def listar_operadores():
    with get_conn() as conn:
        return pd.read_sql_query(
            "SELECT * FROM operadores ORDER BY id DESC", conn
        )


def buscar_operador(operador_id):
    with get_conn() as conn:
        df = pd.read_sql_query(
            "SELECT * FROM operadores WHERE id = ?", conn, params=(operador_id,)
        )
        return df.iloc[0] if not df.empty else None


# ---------- UPDATE ----------
def atualizar_operador(operador_id, nome, email, funcionario_nr, data_nascimento, ativo):
    operador_id = int(operador_id)
    with get_conn() as conn:
        cur = conn.execute(
            """UPDATE operadores
               SET nome = ?, email = ?, funcionario_nr = ?, data_nascimento = ?, ativo = ?
               WHERE id = ?""",
            (nome, email, funcionario_nr, str(data_nascimento), int(ativo), operador_id)
        )
        conn.commit()
        return cur.rowcount


# ---------- DELETE ----------
def deletar_operador(operador_id):
    operador_id = int(operador_id)
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM operadores WHERE id = ?", (operador_id,))
        conn.commit()
        return cur.rowcount