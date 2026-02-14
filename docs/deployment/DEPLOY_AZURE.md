# 🚀 Guia de Deploy - Azure Container Apps

## MedVision AI - Deploy no Azure

### Pré-requisitos
- ✅ Docker Desktop instalado e rodando
- ✅ Conta Microsoft Azure
- ⚙️ Azure CLI (vamos instalar)

---

## PARTE 1: Instalação do Azure CLI

### Windows (PowerShell como Administrador)

```powershell
# Opção 1: Instalador MSI (Recomendado)
# Download direto: https://aka.ms/installazurecliwindows

# Opção 2: Via winget
winget install -e --id Microsoft.AzureCLI

# Opção 3: Via Chocolatey
choco install azure-cli
```

Após instalar, **reinicie o terminal** e verifique:
```powershell
az --version
```

---

## PARTE 2: Login e Configuração Azure

### 2.1 - Login no Azure
```powershell
az login
```
Isso abrirá seu navegador para login.

### 2.2 - Verificar assinatura
```powershell
# Listar assinaturas disponíveis
az account list --output table

# Definir assinatura ativa (se tiver mais de uma)
az account set --subscription "SUBSCRIPTION_ID"
```

### 2.3 - Criar Resource Group
```powershell
# Criar grupo de recursos
az group create --name medvision-rg --location brazilsouth
```

**Localizações disponíveis no Brasil:**
- `brazilsouth` (São Paulo)
- `brazilsoutheast` (Rio de Janeiro)

---

## PARTE 3: Deploy Backend (Azure Container Apps)

### 3.1 - Criar Azure Container Registry (ACR)

```powershell
# Criar registro de containers
az acr create \
  --resource-group medvision-rg \
  --name medvisionacr \
  --sku Basic \
  --admin-enabled true

# Login no ACR
az acr login --name medvisionacr
```

### 3.2 - Build e Push da Imagem Docker

```powershell
cd backend

# Build da imagem
docker build -t medvisionacr.azurecr.io/medvision-backend:latest .

# Push para ACR
docker push medvisionacr.azurecr.io/medvision-backend:latest
```

### 3.3 - Criar Container App Environment

```powershell
# Instalar extensão do Container Apps
az extension add --name containerapp --upgrade

# Criar environment
az containerapp env create \
  --name medvision-env \
  --resource-group medvision-rg \
  --location brazilsouth
```

### 3.4 - Deploy do Backend

```powershell
# Obter credenciais do ACR
$ACR_PASSWORD = az acr credential show --name medvisionacr --query passwords[0].value -o tsv

# Deploy container app
az containerapp create \
  --name medvision-backend \
  --resource-group medvision-rg \
  --environment medvision-env \
  --image medvisionacr.azurecr.io/medvision-backend:latest \
  --registry-server medvisionacr.azurecr.io \
  --registry-username medvisionacr \
  --registry-password $ACR_PASSWORD \
  --target-port 8000 \
  --ingress 'external' \
  --min-replicas 1 \
  --max-replicas 3 \
  --cpu 1.0 \
  --memory 2.0Gi \
  --env-vars \
    ENVIRONMENT=production \
    GEMINI_API_KEY=SUA_CHAVE_AQUI \
    STORAGE_TYPE=local \
    LOG_LEVEL=INFO
```

### 3.5 - Verificar Deploy

```powershell
# Obter URL do backend
az containerapp show \
  --name medvision-backend \
  --resource-group medvision-rg \
  --query properties.configuration.ingress.fqdn -o tsv
```

O backend estará disponível em: `https://medvision-backend.{region}.azurecontainerapps.io`

---

## PARTE 4: Deploy Frontend (Azure Static Web Apps)

### 4.1 - Build do Frontend Local

```powershell
cd frontend

# Instalar dependências
npm install

# Build de produção
npm run build
```

### 4.2 - Deploy via Azure Static Web Apps

```powershell
# Instalar extensão
az extension add --name staticwebapp

# Criar Static Web App
az staticwebapp create \
  --name medvision-frontend \
  --resource-group medvision-rg \
  --source ./dist \
  --location brazilsouth \
  --branch main \
  --app-location "frontend" \
  --output-location "dist"
```

**OU via Portal Azure:**
1. Acesse: https://portal.azure.com
2. Criar recurso → Static Web Apps
3. Conecte seu repositório GitHub
4. Configure build:
   - App location: `/frontend`
   - Output location: `/dist`

### 4.3 - Configurar Variáveis de Ambiente do Frontend

Edite `frontend/.env.production`:
```env
VITE_API_URL=https://medvision-backend.{sua-url}.azurecontainerapps.io
VITE_WS_URL=wss://medvision-backend.{sua-url}.azurecontainerapps.io
```

Rebuild e redeploy:
```powershell
npm run build
az staticwebapp upload --name medvision-frontend --resource-group medvision-rg --source ./dist
```

---

## PARTE 5: Configurar CORS no Backend

Adicione a URL do frontend no arquivo `.env` do backend:

```env
CORS_ORIGINS=["https://medvision-frontend.azurestaticapps.net","http://localhost:5173"]
```

Redeploy do backend:
```powershell
cd backend
docker build -t medvisionacr.azurecr.io/medvision-backend:latest .
docker push medvisionacr.azurecr.io/medvision-backend:latest

# Atualizar container app
az containerapp update \
  --name medvision-backend \
  --resource-group medvision-rg \
  --image medvisionacr.azurecr.io/medvision-backend:latest
```

---

## PARTE 6: Adicionar Redis (Opcional)

```powershell
# Criar Azure Cache for Redis
az redis create \
  --name medvision-redis \
  --resource-group medvision-rg \
  --location brazilsouth \
  --sku Basic \
  --vm-size c0

# Obter connection string
az redis list-keys --name medvision-redis --resource-group medvision-rg

# Atualizar backend com Redis URL
az containerapp update \
  --name medvision-backend \
  --resource-group medvision-rg \
  --set-env-vars REDIS_URL="redis://:{password}@medvision-redis.redis.cache.windows.net:6380?ssl=True"
```

---

## 💰 Estimativa de Custos (Tier Básico)

- **Container Apps:** ~$25-50/mês (1 vCPU, 2GB RAM)
- **Container Registry:** ~$5/mês (Basic)
- **Static Web Apps:** Grátis (tier Free) ou $9/mês (Standard)
- **Redis (opcional):** ~$16/mês (Basic C0)

**Total estimado:** $30-70/mês

---

## 🔧 Comandos Úteis

### Ver logs do backend
```powershell
az containerapp logs show --name medvision-backend --resource-group medvision-rg --follow
```

### Escalar manualmente
```powershell
az containerapp update \
  --name medvision-backend \
  --resource-group medvision-rg \
  --min-replicas 2 \
  --max-replicas 5
```

### Deletar tudo (cuidado!)
```powershell
az group delete --name medvision-rg --yes --no-wait
```

---

## 🎯 Próximos Passos

1. ✅ Instalar Azure CLI
2. ✅ Fazer login: `az login`
3. ✅ Executar script de deploy automatizado: `.\deploy-azure.ps1`
4. ✅ Configurar domínio customizado (opcional)
5. ✅ Configurar CI/CD com GitHub Actions (opcional)

---

## 📚 Links Úteis

- [Azure Container Apps Docs](https://docs.microsoft.com/azure/container-apps/)
- [Azure Static Web Apps Docs](https://docs.microsoft.com/azure/static-web-apps/)
- [Azure CLI Reference](https://docs.microsoft.com/cli/azure/)
- [Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
