# 🛡️ GESTÃO DE ATIVOS NR-13 COM IA - DOCUMENTAÇÃO COMPLETA

**F.A Engenharia - Felipe Alves Consultoria e Serviços**  
**Data:** Março 2026  
**Versão:** 2.0 - Completa com IA

---

## 📋 ÍNDICE

1. [Visão Geral](#visão-geral)
2. [Arquitetura](#arquitetura)
3. [Instalação](#instalação)
4. [Configuração](#configuração)
5. [Como Funciona](#como-funciona)
6. [Funcionalidades](#funcionalidades)
7. [Modelo de Dados](#modelo-de-dados)
8. [Segurança](#segurança)
9. [Troubleshooting](#troubleshooting)
10. [FAQ](#faq)

---

## 🎯 VISÃO GERAL

### O que é?

Sistema web de **gestão de ativos** para empresas sob norma **NR-13**, com:

- ✅ **IA Integrada** - Análise automática de documentos técnicos
- ✅ **Multi-cliente** - Cada cliente tem seu dashboard independente
- ✅ **Custo Zero** - Hospedagem gratuita + IA do cliente
- ✅ **24/7 Online** - Streamlit Cloud sem limite de tempo
- ✅ **WhatsApp Integrado** - Contato automático com Felipe Alves
- ✅ **Banco de Dados Local** - SQLite privado por cliente

### Para quem é?

- Empresas que precisam gerenciar equipamentos NR-13
- Consultores técnicos (Felipe Alves)
- Auditores e conformidade
- Indústrias com equipamentos sob pressão

### Como ganha dinheiro?

```
1. Cliente compra pacote "Gestão de Ativos NR-13"
2. Recebe acesso ao dashboard 24/7
3. Faz upload de documentos (PDF, CSV, Excel)
4. IA analisa e cria gestão automática
5. Sistema detecta problemas
6. Cliente clica "Contatar Felipe"
7. Felipe recebe WhatsApp com oportunidade
8. Felipe vende serviço de consultoria + orçamento
```

---

## 🏗️ ARQUITETURA

### Stack Tecnológico

```
┌─────────────────────────────────────────┐
│         CLIENTE (Browser)                │
│      Upload PDF/CSV/Excel                │
└────────────────┬────────────────────────┘
                 │
        ┌────────▼─────────┐
        │  STREAMLIT CLOUD  │ (Gratuito 24/7)
        │  (app_gestao...)  │
        └────────┬─────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
┌──────────────┐      ┌──────────────┐
│  GOOGLE IA   │      │ SQLite DB    │
│  (Gemini)    │      │ (Local)      │
│  (API Client)│      │ (Privado)    │
└──────────────┘      └──────────────┘
    │
    └──────────────┐
                   ▼
            ┌──────────────┐
            │  WhatsApp    │
            │  (wa.me)     │
            └──────────────┘
```

### Fluxo de Dados

1. **Login** → Cliente identifica-se
2. **Configuração** → Salva API Key (encriptada)
3. **Upload** → Cliente envia documento
4. **Parsing** → Extrai texto de PDF/CSV/Excel
5. **IA Analysis** → Analisa com Gemini/OpenAI
6. **Extração** → Cria lista de equipamentos
7. **Database** → Salva em SQLite local
8. **Gestão** → Dashboard mostra ativos
9. **Detecção** → Identifica problemas
10. **WhatsApp** → Envia alerta para Felipe

---

## 💾 INSTALAÇÃO

### Pré-requisitos

- Python 3.8+
- Conta GitHub
- Conta Streamlit Cloud (gratuita)
- Chave de API: Gemini (gratuita) OU OpenAI (paga)

### Passo 1: Prepare os Arquivos

1. Download dos arquivos:
   - `app_gestao_ativos_ia.py`
   - `requirements_gestao_ativos.txt`

2. Crie pasta no seu computador:
```bash
mkdir gestao_ativos_nr13
cd gestao_ativos_nr13
```

3. Coloque os arquivos lá

### Passo 2: Teste Localmente

```bash
# Instale dependências
pip install -r requirements_gestao_ativos.txt

# Execute
streamlit run app_gestao_ativos_ia.py
```

Acesse: **http://localhost:8501**

### Passo 3: Deploy no GitHub + Streamlit Cloud

#### No GitHub:

1. Crie novo repositório: `gestao-ativos-nr13`
2. Faça upload dos 2 arquivos
3. Copie o link do repositório

#### No Streamlit Cloud:

1. Acesse: https://streamlit.io/cloud
2. Clique "New app"
3. Selecione repositório
4. Configure:
   - Repository: `seu_user/gestao-ativos-nr13`
   - Branch: `main`
   - File: `app_gestao_ativos_ia.py`
5. Clique "Deploy"

✅ **Sua app estará online em 2-3 minutos!**

URL será: `https://seu-usuario-gestao-ativos-nr13.streamlit.app`

---

## ⚙️ CONFIGURAÇÃO

### Para Cliente

1. **Acesse** a app: `https://seu-usuario-gestao-ativos-nr13.streamlit.app`

2. **Crie nova conta** com ID único:
   ```
   ID: empresa_natto_2026
   ```

3. **Configure dados da empresa**:
   - Nome: Natto Alimentos LTDA
   - CNPJ: 00.000.000/0000-00
   - Responsável: João Silva
   - Email: joao@natto.com.br
   - Telefone: (81) 99999-9999

4. **Adicione API Key** (escolha uma):
   - **Opção A: Google Gemini (Gratuito)**
     - Acesse: https://ai.google.dev/
     - Clique "Get API Key"
     - Cole a chave
   
   - **Opção B: OpenAI (Pago)**
     - Acesse: https://platform.openai.com/api-keys
     - Crie nova chave
     - Cole a chave

5. **Teste conexão** → Se OK, salve!

### Para Felipe Alves (Suporte)

- Dashboard mostra **todas as oportunidades** de contato
- Cada cliente gera um banco de dados isolado
- Sem acesso a dados de outros clientes
- Relatórios automáticos de atividade

---

## 📖 COMO FUNCIONA

### Fluxo Completo: Passo a Passo

#### **Semana 1: Cliente faz upload de documentos**

Cliente entra no dashboard e:

1. Clica em "📤 Upload"
2. Arrasta relatório PDF de 50 páginas (relatório técnico NR-13)
3. Sistema mostra: "🤖 Analisando com IA..."
4. IA (Gemini) lê o PDF e extrai:
   - Equipamentos e tags
   - Datas de inspeção
   - Categorias NR-13
   - Fluídos de trabalho
   - Problemas detectados

5. Resultado:
   ```
   ✨ 120 equipamento(s) encontrado(s)!
   
   Resumo: Relatório técnico da planta industrial com 
   análise de 120 equipamentos sob pressão...
   
   ⚠️ Problemas Detectados:
   🔴 Vencimento: 15 equipamentos vencidos
   🟡 Aviso: 8 equipamentos vencem em 30 dias
   ```

#### **Semana 2: Dashboard é populado**

Cliente acessa "🛡️ Gestão de Ativos" e vê:

- 120 equipamentos catalogados
- 97 conformes ✅
- 15 vencidos 🔴
- 8 próximos 30 dias 🟡
- Conformidade: 80.8%

Tabela mostra:
```
TAG            | Tipo          | Local      | Categoria | Status
VP-1.212087    | Vaso Pressão  | Oficina    | V         | Vencido
VP-01/509      | Vaso Pressão  | Sala Máq.  | II        | Vencido
...
```

#### **Semana 3: Cliente detecta oportunidade**

Cliente clica em "💡 Oportunidades" e vê:

```
🔴 VP-1.212087 (Vaso de Pressão)
Tipo: Vencimento de Inspeção Externa
Descrição: Equipamento vencido há 210 dias
Prioridade: Alta
Data Vencimento: 25/08/2025

[📞 Contatar Felipe]
```

Cliente clica no botão **📞 Contatar Felipe**

#### **Semana 4: Felipe recebe oportunidade**

WhatsApp abre automaticamente com:

```
Olá Felipe!

Tenho uma oportunidade de negócio:

📍 Empresa: Natto Alimentos LTDA
🏭 Equipamento: VP-1.212087 (Vaso de Pressão Schulz)
⚠️ Problema: Vencimento de Inspeção Externa
📝 Descrição: Equipamento vencido há 210 dias
⏰ Vencimento: 25/08/2025

Gostaria de um orçamento para regularização.

Acesso ao dashboard: Disponível para consulta.

Obrigado!
```

**Felipe recebe** → Entra em contato → **Vende consultoria + orçamento** 💰

---

## ✨ FUNCIONALIDADES

### 1. **Login Multi-cliente** 👥

```python
# Cada cliente tem ID único
ID: empresa_natto_2026
ID: empresa_exemplo_2026
ID: empresa_teste_2026

# Cada um tem seu banco de dados isolado
clientes_db/
├── cliente_empresa_natto_2026.db
├── cliente_empresa_exemplo_2026.db
└── cliente_empresa_teste_2026.db
```

### 2. **Upload de Documentos** 📤

Suportados:
- **PDF** - Relatórios técnicos (OCR automático)
- **CSV** - Banco de dados de ativos
- **Excel** - Planilhas de equipamentos

Processamento:
```
Upload → Extração → IA Análise → Banco de Dados → Dashboard
```

### 3. **Análise com IA** 🤖

```python
# Sistema envia para IA:
"Analise este relatório NR-13 e extraia:
- Equipamentos (tag, tipo, local)
- Datas de inspeção
- Problemas identificados
- Recomendações"

# IA retorna JSON estruturado
{
  "ativos": [
    {
      "tag": "VP-1.212087",
      "tipo_equipamento": "Vaso de Pressão",
      "categoria_nr13": "V",
      ...
    }
  ],
  "conformidades_detectadas": [...]
}
```

### 4. **Gestão de Ativos** 🛡️

Dashboard com:
- ✅ Tabela de equipamentos editável
- ✅ Filtros (Status, Categoria, Fluído)
- ✅ Métricas (Total, Vencidos, Conformidade)
- ✅ Gráficos (Status, Categoria)
- ✅ Histórico de alterações

### 5. **Detecção de Problemas** ⚠️

Sistema detecta automaticamente:
- Equipamentos vencidos
- Próximos vencimentos (< 30 dias)
- Não conformidades
- Recomendações técnicas

### 6. **Contato WhatsApp** 💬

Botão "Contatar Felipe" gera:
- Link wa.me automático
- Mensagem pré-preenchida
- Contexto completo do problema
- Data/hora de envio registrada

### 7. **Relatórios** 📊

Gerados automaticamente:
- Resumo executivo
- Equipamentos por categoria
- Equipamentos críticos
- Conformidades detectadas
- Exportação CSV/JSON

### 8. **Auditoria** 📝

Registra:
- Quem fez login
- Que documentos foram enviados
- Quais ativos foram criados
- Que contatos foram enviados
- Data e hora de tudo

---

## 💾 MODELO DE DADOS

### Tabela: EMPRESA

```sql
id          | INTEGER (PK)
nome        | TEXT UNIQUE
cnpj        | TEXT
responsavel | TEXT
email       | TEXT
telefone    | TEXT
api_key_ia  | TEXT (encriptada)
tipo_ia     | TEXT (Gemini/OpenAI)
data_criacao| TIMESTAMP
```

### Tabela: ATIVOS

```sql
id                  | INTEGER (PK)
tag                 | TEXT UNIQUE
tipo_equipamento    | TEXT
local               | TEXT
categoria_nr13      | TEXT (I/II/III/IV/V)
fluido              | TEXT
classe_fluido       | TEXT (A/B/C)
data_proxima_externa| DATE
data_proxima_interna| DATE
fabricante          | TEXT
modelo              | TEXT
ano_fabricacao      | INTEGER
status              | TEXT (Ativo/Vencido/Em Manutenção)
observacoes         | TEXT
origem_documento    | TEXT
data_criacao        | TIMESTAMP
data_atualizacao    | TIMESTAMP
```

### Tabela: CONFORMIDADES

```sql
id                  | INTEGER (PK)
ativo_id            | INTEGER (FK)
tipo_problema       | TEXT
descricao           | TEXT
prazo_correcao      | TEXT
status              | TEXT (pendente/resolvido)
prioridade          | TEXT (Alta/Média/Baixa)
data_deteccao       | TIMESTAMP
data_resolucao      | TIMESTAMP
contato_feliz_enviado| BOOLEAN
```

### Tabela: WHATSAPP_ENVIADOS

```sql
id              | INTEGER (PK)
conformidade_id | INTEGER (FK)
mensagem        | TEXT
data_envio      | TIMESTAMP
url_whatsapp    | TEXT
```

---

## 🔐 SEGURANÇA

### Isolamento de Dados

Cada cliente tem:
- ✅ ID único
- ✅ Banco de dados isolado (SQLite)
- ✅ Sem acesso a outros clientes
- ✅ API Key encriptada

### API Key

- ✅ Não é salva em plain text
- ✅ É de propriedade do cliente
- ✅ Sistema não compartilha entre clientes
- ✅ Cliente pode trocar a qualquer hora

### Backup

SQLite permite:
```bash
# Cliente pode fazer backup do seu banco
cp clientes_db/cliente_empresa_natto_2026.db backup.db
```

---

## 🐛 TROUBLESHOOTING

### ❌ "Arquivo não encontrado"
**Solução:** Coloque o arquivo na mesma pasta

### ❌ "ModuleNotFoundError: No module named 'google'"
**Solução:**
```bash
pip install google-generativeai
```

### ❌ "API Key inválida"
**Solução:**
- Verifique se copiou corretamente
- Gere nova chave em https://ai.google.dev/
- Teste a conexão novamente

### ❌ "PDF não conseguiu extrair"
**Solução:**
- PDF pode estar protegido
- Tente converter para imagem primeiro
- Ou envie em CSV/Excel

### ❌ "IA demorou muito"
**Solução:**
- Gemini é gratuito mas pode ficar lento
- Divida documento grande em partes
- Ou use OpenAI (mais rápido)

### ❌ "Banco de dados corrompido"
**Solução:**
```bash
# Delete e recrie
rm clientes_db/cliente_*.db
# Faça novo upload de documentos
```

---

## ❓ FAQ

### P: Quanto custa?
**R:** 
- Streamlit Cloud: GRATUITO
- Gemini API: GRATUITO (limite 60 requisições/min)
- OpenAI: PAGO (~$0,01 por análise)
- Hospedagem: GRATUITO

### P: Quantos clientes posso ter?
**R:** Ilimitado! Cada um em seu banco de dados.

### P: Quanto tempo para analisar um PDF?
**R:** 30 segundos a 2 minutos (depende do tamanho)

### P: Posso usar offline?
**R:** Não. Precisa internet para IA e WhatsApp.

### P: Dados são seguros?
**R:** Sim! Cada cliente tem banco isolado + SQLite local.

### P: Posso exportar dados?
**R:** Sim! CSV, JSON, ou download do banco SQLite.

### P: E se o cliente perde acesso?
**R:** Banco fica na pasta `clientes_db`. Pode recuperar com ID.

### P: Posso customizar?
**R:** Sim! Código está aberto em Python.

### P: Funciona 24/7?
**R:** Sim! Streamlit Cloud roda sem parar.

### P: Como integrar com meu ERP?
**R:** Pode exportar dados em JSON/CSV para qualquer sistema.

---

## 📞 SUPORTE

**Felipe Alves Consultoria e Serviços**

- 📱 WhatsApp: **(81) 99753-8656**
- 📧 Email: **eng.alvescs@gmail.com**
- 🌐 Web: https://wa.me/5581997538656

Disponível para:
- Suporte técnico
- Customizações
- Treinamento de clientes
- Consultoria NR-13

---

## 📊 PRÓXIMOS PASSOS

### Fase 1: MVP (Completo) ✅
- Login multi-cliente
- Upload e análise com IA
- Gestão de ativos
- WhatsApp integrado

### Fase 2: Monetização 💰
- Vender planos (Básico/Pro/Enterprise)
- Adicionar notificações por email
- Relatórios mais detalhados
- Integração com ERP

### Fase 3: Escala 🚀
- API pública para ERP
- Mobile app
- Notificações push
- Inteligência artificial avançada

---

## 📝 VERSÃO & CHANGELOG

**v2.0 (Março 2026)** - VERSÃO COMPLETA COM IA
- ✅ IA integrada (Gemini/OpenAI)
- ✅ Upload multi-formato
- ✅ Multi-cliente escalável
- ✅ WhatsApp automático
- ✅ Relatórios completos
- ✅ Auditoria integrada

**v1.0 (Março 2026)** - MVP
- Login simples
- Upload CSV
- Dashboard básico

---

**Desenvolvido com ❤️ por Claude IA para F.A Engenharia**
