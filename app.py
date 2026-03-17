import re
from datetime import datetime

import streamlit as st

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Calis Academia",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# ESTILO VISUAL - CALIS (PRETO E LARANJA)
# =========================================================
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0f0f0f;
            color: #ffffff;
        }

        .main-title {
            font-size: 2.4rem;
            font-weight: 800;
            color: #ff7a00;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1rem;
            color: #d1d1d1;
            margin-bottom: 2rem;
        }

        .card {
            background: linear-gradient(145deg, #171717, #111111);
            border: 1px solid #2d2d2d;
            border-left: 6px solid #ff7a00;
            border-radius: 18px;
            padding: 1.2rem;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
            min-height: 180px;
        }

        .card-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #ff7a00;
            margin-bottom: 0.4rem;
        }

        .card-text {
            color: #e5e5e5;
            font-size: 0.95rem;
            line-height: 1.5;
        }

        .section-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #ff7a00;
            margin-top: 0.5rem;
            margin-bottom: 1rem;
        }

        .small-label {
            color: #c9c9c9;
            font-size: 0.9rem;
        }

        div[data-testid="stForm"] {
            background-color: #151515;
            border: 1px solid #2b2b2b;
            border-radius: 16px;
            padding: 1rem;
        }

        div[data-testid="stMetric"] {
            background-color: #151515;
            border: 1px solid #2b2b2b;
            border-radius: 14px;
            padding: 0.7rem;
        }

        .stButton > button,
        .stDownloadButton > button {
            background-color: #ff7a00;
            color: white;
            border: none;
            border-radius: 10px;
            font-weight: 700;
            padding: 0.55rem 1rem;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background-color: #e56f00;
            color: white;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# ESTADO INICIAL
# =========================================================
if "registered_teachers" not in st.session_state:
    # E-mails autorizados a acessar o sistema
    st.session_state.registered_teachers = ["admin@calis.com"]

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "logged_user" not in st.session_state:
    st.session_state.logged_user = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

if "students" not in st.session_state:
    # Estrutura temporária em memória.
    # Depois será substituída por leitura/escrita no Databricks.
    st.session_state.students = []


# =========================================================
# FUNÇÕES UTILITÁRIAS
# =========================================================
def is_valid_email(email: str) -> bool:
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(pattern, email.strip()))


def login(email: str) -> bool:
    email = email.strip().lower()
    return email in [teacher.lower() for teacher in st.session_state.registered_teachers]


def logout() -> None:
    st.session_state.authenticated = False
    st.session_state.logged_user = None
    st.session_state.current_page = "home"


# =========================================================
# PLACEHOLDERS PARA DATABRICKS
# =========================================================
# Depois você poderá trocar estas funções pela integração real
# com Databricks SQL, Delta Tables ou outro método de persistência.
def save_teacher_to_databricks(email: str) -> None:
    """
    Placeholder.
    Futuramente, salvar o e-mail do professor em uma tabela no Databricks.
    Exemplo de tabela: calis.professores_autorizados
    """
    pass


# Futuramente, buscar professores autorizados no Databricks.
def load_teachers_from_databricks():
    return st.session_state.registered_teachers


# Futuramente, salvar o aluno em tabela Databricks.
def save_student_to_databricks(student_data: dict) -> None:
    """
    Placeholder.
    Exemplo de tabela: calis.alunos
    """
    pass


# Futuramente, carregar alunos salvos no Databricks.
def load_students_from_databricks():
    return st.session_state.students


# =========================================================
# COMPONENTES DE TELA
# =========================================================
def render_logo_header():
    st.markdown('<div class="main-title">CALIS ACADEMIA</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Sistema interno de gestão para professores</div>',
        unsafe_allow_html=True,
    )


