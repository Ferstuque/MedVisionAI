# 🎯 Guia de Deploy do Frontend - MedVision AI

## ✅ Backend Já Está Funcionando!

**URL do Backend**: https://medvision-backend.livelycoast-50c79e76.brazilsouth.azurecontainerapps.io

---

## 🚀 Opção 1: Testar Frontend Localmente (RECOMENDADO - Mais Rápido)

### Passo 1: Fazer Login no Azure

Abra um **NOVO terminal PowerShell** e execute:

```powershell
az login
```

Isso abrirá o navegador. Faça login com: **RM366142@fiap.com.br**

### Passo 2: Configurar CORS no Backend

Após o login, execute:

```powershell
cd c:\dev\TechChallengeF04\medvision-ai

$env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"

az containerapp update `
    --name medvision-backend `
    --resource-group medvision-rg `
    --replace-env-vars `
        "ENVIRONMENT=production" `
        "GOOGLE_API_KEY=$env:GEMINI_API_KEY" `
        "STORAGE_TYPE=local" `
        "LOG_LEVEL=INFO" `
        "CORS_ORIGINS=['http://localhost:5173','http://localhost:3000','http://127.0.0.1:5173']"
```

### Passo 3: Executar Frontend Localmente

```powershell
cd frontend
npm install
npm run dev
```

### Passo 4: Testar

Abra o navegador em: **http://localhost:5173**

O frontend local se conectará ao backend Azure! 🎉

---

## ☁️ Opção 2: Deploy Frontend no Azure (Produção)

### 2.1: Usando Azure Container Apps (Recomendado)

Após fazer login (Passo 1 acima):

```powershell
cd c:\dev\TechChallengeF04\medvision-ai

.\deploy-frontend-containerapp.ps1 -BackendUrl "https://medvision-backend.livelycoast-50c79e76.brazilsouth.azurecontainerapps.io"
```

Isso vai:
- Build do frontend com as variáveis corretas
- Criar imagem Docker
- Push para Azure Container Registry
- Deploy no Azure Container Apps
- Configurar ingress externo

**Custo Estimado**: ~$20-30/mês (0.5 vCPU, 1GB RAM)

### 2.2: Usando Azure Storage (Mais Barato)

Após fazer login (Passo 1 acima):

```powershell
cd c:\dev\TechChallengeF04\medvision-ai

.\deploy-azure-storage.ps1 -BackendUrl "https://medvision-backend.livelycoast-50c79e76.brazilsouth.azurecontainerapps.io"
```

Isso vai:
- Build do frontend
- Criar Storage Account
- Habilitar Static Website
- Upload dos arquivos

**Custo Estimado**: ~$1-2/mês

---

## 🔧 Problemas Comuns

### Erro: "Subscription not found"

**Solução**:
```powershell
az logout
az login
az account set --subscription "13077401-c730-49df-9829-1530b4a387b8"
```

### Erro: "Container already exists"

**Solução**:
```powershell
# Atualizar em vez de criar
az containerapp update --name medvision-frontend --resource-group medvision-rg --image medvisionacr.azurecr.io/medvision-frontend:latest
```

### CORS Error no Browser

**Solução**: Adicione a URL do frontend no CORS do backend:

```powershell
az containerapp update `
    --name medvision-backend `
    --resource-group medvision-rg `
    --set-env-vars "CORS_ORIGINS=['https://seu-frontend-url','http://localhost:5173']"
```

---

## 📦 Status Atual do Projeto

### ✅ Completo

- ✅ Backend API funcionando
- ✅ YOLOv8 modelo carregado
- ✅ Gemini AI integrado
- ✅ Health checks passando
- ✅ Docker images no ACR
- ✅ Azure Container Apps backend online

### ⏳ Pendente

- ⏳ Frontend deployado (ou executar localmente)
- ⏳ CORS configurado
- ⏳ Teste end-to-end

---

## 🎬 Teste Rápido

### Backend (já funciona):

```powershell
Invoke-WebRequest https://medvision-backend.livelycoast-50c79e76.brazilsouth.azurecontainerapps.io/health
```

### Frontend Local (após executar npm run dev):

```
http://localhost:5173
```

### Frontend Azure (após deploy): 

```
https://medvision-frontend.xxxxx.brazilsouth.azurecontainerapps.io
```

---

## 💡 **Recomendação**

Para testar rápido: **Use a Opção 1** (frontend local + backend Azure)

Para apresentar/produção: **Deploy com a Opção  2**

---

## 🆘 Precisa de Ajuda?

1. Verifique se está logado: `az account show`
2. Veja logs do backend: `az containerapp logs show --name medvision-backend --resource-group medvision-rg --follow`
3. Teste backend: `curl https://medvision-backend.livelycoast-50c79e76.brazilsouth.azurecontainerapps.io/health`

---

**Última Atualização**: 2026-02-14  
**Status**: ✅ Backend Online | ⏳ Aguardando Frontend
