import streamlit as st
import pandas as pd
from datetime import datetime
import hashlib
import os
import json
from PIL import Image

# Configuração da página
st.set_page_config(
    page_title="Calculadora de Leilão para Investidores",
    page_icon="🏠",
    layout="wide"
)

# Função para gerar hash de senha
def make_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Função para verificar hash
def check_hash(password, hashed_text):
    if make_hash(password) == hashed_text:
        return True
    return False

# Função para salvar credenciais
def save_credentials(username, password):
    credentials = {}
    credentials_path = "credentials.json"
    
    # Verifica se o arquivo já existe
    if os.path.exists(credentials_path):
        with open(credentials_path, "r") as file:
            credentials = json.load(file)
    
    # Adiciona novo usuário ou atualiza senha
    credentials[username] = make_hash(password)
    
    # Salva o arquivo
    with open(credentials_path, "w") as file:
        json.dump(credentials, file)

# Função para carregar credenciais
def load_credentials():
    credentials = {}
    credentials_path = "credentials.json"
    
    if os.path.exists(credentials_path):
        with open(credentials_path, "r") as file:
            credentials = json.load(file)
    
    return credentials

# Inicializa usuário administrador se não existir
def init_admin():
    credentials = load_credentials()
    if not credentials.get("admin"):
        save_credentials("admin", "bastos2024")

# Inicializa usuário admin
init_admin()

