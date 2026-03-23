import streamlit as st
import pandas as pd
import sqlite3
import os
import json
from datetime import datetime, timedelta
import hashlib
import base64
from pathlib import Path
import io

# Importações para IA
import google.generativeai as genai
from pdf2image import convert_from_bytes
import PyPDF2

# ============================================================================
# CONFIGURAÇÕES GLOBAIS
# ============================================================================

st.set_page_config(
    page_title="Gestão de Ativos NR-13",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CORES
PRIMARY_COLOR = "#00D1FF"
SECONDARY_COLOR = "#1f1f1f"
SUCCESS_COLOR = "#00CC96"
WARNING_COLOR = "#FFA15A"
DANGER_COLOR = "#FF6B6B"
TEXT_LIGHT = "#FFFFFF"
BG_DARK = "#0a0a0a"

# CSS DARK THEME - CORRIGIDO
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {BG_DARK};
        color: {TEXT_LIGHT};
    }}
    
    body {{
        background-color: {BG_DARK};
        color: {TEXT_LIGHT};
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        color: {PRIMARY_COLOR};
    }}
    
    p, span, div, label {{
        color: {TEXT_LIGHT} !important;
    }}
    
    .stMarkdown {{
        color: {TEXT_LIGHT};
    }}
    
    .card-vencido {{
        background-color: rgba(255, 107, 107, 0.1);
        border: 2px solid {DANGER_COLOR};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }}
    
    .card-aviso {{
        background-color: rgba(255, 161, 90, 0.1);
        border: 2px solid {WARNING_COLOR};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }}
    
    .card-ok {{
        background-color: rgba(0, 204, 150, 0.1);
        border: 2px solid {SUCCESS_COLOR};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }}
    
    .stButton > button {{
        background-color: {PRIMARY_COLOR};
        color: #000;
        font-weight: 700;
    }}
    
    .stButton > button:hover {{
        background-color: #00A8CC;
        color: #000;
    }}
    
    .stTabs [aria-selected="true"] {{
        border-bottom: 3px solid {PRIMARY_COLOR};
        color: {PRIMARY_COLOR};
    }}
    
    .stMetric {{
        background-color: rgba(0, 209, 255, 0.05);
        border-radius: 8px;
        padding: 10px;
    }}
    
    input, textarea, select {{
        background-color: #1a1a1a !important;
        color: {TEXT_LIGHT} !important;
        border: 1px solid {PRIMARY_COLOR} !important;
    }}
    
    .stExpander {{
        background-color: #1a1a1a;
        border: 1px solid {PRIMARY_COLOR};
    }}
    
    .stDataFrame {{
        background-color: #1a1a1a;
    }}
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def get_db_path(cliente_id):
    """Retorna caminho do banco de dados do cliente"""
    db_dir = Path("clientes_db")
    db_dir.mkdir(exist_ok=True)
    return db_dir / f"cliente_{cliente_id}.db"