# =========================================================
# TELA DE LOGIN
# =========================================================
def show_login_screen():
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        render_logo_header()

        st.markdown('<div class="section-title">Login de Professores</div>', unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            login_email = st.text_input("E-mail", placeholder="professor@calis.com")
            login_submit = st.form_submit_button("Entrar")

        if login_submit:
            if not login_email.strip():
                st.error("Informe o e-mail para acessar.")
            elif login(login_email):
                st.session_state.authenticated = True
                st.session_state.logged_user = login_email.strip().lower()
                st.success("Login realizado com sucesso.")
                st.rerun()
            else:
                st.error("E-mail não autorizado para acessar o sistema.")

        st.markdown("---")
        st.markdown('<div class="section-title">Cadastrar professores autorizados</div>', unsafe_allow_html=True)
        st.caption("Apenas e-mails cadastrados poderão entrar no app.")

        with st.form("register_teacher_form", clear_on_submit=True):
            new_teacher_email = st.text_input(
                "Novo e-mail de professor",
                placeholder="novo.professor@calis.com",
            )
            register_submit = st.form_submit_button("Cadastrar e-mail")

        if register_submit:
            email = new_teacher_email.strip().lower()

            if not email:
                st.warning("Digite um e-mail para cadastrar.")
            elif not is_valid_email(email):
                st.warning("Digite um e-mail válido.")
            elif email in [item.lower() for item in st.session_state.registered_teachers]:
                st.info("Esse e-mail já está cadastrado.")
            else:
                st.session_state.registered_teachers.append(email)
                save_teacher_to_databricks(email)
                st.success(f"Professor autorizado com sucesso: {email}")

        st.markdown("---")
        st.write("**E-mails autorizados atualmente:**")
        for teacher_email in load_teachers_from_databricks():
            st.write(f"- {teacher_email}")


# =========================================================
# HOME APÓS LOGIN
# =========================================================
def home_page():
    render_logo_header()

    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        st.caption(f"Professor logado: {st.session_state.logged_user}")
    with top_col2:
        if st.button("Sair"):
            logout()
            st.rerun()

    st.markdown('<div class="section-title">Painel Principal</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Ficha de Alunos</div>
                <div class="card-text">
                    Cadastre alunos, acompanhe informações físicas e registre objetivos e observações.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Acessar Ficha de Alunos", use_container_width=True):
            st.session_state.current_page = "students"
            st.rerun()

    with col2:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Calis Academia</div>
                <div class="card-text">
                    Espaço institucional da academia. Aqui você poderá centralizar avisos, indicadores e informações gerais.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Acessar Calis Academia", use_container_width=True):
            st.session_state.current_page = "academy"
            st.rerun()

    with col3:
        st.markdown(
            """
            <div class="card">
                <div class="card-title">Agenda</div>
                <div class="card-text">
                    Área reservada para compromissos, horários, aulas e organização das atividades dos professores.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Acessar Agenda", use_container_width=True):
            st.session_state.current_page = "agenda"
            st.rerun()


# =========================================================
# PÁGINA - FICHA DE ALUNOS
# =========================================================
def students_page():
    render_logo_header()

    nav1, nav2 = st.columns([5, 1])
    with nav1:
        st.markdown('<div class="section-title">Ficha de Alunos</div>', unsafe_allow_html=True)
    with nav2:
        if st.button("Voltar"):
            st.session_state.current_page = "home"
            st.rerun()

    students_data = load_students_from_databricks()

    col_metric1, col_metric2 = st.columns(2)
    with col_metric1:
        st.metric("Total de alunos cadastrados", len(students_data))
    with col_metric2:
        st.metric("Última atualização", datetime.now().strftime("%d/%m/%Y %H:%M"))

    st.markdown("### Cadastrar novo aluno")

    with st.form("student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome do aluno")
            idade = st.number_input("Idade", min_value=1, max_value=120, step=1)
            peso = st.number_input("Peso (kg)", min_value=0.0, format="%.2f")

        with col2:
            altura = st.number_input("Altura (m)", min_value=0.0, format="%.2f")
            objetivo = st.selectbox(
                "Objetivo",
                [
                    "Emagrecimento",
                    "Hipertrofia",
                    "Condicionamento físico",
                    "Ganho de força",
                    "Reabilitação",
                    "Qualidade de vida",
                    "Outro",
                ],
            )
            observacoes = st.text_area("Observações", placeholder="Ex.: restrições, lesões, rotina, preferências...")

        submitted = st.form_submit_button("Salvar aluno")

    if submitted:
        if not nome.strip():
            st.warning("Informe o nome do aluno.")
        else:
            student_data = {
                "nome": nome.strip(),
                "idade": int(idade),
                "peso": float(peso),
                "altura": float(altura),
                "objetivo": objetivo,
                "observacoes": observacoes.strip(),
                "professor_responsavel": st.session_state.logged_user,
                "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            st.session_state.students.append(student_data)
            save_student_to_databricks(student_data)
            st.success(f"Aluno {nome.strip()} cadastrado com sucesso.")
            st.rerun()

    st.markdown("---")
    st.markdown("### Alunos cadastrados")

    if students_data:
        st.dataframe(students_data, use_container_width=True)
    else:
        st.info("Nenhum aluno cadastrado até o momento.")


# =========================================================
# PÁGINA - CALIS ACADEMIA
# =========================================================
def academy_page():
    render_logo_header()

    nav1, nav2 = st.columns([5, 1])
    with nav1:
        st.markdown('<div class="section-title">Calis Academia</div>', unsafe_allow_html=True)
    with nav2:
        if st.button("Voltar"):
            st.session_state.current_page = "home"
            st.rerun()

    st.info("Esta área foi criada como placeholder. Na próxima etapa podemos adicionar avisos, indicadores, planos ou dados institucionais.")


# =========================================================
# PÁGINA - AGENDA
# =========================================================
def agenda_page():
    render_logo_header()

    nav1, nav2 = st.columns([5, 1])
    with nav1:
        st.markdown('<div class="section-title">Agenda</div>', unsafe_allow_html=True)
    with nav2:
        if st.button("Voltar"):
            st.session_state.current_page = "home"
            st.rerun()

    st.info("Esta área foi criada como placeholder. Na próxima etapa podemos adicionar agenda de aulas, horários, lembretes e compromissos.")


# =========================================================
# CONTROLE DE ROTEAMENTO
# =========================================================
def main():
    if not st.session_state.authenticated:
        show_login_screen()
        return

    page = st.session_state.current_page

    if page == "home":
        home_page()
    elif page == "students":
        students_page()
    elif page == "academy":
        academy_page()
    elif page == "agenda":
        agenda_page()
    else:
        home_page()


if __name__ == "__main__":
    main()
