# 🚀 GUIA DE DEPLOYMENT - GESTÃO DE ATIVOS COM IA

**Coloque sua aplicação online em 10 minutos!**

---

## 📋 ROTEIRO

1. ✅ Preparar arquivos
2. ✅ Criar repositório GitHub
3. ✅ Fazer upload
4. ✅ Conectar Streamlit Cloud
5. ✅ Deploy automático
6. ✅ Acessar app online

**Tempo total: ~10 minutos**

---

## 🎯 PASSO 1: PREPARAR ARQUIVOS

### Crie pasta local

```bash
mkdir gestao_ativos_nr13
cd gestao_ativos_nr13
```

### Coloque 2 arquivos nela:

```
gestao_ativos_nr13/
├── app_gestao_ativos_ia.py
└── requirements_gestao_ativos.txt
```

### Estrutura pronta? ✅

---

## 🐙 PASSO 2: CRIAR REPOSITÓRIO NO GITHUB

### 2.1 Acesse GitHub

- Vá para: **https://github.com/new**
- Ou clique em "+" > "New repository"

### 2.2 Configure repositório

```
Repository name: gestao-ativos-nr13

Description: Sistema de Gestão de Ativos NR-13 com IA

Visibility: ⦿ Public

☐ Add a README file
☐ Add .gitignore
☐ Choose a license
```

### 2.3 Crie

- Clique em **"Create repository"**

✅ **Repositório criado!**

---

## 📤 PASSO 3: FAZER UPLOAD DOS ARQUIVOS

### Opção A: Via GitHub Web (Mais Fácil) ✅

1. Na página do repositório, clique em **"uploading an existing file"**

2. **Arraste os arquivos** para a área:
   - `app_gestao_ativos_ia.py`
   - `requirements_gestao_ativos.txt`

3. Clique em **"Commit changes"**

✅ **Arquivos no GitHub!**

### Opção B: Via Git (Linha de Comando)

```bash
# 1. Clone o repositório
git clone https://github.com/seu_usuario/gestao-ativos-nr13.git
cd gestao-ativos-nr13

# 2. Copie os arquivos para a pasta
cp /caminho/para/app_gestao_ativos_ia.py .
cp /caminho/para/requirements_gestao_ativos.txt .

# 3. Adicione ao git
git add .

# 4. Commit
git commit -m "Upload app gestão de ativos com IA"

# 5. Push
git push origin main
```

✅ **Arquivos no GitHub!**

---

## ☁️ PASSO 4: CONECTAR STREAMLIT CLOUD

### 4.1 Acesse Streamlit Cloud

- Vá para: **https://streamlit.io/cloud**
- Clique em **"Sign in with GitHub"**
- Autorize o acesso

### 4.2 Crie nova app

- Clique em **"New app"**

### 4.3 Configure

```
Choose repository:
seu_usuario / gestao-ativos-nr13

Branch: main

Main file path: app_gestao_ativos_ia.py
```

### 4.4 Deploy

- Clique em **"Deploy"**

🎉 **Streamlit está compilando!** Pode levar 2-3 minutos...

---

## ✅ PASSO 5: VERIFICAR DEPLOY

### A aplicação está pronta quando:

✅ Página mostra **"Your app is ready!"**  
✅ URL como: `https://seu-usuario-gestao-ativos-nr13.streamlit.app`  
✅ Sem mensagens de erro  

---

## 🌐 PASSO 6: ACESSAR APP ONLINE

### URL da sua app:

```
https://seu-usuario-gestao-ativos-nr13.streamlit.app
```

### Teste:

1. Acesse a URL
2. Crie novo cliente com ID: `teste_2026`
3. Configure dados da empresa
4. Adicione chave Gemini (veja abaixo)
5. Faça upload de documento de teste
6. Veja a IA analisar! 🤖

---

## 🔑 COMO OBTER CHAVE DE IA (GRATUITA)

### Google Gemini (Gratuito) ✅

1. Acesse: **https://ai.google.dev/**
2. Clique em **"Get API Key"**
3. Clique em **"Create API Key"**
4. Escolha **"Create API key in new project"**
5. Copie a chave
6. Cole na app em "Chave de API da IA"

**Limite:** 60 requisições/minuto (gratuito)

### OpenAI (Pago)

1. Acesse: **https://platform.openai.com/api-keys**
2. Clique em **"Create new secret key"**
3. Copie
4. Cole na app

**Custo:** ~$0,01 por análise (mais rápido que Gemini)

---

## 🔄 ATUALIZAR A APP

Quando quiser fazer mudanças:

### Via GitHub Web:

1. Abra seu repositório
2. Clique no arquivo a editar
3. Clique no ✏️ (Edit)
4. Altere o código
5. Clique em **"Commit changes"**
6. Streamlit atualiza automaticamente em 1-2 minutos!

### Via Git Local:

```bash
# 1. Faça mudanças
nano app_gestao_ativos_ia.py

# 2. Commit
git add .
git commit -m "Descrição da mudança"

# 3. Push
git push origin main

# Streamlit atualiza automaticamente!
```

---

## 🐛 TROUBLESHOOTING

### ❌ "App takes too long to load"

**Solução:**
- Clique em **⋯** (menu) > **Settings**
- Tente **"Reboot app"**
- Aguarde 2 minutos

### ❌ "ModuleNotFoundError"

**Solução:**
- Verifique se `requirements_gestao_ativos.txt` está no repositório
- Se não, faça upload dele
- Clique em **Reboot app**

### ❌ "ConnectionError: Failed to connect to API"

**Solução:**
- Chave de API pode estar inválida
- Gere nova chave em https://ai.google.dev/
- Atualize no dashboard da app

### ❌ "Arquivo não encontrado"

**Solução:**
- Arquivo nome pode estar errado
- Nomes devem ser exatos (case-sensitive):
  - `app_gestao_ativos_ia.py` (não `App_Gestao...`)
  - `requirements_gestao_ativos.txt` (não `requirements.txt`)

---

## 📊 USAR MÚLTIPLAS APPS (1 POR CLIENTE)

Se quiser dar acesso direto a clientes, pode criar múltiplas apps:

```
seu-usuario-gestao-ativos-natto.streamlit.app
seu-usuario-gestao-ativos-exemplo.streamlit.app
seu-usuario-gestao-ativos-teste.streamlit.app
```

### Como criar segunda app:

1. Mesmo repositório, crie arquivo `app_cliente_2.py`
2. Em Streamlit Cloud: **New app**
3. Mesmo repositório, arquivo diferente: `app_cliente_2.py`
4. Deploy

Cada app tem seu banco de dados isolado! ✅

---

## 🔒 SEGURANÇA

### API Key está segura?

✅ **Sim!** Suas chaves:
- Não são enviadas para a Anthropic
- Não são registradas em logs públicos
- Ficam locais na app (Streamlit Cloud tem TLS)
- Cliente pode trocar a qualquer hora

### E os dados dos clientes?

✅ **Seguros!** Cada cliente tem:
- Banco SQLite isolado
- Nenhum compartilhamento entre clientes
- Auditoria completa de acesso
- Pode fazer backup do banco

---

## 📱 COMPARTILHAR COM CLIENTE

Após deploy, compartilhe:

```
🎉 Sua app está pronta!

URL: https://seu-usuario-gestao-ativos-nr13.streamlit.app

Como usar:
1. Crie nova conta com ID da sua empresa
2. Configure dados (nome, email, telefone)
3. Adicione chave Gemini (gratuita em ai.google.dev)
4. Faça upload de relatório PDF
5. Veja a IA analisar seus equipamentos!
6. Quando precisar de ajuda, clique "Contatar Felipe"

Precisa de ajuda?
📞 WhatsApp: (81) 99753-8656
📧 Email: eng.alvescs@gmail.com
```

---

## 💾 BACKUP DOS DADOS

Cliente quer backup de seus dados?

1. Em Streamlit Cloud: **⋯ > Settings > App files**
2. Procure pasta `clientes_db`
3. Download do arquivo `cliente_[ID].db`
4. Pronto! Tem copy do banco SQLite

---

## 🚀 PRÓXIMOS PASSOS

- [ ] Deploy concluído
- [ ] App acessível online
- [ ] Chave de IA configurada
- [ ] Primeiro cliente criado
- [ ] Primeiro documento analisado
- [ ] Primeiro WhatsApp enviado para Felipe
- [ ] Primeira venda realizada 💰

---

## ✨ CHECKLIST FINAL

- [ ] Repositório GitHub criado
- [ ] 2 arquivos no repositório
- [ ] Streamlit Cloud conectado
- [ ] App em deploy
- [ ] URL recebida
- [ ] App abre sem erros
- [ ] Teste com ID "teste_2026"
- [ ] Chave Gemini funcionando
- [ ] Upload de arquivo OK
- [ ] IA analisou com sucesso

---

## 📞 DÚVIDAS?

**Felipe Alves Consultoria e Serviços**
- 📱 WhatsApp: **(81) 99753-8656**
- 📧 Email: **eng.alvescs@gmail.com**

Qualquer problema, mande mensagem! ⚡

---

**Pronto? Comece agora! 🚀**