def init_database(cliente_id):
    """Inicializa banco de dados do cliente"""
    db_path = get_db_path(cliente_id)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # TABELA: EMPRESA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empresa (
            id INTEGER PRIMARY KEY,
            nome TEXT UNIQUE,
            cnpj TEXT,
            responsavel TEXT,
            email TEXT,
            telefone TEXT,
            api_key_ia TEXT,
            tipo_ia TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # TABELA: ATIVOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ativos (
            id INTEGER PRIMARY KEY,
            tag TEXT UNIQUE,
            tipo_equipamento TEXT,
            local TEXT,
            categoria_nr13 TEXT,
            fluido TEXT,
            classe_fluido TEXT,
            data_proxima_externa DATE,
            data_proxima_interna DATE,
            fabricante TEXT,
            modelo TEXT,
            ano_fabricacao INTEGER,
            status TEXT,
            observacoes TEXT,
            origem_documento TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # TABELA: DOCUMENTOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY,
            nome_arquivo TEXT,
            tipo_arquivo TEXT,
            data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tamanho_bytes INTEGER,
            resumo_analise_ia TEXT,
            ativos_extraidos INTEGER,
            status TEXT
        )
    """)
    
    # TABELA: CONFORMIDADES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conformidades (
            id INTEGER PRIMARY KEY,
            ativo_id INTEGER,
            tipo_problema TEXT,
            descricao TEXT,
            prazo_correcao TEXT,
            status TEXT,
            prioridade TEXT,
            data_deteccao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_resolucao TIMESTAMP,
            contato_feliz_enviado BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (ativo_id) REFERENCES ativos(id)
        )
    """)
    
    # TABELA: HISTÓRICO WHATSAPP
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS whatsapp_enviados (
            id INTEGER PRIMARY KEY,
            conformidade_id INTEGER,
            mensagem TEXT,
            data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            url_whatsapp TEXT,
            FOREIGN KEY (conformidade_id) REFERENCES conformidades(id)
        )
    """)
    
    # TABELA: AUDITORIA
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY,
            operacao TEXT,
            tabela TEXT,
            descricao TEXT,
            usuario TEXT,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def get_empresa(cliente_id):
    """Retorna dados da empresa"""
    db_path = get_db_path(cliente_id)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empresa LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result

def salvar_empresa(cliente_id, nome, cnpj, responsavel, email, telefone, api_key, tipo_ia):
    """Salva dados da empresa"""
    db_path = get_db_path(cliente_id)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO empresa 
            (nome, cnpj, responsavel, email, telefone, api_key_ia, tipo_ia)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nome, cnpj, responsavel, email, telefone, api_key, tipo_ia))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar empresa: {e}")
        return False
    finally:
        conn.close()

def salvar_ativos(cliente_id, df_ativos):
    """Salva múltiplos ativos"""
    db_path = get_db_path(cliente_id)
    conn = sqlite3.connect(str(db_path))
    
    try:
        df_ativos.to_sql('ativos', conn, if_exists='append', index=False)
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar ativos: {e}")
        return False
    finally:
        conn.close()

def get_ativos(cliente_id):
    """Retorna todos os ativos"""
    db_path = get_db_path(cliente_id)
    conn = sqlite3.connect(str(db_path))
    df = pd.read_sql_query("SELECT * FROM ativos", conn)
    conn.close()
    return df

def get_conformidades(cliente_id):
    """Retorna todas as conformidades"""
    db_path = get_db_path(cliente_id)
    conn = sqlite3.connect(str(db_path))
    df = pd.read_sql_query("""
        SELECT c.*, a.tag, a.tipo_equipamento 
        FROM conformidades c
        LEFT JOIN ativos a ON c.ativo_id = a.id
        ORDER BY c.data_deteccao DESC
    """, conn)
    conn.close()
    return df

def salvar_conformidade(cliente_id, ativo_id, tipo_problema, descricao, prazo, prioridade):
    """Salva conformidade detectada"""
    db_path = get_db_path(cliente_id)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO conformidades 
            (ativo_id, tipo_problema, descricao, prazo_correcao, status, prioridade)
            VALUES (?, ?, ?, ?, 'pendente', ?)
        """, (ativo_id, tipo_problema, descricao, prazo, prioridade))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        st.error(f"Erro ao salvar conformidade: {e}")
        return None
    finally:
        conn.close()

# ============================================================================
# IA FUNCTIONS
# ============================================================================

def testar_conexao_ia(api_key, tipo_ia):
    """Testa conexão com IA"""
    try:
        if tipo_ia == "Gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Teste de conexão. Responda apenas com 'OK'")
            return "OK" in response.text or response.text.strip() == "OK"
        return False
    except Exception as e:
        st.error(f"Erro na conexão: {e}")
        return False

