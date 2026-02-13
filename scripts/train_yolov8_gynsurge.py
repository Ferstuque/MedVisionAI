#!/usr/bin/env python3
"""
Fine-tuning YOLOv8 para detecção de instrumentos cirúrgicos
Dataset: GynSurge (Gynecological Surgery)

Uso:
    python scripts/train_yolov8_gynsurge.py
"""

import os
from pathlib import Path
from ultralytics import YOLO
import torch
import yaml


class YOLOv8Trainer:
    """Treinador YOLOv8 para instrumentos cirúrgicos"""
    
    def __init__(self, data_yaml_path: str, output_dir: str = 'runs/train'):
        """
        Args:
            data_yaml_path: Caminho para data.yaml do dataset
            output_dir: Diretório para salvar resultados
        """
        self.data_yaml_path = Path(data_yaml_path)
        self.output_dir = Path(output_dir)
        
        if not self.data_yaml_path.exists():
            raise FileNotFoundError(f"data.yaml não encontrado: {self.data_yaml_path}")
        
        # Carrega configurações do dataset
        with open(self.data_yaml_path, 'r') as f:
            self.data_config = yaml.safe_load(f)
        
        print(f"📊 Dataset: {self.data_config['nc']} classes")
        print(f"   Classes: {', '.join(self.data_config['names'][:5])}...")
    
    def train(self, 
              model_size: str = 'n',
              epochs: int = 100,
              batch_size: int = 16,
              img_size: int = 640,
              patience: int = 50,
              device: str = None):
        """
        Treina modelo YOLOv8
        
        Args:
            model_size: Tamanho do modelo (n, s, m, l, x)
            epochs: Número de épocas
            batch_size: Tamanho do batch
            img_size: Tamanho das imagens
            patience: Early stopping patience
            device: 'cuda', 'cpu', ou None (auto)
        """
        
        print()
        print("=" * 70)
        print("🚀 INICIANDO FINE-TUNING YOLOV8")
        print("=" * 70)
        print()
        
        # Detecta device
        if device is None:
            device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        print(f"🖥️  Device: {device.upper()}")
        
        if device == 'cpu':
            print("   ⚠️ AVISO: Treinamento em CPU será MUITO lento!")
            print("   📌 Recomendado: Use Google Colab (GPU gratuita) ou Kaggle")
        
        print(f"📦 Modelo: YOLOv8{model_size}")
        print(f"🔢 Épocas: {epochs}")
        print(f"📏 Batch size: {batch_size}")
        print(f"🖼️  Image size: {img_size}x{img_size}")
        print()
        
        # Carrega modelo pré-treinado (transfer learning)
        model_name = f'yolov8{model_size}.pt'
        print(f"⬇️  Carregando modelo pré-treinado: {model_name}")
        model = YOLO(model_name)
        
        # Configurações de treinamento
        train_args = {
            'data': str(self.data_yaml_path),
            'epochs': epochs,
            'batch': batch_size,
            'imgsz': img_size,
            'patience': patience,
            'device': device,
            'project': str(self.output_dir),
            'name': f'gynsurge_yolov8{model_size}',
            
            # Otimizações
            'optimizer': 'AdamW',  # Melhor que SGD para fine-tuning
            'lr0': 0.001,          # Learning rate inicial (menor para fine-tuning)
            'lrf': 0.01,           # Learning rate final
            'momentum': 0.937,
            'weight_decay': 0.0005,
            
            # Data augmentation
            'hsv_h': 0.015,        # Hue augmentation
            'hsv_s': 0.7,          # Saturation
            'hsv_v': 0.4,          # Value
            'degrees': 0.0,        # Rotation (médico: sem rotação)
            'translate': 0.1,      # Translation
            'scale': 0.5,          # Scaling
            'shear': 0.0,          # Shear
            'perspective': 0.0,    # Perspective
            'flipud': 0.0,         # Flip vertical (não para cirurgia)
            'fliplr': 0.5,         # Flip horizontal
            'mosaic': 1.0,         # Mosaic augmentation
            'mixup': 0.0,          # MixUp augmentation
            
            # Validação
            'val': True,
            'save': True,
            'save_period': 10,     # Salva checkpoint a cada 10 épocas
            'plots': True,
            
            # Performance
            'cache': True,         # Cache images para treino mais rápido
            'workers': 8,
            'amp': True,           # Automatic Mixed Precision (mais rápido)
        }
        
        print("⚙️  Configurações:")
        print(f"   • Optimizer: {train_args['optimizer']}")
        print(f"   • Learning rate: {train_args['lr0']} → {train_args['lrf']}")
        print(f"   • Data augmentation: Enabled")
        print(f"   • Mixed precision: {train_args['amp']}")
        print()
        
        input("📋 Pressione ENTER para iniciar o treinamento...")
        print()
        
        # Treina!
        print("🎓 Iniciando treinamento...")
        print("-" * 70)
        
        try:
            results = model.train(**train_args)
            
            print()
            print("=" * 70)
            print("✅ TREINAMENTO CONCLUÍDO!")
            print("=" * 70)
            
            # Caminho do melhor modelo
            best_model_path = Path(self.output_dir) / train_args['name'] / 'weights' / 'best.pt'
            last_model_path = Path(self.output_dir) / train_args['name'] / 'weights' / 'last.pt'
            
            print(f"📦 Melhor modelo: {best_model_path}")
            print(f"📦 Último modelo: {last_model_path}")
            print()
            
            # Avalia no conjunto de teste
            if 'test' in self.data_config:
                print("🧪 Avaliando no conjunto de teste...")
                test_results = model.val(split='test')
                print(f"   mAP50: {test_results.box.map50:.4f}")
                print(f"   mAP50-95: {test_results.box.map:.4f}")
            
            print()
            print("🎯 PRÓXIMOS PASSOS:")
            print(f"   1. Copie o melhor modelo para:")
            print(f"      backend/models_weights/yolov8_gyneco.pt")
            print()
            print(f"   2. Reinicie o backend - ele carregará automaticamente")
            print()
            print(f"   3. Faça upload de vídeo cirúrgico para testar!")
            
            return str(best_model_path)
        
        except KeyboardInterrupt:
            print()
            print("⚠️ Treinamento interrompido pelo usuário")
            return None
        
        except Exception as e:
            print()
            print(f"❌ ERRO durante treinamento: {e}")
            raise


