# %% [markdown]
# # 🏥 Fine-Tuning YOLOv8 - MedVision AI
# 
# Treinamento de modelo de detecção de instrumentos cirúrgicos usando dataset GynSurge
# 
# **GPU Recomendada:** Runtime > Change runtime type > GPU (T4)

# %% [markdown]
# ## 📦 1. Instalação de Dependências

# %%
!pip install -q ultralytics roboflow

# Importações
from ultralytics import YOLO
import torch
from pathlib import Path
import yaml
import shutil

print(f"✅ PyTorch: {torch.__version__}")
print(f"✅ CUDA disponível: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"   GPU: {torch.cuda.get_device_name(0)}")

# %% [markdown]
# ## 📂 2. Preparar Dataset
# 
# **Opções:**
# 
# ### Opção A: Upload Manual (Recomendado para dataset próprio)
# ```python
# from google.colab import files
# uploaded = files.upload()  # Faça upload do dataset.zip
# !unzip -q dataset.zip -d /content/dataset
# ```
# 
# ### Opção B: Google Drive
# ```python
# from google.colab import drive
# drive.mount('/content/drive')
# # Dataset em: /content/drive/MyDrive/datasets/gynsurge
# ```
# 
# ### Opção C: Download Direto

# %%
# Exemplo: Download de dataset de exemplo
# AJUSTE para seu dataset real

import os

# Estrutura de diretórios
os.makedirs('/content/dataset/images/train', exist_ok=True)
os.makedirs('/content/dataset/images/val', exist_ok=True)
os.makedirs('/content/dataset/labels/train', exist_ok=True)
os.makedirs('/content/dataset/labels/val', exist_ok=True)

print("📁 Estrutura de diretórios criada")

# %% [markdown]
# ## 📝 3. Criar data.yaml
# 
# Configure as classes do seu dataset

# %%
data_yaml_content = """
# GynSurge Dataset - Instrumentos Cirúrgicos

path: /content/dataset
train: images/train
val: images/val

# Classes (ajuste para seu dataset)
nc: 10
names:
  - needle-holder
  - needle
  - irrigator
  - needle-holder-head
  - needle-thread
  - scissors
  - grasper
  - clip-applier
  - hook
  - other
"""

with open('/content/data.yaml', 'w') as f:
    f.write(data_yaml_content)

print("✅ data.yaml criado")

# Visualiza
!cat /content/data.yaml

# %% [markdown]
# ## 📊 4. Verificar Dataset

# %%
# Conta imagens e labels
import glob

train_images = len(glob.glob('/content/dataset/images/train/*'))
train_labels = len(glob.glob('/content/dataset/labels/train/*.txt'))
val_images = len(glob.glob('/content/dataset/images/val/*'))
val_labels = len(glob.glob('/content/dataset/labels/val/*.txt'))

print("📊 ESTATÍSTICAS DO DATASET")
print("=" * 50)
print(f"Train: {train_images} imagens, {train_labels} labels")
print(f"Val:   {val_images} imagens, {val_labels} labels")

if train_images == 0:
    print("\n⚠️ ATENÇÃO: Nenhuma imagem encontrada!")
    print("   Faça upload do dataset antes de continuar")
else:
    print(f"\n✅ Dataset pronto para treinamento!")

# %% [markdown]
# ## 🎓 5. Treinar Modelo
# 
# **Configurações:**
# - Model: yolov8n (nano - mais rápido)
# - Epochs: 100 (ajuste conforme necessário)
# - Batch: 16 (reduza se ficar sem memória)

# %%
# Carrega modelo pré-treinado (transfer learning)
model = YOLO('yolov8n.pt')

print("📦 Modelo YOLOv8n carregado")
print("🚀 Iniciando fine-tuning...")

# %%
# TREINAMENTO
results = model.train(
    data='/content/data.yaml',
    epochs=100,
    imgsz=640,
    batch=16,
    device=0,  # GPU
    
    # Otimizações
    optimizer='AdamW',
    lr0=0.001,
    lrf=0.01,
    momentum=0.937,
    weight_decay=0.0005,
    
    # Data Augmentation
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    degrees=0.0,
    translate=0.1,
    scale=0.5,
    flipud=0.0,
    fliplr=0.5,
    mosaic=1.0,
    
    # Salvamento
    project='/content/runs/train',
    name='gynsurge_yolov8n',
    save=True,
    save_period=10,
    
    # Performance
    cache=True,
    workers=8,
    amp=True,
    patience=50,
    plots=True,
    verbose=True
)

print("\n✅ TREINAMENTO CONCLUÍDO!")

# %% [markdown]
# ## 📈 6. Visualizar Resultados

# %%
# Lista arquivos gerados
!ls -lah /content/runs/train/gynsurge_yolov8n/

# %%
# Mostra gráficos de treinamento
from IPython.display import Image, display

print("📊 RESULTADOS DO TREINAMENTO")
print("=" * 50)

# Results plot
display(Image(filename='/content/runs/train/gynsurge_yolov8n/results.png'))

# Confusion matrix
print("\n📊 Matriz de Confusão:")
display(Image(filename='/content/runs/train/gynsurge_yolov8n/confusion_matrix.png'))

# Validation predictions
print("\n🔍 Predições de Validação:")
display(Image(filename='/content/runs/train/gynsurge_yolov8n/val_batch0_pred.jpg'))

# %% [markdown]
# ## 🧪 7. Validar Modelo

# %%
# Carrega melhor modelo
best_model = YOLO('/content/runs/train/gynsurge_yolov8n/weights/best.pt')

# Valida
val_results = best_model.val(split='val')

print("\n📊 MÉTRICAS DE VALIDAÇÃO")
print("=" * 50)
print(f"mAP50:    {val_results.box.map50:.4f}")
print(f"mAP50-95: {val_results.box.map:.4f}")
print(f"Precision: {val_results.box.mp:.4f}")
print(f"Recall:    {val_results.box.mr:.4f}")

# %% [markdown]
# ## 🎯 8. Testar com Imagem

# %%
# Upload de imagem de teste (opcional)
# from google.colab import files
# uploaded = files.upload()

# Ou testa com imagem do validation set
import glob
test_image = glob.glob('/content/dataset/images/val/*')[0]

# Predição
results = best_model.predict(
    test_image,
    save=True,
    conf=0.25,
    save_txt=True
)

# Mostra resultado
from IPython.display import Image, display
print(f"\n🔍 Testando: {Path(test_image).name}")
display(Image(filename=results[0].save_dir / results[0].path))

print(f"\n📦 Detecções: {len(results[0].boxes)}")
for box in results[0].boxes:
    cls_id = int(box.cls)
    conf = float(box.conf)
    cls_name = best_model.names[cls_id]
    print(f"   • {cls_name}: {conf:.2%}")

# %% [markdown]
# ## 💾 9. Download Modelo Treinado

# %%
# Compacta modelos
!zip -9 -r /content/gynsurge_models.zip /content/runs/train/gynsurge_yolov8n/weights/

# Download
from google.colab import files

print("📥 Baixando modelos treinados...")
print("   • best.pt  (melhor modelo)")
print("   • last.pt  (último checkpoint)")

files.download('/content/gynsurge_models.zip')

print("\n✅ Download concluído!")
print("\n🎯 PRÓXIMO PASSO:")
print("   1. Extraia gynsurge_models.zip")
print("   2. Copie best.pt para:")
print("      backend/models_weights/yolov8_gyneco.pt")
print("   3. Reinicie o backend")

# %% [markdown]
# ## 🔧 10. Exportar para Outros Formatos (Opcional)

# %%
# Exporta para ONNX (mais rápido para inferência)
best_model.export(format='onnx', imgsz=640)

# Exporta para TensorRT (NVIDIA GPU)
# best_model.export(format='engine', imgsz=640, device=0)

print("\n✅ Modelo exportado!")

# %% [markdown]
# ## 📝 11. Informações do Modelo

# %%
# Info do modelo
print("📦 INFORMAÇÕES DO MODELO")
print("=" * 50)
print(f"Tipo: YOLOv8n")
print(f"Classes: {best_model.names}")
print(f"Weights: /content/runs/train/gynsurge_yolov8n/weights/best.pt")
print(f"Tamanho: {Path('/content/runs/train/gynsurge_yolov8n/weights/best.pt').stat().st_size / 1024 / 1024:.1f} MB")

# %% [markdown]
# ---
# 
# ## ✅ Checklist
# 
# - [ ] Dataset preparado e validado
# - [ ] Treinamento concluído sem erros
# - [ ] Métricas aceitáveis (mAP50 > 0.5)
# - [ ] Testado em imagens reais
# - [ ] Modelo baixado (best.pt)
# - [ ] Modelo copiado para backend/models_weights/
# - [ ] Backend reiniciado
# - [ ] Testado em vídeo cirúrgico real via interface
# 
# ---
# 
# **🎉 Parabéns! Modelo treinado com sucesso!**
# 
# Para dúvidas, consulte: `docs/FINE_TUNING_GUIDE.md`
