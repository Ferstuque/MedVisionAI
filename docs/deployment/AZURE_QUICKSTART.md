# 🚀 Quick Start - Deploy Azure MedVision AI

## Passo a Passo Rápido

### 1️⃣ Instalar Azure CLI

**Opção mais fácil - MSI Installer:**
```powershell
# Download direto
Start-Process "https://aka.ms/installazurecliwindows"
```

**Ou via Winget:**
```powershell
winget install -e --id Microsoft.AzureCLI
```

**Após instalar, reinicie o terminal!**

---

### 2️⃣ Login no Azure

```powershell
# Login
az login

# Verificar conta
az account show

# Se tiver múltiplas assinaturas, selecione uma
az account list --output table
az account set --subscription "SUBSCRIPTION_ID"
```

---

### 3️⃣ Definir sua Gemini API Key

```powershell
$env:GEMINI_API_KEY = "sua-chave-gemini-aqui"
```

---

### 4️⃣ Deploy do Backend (Automatizado)

```powershell
cd c:\dev\TechChallengeF04\medvision-ai

# Executar script de deploy
.\deploy-azure.ps1
```

**O script vai:**
- ✅ Criar Resource Group
- ✅ Criar Azure Container Registry (ACR)
- ✅ Fazer build da imagem Docker
- ✅ Push para ACR
- ✅ Criar Container App Environment
- ✅ Deploy do backend no Azure Container Apps
- ✅ Te dar a URL do backend

**Tempo estimado:** 10-15 minutos

---

### 5️⃣ Deploy do Frontend (Opção Simples)

Depois que o backend estiver no ar, você receberá uma URL tipo:
```
https://medvision-backend.brazilsouth-01.azurecontainerapps.io
```

Use essa URL para deploy do frontend:

```powershell
# Deploy via Azure Storage (mais simples)
.\deploy-azure-storage.ps1 -BackendUrl "https://sua-url-backend-aqui"
```

**OU via Static Web Apps (mais recursos):**
```powershell
.\deploy-azure-frontend.ps1 -BackendUrl "https://sua-url-backend-aqui"
```

---

### 6️⃣ Configurar CORS

Após deploy do frontend, adicione a URL do frontend no backend:

```powershell
$frontendUrl = "https://medvisionfrontend.z15.web.core.windows.net"

az containerapp update `
  --name medvision-backend `
  --resource-group medvision-rg `
  --set-env-vars "CORS_ORIGINS=['$frontendUrl','http://localhost:5173']"
```

---

## 🎯 Resumo dos Custos

| Serviço | Tier | Custo/mês (USD) |
|---------|------|-----------------|
| Container Apps | 1 vCPU, 2GB | ~$25-50 |
| Container Registry | Basic | ~$5 |
| Storage (Frontend) | LRS | ~$1-2 |
| **TOTAL ESTIMADO** | | **$30-60/mês** |

---

## 📋 Comandos Úteis

### Ver logs do backend
```powershell
az containerapp logs show --name medvision-backend --resource-group medvision-rg --follow
```

### Ver status
```powershell
az containerapp show --name medvision-backend --resource-group medvision-rg --query properties.runningStatus
```

### Atualizar backend (após mudanças no código)
```powershell
.\deploy-azure.ps1
```

### Deletar tudo (cuidado!)
```powershell
az group delete --name medvision-rg --yes --no-wait
```

---

## ❓ Troubleshooting

### Erro: "Storage account name already taken"
O nome do storage precisa ser único globalmente. Mude no script:
```powershell
.\deploy-azure-storage.ps1 -StorageAccountName "medvision2024frontend" -BackendUrl "..."
```

### Erro: "CORS blocked"
Configure CORS no backend com a URL do frontend.

### Backend não responde
Verifique logs:
```powershell
az containerapp logs show --name medvision-backend --resource-group medvision-rg --follow
```

---

## 🎉 Pronto!

Sua aplicação estará no ar em:
- **Backend:** https://medvision-backend.{region}.azurecontainerapps.io
- **Frontend:** https://{storage-account}.z15.web.core.windows.net
- **API Docs:** https://medvision-backend.{region}.azurecontainerapps.io/docs

---

## 🚀 Melhorias Opcionais

1. **Domínio Customizado:**
   - Configure Azure DNS ou use seu domínio
   - Adicione SSL certificate (Let's Encrypt grátis)

2. **CI/CD com GitHub Actions:**
   - Push para GitHub
   - Configure workflow automático

3. **Monitoramento:**
   - Azure Application Insights
   - Azure Monitor

4. **Backup:**
   - Azure Backup para dados
   - Replicação geo-redundante

---

Para mais detalhes, veja: [DEPLOY_AZURE.md](DEPLOY_AZURE.md)