# CSS customizado - Cores do site bastosmoraesadvocacia.com.br
st.markdown("""
<style>
    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    h1 {
        color: #D4AF37; /* Cor dourada para títulos */
        text-align: center;
        margin-bottom: 30px;
    }
    h2, h3, h4 {
        color: #D4AF37; /* Cor dourada para subtítulos */
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        padding: 10px 20px;
        border-radius: 4px 4px 0 0;
    }
    .stTabs [aria-selected="true"] {
        background-color: #800000; /* Vermelho escuro do site */
        color: #D4AF37; /* Dourado */
    }
    .result-highlight {
        font-weight: bold;
        color: #D4AF37;
        padding: 10px;
        border-radius: 5px;
        background-color: #800000;
    }
    .positive {
        color: #D4AF37; /* Dourado para valores positivos */
    }
    .negative {
        color: #e74c3c; /* Vermelho para valores negativos */
    }
    .info-block {
        background-color: rgba(128, 0, 0, 0.05); /* Vermelho escuro com transparência */
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
        border: 1px solid rgba(212, 175, 55, 0.3); /* Borda dourada */
    }
    .stExpander {
        border: 1px solid #800000;
        border-radius: 5px;
    }
    .stButton>button {
        background-color: #800000;
        color: #D4AF37;
    }
    .stButton>button:hover {
        background-color: #6B0000;
        color: #D4AF37;
    }
    .main .block-container {
        max-width: 1200px;
        padding: 2rem;
    }
    /* Cores para selectbox e radio buttons */
    .stRadio > div {
        padding: 10px;
        border-radius: 5px;
    }
    .stRadio label {
        color: #800000;
    }
    .stCheckbox label {
        color: #800000;
    }
    footer {
        visibility: hidden;
    }
    
    /* Configuração para facilitar a navegação com Enter */
    input {
        user-select: all;
    }
    input:focus {
        user-select: all;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar variável de sessão para autenticação
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Função para login
def login():
    credentials = load_credentials()
    username = st.session_state.login_username
    password = st.session_state.login_password
    
    if username in credentials:
        if check_hash(password, credentials[username]):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success(f"Login bem-sucedido! Bem-vindo, {username}!")
        else:
            st.error("Senha incorreta!")
    else:
        st.error("Usuário não encontrado!")

# Interface de login se não estiver autenticado
if not st.session_state.authenticated:
    # Logo do escritório
    try:
        logo = Image.open("logo.jpg")
        st.image(logo, width=200)
    except Exception as e:
        st.error(f"Não foi possível carregar o logo: {e}")
    
    # Título
    st.title("Calculadora de Leilão para Investidores")
    
    st.markdown("<div class='info-block'>", unsafe_allow_html=True)
    st.header("Acesso Restrito")
    
    # Formulário de Login
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.text_input("Usuário", key="login_username")
        st.text_input("Senha", type="password", key="login_password")
        st.button("Entrar", on_click=login)
    
    with col2:
        st.markdown("""
        <div style='background-color: rgba(128, 0, 0, 0.05); padding: 20px; border-radius: 10px; height: 100%;'>
            <h3 style='color: #D4AF37;'>Bastos Moraes Advocacia</h3>
            <p>Esta calculadora é exclusiva para clientes e parceiros do escritório.</p>
            <p>Para obter acesso, entre em contato conosco.</p>
            <a href='https://api.whatsapp.com/message/XVSEPLILBK6LB1?autoload=1&app_absent=0' target='_blank' style='color: #800000;'>
                <button style='background-color: #800000; color: #D4AF37; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;'>
                    📱 Entre em contato pelo WhatsApp
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Rodapé
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #D4AF37;'>Bastos Moraes Advocacia | Todos os direitos reservados Copyright © 2023-2025</p>", unsafe_allow_html=True)
    
    st.stop()  # Para a execução aqui se não estiver autenticado

# Se chegou aqui, é porque está autenticado
# Logo do escritório
try:
    logo = Image.open("logo.jpg")
    st.image(logo, width=200)
except Exception as e:
    st.error(f"Não foi possível carregar o logo: {e}")

# Título
st.title("Calculadora de Leilão para Investidores")

# Botão de logout
if st.session_state.authenticated:
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()
    
    with col1:
        st.markdown(f"<p style='text-align: right; color: #800000;'>Usuário conectado: <b>{st.session_state.username}</b></p>", unsafe_allow_html=True)

# Criação de abas
tab1, tab2 = st.tabs(["Calculadora", "Como utilizar"])

with tab1:
    # Formulário de cálculo
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='info-block'>", unsafe_allow_html=True)
        st.subheader("Dados do Imóvel")
        
        # Formato de data brasileiro (dd/mm/aaaa)
        data_compra = st.date_input("Data de Compra", datetime.now(), format="DD/MM/YYYY")
        valor_arrematacao = st.number_input("Valor de Arrematação (R$)", min_value=0.0, step=1000.0, format="%.2f")
        valor_venda = st.number_input("Valor de Venda (R$)", min_value=0.0, step=1000.0, format="%.2f")
        
        st.subheader("Forma de Pagamento")
        forma_pagamento = st.radio("Selecione a forma de pagamento:", ["À Vista", "Financiado"])
        
        if forma_pagamento == "À Vista":
            percentual_vista = 100.0
            percentual_financiado = 0.0
            valor_vista = valor_arrematacao
            valor_financiado = 0.0
            valor_parcela = 0.0
        else:
            percentual_vista = st.slider("Percentual de Entrada", 0.0, 100.0, 30.0, 1.0, format="%.1f")
            percentual_financiado = 100.0 - percentual_vista
            valor_vista = valor_arrematacao * (percentual_vista / 100)
            valor_financiado = valor_arrematacao * (percentual_financiado / 100)
            valor_parcela = st.number_input("Valor da Parcela (R$)", min_value=0.0, step=100.0, format="%.2f")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='info-block'>", unsafe_allow_html=True)
        st.subheader("Custos e Despesas")
        
        comissao_leiloeiro = st.number_input("Comissão do Leiloeiro (%)", min_value=0, max_value=100, value=5, step=1) / 100
        itbi = st.number_input("ITBI (%)", min_value=0.0, max_value=100.0, value=3.0, step=0.1) / 100
        registro = st.number_input("Registro (R$)", min_value=0.0, value=2500.0, step=100.0)
        escritura = st.number_input("Escritura (R$)", min_value=0.0, value=1500.0, step=100.0)
        
        # Opções de honorários advocatícios
        tipo_honorarios = st.radio("Honorários Advocatícios:", ["Escolher Pacote de Serviços", "Informar Valor Percentual", "Informar Valor Fixo"])
        
        # Inicializar variáveis
        honorarios = 0.0
        base_honorarios = "arrematacao"
        
        # Verificar se o cliente é PRIME IMÓVEIS e valor está abaixo de 150.000
        is_prime_client = st.checkbox("Cliente PRIME IMÓVEIS")
        
        if tipo_honorarios == "Escolher Pacote de Serviços":
            # Definir as opções de pacote com base no valor de arrematação e se é cliente PRIME
            pacote_options = [
                "Connoisseur | 3,5% da arrematação",
                "Veritas | 5% da arrematação",
                "AvantGarde | 7% da arrematação",
                "Pinnacle | 10% da arrematação"
            ]
            
            # Adicionar Strategic Prime apenas se for cliente PRIME e valor < 150.000
            if is_prime_client and valor_arrematacao <= 150000:
                pacote_options.append("Strategic Prime | 10% sobre o lucro líquido")
                
            pacote_honorarios = st.selectbox(
                "Selecione o Pacote:",
                pacote_options
            )
            
            if "Connoisseur" in pacote_honorarios:
                honorarios = 0.035
                base_honorarios = "arrematacao"
            elif "Veritas" in pacote_honorarios:
                honorarios = 0.05
                base_honorarios = "arrematacao"
            elif "AvantGarde" in pacote_honorarios:
                honorarios = 0.07
                base_honorarios = "arrematacao"
            elif "Pinnacle" in pacote_honorarios:
                honorarios = 0.10
                base_honorarios = "arrematacao"
            elif "Strategic Prime" in pacote_honorarios:
                honorarios = 0.10
                base_honorarios = "lucro_liquido"
        elif tipo_honorarios == "Informar Valor Percentual":
            honorarios = st.number_input("Honorários Advocatícios (%)", min_value=0.0, max_value=100.0, value=2.0, step=0.1) / 100
            base_honorarios = "arrematacao"
        else: # Valor Fixo
            honorarios_fixo = st.number_input("Honorários Advocatícios (R$)", min_value=0.0, value=5000.0, step=500.0)
            honorarios = honorarios_fixo
            base_honorarios = "fixo"
        
        custas_processuais = st.number_input("Custas Processuais (%)", min_value=0.0, max_value=100.0, value=1.0, step=0.1) / 100
        
        st.subheader("Outras Despesas")
        
        # Opções de reformas
        tipo_reforma = st.radio("Reformas:", ["Informar Percentual", "Informar Valor Fixo"])
        if tipo_reforma == "Informar Percentual":
            reformas_perc = st.number_input("Reformas (% do valor de arrematação)", min_value=0.0, max_value=100.0, value=5.0, step=0.1) / 100
            valor_reformas_calc = valor_arrematacao * reformas_perc
            tipo_reformas = "percentual"
        else:
            valor_reformas_fixo = st.number_input("Valor da Reforma (R$)", min_value=0.0, value=10000.0, step=1000.0)
            tipo_reformas = "fixo"
        
        tem_condominio = st.checkbox("Imóvel possui despesa de condomínio")
        if tem_condominio:
            valor_condominio = st.number_input("Valor do Condomínio Mensal (R$)", min_value=0.0, value=500.0, step=100.0)
        else:
            valor_condominio = 0.0
            
        despesas_diversas = st.number_input("Despesas Diversas (R$)", min_value=0.0, value=0.0, step=100.0)
        st.caption("Eventuais dívidas que o arrematante assumirá como IPTU/ITR e Condomínio em atraso e/ou despesas com a contratação do crédito junto ao banco quando for financiado")
        
        # Imposto fixo em 15%
        imposto_ganho = 0.15
        st.text(f"Imposto sobre Ganho de Capital: 15%")
        
        tempo_operacao = st.number_input("Tempo de Operação (meses)", min_value=1, value=6, step=1)
        
        custos_mensais_adicionais = st.number_input("Outros Custos Mensais (R$)", min_value=0.0, value=0.0, step=100.0)
        st.caption("Ex: IPTU/ITR mensal")
        custo_mensal_total = custos_mensais_adicionais + valor_condominio
        
        if forma_pagamento == "Financiado":
            custo_mensal_total += valor_parcela
        
        st.markdown("</div>", unsafe_allow_html=True)

    # Cálculos
    valor_comissao = valor_arrematacao * comissao_leiloeiro
    valor_itbi = valor_arrematacao * itbi
    valor_custas = valor_arrematacao * custas_processuais
    
    # Cálculo das reformas - definir com um valor padrão para evitar problemas
    valor_reformas = 0.0
    if 'tipo_reformas' in locals() and tipo_reformas == "percentual" and 'reformas_perc' in locals():
        valor_reformas = valor_arrematacao * reformas_perc
    elif 'tipo_reformas' in locals() and tipo_reformas == "fixo" and 'valor_reformas_fixo' in locals():
        valor_reformas = valor_reformas_fixo
    else:
        # Caso padrão se não tiver as variáveis definidas
        if 'tipo_reforma' in locals() and tipo_reforma == "Informar Percentual" and 'reformas_perc' in locals():
            valor_reformas = valor_arrematacao * reformas_perc
        elif 'tipo_reforma' in locals() and tipo_reforma == "Informar Valor Fixo" and 'valor_reformas_fixo' in locals():
            valor_reformas = valor_reformas_fixo
    
    # Cálculo dos honorários dependendo do tipo selecionado
    if base_honorarios == "arrematacao":
        valor_honorarios = valor_arrematacao * honorarios
    elif base_honorarios == "lucro_liquido":
        # Vamos precisar calcular o lucro líquido primeiro, para isso precisamos calcular impostos
        # sem incluir os honorários (para evitar circularidade no cálculo)
        custos_sem_honorarios = (
            valor_comissao + 
            valor_itbi + 
            registro + 
            escritura + 
            valor_custas + 
            valor_reformas + 
            despesas_diversas + 
            (custo_mensal_total * tempo_operacao)
        )
        
        investimento_sem_honorarios = valor_arrematacao + custos_sem_honorarios
        lucro_bruto_sem_honorarios = valor_venda - investimento_sem_honorarios
        
        # Cálculo do imposto sem considerar honorários
        imposto_sem_honorarios = ((valor_venda - valor_arrematacao) - custos_sem_honorarios) * imposto_ganho if ((valor_venda - valor_arrematacao) - custos_sem_honorarios) > 0 else 0
        
        # Lucro líquido sem honorários
        lucro_liquido_sem_honorarios = lucro_bruto_sem_honorarios - imposto_sem_honorarios
        
        # Honorários são calculados sobre o lucro líquido (apenas se for positivo)
        valor_honorarios = lucro_liquido_sem_honorarios * honorarios if lucro_liquido_sem_honorarios > 0 else 0
    else:  # fixo
        valor_honorarios = honorarios
    
    custos_totais = (
        valor_comissao + 
        valor_itbi + 
        registro + 
        escritura + 
        valor_honorarios + 
        valor_custas + 
        valor_reformas + 
        despesas_diversas + 
        (custo_mensal_total * tempo_operacao)
    )
    
    custos_dedutiveis = (
        valor_comissao + 
        valor_itbi + 
        registro + 
        escritura + 
        valor_honorarios + 
        valor_custas + 
        valor_reformas + 
        despesas_diversas + 
        (custo_mensal_total * tempo_operacao)
    )
    
    investimento_total = valor_arrematacao + custos_totais
    lucro_bruto = valor_venda - investimento_total
    imposto_renda = ((valor_venda - valor_arrematacao) - custos_dedutiveis) * imposto_ganho if ((valor_venda - valor_arrematacao) - custos_dedutiveis) > 0 else 0
    lucro_liquido = lucro_bruto - imposto_renda
    
    roi_total = lucro_liquido / investimento_total if investimento_total > 0 else 0
    roi_mensal = roi_total / tempo_operacao if tempo_operacao > 0 else 0
    roi_anual = roi_mensal * 12
    
    # Exibição de resultados
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("<div class='info-block'>", unsafe_allow_html=True)
        st.markdown("#### Valores Pagos")
        st.markdown(f"**À Vista:** R$ {valor_vista:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**Financiado:** R$ {valor_financiado:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        if forma_pagamento == "Financiado":
            st.markdown(f"**Valor da Parcela:** R$ {valor_parcela:,.2f}/mês".replace(',', 'X').replace('.', ',').replace('X', '.'))
            st.markdown(f"**Total Pago em Parcelas:** R$ {valor_parcela * tempo_operacao:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**Valor de Arrematação:** R$ {valor_arrematacao:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='info-block'>", unsafe_allow_html=True)
        st.markdown("#### Custos")
        st.markdown(f"**Comissão Leiloeiro:** R$ {valor_comissao:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**ITBI:** R$ {valor_itbi:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**Registro:** R$ {registro:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**Escritura:** R$ {escritura:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**Honorários:** R$ {valor_honorarios:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**Custas Processuais:** R$ {valor_custas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**Reformas:** R$ {valor_reformas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        if tem_condominio:
            st.markdown(f"**Condomínio:** R$ {valor_condominio * tempo_operacao:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**Despesas Diversas:** R$ {despesas_diversas:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**Custos Mensais:** R$ {custo_mensal_total * tempo_operacao:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**Total de Custos:** R$ {custos_totais:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div class='info-block'>", unsafe_allow_html=True)
        st.markdown("#### Resultado")
        
        lucro_class = "positive" if lucro_liquido >= 0 else "negative"
        roi_class = "positive" if roi_total >= 0 else "negative"
        
        st.markdown(f"**Investimento Total:** R$ {investimento_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**Imposto de Renda:** R$ {imposto_renda:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        st.markdown(f"**Lucro Líquido:** <span class='{lucro_class}'>R$ {lucro_liquido:,.2f}</span>".replace(',', 'X').replace('.', ',').replace('X', '.'), unsafe_allow_html=True)
        st.markdown(f"**ROI Total:** <span class='{roi_class}'>{roi_total:.2%}</span>", unsafe_allow_html=True)
        st.markdown(f"**ROI Mensal:** <span class='{roi_class}'>{roi_mensal:.2%}</span>", unsafe_allow_html=True)
        st.markdown(f"**ROI Anualizado:** <span class='{roi_class}'>{roi_anual:.2%}</span>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Botões de impressão e contato
    col_print, col_contact = st.columns(2)
    
    with col_print:
        if st.button("📝 Imprimir / Salvar PDF"):
            html_print_code = """
            <script>
            window.open('', '_blank').document.write(`
                <html>
                    <head>
                        <title>Calculadora de Leilão - Resultado</title>
                        <style>
                            body { font-family: Arial, sans-serif; margin: 20px; }
                            h1 { color: #800000; text-align: center; }
                            .logo { text-align: center; margin-bottom: 20px; }
                            .section { margin-bottom: 20px; padding: 10px; border: 1px solid #e0e0e0; }
                            .header { background-color: #800000; color: #D4AF37; padding: 5px; }
                            table { width: 100%; border-collapse: collapse; }
                            td { padding: 5px; border-bottom: 1px solid #e0e0e0; }
                            .value { text-align: right; font-weight: bold; }
                            .positive { color: #006400; }
                            .negative { color: #8B0000; }
                            .footer { text-align: center; margin-top: 30px; font-size: 12px; color: #888; }
                            @media print {
                                body { -webkit-print-color-adjust: exact; }
                                .no-print { display: none; }
                                button { display: none; }
                            }
                        </style>
                    </head>
                    <body>
                        <div class="logo">
                            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZAAAAGQCAYAAACAvzbMAAAACXBIWXMAAAsTAAALEwEAmpwYAAAF62lUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPD94cGFja2V0IGJlZ2luPSLvu78iIGlkPSJXNU0wTXBDZWhpSHpyZVN6TlRjemtjOWQiPz4gPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iQWRvYmUgWE1QIENvcmUgNi4wLWMwMDIgNzkuMTY0NDg4LCAyMDIwLzA3LzEwLTIyOjA2OjUzICAgICAgICAiPiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPiA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtbG5zOmRjPSJodHRwOi8vcHVybC5vcmcvZGMvZWxlbWVudHMvMS4xLyIgeG1sbnM6cGhvdG9zaG9wPSJodHRwOi8vbnMuYWRvYmUuY29tL3Bob3Rvc2hvcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RFdnQ9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZUV2ZW50IyIgeG1wOkNyZWF0b3JUb29sPSJBZG9iZSBQaG90b3Nob3AgMjIuMCAoV2luZG93cykiIHhtcDpDcmVhdGVEYXRlPSIyMDIzLTEwLTE4VDEwOjUxOjA3LTAzOjAwIiB4bXA6TW9kaWZ5RGF0ZT0iMjAyMy0xMC0xOFQxMDo1MjowNi0wMzowMCIgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMy0xMC0xOFQxMDo1MjowNi0wMzowMCIgZGM6Zm9ybWF0PSJpbWFnZS9wbmciIHBob3Rvc2hvcDpDb2xvck1vZGU9IjMiIHBob3Rvc2hvcDpJQ0NQcm9maWxlPSJzUkdCIElFQzYxOTY2LTIuMSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDplM2QzMzUwYS01NjgxLTRjNGQtODYxMS05M2JmNGNkMWYwYmUiIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6YmI5NDE5NjAtZGI0Mi00NWI3LWEwMDYtZTcwMzAxZDJkMzgwIiB4bXBNTTpPcmlnaW5hbERvY3VtZW50SUQ9InhtcC5kaWQ6YmI5NDE5NjAtZGI0Mi00NWI3LWEwMDYtZTcwMzAxZDJkMzgwIj4gPHhtcE1NOkhpc3Rvcnk+IDxyZGY6U2VxPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0iY3JlYXRlZCIgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDpiYjk0MTk2MC1kYjQyLTQ1YjctYTAwNi1lNzAzMDFkMmQzODAiIHN0RXZ0OndoZW49IjIwMjMtMTAtMThUMTA6NTE6MDctMDM6MDAiIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkFkb2JlIFBob3Rvc2hvcCAyMi4wIChXaW5kb3dzKSIvPiA8cmRmOmxpIHN0RXZ0OmFjdGlvbj0ic2F2ZWQiIHN0RXZ0Omluc3RhbmNlSUQ9InhtcC5paWQ6ZTNkMzM1MGEtNTY4MS00YzRkLTg2MTEtOTNiZjRjZDFmMGJlIiBzdEV2dDp3aGVuPSIyMDIzLTEwLTE4VDEwOjUyOjA2LTAzOjAwIiBzdEV2dDpzb2Z0d2FyZUFnZW50PSJBZG9iZSBQaG90b3Nob3AgMjIuMCAoV2luZG93cykiIHN0RXZ0OmNoYW5nZWQ9Ii8iLz4gPC9yZGY6U2VxPiA8L3htcE1NOkhpc3Rvcnk+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+kGw8BgAAM9hJREFUeJzsnX3sFPl94D9fX8M5oDBrXIJTGxuvuQSdlVBsdH0h7EWJL8DWJhzYsoFVm1BL2HUOt5v1NXdqpNBzRdJYwc3loMS1pCb1bXEO0tY+lohzzuYuPsclMYZJ4hTO9YK9R+HYxlwvGANP/5h9PTOzPTP7zMyzzzy/j/RqzeybN78ZPM+83+f7PG8gRAP4wA8+dVe7LZ07/tJDo3FfixDNRgREpEIIDMc8ZWRkdOz61NQDUkTEaiUCIlJhEw/nuXo0GbOJyfVosiJCIgREiNlUISAAQVVCIhDCZUSA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" alt="Bastos Moraes Advocacia">
                        </div>
                        <h1>Calculadora de Leilão para Investidores</h1>
                        
                        <div class="section">
                            <div class="header">Dados do Imóvel</div>
                            <table>
                                <tr>
                                    <td>Data de Compra:</td>
                                    <td class="value">${data_compra}</td>
                                </tr>
                                <tr>
                                    <td>Valor de Arrematação:</td>
                                    <td class="value">R$ ${valor_arrematacao.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td>Valor de Venda:</td>
                                    <td class="value">R$ ${valor_venda.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td>Forma de Pagamento:</td>
                                    <td class="value">${forma_pagamento}</td>
                                </tr>
                                <tr>
                                    <td>Valor Pago à Vista:</td>
                                    <td class="value">R$ ${valor_vista.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td>Valor Financiado:</td>
                                    <td class="value">R$ ${valor_financiado.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div class="section">
                            <div class="header">Custos</div>
                            <table>
                                <tr>
                                    <td>Comissão do Leiloeiro:</td>
                                    <td class="value">R$ ${valor_comissao.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td>ITBI:</td>
                                    <td class="value">R$ ${valor_itbi.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td>Registro:</td>
                                    <td class="value">R$ ${registro.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td>Escritura:</td>
                                    <td class="value">R$ ${escritura.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td>Honorários Advocatícios:</td>
                                    <td class="value">R$ ${valor_honorarios.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td>Custas Processuais:</td>
                                    <td class="value">R$ ${valor_custas.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td>Reformas:</td>
                                    <td class="value">R$ ${valor_reformas.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td>Despesas Diversas:</td>
                                    <td class="value">R$ ${despesas_diversas.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td>Custos Mensais (Total):</td>
                                    <td class="value">R$ ${(custo_mensal_total * tempo_operacao).toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td><strong>Total de Custos:</strong></td>
                                    <td class="value"><strong>R$ ${custos_totais.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</strong></td>
                                </tr>
                            </table>
                        </div>
                        
                        <div class="section">
                            <div class="header">Resultado</div>
                            <table>
                                <tr>
                                    <td>Investimento Total:</td>
                                    <td class="value">R$ ${investimento_total.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td>Imposto de Renda:</td>
                                    <td class="value">R$ ${imposto_renda.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</td>
                                </tr>
                                <tr>
                                    <td><strong>Lucro Líquido:</strong></td>
                                    <td class="value ${lucro_liquido >= 0 ? 'positive' : 'negative'}"><strong>R$ ${lucro_liquido.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2})}</strong></td>
                                </tr>
                                <tr>
                                    <td>ROI Total:</td>
                                    <td class="value ${roi_total >= 0 ? 'positive' : 'negative'}">${(roi_total * 100).toFixed(2)}%</td>
                                </tr>
                                <tr>
                                    <td>ROI Mensal:</td>
                                    <td class="value ${roi_mensal >= 0 ? 'positive' : 'negative'}">${(roi_mensal * 100).toFixed(2)}%</td>
                                </tr>
                                <tr>
                                    <td>ROI Anualizado:</td>
                                    <td class="value ${roi_anual >= 0 ? 'positive' : 'negative'}">${(roi_anual * 100).toFixed(2)}%</td>
                                </tr>
                            </table>
                        </div>
                        
                        <div class="footer">
                            <p>Bastos Moraes Advocacia | Todos os direitos reservados &copy; 2023-2025</p>
                            <button class="no-print" onclick="window.print()">Imprimir</button>
                        </div>
                    </body>
                </html>
            `);
            </script>
            """
            st.components.v1.html(html_print_code, height=0)
            st.success("Um PDF foi gerado em uma nova aba. Salve ou imprima o documento pela interface do navegador.")
    
    with col_contact:
        if st.button("📱 Entre em Contato"):
            st.markdown("""
            <script>
            window.open('https://api.whatsapp.com/message/XVSEPLILBK6LB1?autoload=1&app_absent=0', '_blank');
            </script>
            """, unsafe_allow_html=True)
            st.success("Redirecionando para o WhatsApp do escritório...")
            st.markdown(f'<a href="https://api.whatsapp.com/message/XVSEPLILBK6LB1?autoload=1&app_absent=0" target="_blank">Clique aqui se não for redirecionado automaticamente</a>', unsafe_allow_html=True)

with tab2:
    st.markdown("""
    ## Como utilizar a Calculadora de Leilão

    ### Objetivo
    Esta calculadora permite que investidores simulem operações de compra em leilões imobiliários, 
    calculando todos os custos envolvidos e o potencial retorno do investimento.

    ### Instruções
    1. Preencha os **Dados do Imóvel** (valor de arrematação e valor de venda)
    2. Selecione a **Forma de Pagamento** (à vista ou financiado)
    3. Configure os **Custos e Despesas** conforme sua situação específica
    4. Verifique o **Resultado** para análise do potencial retorno do investimento

    ### Campos Importantes
    - **Valor de Arrematação**: valor pelo qual o imóvel foi arrematado no leilão
    - **Valor de Venda**: valor estimado de venda futura do imóvel
    - **Forma de Pagamento**: à vista ou financiado (com parcelas mensais)
    - **Comissão do Leiloeiro**: normalmente entre 5% e 10% do valor de arrematação
    - **ITBI**: Imposto de Transmissão de Bens Imóveis (varia por município)
    - **Reformas**: estimativa de gastos com reformas (% do valor de arrematação)
    - **Condomínio**: despesas mensais de condomínio, se aplicável
    - **Tempo de Operação**: período estimado para concluir toda a operação

    ### Pacotes de Honorários Advocatícios
    """)
    
    st.markdown("""
    #### Pacote Connoisseur | 3,5% da arrematação
    Indicado para quem já adquiriu um imóvel em leilão e necessita apenas de suporte na imissão na posse e na regularização pós-arrematação.
    
    #### Pacote Veritas | 5% da arrematação
    Voltado para quem deseja segurança na análise de oportunidades antes da arrematação. Oferece a análise jurídica de até quatro oportunidades mensais enviadas pelo cliente, além do suporte completo na aquisição e regularização do imóvel.
    
    #### Pacote AvantGarde | 7% da arrematação
    Ideal para quem busca total comodidade e acompanhamento integral. O cliente recebe até seis oportunidades de imóveis por mês selecionadas conforme seu perfil, além de contar com participação em leilões, registro da propriedade, regularização documental e imissão na posse.
    
    #### Pacote Pinnacle | 10% da arrematação
    A opção mais completa. Inclui todos os serviços do pacote Avant-Garde, acrescentando ainda a execução da reforma do imóvel arrematado e o gerenciamento da venda do bem, focando na maximização da rentabilidade para o investidor.
    
    #### Pacote Strategic Prime | 10% sobre o lucro
    Uma solução jurídica inovadora e personalizada para investidores que atuam com imóveis CAIXA de até R$ 150.000,00. Com uma estrutura de honorários baseada no lucro real da operação, este modelo reduz o impacto financeiro inicial e alinha os interesses entre escritório e investidor.
    """)
    
    st.markdown("""
    ### Resultados
    - **Investimento Total**: soma do valor de arrematação e todos os custos
    - **Lucro Líquido**: valor de venda menos investimento total e impostos
    - **ROI Total**: retorno percentual sobre o investimento total
    - **ROI Mensal e Anualizado**: retorno proporcional ao tempo da operação
    """)

    st.info("Observação: Esta calculadora é uma ferramenta de simulação. Consulte um especialista jurídico e financeiro antes de tomar decisões de investimento.")

# Rodapé
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #D4AF37;'>Bastos Moraes Advocacia | Todos os direitos reservados Copyright © 2023-2025</p>", unsafe_allow_html=True)