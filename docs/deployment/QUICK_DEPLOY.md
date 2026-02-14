# 🚀 DEPLOY RÁPIDO - MedVision AI

## ✅ Pré-requisitos

Antes de começar, certifique-se de ter:

- [ ] Docker Desktop instalado e rodando ✅
- [ ] Conta Google Cloud (https://console.cloud.google.com/)
- [ ] Conta Netlify (https://app.netlify.com/)
- [ ] Google Cloud SDK instalado (https://cloud.google.com/sdk/docs/install)
- [ ] Gemini API Key (https://aistudio.google.com/app/apikey)

---

## 📝 PASSO 1: Criar Projeto GCP

1. Acesse: https://console.cloud.google.com/
2. Clique em **"Select a project"** → **"New Project"**
3. Nome: `medvision-ai-prod` (ou outro de sua preferência)
4. **ANOTE o PROJECT_ID** (ex: `medvision-ai-prod-123456`)

---

## 📝 PASSO 2: Configurar GCP CLI

Abra o PowerShell e execute:

```powershell
# Login no GCP
gcloud auth login

# Definir seu projeto (substitua SEU_PROJECT_ID)
gcloud config set project SEU_PROJECT_ID

# Ativar APIs necessárias (demora ~1 minuto)
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

## 📝 PASSO 3: Obter Gemini API Key

1. Acesse: https://aistudio.google.com/app/apikey
2. Clique em **"Create API Key"**
3. **COPIE E GUARDE** a chave (formato: `AIzaSy...`)

---

## 📝 PASSO 4: Deploy do Backend

Execute o script PowerShell (substitua os valores):

```powershell
# No diretório raiz do projeto
cd C:\dev\TechChallengeF04\medvision-ai

# Executar script de deploy (substitua PROJECT_ID e GEMINI_KEY)
.\deploy-backend.ps1 -ProjectId "SEU_PROJECT_ID" -GeminiApiKey "SUA_GEMINI_API_KEY"
```

**Aguarde ~5-10 minutos** para o build e deploy.

O script vai mostrar a **URL do backend** no final. Exemplo:
```
https://medvision-backend-xxxxx-uc.a.run.app
```

**COPIE ESSA URL!** ⚠️

---

## 📝 PASSO 5: Configurar Frontend

Edite o arquivo `frontend/.env.production`:

```env
VITE_API_URL=https://medvision-backend-xxxxx-uc.a.run.app
VITE_WS_URL=wss://medvision-backend-xxxxx-uc.a.run.app
VITE_APP_NAME=MedVision AI
VITE_APP_VERSION=1.0.0
```

**Substitua pela URL copiada no passo anterior!**

---

## 📝 PASSO 6: Build do Frontend

```powershell
cd frontend

# Instalar dependências (se necessário)
npm install

# Build de produção
npm run build
```

Aguarde ~1-2 minutos. A pasta `dist/` será criada.

---

## 📝 PASSO 7: Deploy no Netlify

### Opção A: Deploy Manual (Mais Fácil) ⭐

1. Acesse: https://app.netlify.com/
2. Clique em **"Add new site"** → **"Deploy manually"**
3. **Arraste a pasta `frontend/dist`** para o Netlify
4. Aguarde o upload (~30 segundos)
5. **COPIE a URL gerada** (ex: `https://random-name-123.netlify.app`)

### Opção B: Deploy via CLI

```powershell
# Instalar Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
cd frontend
netlify deploy --prod --dir=dist
```

---

## 📝 PASSO 8: Configurar CORS

Agora que você tem a URL do Netlify, configure o CORS no backend:

```powershell
gcloud run services update medvision-backend `
  --region us-central1 `
  --update-env-vars 'CORS_ORIGINS=["https://sua-url.netlify.app","https://www.sua-url.netlify.app"]'
```

**Substitua `sua-url.netlify.app` pela URL do passo 7!**

---

## ✅ PASSO 9: Testar

1. Acesse a URL do Netlify
2. Teste upload de um vídeo
3. Teste upload de um áudio
4. Verifique se os relatórios são gerados

---

## 🔍 Troubleshooting

### ❌ Erro: "gcloud: command not found"
→ Instale o Google Cloud SDK: https://cloud.google.com/sdk/docs/install

### ❌ Backend não conecta
→ Verifique logs:
```powershell
gcloud run logs read medvision-backend --region us-central1 --limit=50
```

### ❌ CORS Error no Frontend
→ Execute novamente o PASSO 8 com a URL correta do Netlify

### ❌ WebSocket não funciona
→ Certifique-se de usar `wss://` (não `ws://`) no `.env.production`

---

## 📊 Custos Aproximados

- **Cloud Run**: ~$5-15/mês (ou grátis no free tier até 2M requests)
- **Storage (GCR)**: ~$1-5/mês
- **Netlify**: Grátis (até 100GB bandwidth)
- **Gemini API**: Variável (free tier: 15 requests/min)

**Total estimado**: $0-20/mês para uso moderado

---

## 🎉 Pronto!

Seu MedVision AI está no ar! 🚀

- **Frontend**: https://sua-url.netlify.app
- **Backend**: https://medvision-backend-xxxxx.run.app

---

## 📞 Comandos Úteis

```powershell
# Ver logs do Cloud Run
gcloud run logs read medvision-backend --region us-central1 --tail

# Atualizar variável de ambiente
gcloud run services update medvision-backend --update-env-vars KEY=VALUE

# Ver status do serviço
gcloud run services describe medvision-backend --region us-central1

# Deletar serviço (cuidado!)
gcloud run services delete medvision-backend --region us-central1
```

---

**Documentação completa**: Ver arquivo `DEPLOY_GUIDE.md`