def main():
    """Função principal"""
    
    print("=" * 70)
    print("🏥 FINE-TUNING YOLOV8 - INSTRUMENTOS CIRÚRGICOS")
    print("=" * 70)
    print()
    
    # Configuração
    DATA_YAML = "C:/dev/TechChallengeF04/medvision-ai/datasets/gynsurge_yolo/data.yaml"
    OUTPUT_DIR = "C:/dev/TechChallengeF04/medvision-ai/backend/runs/train"
    
    if not Path(DATA_YAML).exists():
        print("❌ ERRO: data.yaml não encontrado!")
        print(f"   Esperado em: {DATA_YAML}")
        print()
        print("🔧 Execute primeiro:")
        print("   python scripts/prepare_gynsurge_dataset.py")
        return
    
    # Menu de configuração
    print("📋 CONFIGURAÇÃO DE TREINAMENTO")
    print("-" * 70)
    print()
    print("Tamanho do modelo:")
    print("  [n] Nano   (mais rápido, menos preciso)  ⭐ Recomendado para CPU")
    print("  [s] Small  (equilibrado)")
    print("  [m] Medium (mais lento, mais preciso)")
    print("  [l] Large  (requer GPU potente)")
    print("  [x] XLarge (melhor qualidade)")
    print()
    
    model_size = input("Escolha [n/s/m/l/x] (padrão=n): ").strip().lower() or 'n'
    
    if model_size not in ['n', 's', 'm', 'l', 'x']:
        print(f"⚠️ Tamanho inválido, usando 'n'")
        model_size = 'n'
    
    print()
    epochs_input = input("Número de épocas (padrão=100): ").strip()
    epochs = int(epochs_input) if epochs_input else 100
    
    print()
    batch_input = input("Batch size (padrão=16, reduza se ficar sem memória): ").strip()
    batch_size = int(batch_input) if batch_input else 16
    
    print()
    
    # Cria trainer
    trainer = YOLOv8Trainer(DATA_YAML, OUTPUT_DIR)
    
    # Treina
    best_model = trainer.train(
        model_size=model_size,
        epochs=epochs,
        batch_size=batch_size,
        img_size=640,
        patience=50
    )
    
    if best_model:
        # Copia automaticamente para backend
        dest_model = Path("C:/dev/TechChallengeF04/medvision-ai/backend/models_weights/yolov8_gyneco.pt")
        dest_model.parent.mkdir(parents=True, exist_ok=True)
        
        import shutil
        shutil.copy(best_model, dest_model)
        print()
        print(f"✅ Modelo copiado para: {dest_model}")
        print("🔄 Reinicie o backend para usar o novo modelo!")


if __name__ == '__main__':
    main()