def analisar_documento_com_ia(api_key, tipo_ia, conteudo_documento):
    """Analisa documento com IA e extrai dados de ativos"""
    try:
        if tipo_ia == "Gemini":
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            Você é um especialista em análise de relatórios técnicos NR-13.
            
            Analise o seguinte documento e extraia informações sobre equipamentos/ativos:
            
            {conteudo_documento[:3000]}
            
            Para cada equipamento encontrado, extraia em formato JSON:
            {{
                "ativos": [
                    {{
                        "tag": "identificador do equipamento",
                        "tipo_equipamento": "tipo/modelo",
                        "local": "local de instalação",
                        "categoria_nr13": "I/II/III/IV/V",
                        "fluido": "fluído de trabalho",
                        "classe_fluido": "A/B/C",
                        "data_proxima_externa": "YYYY-MM-DD",
                        "data_proxima_interna": "YYYY-MM-DD",
                        "fabricante": "fabricante",
                        "modelo": "modelo",
                        "ano_fabricacao": 2020,
                        "status": "Ativo/Vencido/Em Manutenção",
                        "observacoes": "observações relevantes"
                    }}
                ],
                "resumo": "resumo executivo do documento",
                "conformidades_detectadas": [
                    {{
                        "tipo": "Vencimento/Não Conformidade/Recomendação",
                        "descricao": "descrição do problema",
                        "prioridade": "Alta/Média/Baixa"
                    }}
                ]
            }}
            
            Retorne APENAS o JSON válido, sem markdown ou explicações adicionais.
            Se não encontrar equipamentos, retorne {{"ativos": [], "resumo": "Sem equipamentos encontrados", "conformidades_detectadas": []}}
            """
            
            response = model.generate_content(prompt)
            
            try:
                resultado = json.loads(response.text)
                return resultado
            except json.JSONDecodeError:
                import re
                json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                return {
                    "ativos": [],
                    "resumo": response.text,
                    "conformidades_detectadas": []
                }
        
        return None
    except Exception as e:
        st.error(f"Erro na análise com IA: {e}")
        return None

# ============================================================================
# DOCUMENT PARSING
# ============================================================================

def extrair_texto_pdf(arquivo_pdf):
    """Extrai texto de PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(arquivo_pdf)
        texto = ""
        for page in pdf_reader.pages:
            texto += page.extract_text()
        return texto
    except Exception as e:
        st.error(f"Erro ao ler PDF: {e}")
        return None

def extrair_dados_csv(arquivo_csv):
    """Extrai dados de CSV"""
    try:
        df = pd.read_csv(arquivo_csv)
        return df, df.to_string()
    except Exception as e:
        st.error(f"Erro ao ler CSV: {e}")
        return None, None

def extrair_dados_excel(arquivo_excel):
    """Extrai dados de Excel"""
    try:
        df = pd.read_excel(arquivo_excel)
        return df, df.to_string()
    except Exception as e:
        st.error(f"Erro ao ler Excel: {e}")
        return None, None

# ============================================================================
# UTILITÁRIOS
# ============================================================================

def calcular_dias_vencimento(data_inspecao):
    """Calcula dias para vencimento"""
    data_referencia = datetime(2026, 3, 23)
    dias = (pd.to_datetime(data_inspecao) - data_referencia).days
    return dias

def gerar_link_whatsapp(telefone, mensagem):
    """Gera link WhatsApp"""
    import urllib.parse
    msg_encoded = urllib.parse.quote(mensagem)
    telefone_clean = str(telefone).replace("+", "").replace("-", "").replace(" ", "")
    return f"https://wa.me/{telefone_clean}?text={msg_encoded}"

