import streamlit as st
import pandas as pd
from datetime import date
from database import (
    init_db, criar_operador, listar_operadores,
    buscar_operador, atualizar_operador, deletar_operador
)

# -------- Configuração --------
st.set_page_config(page_title="CRUD Operadores", layout="wide")
init_db()

st.title("👷 Base dados Operadores")


# -------- Controle de estado --------
if "modo" not in st.session_state:
    st.session_state.modo = "listar"

if "operador_edicao" not in st.session_state:
    st.session_state.operador_edicao = None


# -------- Sidebar --------
with st.sidebar:
    st.header("Ações")
    if st.button("📋 Listar", use_container_width=True):
        st.session_state.modo = "listar"
        st.rerun()

    if st.button("➕ Novo operador", use_container_width=True):
        st.session_state.modo = "criar"
        st.rerun()


# =========================================================
# READ — listar
# =========================================================
if st.session_state.modo == "listar":
    st.subheader("📋 Operadores registados na base dados")

    df = listar_operadores()

    if df.empty:
        st.info("Nenhum operador cadastrado ainda.")
    else:
        df_exibir = df.copy()
        df_exibir["ativo"] = df_exibir["ativo"].map({1: "✅", 0: "❌"})

        st.dataframe(
            df_exibir,
            column_config={
                "id": st.column_config.NumberColumn(
                    "ID", width=50, format="%d"
                ),
                "nome": st.column_config.TextColumn(
                    "Nome", width=150
                ),
                "email": st.column_config.TextColumn(
                    "E-mail", width=250
                ),
                "funcionario_nr": st.column_config.TextColumn(
                    "Funcionário Nº", width=120
                ),
                "data_nascimento": st.column_config.DateColumn(
                    "Nascimento", format="DD/MM/YYYY", width=120
                ),
                "ativo": st.column_config.TextColumn(
                    "Ativo", width=60
                ),
            },
            hide_index=True,
            use_container_width=False
        )

        st.divider()
        st.subheader("⚙️ Ações por operador")

        ids = df["id"].tolist()
        nomes = dict(zip(df["id"], df["nome"]))

        operador_id = st.selectbox(
            "Selecione um operador",
            options=ids,
            format_func=lambda x: f"#{x} — {nomes[x]}",
            key="sel_operador"
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("✏️ Editar", use_container_width=True):
                st.session_state.modo = "editar"
                st.session_state.operador_edicao = operador_id
                st.rerun()

        with col2:
            if st.button("🗑️ Excluir", type="primary", use_container_width=True):
                linhas = deletar_operador(operador_id)
                if linhas > 0:
                    st.success(f"Operador {operador_id} excluído!")
                else:
                    st.error("Nenhum operador excluído.")
                st.session_state.pop("sel_operador", None)
                st.rerun()


# =========================================================
# CREATE — novo operador
# =========================================================
elif st.session_state.modo == "criar":
    st.subheader("➕ Novo operador")

    with st.form("form_criar", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome *")
            funcionario_nr = st.text_input("Funcionário Nº")

        with col2:
            email = st.text_input("E-mail *")
            data_nasc = st.date_input(
                "Data de nascimento",
                value=date(1990, 1, 1),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                format="DD/MM/YYYY"
            )

        ativo = st.checkbox("Operador ativo", value=True)

        col_a, col_b = st.columns([1, 5])
        with col_a:
            salvar = st.form_submit_button("💾 Salvar", use_container_width=True)
        with col_b:
            cancelar = st.form_submit_button("❌ Cancelar")

        if salvar:
            if not nome or not email or not funcionario_nr:
                st.error("Nome,numero e e-mail são obrigatórios.")
            else:
                novo_id = criar_operador(
                    nome, email, funcionario_nr, data_nasc, ativo
                )
                st.success(f"Operador #{novo_id} criado com sucesso!")
                st.session_state.modo = "listar"
                st.rerun()

        if cancelar:
            st.session_state.modo = "listar"
            st.rerun()


# =========================================================
# UPDATE — editar operador
# =========================================================
elif st.session_state.modo == "editar":
    operador = buscar_operador(st.session_state.operador_edicao)

    if operador is None:
        st.error("Operador não encontrado.")
        st.session_state.modo = "listar"
        st.session_state.operador_edicao = None
        st.rerun()

    st.subheader(f"✏️ Editando o {operador['id']}º operador da base,  {operador['nome']} com o nr {operador['funcionario_nr']} ")

    data_nasc_db = pd.to_datetime(operador["data_nascimento"]).date()

    with st.form("form_editar"):
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome *", value=operador["nome"], key="edit_nome")
            funcionario_nr = st.text_input(
                "Funcionário Nº",
                value=operador["funcionario_nr"] or "",
                key="edit_func"
            )

        with col2:
            email = st.text_input("E-mail *", value=operador["email"], key="edit_email")
            data_nasc = st.date_input(
                "Data de nascimento",
                value=data_nasc_db,
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                format="DD/MM/YYYY",
                key="edit_data"
            )

        ativo = st.checkbox(
            "Operador ativo", value=bool(operador["ativo"]), key="edit_ativo"
        )

        col_a, col_b = st.columns([1, 5])
        with col_a:
            salvar = st.form_submit_button("💾 Salvar", use_container_width=True)
        with col_b:
            cancelar = st.form_submit_button("❌ Cancelar")

        if salvar:
            if not nome or not email:
                st.error("Nome e e-mail são obrigatórios.")
            else:
                linhas = atualizar_operador(
                    int(operador["id"]), nome, email,
                    funcionario_nr, data_nasc, ativo
                )

                if linhas == 0:
                    st.error("Nenhuma linha atualizada. Verifique o ID.")
                else:
                    st.success("Operador atualizado com sucesso!")

                    st.session_state.modo = "listar"
                    st.session_state.operador_edicao = None
                    for k in ["edit_nome", "edit_func", "edit_email",
                              "edit_data", "edit_ativo"]:
                        st.session_state.pop(k, None)
                    st.session_state.pop("sel_operador", None)

                    st.rerun()

        if cancelar:
            st.session_state.modo = "listar"
            st.session_state.operador_edicao = None
            st.rerun()