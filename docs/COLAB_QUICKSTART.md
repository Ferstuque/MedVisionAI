# 🚀 Guia Rápido: Fine-Tuning no Google Colab

## 📋 Preparação (Faça ANTES de abrir o Colab):

### 1️⃣ Compactar Dataset

No PowerShell:
```powershell
cd C:\dev\TechChallengeF04
Compress-Archive -Path "Instrument_Anatomy_Original_Dataset" -DestinationPath "Instrument_Anatomy_Original_Dataset.zip"
```

**Aguarde:** ~5-10 minutos (12,394 imagens)

### 2️⃣ Upload para Google Drive (Recomendado)

1. Acesse: https://drive.google.com
2. Crie pasta: `MedVision_AI`
3. Faça upload: `Instrument_Anatomy_Original_Dataset.zip`
4. **Aguarde upload completar** (pode levar 30-60 min dependendo da internet)

---

## 🎓 Executar Treinamento no Colab:

### Passo 1: Abrir Notebook

1. Acesse: https://colab.research.google.com
2. **Upload notebook:**
   - File > Upload notebook
   - Selecione: `notebooks/FINE_TUNING_GYNSURGE_COLAB.ipynb`

### Passo 2: Ativar GPU

- Runtime > Change runtime type
- **Hardware accelerator:** GPU
- **GPU type:** T4 (gratuito)
- Save

### Passo 3: Executar Células

Execute **uma célula por vez** (Shift+Enter):

1. ✅ **Setup Inicial** - Instala dependências (~1 min)
2. ✅ **Upload Dataset** - Monta Google Drive (~30 seg)
3. ✅ **Conversão COCO→YOLO** - Processa anotações (~10-15 min)
4. ✅ **Configurar Treinamento** - Define hyperparmetros (~5 seg)
5. ⏱️  **TREINAR** - **AGUARDE 2-3 HORAS!** ☕🍕
6. ✅ **Visualizar Resultados** - Gráficos (~10 seg)
7. ✅ **Validar Modelo** - Métricas finais (~2 min)
8. ✅ **Testar Imagem** - Exemplo de detecção (~10 seg)
9. 💾 **Salvar no Google Drive** - AUTOMÁTICO! (~5 seg)
10. ✅ **Download Opcional** - Alternativa via navegador

---

## ⏱️ Timeline Estimado:

```
00:00 - Setup e upload dataset         (~15 min)
00:15 - Conversão COCO→YOLO           (~15 min)
00:30 - Início do treinamento
02:30 - Fim do treinamento (100 épocas)
02:35 - Validação e download
02:40 - FIM! Modelo pronto! ✅
```

---

## 📊 O que Observar Durante Treinamento:

### Métricas Boas:
- ✅ `box_loss` diminuindo consistentemente
- ✅ `cls_loss` diminuindo consistentemente
- ✅ `mAP50` aumentando (meta: >0.5, excelente: >0.7)

### Sinais de Problemas:
- ⚠️ Loss oscilando muito (reduza learning rate)
- ⚠️ CUDA OOM (reduza batch_size para 8)
- ⚠️ mAP50 < 0.3 após 50 épocas (problema nos dados)

---

## 💾 Salvamento Automático no Google Drive! 🎉

### ✨ NOVIDADE: Modelo Salvo Automaticamente!

O notebook agora **salva automaticamente** o modelo treinado no seu Google Drive, na **mesma pasta do dataset**!

Após o treinamento (Passo 8), o modelo é salvo como:
- ✅ `yolov8_gyneco_LATEST.pt` - Sempre a versão mais recente
- ✅ `yolov8_gyneco_YYYYMMDD_HHMMSS.pt` - Versão com timestamp
- ✅ `yolov8_gyneco_last.pt` - Último checkpoint

**Vantagens:**
- 🚀 Sem necessidade de download manual
- 💾 Modelo fica seguro no Drive (não perde se desconectar)
- 📅 Versionamento automático com timestamps
- ⚡ Acesso direto pelo Windows Explorer (Drive Desktop)

---

## 📥 Após Treinamento:

### 1. Baixar do Google Drive

Acesse seu Google Drive:
- Navegue até: **`Meu Drive/MedVision_AI/`** (ou pasta configurada)
- Baixe: **`yolov8_gyneco_LATEST.pt`** ← Use este!

