import streamlit as st
import pandas as pd
import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
import io
import urllib.parse
from pathlib import Path
import os
import base64

# ============================================================================
# CONFIGURAÇÃO GLOBAL
# ============================================================================

st.set_page_config(
    page_title="Gestão de Ativos NR-13 com IA",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CORES (Dark Theme + Azul Ciano)
PRIMARY_COLOR = "#00D1FF"
SECONDARY_COLOR = "#1f1f1f"
BACKGROUND = "#0f0f0f"
SUCCESS_COLOR = "#00CC96"
WARNING_COLOR = "#FFA15A"
DANGER_COLOR = "#FF6B6B"
TEXT_LIGHT = "#FFFFFF"

# CSS DARK THEME
st.markdown(f"""
    <style>
    :root {{
        --primary-color: {PRIMARY_COLOR};
        --secondary-color: {SECONDARY_COLOR};
        --text-light: {TEXT_LIGHT};
    }}
    
    .stApp {{
        background-color: {BACKGROUND};
        color: {TEXT_LIGHT};
    }}
    
    h1, h2, h3 {{
        color: {PRIMARY_COLOR};
        font-weight: 700;
    }}
    
    .contact-card {{
        background: linear-gradient(135deg, #1a1a1a 0%, #0f0f0f 100%);
        border-left: 4px solid {PRIMARY_COLOR};
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }}
    
    .contact-card-title {{
        color: {PRIMARY_COLOR};
        font-weight: 700;
        font-size: 18px;
    }}
    
    .contact-card-info {{
        color: {TEXT_LIGHT};
        font-size: 14px;
        margin-top: 5px;
    }}
    
    .alert-vencido {{
        background-color: rgba(255, 107, 107, 0.1);
        border: 2px solid {DANGER_COLOR};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }}
    
    .alert-warning {{
        background-color: rgba(255, 161, 90, 0.1);
        border: 2px solid {WARNING_COLOR};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }}
    
    .alert-ok {{
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
        border-radius: 6px;
        padding: 10px 20px;
        width: 100%;
    }}
    
    .stButton > button:hover {{
        background-color: #00A8CC;
        color: {TEXT_LIGHT};
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 5px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: #1a1a1a;
        border-bottom: 2px solid #333;
        color: {TEXT_LIGHT};
    }}
    
    .stTabs [aria-selected="true"] {{
        border-bottom: 3px solid {PRIMARY_COLOR};
        color: {PRIMARY_COLOR};
    }}
    
    .watermark {{
        position: fixed;
        bottom: 15px;
        right: 15px;
        opacity: 0.05;
        z-index: -1;
        font-size: 48px;
        font-weight: bold;
        color: {PRIMARY_COLOR};
    }}
    </style>
    <div class="watermark">F.A Engenharia</div>
""", unsafe_allow_html=True)

# ============================================================================
# INICIALIZAÇÃO
# ============================================================================

def init_session_state():
    if 'cliente_logado' not in st.session_state:
        st.session_state.cliente_logado = False
    if 'cliente_config' not in st.session_state:
        st.session_state.cliente_config = None
    if 'db_path' not in st.session_state:
        st.session_state.db_path = None

init_session_state()

# ============================================================================
# BANCO DE DADOS
# ============================================================================

def criar_banco_dados(cnpj):
    """Cria banco de dados SQLite para cada cliente"""
    if not os.path.exists('clientes'):
        os.makedirs('clientes')
    
    db_path = f'clientes/{cnpj}.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Tabela: Empresa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empresa (
            id INTEGER PRIMARY KEY,
            cnpj TEXT UNIQUE,
            nome TEXT NOT NULL,
            responsavel TEXT,
            email TEXT,
            telefone TEXT,
            whatsapp TEXT,
            api_key_ia TEXT,
            tipo_ia TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela: Ativos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ativos (
            id INTEGER PRIMARY KEY,
            tag TEXT UNIQUE NOT NULL,
            tipo_equipamento TEXT,
            local TEXT,
            categoria_nr13 TEXT,
            fluido TEXT,
            classe_fluido TEXT,
            data_proxima_externa TEXT,
            data_proxima_interna TEXT,
            fabricante TEXT,
            modelo TEXT,
            ano_fabricacao INTEGER,
            status TEXT DEFAULT 'Ativo',
            observacoes TEXT,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela: Documentos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY,
            nome_arquivo TEXT,
            tipo_arquivo TEXT,
            conteudo_analisado TEXT,
            resumo_analisa_ia TEXT,
            ativos_extraidos INTEGER DEFAULT 0,
            data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela: Conformidades
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conformidades (
            id INTEGER PRIMARY KEY,
            ativo_id INTEGER,
            tipo_problema TEXT,
            descricao TEXT,
            prazo_correcao TEXT,
            status TEXT DEFAULT 'pendente',
            prioridade TEXT DEFAULT 'media',
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_resolucao TIMESTAMP,
            FOREIGN KEY (ativo_id) REFERENCES ativos(id)
        )
    ''')
    
    # Tabela: Histórico WhatsApp
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_whatsapp (
            id INTEGER PRIMARY KEY,
            conformidade_id INTEGER,
            mensagem TEXT,
            url_whatsapp TEXT,
            data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conformidade_id) REFERENCES conformidades(id)
        )
    ''')
    
    conn.commit()
    return db_path, conn

def executar_query(db_path, query, params=None):
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        conn.commit()
        resultado = cursor.fetchall()
        conn.close()
        return resultado
    except Exception as e:
        st.error(f"Erro no banco de dados: {str(e)}")
        return None

def obter_empresa(db_path):
    query = "SELECT * FROM empresa LIMIT 1"
    resultado = executar_query(db_path, query)
    if resultado:
        return dict(resultado[0])
    return None

def salvar_empresa(db_path, cnpj, nome, responsavel, email, telefone, whatsapp, api_key, tipo_ia):
    api_key_encoded = base64.b64encode(api_key.encode()).decode()
    
    query = '''
        INSERT OR REPLACE INTO empresa 
        (cnpj, nome, responsavel, email, telefone, whatsapp, api_key_ia, tipo_ia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    params = (cnpj, nome, responsavel, email, telefone, whatsapp, api_key_encoded, tipo_ia)
    executar_query(db_path, query, params)

def obter_ativos(db_path):
    query = "SELECT * FROM ativos ORDER BY data_criacao DESC"
    resultado = executar_query(db_path, query)
    if resultado:
        return [dict(row) for row in resultado]
    return []

def salvar_ativo(db_path, ativo_dict):
    query = '''
        INSERT OR REPLACE INTO ativos 
        (tag, tipo_equipamento, local, categoria_nr13, fluido, classe_fluido,
         data_proxima_externa, data_proxima_interna, fabricante, modelo,
         ano_fabricacao, status, observacoes, data_atualizacao)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    '''
    params = (
        ativo_dict.get('tag'),
        ativo_dict.get('tipo_equipamento'),
        ativo_dict.get('local'),
        ativo_dict.get('categoria_nr13'),
        ativo_dict.get('fluido'),
        ativo_dict.get('classe_fluido'),
        ativo_dict.get('data_proxima_externa'),
        ativo_dict.get('data_proxima_interna'),
        ativo_dict.get('fabricante'),
        ativo_dict.get('modelo'),
        ativo_dict.get('ano_fabricacao'),
        ativo_dict.get('status', 'Ativo'),
        ativo_dict.get('observacoes')
    )
    executar_query(db_path, query, params)

# ============================================================================
# EXTRAÇÃO DE DOCUMENTOS
# ============================================================================

def extrair_pdf(arquivo_pdf):
    try:
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(arquivo_pdf)
        texto = ""
        for page in pdf_reader.pages:
            texto += page.extract_text()
        return texto
    except Exception as e:
        st.error(f"Erro ao ler PDF: {str(e)}")
        return None

def extrair_csv(arquivo_csv):
    try:
        df = pd.read_csv(arquivo_csv)
        return df.to_json(orient='records')
    except Exception as e:
        st.error(f"Erro ao ler CSV: {str(e)}")
        return None

def extrair_excel(arquivo_excel):
    try:
        df = pd.read_excel(arquivo_excel)
        return df.to_json(orient='records')
    except Exception as e:
        st.error(f"Erro ao ler Excel: {str(e)}")
        return None

def processar_documento(arquivo, tipo_arquivo):
    if tipo_arquivo == 'pdf':
        return extrair_pdf(arquivo)
    elif tipo_arquivo == 'csv':
        return extrair_csv(arquivo)
    elif tipo_arquivo in ['xls', 'xlsx']:
        return extrair_excel(arquivo)
    else:
        st.error(f"Tipo de arquivo não suportado: {tipo_arquivo}")
        return None

# ============================================================================
# FUNÇÕES UTILITÁRIAS
# ============================================================================

def calcular_dias_vencimento(data_str):
    try:
        data_inspecao = datetime.strptime(data_str, "%Y-%m-%d")
        data_referencia = datetime.now()
        dias = (data_inspecao - data_referencia).days
        return dias
    except:
        return None

def verificar_itens_vencidos(ativos):
    vencidos = []
    for ativo in ativos:
        dias_ext = calcular_dias_vencimento(ativo.get('data_proxima_externa', '2025-01-01'))
        dias_int = calcular_dias_vencimento(ativo.get('data_proxima_interna', '2025-01-01'))
        
        if dias_ext and dias_ext <= 0:
            vencidos.append({
                'tag': ativo.get('tag'),
                'tipo': ativo.get('tipo_equipamento'),
                'dias_vencidos': dias_ext,
                'tipo_vencimento': 'Externa'
            })
        
        if dias_int and dias_int <= 0:
            vencidos.append({
                'tag': ativo.get('tag'),
                'tipo': ativo.get('tipo_equipamento'),
                'dias_vencidos': dias_int,
                'tipo_vencimento': 'Interna'
            })
    
    return vencidos

def calcular_conformidade(ativos):
    if not ativos:
        return 0
    
    total = len(ativos)
    vencidos = len(verificar_itens_vencidos(ativos))
    conformidade = ((total - vencidos) / total * 100) if total > 0 else 0
    return conformidade

def gerar_link_whatsapp(telefone, ativo_tag, empresa_nome, dias_vencido):
    mensagem = f"""Olá Felipe, a empresa {empresa_nome} tem o equipamento {ativo_tag} vencido há {abs(dias_vencido)} dias. Solicito orçamento para regularização."""
    
    msg_encoded = urllib.parse.quote(mensagem)
    telefone_clean = telefone.replace("+", "").replace("-", "").replace(" ", "")
    
    return f"https://wa.me/{telefone_clean}?text={msg_encoded}"

# ============================================================================
# INTEGRAÇÃO COM IA (Gemini, OpenAI, Claude)
# ============================================================================

def analisar_com_ia(api_key_encoded, tipo_ia, prompt):
    try:
        api_key = base64.b64decode(api_key_encoded).decode()
        
        if tipo_ia == "Gemini":
            return analisar_gemini(api_key, prompt)
        elif tipo_ia == "OpenAI":
            return analisar_openai(api_key, prompt)
        elif tipo_ia == "Claude":
            return analisar_claude(api_key, prompt)
    except Exception as e:
        st.error(f"Erro ao análisar com IA: {str(e)}")
        return None

def analisar_gemini(api_key, prompt):
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Erro Gemini: {str(e)}")
        return None

def analisar_openai(api_key, prompt):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Erro OpenAI: {str(e)}")
        return None

def analisar_claude(api_key, prompt):
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        st.error(f"Erro Claude: {str(e)}")
        return None

# ============================================================================
# PÁGINA: LOGIN
# ============================================================================

def pagina_login():
    st.markdown("<h1 style='color: #00D1FF;'>🛡️ Gestão de Ativos NR-13 com IA</h1>", unsafe_allow_html=True)
    st.markdown("*Sistema inteligente de análise e gestão de equipamentos sob norma NR-13*")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Dados da Empresa")
        
        cnpj = st.text_input("CNPJ (sem formatação)", placeholder="00000000000000")
        nome_empresa = st.text_input("Nome da Empresa")
        responsavel = st.text_input("Responsável Técnico")
        email = st.text_input("Email da Empresa")
        telefone = st.text_input("Telefone")
        whatsapp = st.text_input("WhatsApp com +55", placeholder="+5581999999999")
    
    with col2:
        st.markdown("### 🤖 Configuração de IA")
        
        tipo_ia = st.selectbox(
            "Escolha seu provedor de IA",
            ["Gemini (Google - Gratuito)", "OpenAI (ChatGPT)", "Claude (Anthropic)"]
        )
        
        if "Gemini" in tipo_ia:
            tipo_ia_short = "Gemini"
            st.success("✅ **Gemini é GRATUITO!**\n\nObtenha em: https://ai.google.dev/tutorials/python_quickstart")
        elif "OpenAI" in tipo_ia:
            tipo_ia_short = "OpenAI"
            st.info("📌 Obtenha sua chave em: https://platform.openai.com/api-keys")
        else:
            tipo_ia_short = "Claude"
            st.info("📌 Obtenha sua chave em: https://console.anthropic.com")
        
        api_key = st.text_input("Cole sua API Key aqui", type="password")
    
    st.divider()
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("✅ Entrar / Cadastrar", use_container_width=True):
            if not cnpj or not nome_empresa or not api_key:
                st.error("❌ Preencha todos os campos obrigatórios!")
            else:
                db_path, conn = criar_banco_dados(cnpj)
                conn.close()
                
                salvar_empresa(db_path, cnpj, nome_empresa, responsavel, email, telefone, whatsapp, api_key, tipo_ia_short)
                
                st.session_state.cliente_logado = True
                st.session_state.cliente_config = {
                    'cnpj': cnpj,
                    'nome': nome_empresa,
                    'responsavel': responsavel,
                    'email': email,
                    'telefone': telefone,
                    'whatsapp': whatsapp,
                    'tipo_ia': tipo_ia_short
                }
                st.session_state.db_path = db_path
                
                st.success("✅ Login realizado com sucesso!")
                st.rerun()
    
    with col_btn2:
        st.info("💡 Use Gemini (gratuito) para começar sem custos!")
    
    st.divider()
    
    st.markdown("### 📞 Contato - Felipe Alves Consultoria")
    st.markdown(f"""
    <div class="contact-card">
        <div class="contact-card-title">Felipe Alves Consultoria e Serviços</div>
        <div class="contact-card-info">
            <b>WhatsApp:</b> (81) 99753-8656<br>
            <b>Email:</b> eng.alvescs@gmail.com<br>
            <a href="https://wa.me/5581997538656" target="_blank" style="color: #00D1FF; text-decoration: none;">
                💬 Enviar WhatsApp →
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# PÁGINA: DASHBOARD
# ============================================================================

def pagina_dashboard():
    
    col_titulo, col_contato = st.columns([2, 1])
    
    with col_titulo:
        st.markdown(f"<h1 style='color: #00D1FF;'>🛡️ Gestão de Ativos - {st.session_state.cliente_config['nome']}</h1>", unsafe_allow_html=True)
    
    with col_contato:
        st.markdown(f"""
        <div class="contact-card">
            <div class="contact-card-title">Felipe Alves</div>
            <div class="contact-card-info">
                <b>WhatsApp:</b> (81) 99753-8656<br>
                <a href="https://wa.me/5581997538656" target="_blank" style="color: #00D1FF; text-decoration: none;">
                    💬 Contatar →
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    ativos = obter_ativos(st.session_state.db_path)
    vencidos = verificar_itens_vencidos(ativos)
    conformidade_pct = calcular_conformidade(ativos)
    
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("📦 Total de Ativos", len(ativos))
    
    with m2:
        a_vencer = len([x for x in ativos if calcular_dias_vencimento(x.get('data_proxima_externa', '2025-01-01')) and 0 < calcular_dias_vencimento(x.get('data_proxima_externa', '2025-01-01')) <= 30])
        st.metric("⏰ A Vencer (30 dias)", a_vencer)
    
    with m3:
        st.metric("🔴 Vencidos", len(vencidos), delta_color="inverse")
    
    with m4:
        st.metric("✅ Conformidade NR-13", f"{conformidade_pct:.0f}%")
    
    st.divider()
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Inventário",
        "📁 Upload de Documentos",
        "💡 Recomendações",
        "📊 Relatórios",
        "⚙️ Configurações",
        "🚪 Sair"
    ])
    
    # ==================== ABA 1: INVENTÁRIO ====================
    with tab1:
        st.markdown("<h3 style='color: #00D1FF;'>📋 Base de Dados de Ativos</h3>", unsafe_allow_html=True)
        
        if len(ativos) > 0:
            df_ativos = pd.DataFrame(ativos)
            st.dataframe(df_ativos, use_container_width=True, hide_index=True)
        else:
            st.info("📭 Nenhum ativo registrado ainda. Faça upload de um documento para começar!")
    
    # ==================== ABA 2: UPLOAD ====================
    with tab2:
        st.markdown("<h3 style='color: #00D1FF;'>📁 Upload de Documentos com Análise IA</h3>", unsafe_allow_html=True)
        
        st.markdown("📄 Envie relatórios técnicos, planilhas ou documentos. A IA analisará automaticamente!")
        
        arquivo_upload = st.file_uploader(
            "Escolha um arquivo (PDF, CSV, Excel)",
            type=['pdf', 'csv', 'xlsx', 'xls']
        )
        
        if arquivo_upload:
            tipo_arquivo = arquivo_upload.name.split('.')[-1]
            
            with st.spinner("🔍 Processando documento com IA..."):
                conteudo = processar_documento(arquivo_upload, tipo_arquivo)
                
                if conteudo:
                    st.success("✅ Documento processado!")
                    
                    empresa = obter_empresa(st.session_state.db_path)
                    
                    if empresa and empresa.get('api_key_ia'):
                        prompt = f"""Você é um especialista em NR-13. Analise este documento e extraia em JSON:

{{
    "ativos": [
        {{
            "tag": "ID único",
            "tipo_equipamento": "tipo",
            "local": "localização",
            "categoria_nr13": "I/II/III/IV/V",
            "fluido": "fluído",
            "classe_fluido": "A/B/C",
            "data_proxima_externa": "YYYY-MM-DD",
            "data_proxima_interna": "YYYY-MM-DD",
            "fabricante": "marca",
            "modelo": "modelo",
            "ano_fabricacao": 2020
        }}
    ],
    "problemas": [
        {{
            "tipo": "vencimento/não_conformidade",
            "descricao": "descrição",
            "severidade": "alta/media/baixa"
        }}
    ],
    "resumo": "resumo executivo"
}}

Documento: {conteudo[:3000]}

RETORNE APENAS O JSON."""
                        
                        resposta_ia = analisar_com_ia(empresa['api_key_ia'], empresa['tipo_ia'], prompt)
                        
                        if resposta_ia:
                            try:
                                resposta_limpa = resposta_ia.strip()
                                if '```' in resposta_limpa:
                                    resposta_limpa = resposta_limpa.split('```')[1]
                                    if resposta_limpa.startswith('json'):
                                        resposta_limpa = resposta_limpa[4:]
                                
                                dados_ia = json.loads(resposta_limpa)
                                
                                st.markdown("### 🤖 Análise da IA")
                                
                                if dados_ia.get('ativos'):
                                    st.markdown(f"**✅ {len(dados_ia['ativos'])} equipamentos encontrados**")
                                    
                                    if st.button("➕ Adicionar todos ao sistema"):
                                        contador = 0
                                        for ativo in dados_ia['ativos']:
                                            try:
                                                salvar_ativo(st.session_state.db_path, ativo)
                                                contador += 1
                                            except:
                                                pass
                                        
                                        st.success(f"✅ {contador} ativos adicionados!")
                                        st.rerun()
                                    
                                    with st.expander("📋 Ver detalhes dos equipamentos"):
                                        for ativo in dados_ia['ativos'][:5]:
                                            st.json(ativo)
                                
                                if dados_ia.get('problemas'):
                                    st.markdown("### ⚠️ Problemas Detectados")
                                    
                                    for problema in dados_ia['problemas']:
                                        icon = "🔴" if problema.get('severidade') == 'alta' else "🟡" if problema.get('severidade') == 'media' else "🟢"
                                        st.markdown(f"**{icon} {problema.get('tipo')}:** {problema.get('descricao')}")
                                
                                if dados_ia.get('resumo'):
                                    st.markdown("### 📋 Resumo Executivo")
                                    st.info(dados_ia['resumo'])
                            
                            except json.JSONDecodeError:
                                st.error("❌ Erro ao processar resposta IA")
                        else:
                            st.error("❌ Erro na IA. Verifique sua API Key.")
                    else:
                        st.error("❌ Configure sua API Key nas Configurações")
    
    # ==================== ABA 3: RECOMENDAÇÕES ====================
    with tab3:
        st.markdown("<h3 style='color: #00D1FF;'>💡 Recomendações e Alertas</h3>", unsafe_allow_html=True)
        
        if len(vencidos) > 0:
            st.markdown("""
            <div class="alert-vencido">
                <b>🚨 ALERTAS CRÍTICOS!</b><br>
                Equipamentos com inspeção vencida detectados.
            </div>
            """, unsafe_allow_html=True)
            
            for item_vencido in vencidos:
                col_info, col_acao = st.columns([3, 1])
                
                with col_info:
                    st.markdown(f"""
                    <div class="alert-vencido">
                        <b>Tag:</b> {item_vencido['tag']}<br>
                        <b>Tipo:</b> {item_vencido['tipo']}<br>
                        <b>Vencido há:</b> <span style='color: #FF6B6B;'>{abs(item_vencido['dias_vencidos'])} dias</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_acao:
                    link_wa = gerar_link_whatsapp(
                        st.session_state.cliente_config['whatsapp'],
                        item_vencido['tag'],
                        st.session_state.cliente_config['nome'],
                        item_vencido['dias_vencidos']
                    )
                    
                    st.markdown(f"""
                    <a href="{link_wa}" target="_blank">
                        <button style="background-color: #00D1FF; color: #000; padding: 8px; border: none; border-radius: 6px; cursor: pointer; font-weight: 700; width: 100%;">
                            💬 Contatar
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="alert-ok">
                <b>✅ Tudo em dia!</b><br>
                Nenhum equipamento vencido.
            </div>
            """, unsafe_allow_html=True)
    
    # ==================== ABA 4: RELATÓRIOS ====================
    with tab4:
        st.markdown("<h3 style='color: #00D1FF;'>📊 Relatórios</h3>", unsafe_allow_html=True)
        
        col_rel1, col_rel2 = st.columns(2)
        
        with col_rel1:
            st.markdown("**Status dos Ativos**")
            if ativos:
                status_count = pd.Series([a.get('status', 'Desconhecido') for a in ativos]).value_counts()
                st.bar_chart(status_count)
        
        with col_rel2:
            st.markdown("**Categoria NR-13**")
            if ativos:
                cat_count = pd.Series([a.get('categoria_nr13', 'N/A') for a in ativos]).value_counts()
                st.bar_chart(cat_count)
        
        st.divider()
        
        if st.button("📥 Baixar Relatório em CSV"):
            if ativos:
                df = pd.DataFrame(ativos)
                csv = df.to_csv(index=False, encoding='utf-8')
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"ativos_{st.session_state.cliente_config['cnpj']}.csv",
                    mime="text/csv"
                )
            else:
                st.warning("Nenhum ativo para exportar")
    
    # ==================== ABA 5: CONFIGURAÇÕES ====================
    with tab5:
        st.markdown("<h3 style='color: #00D1FF;'>⚙️ Configurações</h3>", unsafe_allow_html=True)
        
        empresa = obter_empresa(st.session_state.db_path)
        
        if empresa:
            col_c1, col_c2 = st.columns(2)
            
            with col_c1:
                st.text_input("CNPJ", value=empresa['cnpj'], disabled=True)
                st.text_input("Responsável", value=empresa['responsavel'], disabled=True)
            
            with col_c2:
                st.text_input("Email", value=empresa['email'], disabled=True)
                st.text_input("WhatsApp", value=empresa['whatsapp'], disabled=True)
            
            st.markdown(f"**IA Configurada:** {empresa['tipo_ia']}")
    
    # ==================== ABA 6: SAIR ====================
    with tab6:
        st.markdown("<h3 style='color: #00D1FF;'>🚪 Sair</h3>", unsafe_allow_html=True)
        
        if st.button("Logout", use_container_width=True):
            st.session_state.cliente_logado = False
            st.session_state.cliente_config = None
            st.session_state.db_path = None
            st.rerun()

# ============================================================================
# MAIN
# ============================================================================

def main():
    if st.session_state.cliente_logado:
        pagina_dashboard()
    else:
        pagina_login()

if __name__ == "__main__":
    main()
