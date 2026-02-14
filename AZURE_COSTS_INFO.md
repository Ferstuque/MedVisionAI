# 💰 Informações de Custos - Azure Container Apps

**Data:** 14 de Fevereiro de 2026  
**Subscription:** Azure subscription 1 (FIAP)  
**Região:** Brazil South  
**Resource Group:** medvision-rg

---

## 📊 Resumo Executivo

O MedVision AI está rodando em **Azure Container Apps** com modelo de cobrança **Pay-as-You-Go** (Consumption-based). Isso significa:

✅ **Você só paga pelo que usar**  
✅ **Sem cobranças quando não há tráfego**  
✅ **Escala automática de 0 a N réplicas**  
✅ **Ideal para MVPs e projetos acadêmicos**  

---

## 🏗️ Recursos Provisionados

### 1. Azure Container Registry (ACR)
- **Nome:** medvisionacr
- **SKU:** **Basic**
- **Pricing:** $0.167/dia (~$5/mês)
- **Storage:** Primeiros 10 GB incluídos
- **Descrição:** Armazena imagens Docker do backend/frontend

**💡 Importante:** Este é o **único recurso com cobrança fixa mensal**, mesmo sem uso.

---

### 2. Azure Container Apps - Backend
- **Nome:** medvision-backend
- **Tipo:** Consumption workload profile
- **CPU:** 1.0 vCPU
- **Memória:** 2.0 Gi
- **Réplicas:** 1 min, 3 max (auto-scaling)

**Cobrança por consumo:**
- **vCPU-s:** $0.000024/segundo por vCPU
- **GiB-s:** $0.000003/segundo por GiB

**Cálculo estimado (1 réplica ativa 24h):**
```
CPU:     1.0 vCPU × 86,400s × $0.000024 = $2.07/dia
Memória: 2.0 GiB  × 86,400s × $0.000003 = $0.52/dia
Total Backend: ~$2.60/dia (~$78/mês) - SE FICAR RODANDO 24/7
```

**🎯 Com tráfego baixo/intermitente:**
- Réplicas reduzem para 1 automaticamente
- Pode escalar para 0 se configurado (zero cost quando idle)
- **Custo real: $0.20-1.00/dia** (~$6-30/mês)

---

### 3. Azure Container Apps - Frontend
- **Nome:** medvision-frontend
- **Tipo:** Consumption workload profile
- **CPU:** 0.5 vCPU
- **Memória:** 1.0 Gi
- **Réplicas:** 1 min, 3 max (auto-scaling)

**Cálculo estimado (1 réplica ativa 24h):**
```
CPU:     0.5 vCPU × 86,400s × $0.000024 = $1.04/dia
Memória: 1.0 GiB  × 86,400s × $0.000003 = $0.26/dia
Total Frontend: ~$1.30/dia (~$39/mês) - SE FICAR RODANDO 24/7
```

**🎯 Com tráfego baixo/intermitente:**
- **Custo real: $0.10-0.50/dia** (~$3-15/mês)

---

### 4. Azure Container Apps Environment
- **Nome:** medvision-env
- **Pricing:** Incluído no preço dos Container Apps
- **Descrição:** Infraestrutura compartilhada (networking, scaling, monitoring)

---

### 5. Log Analytics Workspace
- **Nome:** workspace-medvisionrgN0cH
- **Pricing:** **Pay-as-you-go**
- **Primeiros 5 GB/mês:** **GRATUITOS** ✅
- **Acima de 5 GB:** $2.30/GB

**Estimativa:** ~$0-5/mês (logs básicos de aplicação)

---

## 💵 Custo Total Estimado

### Cenário 1: Uso Contínuo 24/7 (Pior Caso)
```
Azure Container Registry:  $5.00/mês  (fixo)
Backend (24/7):           $78.00/mês
Frontend (24/7):          $39.00/mês
Log Analytics:             $2.00/mês
───────────────────────────────────────
TOTAL:                   ~$124.00/mês
```

### Cenário 2: Uso Intermitente - MVPAcadêmico (Realista) ⭐
```
Azure Container Registry:  $5.00/mês  (fixo)
Backend (tráfego baixo):  $15.00/mês  (auto-scaling)
Frontend (tráfego baixo): $10.00/mês  (auto-scaling)
Log Analytics:             $2.00/mês
───────────────────────────────────────
TOTAL:                    ~$32.00/mês  (~$1.07/dia)
```

### Cenário 3: Sem Uso / Idle
```
Azure Container Registry:  $5.00/mês  (fixo - único custo)
Backend (min replicas=0):  $0.00/mês  (se configurado para escalar para 0)
Frontend (min replicas=0): $0.00/mês  (se configurado para escalar para 0)
Log Analytics:             $0.00/mês  (dentro dos 5GB free tier)
───────────────────────────────────────
TOTAL:                     ~$5.00/mês  ✅
```

---

## ⚙️ Modalidade de Cobrança

### Pay-as-You-Go (Consumo sob demanda)