**OU** se tiver Google Drive Desktop instalado:
```powershell
# Acesso direto via Windows Explorer
G:\Meu Drive\MedVision_AI\yolov8_gyneco_LATEST.pt
```

### 2. Copiar para Backend
```powershell
# Opção 1: Baixado via navegador
copy "C:\Users\SEU_NOME\Downloads\yolov8_gyneco_LATEST.pt" ^
     C:\dev\TechChallengeF04\medvision-ai\backend\models_weights\yolov8_gyneco.pt

# Opção 2: Google Drive Desktop
copy "G:\Meu Drive\MedVision_AI\yolov8_gyneco_LATEST.pt" ^
     C:\dev\TechChallengeF04\medvision-ai\backend\models_weights\yolov8_gyneco.pt
```

### 3. Reiniciar Backend

No terminal do backend (Ctrl+C e depois):
```powershell
cd C:\dev\TechChallengeF04\medvision-ai\backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verifique logs:**
```
✅ Modelo YOLOv8 carregado: custom
✅ Classes detectáveis: X  (número de instrumentos)
```

### 4. Testar!

1. Acesse: http://localhost:5174
2. Faça upload de vídeo cirúrgico real
3. **Veja os instrumentos sendo detectados!** 🎬

---

## 🐛 Troubleshooting:

### "CUDA Out of Memory"
```python
# Na célula de configuração, ajuste:
BATCH_SIZE = 8  # ou 4 se ainda der erro
```

### "Conversion taking too long"
- Normal! 12k+ imagens leva ~10-15 minutos
- Veja progresso nas mensagens de log

### "mAP50 muito baixo (<0.3)"
- Treine por mais épocas (150-200)
- Ou use modelo maior: `MODEL_SIZE = 's'`

### "Session disconnected"
- Colab gratuito desconecta após 12h inativo
- Salve checkpoints a cada 10 épocas (já configurado)
- Use Colab Pro se precisar sessões longas

---

## 🎯 Checklist Final:

Antes de começar, confirme:
- [ ] Dataset compactado: `Instrument_Anatomy_Original_Dataset.zip`
- [ ] Upload no Google Drive concluído
- [ ] Google Colab aberto com GPU T4 ativada
- [ ] Notebook `FINE_TUNING_GYNSURGE_COLAB.ipynb` carregado
- [ ] Tempo disponível: ~3 horas (pode sair, mas mantenha aba aberta)

---

**🚀 BOA SORTE COM O TREINAMENTO!**

Se tiver dúvidas durante o processo, consulte:
- `docs/FINE_TUNING_GUIDE.md` - Guia completo e detalhado
- Logs do Colab - Mensagens de erro/progresso
- Gráficos de treinamento - Convergência das métricas

---

## 📧 Informações Úteis:

- **Dataset:** 12,394 imagens
- **Classes:** ~10 instrumentos cirúrgicos
- **Formato original:** COCO JSON
- **Formato treinamento:** YOLO TXT
- **Modelo base:** YOLOv8n (6MB)
- **Modelo final:** ~6-8MB (após fine-tuning)
- **Tempo estimado:** 2-3 horas (100 épocas, GPU T4)
- **VRAM necessária:** ~6-8GB (T4 tem 16GB, sobra!)

---

## 💾 Versionamento Automático:

O notebook salva **3 versões** do modelo no Google Drive:

1. **`yolov8_gyneco_LATEST.pt`** 
   - Sempre sobrescrito com a versão mais recente
   - **Use este para o backend!**

2. **`yolov8_gyneco_YYYYMMDD_HHMMSS.pt`**
   - Versão com timestamp (ex: yolov8_gyneco_20260210_143522.pt)
   - Mantém histórico de treinamentos
   - Útil para comparar versões diferentes

3. **`yolov8_gyneco_last.pt`**
   - Último checkpoint (pode não ser o melhor)
   - Use se o treinamento não completou

**💡 Dica:** Mantenha os arquivos com timestamp para voltar a versões anteriores se o novo modelo não performar bem!

---

**🎉 Depois do treinamento, seu MedVision AI estará 100% funcional para detecção de instrumentos cirúrgicos!**
