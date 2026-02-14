# 🚀 Guia de Deploy - MedVision AI

## Cloud Run (Backend) + Netlify (Frontend)

### Pré-requisitos
- ✅ Docker Desktop instalado e rodando
- ✅ Conta Google Cloud Platform (GCP)
- ✅ Conta Netlify
- ✅ Google Cloud SDK (gcloud CLI) instalado
- ✅ Gemini API Key

---

## PARTE 1: Setup Google Cloud

### 1.1 - Instalar Google Cloud SDK (se necessário)

Download: https://cloud.google.com/sdk/docs/install

### 1.2 - Autenticar e Configurar

```powershell
# Login
gcloud auth login

# Configurar projeto
gcloud config set project SEU_PROJECT_ID

# Ativar APIs necessárias
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

---

## PARTE 2: Deploy Backend no Cloud Run

### 2.1 - Configurar variáveis

Copie `.env.production.example` para `.env.production` e preencha:
- `GEMINI_API_KEY` - sua chave do Gemini

### 2.2 - Build e Push da imagem Docker

```powershell
cd backend

# Build da imagem
docker build -t gcr.io/SEU_PROJECT_ID/medvision-backend:latest .

# Configurar Docker para GCR
gcloud auth configure-docker

# Push para Google Container Registry
docker push gcr.io/SEU_PROJECT_ID/medvision-backend:latest
```

### 2.3 - Deploy no Cloud Run

```powershell
gcloud run deploy medvision-backend \
  --image gcr.io/SEU_PROJECT_ID/medvision-backend:latest \
  --platform managed \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --timeout 3600 \
  --max-instances 10 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=sua-chave-aqui
```

### 2.4 - Anotar URL do Backend

Após deploy, anote a URL gerada (algo como):
`https://medvision-backend-xxxxx-uc.a.run.app`

---

## PARTE 3: Deploy Frontend no Netlify

### 3.1 - Preparar Frontend

Criar arquivo `.env.production` no frontend:

```env
VITE_API_URL=https://medvision-backend-xxxxx-uc.a.run.app
VITE_WS_URL=wss://medvision-backend-xxxxx-uc.a.run.app
VITE_APP_NAME=MedVision AI
VITE_APP_VERSION=1.0.0
```

### 3.2 - Build Local (Teste)

```powershell
cd frontend
npm install
npm run build
```

### 3.3 - Deploy no Netlify

**Opção A: Via Netlify CLI**

```powershell
# Instalar Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod --dir=dist
```

**Opção B: Via Interface Web**

1. Acesse: https://app.netlify.com/
2. Clique em **"Add new site"** → **"Deploy manually"**
3. Arraste a pasta `frontend/dist`
4. Configure Environment Variables:
   - `VITE_API_URL` = URL do Cloud Run
   - `VITE_WS_URL` = URL do Cloud Run (wss://)

### 3.4 - Configurar Custom Domain (Opcional)

No painel Netlify:
- Domain Settings → Add custom domain

---

## PARTE 4: Configurar CORS no Backend

Após ter a URL do Netlify, adicione ao Cloud Run:

```powershell
gcloud run services update medvision-backend \
  --region us-central1 \
  --update-env-vars CORS_ORIGINS='["https://seu-app.netlify.app"]'
```

---

## PARTE 5: Testes Finais

1. Acesse a URL do Netlify
2. Teste upload de vídeo
3. Teste upload de áudio
4. Verifique logs no Cloud Run:

```powershell
gcloud run logs read medvision-backend --region us-central1
```

---

## 📊 Custos Estimados (baixo tráfego)

- **Cloud Run**: ~$5-20/mês (free tier: 2M requests/mês)
- **Container Registry**: ~$1-5/mês
- **Netlify**: Grátis (100GB bandwidth)
- **Gemini API**: Variável (free tier disponível)

---

## 🔧 Troubleshooting

### Backend não inicia
- Verificar logs: `gcloud run logs read medvision-backend`
- Conferir GEMINI_API_KEY configurada
- Checar limites de memória/CPU

### Frontend não conecta ao backend
- Verificar CORS configurado
- Confirmar variáveis VITE_API_URL / VITE_WS_URL
- Testar URL do backend direto no navegador

### WebSocket não funciona
- Cloud Run suporta WebSocket nativamente
- Usar `wss://` (não `ws://`)
- Timeout configurado para 3600s

---

## 📝 Comandos Úteis

```powershell
# Ver logs do Cloud Run
gcloud run logs read medvision-backend --region us-central1 --limit=50

# Atualizar variáveis de ambiente
gcloud run services update medvision-backend --update-env-vars KEY=VALUE

# Ver detalhes do serviço
gcloud run services describe medvision-backend --region us-central1

# Deletar serviço
gcloud run services delete medvision-backend --region us-central1
```

---

## ✅ Checklist Final

- [ ] Projeto GCP criado e configurado
- [ ] APIs habilitadas (Cloud Run, Container Registry)
- [ ] Gemini API Key obtida
- [ ] Backend buildado e pushado para GCR
- [ ] Backend deployado no Cloud Run
- [ ] URL do backend anotada
- [ ] Frontend configurado com URL do backend
- [ ] Frontend deployado no Netlify
- [ ] CORS configurado no backend
- [ ] Testes funcionais realizados
- [ ] Logs verificados

---

**Deploy completo! 🎉**
