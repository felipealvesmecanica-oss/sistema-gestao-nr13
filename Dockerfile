FROM python:3.11-slim

WORKDIR /app

COPY requirements_gestao_ativos.txt .
RUN pip install --no-cache-dir -r requirements_gestao_ativos.txt

COPY app_gestao_ativos_ia.py .
COPY .streamlit_config.toml .

EXPOSE 5000

CMD ["streamlit", "run", "app_gestao_ativos_ia.py", "--server.port=5000", "--server.address=0.0.0.0"]
```

4. Clique: **"Commit changes"**

### Passo 2: Deletar Procfile

1. Abra **`Procfile`**

2. Clique: **✏️ Edit**

3. Clique em **"Delete file"** (ícone de lixo)

4. Clique: **"Commit changes"**

### Passo 3: Deploy

1. Em Railway, clique: **"Deploy"**

2. Aguarde 5-10 minutos (Docker leva mais tempo)

3. Deve funcionar! ✅

---

## ✅ SOLUÇÃO 3: Mudar para Streamlit Cloud (Rápido)

Se Railway continuar dando problema, você pode voltar para **Streamlit Cloud** (tão bom quanto):

1. Acesse: **https://streamlit.io/cloud**

2. Clique: **"New app"**

3. Selecione repositório GitHub

4. Deploy em 2 minutos!

---

## 🎯 ESTRUTURA FINAL (Solução 1)

Seu GitHub deve ter:
```
gestao-ativos-nr13/
├── app_gestao_ativos_ia.py
├── requirements_gestao_ativos.txt
├── .streamlit_config.toml
├── Procfile (simplificado)
├── runtime.txt (NOVO!)
├── .railwayignore
└── (outros arquivos markdown)
```

---

## 📝 CHECKLIST SOLUÇÃO 1

- [ ] Criou arquivo `runtime.txt` com `python-3.11.7`
- [ ] Atualizou `Procfile` (removeu `--server.port=$PORT` etc)
- [ ] Commitou ambos os arquivos
- [ ] Railway faz novo deploy
- [ ] Aguarda 3-5 minutos
- [ ] App fica VERDE ✅

---

## ⚡ PASSO A PASSO RÁPIDO (Solução 1)

### **Etapa 1: Criar runtime.txt** (1 min)

GitHub → "Add file" → "Create new file"
- Nome: `runtime.txt`
- Conteúdo: `python-3.11.7`
- Commit

### **Etapa 2: Atualizar Procfile** (1 min)

GitHub → Abrir `Procfile` → Edit
- Apague tudo
- Cole: `web: streamlit run app_gestao_ativos_ia.py`
- Commit

### **Etapa 3: Deploy** (5 min)

Railway → "Deploy"
- Aguarde build
- Deve ficar VERDE ✅

---

## 🔍 SE DER ERRO NOVAMENTE

Tire print do erro e envie com:
- Qual solução tentou (1, 2 ou 3)
- Qual arquivo criou/atualizou
- Mensagem de erro completa

📱 **WhatsApp:** (81) 99753-8656

---

## 💡 POR QUE FUNCIONA

- `runtime.txt` → Diz ao Railway qual versão Python usar
- `Procfile` simplificado → Diz como iniciar a app
- Railway detecta Python e instala tudo certo ✅

---

## ✅ RECOMENDAÇÃO FINAL

**Use SOLUÇÃO 1** (runtime.txt + Procfile simplificado)
- Mais rápida
- Mais simples
- Funciona 99% das vezes

**Se não funcionar:**
- Use SOLUÇÃO 2 (Docker)
- Ou volte para Streamlit Cloud (que funciona com certeza)

---

## 🚀 FAÇA AGORA!

1. Crie `runtime.txt` com `python-3.11.7`
2. Simplifique `Procfile`
3. Deploy no Railway

**Tempo total: 7 minutos** ⚡

---

## 📞 RESULTADO ESPERADO

Após deploy com sucesso:
```
✅ Build › Sucesso
✅ Implantação › Sucesso
✅ Status › ONLINE 🟢
✅ URL › https://sistema-gestao-nr13-production.up.railway.app