def registrar_auditoria(cliente_id, operacao, tabela, descricao, usuario="Sistema"):
    """Registra ação na auditoria"""
    db_path = get_db_path(cliente_id)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO auditoria (operacao, tabela, descricao, usuario)
        VALUES (?, ?, ?, ?)
    """, (operacao, tabela, descricao, usuario))
    conn.commit()
    conn.close()

# ============================================================================
# INICIALIZAÇÃO DO SESSION STATE
# ============================================================================

def init_session():
    """Inicializa variáveis de sessão"""
    if 'cliente_id' not in st.session_state:
        st.session_state.cliente_id = None
    
    if 'empresa_configurada' not in st.session_state:
        st.session_state.empresa_configurada = False
    
    if 'ativos_df' not in st.session_state:
        st.session_state.ativos_df = pd.DataFrame()
    
    if 'conformidades_df' not in st.session_state:
        st.session_state.conformidades_df = pd.DataFrame()

init_session()

# ============================================================================
# PAGES
# ============================================================================

def pagina_login():
    """Página de login/seleção de cliente"""
    st.markdown("<h1 style='color: #00D1FF; text-align: center;'>🔐 Acesso ao Sistema</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Cliente Existente")
        cliente_id = st.text_input("ID do Cliente:", placeholder="ex: empresa_123")
        
        if st.button("Acessar", key="btn_acessar"):
            db_path = get_db_path(cliente_id)
            if db_path.exists():
                st.session_state.cliente_id = cliente_id
                init_database(cliente_id)
                st.success(f"✅ Bem-vindo de volta!")
                st.rerun()
            else:
                st.error("❌ Cliente não encontrado. Crie um novo acesso.")
    
    with col2:
        st.markdown("### 🆕 Novo Cliente")
        novo_cliente_id = st.text_input("ID do Novo Cliente:", placeholder="ex: empresa_123")
        
        if st.button("Criar Novo Acesso", key="btn_novo"):
            if novo_cliente_id:
                st.session_state.cliente_id = novo_cliente_id
                init_database(novo_cliente_id)
                st.success(f"✅ Conta criada! Configure seus dados.")
                st.rerun()
            else:
                st.error("❌ Digite um ID para o cliente")

def pagina_configuracao():
    """Página de configuração da empresa"""
    st.markdown("<h1 style='color: #00D1FF;'>⚙️ Configuração da Empresa</h1>", unsafe_allow_html=True)
    
    cliente_id = st.session_state.cliente_id
    empresa = get_empresa(cliente_id)
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome = st.text_input("Nome da Empresa", value=empresa[1] if empresa else "")
        cnpj = st.text_input("CNPJ", value=empresa[2] if empresa else "")
        responsavel = st.text_input("Responsável", value=empresa[3] if empresa else "")
        email = st.text_input("Email", value=empresa[4] if empresa else "")
    
    with col2:
        telefone = st.text_input("Telefone", value=empresa[5] if empresa else "")
        
        st.markdown("### 🤖 Configuração da IA")
        tipo_ia = st.selectbox(
            "Escolha a IA para análise:",
            ["Gemini (Google)"],
            index=0
        )
        
        api_key = st.text_input(
            "Chave de API da IA:",
            value=empresa[6] if empresa and empresa[6] else "",
            type="password",
            help="Sua chave não será compartilhada"
        )
        
        if st.button("🔗 Testar Conexão"):
            with st.spinner("Testando..."):
                if testar_conexao_ia(api_key, "Gemini"):
                    st.success("✅ Conexão OK!")
                else:
                    st.error("❌ Falha na conexão. Verifique a chave de API.")
    
    if st.button("💾 Salvar Configurações", use_container_width=True):
        if nome and email and api_key:
            if salvar_empresa(
                cliente_id,
                nome,
                cnpj,
                responsavel,
                email,
                telefone,
                api_key,
                "Gemini"
            ):
                st.session_state.empresa_configurada = True
                st.success("✅ Configurações salvas com sucesso!")
                registrar_auditoria(cliente_id, "CONFIGURACAO", "empresa", f"Empresa {nome} configurada")
        else:
            st.error("❌ Preencha todos os campos obrigatórios")

def pagina_upload():
    """Página de upload e análise de documentos"""
    st.markdown("<h1 style='color: #00D1FF;'>📤 Upload de Documentos</h1>", unsafe_allow_html=True)
    
    cliente_id = st.session_state.cliente_id
    empresa = get_empresa(cliente_id)
    
    if not empresa or not empresa[6]:
        st.warning("⚠️ Configure a chave de API primeiro na aba 'Configuração'")
        return
    
    st.markdown("### 📋 Formatos Suportados")
    st.info("**PDF** (Relatórios técnicos) | **CSV** (Banco de dados) | **Excel** (Planilhas)")
    
    uploaded_files = st.file_uploader(
        "Arraste ou selecione seus arquivos:",
        type=["pdf", "csv", "xlsx"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for arquivo in uploaded_files:
            with st.spinner(f"📍 Processando {arquivo.name}..."):
                conteudo = None
                df_dados = None
                tipo_arquivo = arquivo.name.split('.')[-1].lower()
                
                if tipo_arquivo == "pdf":
                    conteudo = extrair_texto_pdf(arquivo)
                elif tipo_arquivo == "csv":
                    df_dados, conteudo = extrair_dados_csv(arquivo)
                elif tipo_arquivo == "xlsx":
                    df_dados, conteudo = extrair_dados_excel(arquivo)
                
                if conteudo:
                    st.success(f"✅ Arquivo lido com sucesso!")
                    
                    st.info("🤖 Analisando com IA...")
                    api_key = empresa[6]
                    tipo_ia = empresa[7]
                    
                    resultado_ia = analisar_documento_com_ia(api_key, tipo_ia, conteudo)
                    
                    if resultado_ia:
                        ativos_encontrados = resultado_ia.get("ativos", [])
                        
                        if ativos_encontrados:
                            st.success(f"✨ {len(ativos_encontrados)} equipamento(s) encontrado(s)!")
                            
                            df_ativos = pd.DataFrame(ativos_encontrados)
                            salvar_ativos(cliente_id, df_ativos)
                            
                            st.session_state.ativos_df = df_ativos
                            
                            registrar_auditoria(
                                cliente_id,
                                "UPLOAD",
                                "documentos",
                                f"Upload {arquivo.name} - {len(ativos_encontrados)} ativos extraídos"
                            )
                            
                            st.markdown("### 📊 Resumo da Análise")
                            st.info(resultado_ia.get("resumo", "Análise concluída"))
                            
                            conformidades = resultado_ia.get("conformidades_detectadas", [])
                            if conformidades:
                                st.markdown("### ⚠️ Problemas Detectados")
                                for conf in conformidades:
                                    if conf.get("prioridade") == "Alta":
                                        st.error(f"🔴 {conf.get('tipo')}: {conf.get('descricao')}")
                                    elif conf.get("prioridade") == "Média":
                                        st.warning(f"🟡 {conf.get('tipo')}: {conf.get('descricao')}")
                                    else:
                                        st.info(f"🔵 {conf.get('tipo')}: {conf.get('descricao')}")
                        else:
                            st.warning("⚠️ Nenhum equipamento encontrado no documento")

def pagina_gestao_ativos():
    """Página de gestão de ativos"""
    st.markdown("<h1 style='color: #00D1FF;'>🛡️ Gestão de Ativos</h1>", unsafe_allow_html=True)
    
    cliente_id = st.session_state.cliente_id
    df_ativos = get_ativos(cliente_id)
    
    if df_ativos.empty:
        st.info("📤 Faça upload de documentos primeiro para popular a gestão de ativos")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_ativos = len(df_ativos)
    vencidos = len(df_ativos[df_ativos['status'] == 'Vencido'])
    ativos_ok = len(df_ativos[df_ativos['status'] == 'Ativo'])
    conformidade = (ativos_ok / total_ativos * 100) if total_ativos > 0 else 0
    
    with col1:
        st.metric("📦 Total de Ativos", total_ativos)
    with col2:
        st.metric("✅ Ativos/Conformes", ativos_ok)
    with col3:
        st.metric("🔴 Vencidos", vencidos, delta_color="inverse")
    with col4:
        st.metric("📊 Conformidade NR-13", f"{conformidade:.0f}%")
    
    st.divider()
    
    col_filtro1, col_filtro2, col_filtro3 = st.columns(3)
    
    with col_filtro1:
        filtro_status = st.multiselect(
            "Filtrar por Status",
            options=df_ativos['status'].unique(),
            default=df_ativos['status'].unique()
        )
    
    with col_filtro2:
        filtro_categoria = st.multiselect(
            "Filtrar por Categoria",
            options=df_ativos['categoria_nr13'].unique(),
            default=df_ativos['categoria_nr13'].unique()
        )
    
    with col_filtro3:
        filtro_fluido = st.multiselect(
            "Filtrar por Fluído",
            options=df_ativos['fluido'].unique(),
            default=df_ativos['fluido'].unique()
        )
    
    df_filtrado = df_ativos[
        (df_ativos['status'].isin(filtro_status)) &
        (df_ativos['categoria_nr13'].isin(filtro_categoria)) &
        (df_ativos['fluido'].isin(filtro_fluido))
    ]
    
    st.markdown("### 📋 Tabela de Ativos")
    
    column_config = {
        "tag": st.column_config.TextColumn("TAG", width="small"),
        "tipo_equipamento": st.column_config.TextColumn("Tipo", width="medium"),
        "local": st.column_config.TextColumn("Local", width="small"),
        "categoria_nr13": st.column_config.SelectboxColumn("Categoria", options=["I", "II", "III", "IV", "V"]),
        "fluido": st.column_config.TextColumn("Fluído", width="small"),
        "data_proxima_externa": st.column_config.DateColumn("Próx. Externa"),
        "data_proxima_interna": st.column_config.DateColumn("Próx. Interna"),
        "status": st.column_config.SelectboxColumn("Status", options=["Ativo", "Vencido", "Em Manutenção"]),
    }
    
    st.dataframe(
        df_filtrado,
        column_config=column_config,
        use_container_width=True,
        height=400
    )
    
    st.divider()
    st.markdown("### 📊 Análises Visuais")
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.markdown("**Status dos Equipamentos**")
        status_count = df_ativos['status'].value_counts()
        st.bar_chart(status_count)
    
    with col_graf2:
        st.markdown("**Distribuição por Categoria**")
        cat_count = df_ativos['categoria_nr13'].value_counts()
        st.bar_chart(cat_count)

def pagina_oportunidades():
    """Página de oportunidades de negócio"""
    st.markdown("<h1 style='color: #00D1FF;'>💡 Oportunidades de Negócio</h1>", unsafe_allow_html=True)
    
    cliente_id = st.session_state.cliente_id
    empresa = get_empresa(cliente_id)
    df_ativos = get_ativos(cliente_id)
    
    if df_ativos.empty:
        st.info("📤 Faça upload de documentos para gerar oportunidades")
        return
    
    problemas = []
    
    for idx, row in df_ativos.iterrows():
        if row['status'] == 'Vencido':
            dias_vencidos = calcular_dias_vencimento(row['data_proxima_externa'])
            problemas.append({
                'ativo_id': idx,
                'tag': row['tag'],
                'tipo': row['tipo_equipamento'],
                'problema': 'Vencimento de Inspeção Externa',
                'descricao': f"Equipamento vencido há {abs(dias_vencidos)} dias",
                'prioridade': 'Alta',
                'data_vencimento': row['data_proxima_externa']
            })
        
        try:
            dias_externa = calcular_dias_vencimento(row['data_proxima_externa'])
            if 0 < dias_externa < 30:
                problemas.append({
                    'ativo_id': idx,
                    'tag': row['tag'],
                    'tipo': row['tipo_equipamento'],
                    'problema': 'Vencimento Próximo (< 30 dias)',
                    'descricao': f"Inspeção externa vence em {dias_externa} dias",
                    'prioridade': 'Média',
                    'data_vencimento': row['data_proxima_externa']
                })
        except:
            pass
    
    if not problemas:
        st.success("✅ Tudo em dia! Nenhuma oportunidade detectada.")
        return
    
    problemas_sorted = sorted(problemas, key=lambda x: {'Alta': 0, 'Média': 1, 'Baixa': 2}[x['prioridade']])
    
    for idx, problema in enumerate(problemas_sorted):
        cor_prioridade = {
            'Alta': 'red',
            'Média': 'orange',
            'Baixa': 'green'
        }[problema['prioridade']]
        
        with st.container():
            col_info, col_acao = st.columns([3, 1])
            
            with col_info:
                st.markdown(f"""
                <div style="
                    background-color: rgba(255, 107, 107, 0.1);
                    border-left: 4px solid {'#FF6B6B' if problema['prioridade'] == 'Alta' else '#FFA15A'};
                    padding: 15px;
                    border-radius: 8px;
                    margin: 10px 0;
                ">
                    <h4 style="color: #00D1FF; margin: 0;">🔴 {problema['tag']}</h4>
                    <p style="margin: 5px 0; color: #FFFFFF;"><b>Tipo:</b> {problema['tipo']}</p>
                    <p style="margin: 5px 0; color: #FFFFFF;"><b>Problema:</b> {problema['problema']}</p>
                    <p style="margin: 5px 0; color: #FFFFFF;"><b>Descrição:</b> {problema['descricao']}</p>
                    <p style="margin: 5px 0; color: {'#FF6B6B' if problema['prioridade'] == 'Alta' else '#FFA15A'};"><b>Prioridade:</b> {problema['prioridade']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_acao:
                if st.button(f"📞 Contatar", key=f"btn_{idx}", use_container_width=True):
                    mensagem = f"""
Olá Felipe!

Tenho uma oportunidade de negócio:

📍 **Empresa:** {empresa[1] if empresa else 'Não configurada'}
🏭 **Equipamento:** {problema['tag']} ({problema['tipo']})
⚠️ **Problema:** {problema['problema']}
📝 **Descrição:** {problema['descricao']}
⏰ **Vencimento:** {problema['data_vencimento']}

Gostaria de um orçamento para regularização.

Acesso ao dashboard: Disponível para consulta.

Obrigado!
                    """
                    
                    link_wa = gerar_link_whatsapp("+5581997538656", mensagem.strip())
                    
                    conformidade_id = salvar_conformidade(
                        cliente_id,
                        idx,
                        problema['problema'],
                        problema['descricao'],
                        str(problema['data_vencimento']),
                        problema['prioridade']
                    )
                    
                    if conformidade_id:
                        db_path = get_db_path(cliente_id)
                        conn = sqlite3.connect(str(db_path))
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO whatsapp_enviados (conformidade_id, mensagem, url_whatsapp)
                            VALUES (?, ?, ?)
                        """, (conformidade_id, mensagem.strip(), link_wa))
                        conn.commit()
                        conn.close()
                        
                        registrar_auditoria(
                            cliente_id,
                            "WHATSAPP",
                            "conformidades",
                            f"Contato enviado para {problema['tag']}"
                        )
                    
                    st.markdown(f"""
                    <a href="{link_wa}" target="_blank">
                        <button style="
                            background-color: #25D366;
                            color: white;
                            padding: 10px 20px;
                            border: none;
                            border-radius: 6px;
                            cursor: pointer;
                            font-weight: 700;
                            width: 100%;
                        ">
                        ✅ WhatsApp Aberto
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
        
        st.divider()

def pagina_relatorios():
    """Página de relatórios"""
    st.markdown("<h1 style='color: #00D1FF;'>📊 Relatórios</h1>", unsafe_allow_html=True)
    
    cliente_id = st.session_state.cliente_id
    empresa = get_empresa(cliente_id)
    df_ativos = get_ativos(cliente_id)
    df_conformidades = get_conformidades(cliente_id)
    
    if df_ativos.empty:
        st.info("📤 Nenhum dado disponível")
        return
    
    st.markdown("### 📈 Resumo Executivo")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Equipamentos", len(df_ativos))
    with col2:
        vencidos = len(df_ativos[df_ativos['status'] == 'Vencido'])
        st.metric("Equipamentos Vencidos", vencidos)
    with col3:
        conformes = len(df_ativos[df_ativos['status'] == 'Ativo'])
        st.metric("Equipamentos Conformes", conformes)
    with col4:
        conf_pct = (conformes / len(df_ativos) * 100) if len(df_ativos) > 0 else 0
        st.metric("Conformidade NR-13", f"{conf_pct:.1f}%")
    
    st.divider()
    
    st.markdown("### 📋 Equipamentos por Categoria")
    df_por_categoria = df_ativos.groupby('categoria_nr13').size()
    st.bar_chart(df_por_categoria)
    
    st.divider()
    
    st.markdown("### 🚨 Equipamentos Críticos")
    df_criticos = df_ativos[df_ativos['status'] == 'Vencido'].sort_values('data_proxima_externa')
    
    if not df_criticos.empty:
        st.dataframe(
            df_criticos[['tag', 'tipo_equipamento', 'local', 'categoria_nr13', 'data_proxima_externa']],
            use_container_width=True
        )
    else:
        st.success("✅ Nenhum equipamento crítico")
    
    st.divider()
    
    st.markdown("### 📝 Conformidades Detectadas")
    if not df_conformidades.empty:
        st.dataframe(
            df_conformidades[['tag', 'tipo_problema', 'descricao', 'status', 'prioridade']],
            use_container_width=True
        )
    else:
        st.info("Nenhuma conformidade registrada")
    
    st.divider()
    
    st.markdown("### 💾 Exportar Dados")
    
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        csv = df_ativos.to_csv(index=False)
        st.download_button(
            "📥 Baixar Ativos (CSV)",
            csv,
            f"ativos_{datetime.now().strftime('%Y%m%d')}.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col_export2:
        json_str = df_ativos.to_json(orient='records', date_format='iso')
        st.download_button(
            "📥 Baixar Dados (JSON)",
            json_str,
            f"gestao_ativos_{datetime.now().strftime('%Y%m%d')}.json",
            "application/json",
            use_container_width=True
        )

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

def main():
    """Função principal"""
    
    if not st.session_state.cliente_id:
        pagina_login()
        return
    
    with st.sidebar:
        st.markdown(f"<h3 style='color: #00D1FF;'>👤 {st.session_state.cliente_id}</h3>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin: 20px 0;">
            <h2 style="color: #00D1FF;">🛡️</h2>
            <p style="font-size: 12px; color: #999;">Gestão de Ativos NR-13</p>
            <p style="font-size: 10px; color: #666;">Powered by IA</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        empresa = get_empresa(st.session_state.cliente_id)
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
            border-left: 4px solid #00D1FF;
            padding: 15px;
            border-radius: 8px;
        ">
            <h4 style="color: #00D1FF; margin: 0;">📞 Suporte</h4>
            <p style="margin: 5px 0; font-size: 12px; color: #FFFFFF;">
                <b>Felipe Alves Consultoria e Serviços</b><br>
                📱 (81) 99753-8656<br>
                📧 eng.alvescs@gmail.com
            </p>
            <a href="https://wa.me/5581997538656" target="_blank" style="
                display: inline-block;
                background-color: #25D366;
                color: white;
                padding: 8px 12px;
                text-decoration: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 700;
                margin-top: 10px;
                width: 100%;
                text-align: center;
                box-sizing: border-box;
            ">WhatsApp</a>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        pagina = st.radio(
            "Navegação",
            [
                "⚙️ Configuração",
                "📤 Upload",
                "🛡️ Gestão de Ativos",
                "💡 Oportunidades",
                "📊 Relatórios"
            ]
        )
        
        st.divider()
        
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state.cliente_id = None
            st.rerun()
    
    if pagina == "⚙️ Configuração":
        pagina_configuracao()
    elif pagina == "📤 Upload":
        pagina_upload()
    elif pagina == "🛡️ Gestão de Ativos":
        pagina_gestao_ativos()
    elif pagina == "💡 Oportunidades":
        pagina_oportunidades()
    elif pagina == "📊 Relatórios":
        pagina_relatorios()

if __name__ == "__main__":
    main()