**Características:**
- ✅ **Sem compromisso de longo prazo**
- ✅ **Pague apenas pelo que usar**
- ✅ **Cancele a qualquer momento**
- ✅ **Ideal para protótipos, MVPs, estudos acadêmicos**
- ⚠️ **Preços podem variar por região**

**Cobrança mensal:** Recursos são somados ao fim do ciclo de faturamento (geralmente até o dia 5 do mês seguinte).

**Sem uso = Sem cobrança?**
- ✅ **Container Apps:** SIM - se escalar para 0 réplicas
- ⚠️ **Container Registry:** NÃO - cobrança fixa mensal (~$5)
- ✅ **Log Analytics:** SIM - primeiros 5GB gratuitos

---

## 🔍 Como Verificar Custos Reais

### 1. Via Portal Azure
1. Acesse: https://portal.azure.com
2. Busque por **"Cost Management + Billing"**
3. Clique em **"Cost analysis"**
4. Filtre por Resource Group: **medvision-rg**
5. Visualize custos diários/mensais

### 2. Via Azure CLI
```powershell
# Custos acumulados do mês atual
az consumption usage list --start-date 2026-02-01 --end-date 2026-02-28

# Custos por recurso
az costmanagement query \
  --type Usage \
  --scope "/subscriptions/<subscription-id>/resourceGroups/medvision-rg" \
  --timeframe MonthToDate
```

### 3. Configurar Alertas de Custo
1. Portal Azure > Cost Management > **Budgets**
2. Criar orçamento mensal (ex: $50)
3. Configurar alerta em 80% e 100%
4. Receber notificações por email

---

## 💡 Dicas para Reduzir Custos

### 1. Escalar para Zero Quando Não Usar
```powershell
# Reduzir réplicas mínimas para 0 (desliga quando idle)
az containerapp update \
  --name medvision-backend \
  --resource-group medvision-rg \
  --min-replicas 0 \
  --max-replicas 3
```

**Resultado:** $0 de custo quando não há tráfego! ✅

### 2. Deletar Registry se Não For Usar
```powershell
# Remover ACR (única cobrança fixa)
az acr delete --name medvisionacr --resource-group medvision-rg
```

**Resultado:** Economiza $5/mês, mas precisa rebuildar imagens se reativar.

### 3. Pausar/Desligar Temporariamente
```powershell
# Parar todas as réplicas
az containerapp update --name medvision-backend --resource-group medvision-rg --min-replicas 0 --max-replicas 0
az containerapp update --name medvision-frontend --resource-group medvision-rg --min-replicas 0 --max-replicas 0
```

**Resultado:** ~$5/mês total (apenas ACR).

### 4. Deletar Tudo Quando Não Precisar
```powershell
# Remover resource group inteiro
az group delete --name medvision-rg --yes --no-wait
```

**Resultado:** **$0/mês** 🎉  
**Atenção:** Dados e configurações são perdidos!

---

## 🎓 Para Projeto Acadêmico - Recomendações

### Opção 1: Manter Ativo Durante Apresentação
- **Período:** 1-2 semanas
- **Custo estimado:** $15-30 total
- **Benefício:** Demo funcionando 24/7, fácil acesso

### Opção 2: Ligar Apenas Para Demos
- **Configuração:** Min replicas = 0
- **Custo:** ~$5/mês (apenas ACR)
- **Benefício:** Economiza ~$27/mês, liga em <30s quando acessar

### Opção 3: Deletar Após Apresentação
- **Configuração:** `az group delete --name medvision-rg`
- **Custo:** $0 após deletar
- **Benefício:** Zero custos, pode reprovisionar depois se necessário

---

## 📞 Suporte e Billing

**Azure Support:**
- Portal: https://portal.azure.com/#blade/Microsoft_Azure_Support/HelpAndSupportBlade
- Phone: +55 11 3957-5647 (Brasil)

**Billing & Invoices:**
- Portal: https://portal.azure.com/#view/Microsoft_Azure_Billing/SubscriptionsBlade

**Azure Pricing Calculator:**
- https://azure.microsoft.com/en-us/pricing/calculator/

---

## ✅ Resumo Final

| Item | Valor Mensal | Observação |
|------|--------------|------------|
| **Custo Fixo (ACR)** | $5.00 | Único custo garantido |
| **Uso Real Estimado** | $32.00 | Com tráfego intermitente |
| **Sem Uso (min=0)** | $5.00 | Escala para zero ✅ |
| **Deletar Tudo** | $0.00 | Reprovisionar depois |

**🎯 Para MVP Acadêmico:** Configurar min-replicas=0 → **~$5/mês quando não usar** ✅

---

**Última Atualização:** 14/02/2026  
**Fontes:**
- [Azure Container Apps Pricing](https://azure.microsoft.com/en-us/pricing/details/container-apps/)
- [Azure Container Registry Pricing](https://azure.microsoft.com/en-us/pricing/details/container-registry/)
- [Azure Log Analytics Pricing](https://azure.microsoft.com/en-us/pricing/details/monitor/)
