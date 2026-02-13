#!/usr/bin/env python3
"""
Prepara dataset GynSurge para treinamento YOLOv8
Converte segmentações para bounding boxes no formato YOLO

Dataset: https://ftp.itec.aau.at/datasets/GynSurge/
"""

import os
import json
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Dict
import shutil


class GynSurgePreparator:
    """Prepara dataset GynSurge para YOLOv8"""
    
    # Mapeamento de classes (ajuste conforme anotações reais)
    CLASSES = {
        'needle-holder': 0,
        'needle': 1,
        'irrigator': 2,
        'needle-holder-head': 3,
        'needle-thread': 4,
        'scissors': 5,
        'grasper': 6,
        'clip-applier': 7,
        'hook': 8,
        'other': 9
    }
    
    def __init__(self, input_dir: str, output_dir: str):
        """
        Args:
            input_dir: Diretório com dataset GynSurge original
            output_dir: Diretório de saída no formato YOLO
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        
        # Cria estrutura YOLO
        self.images_dir = self.output_dir / 'images'
        self.labels_dir = self.output_dir / 'labels'
        
        for split in ['train', 'val', 'test']:
            (self.images_dir / split).mkdir(parents=True, exist_ok=True)
            (self.labels_dir / split).mkdir(parents=True, exist_ok=True)
    
    def mask_to_bbox(self, mask: np.ndarray) -> Tuple[int, int, int, int]:
        """
        Converte máscara de segmentação para bounding box
        
        Args:
            mask: Máscara binária (H, W)
        
        Returns:
            (x_min, y_min, x_max, y_max)
        """
        rows = np.any(mask, axis=1)
        cols = np.any(mask, axis=0)
        
        if not rows.any() or not cols.any():
            return None
        
        y_min, y_max = np.where(rows)[0][[0, -1]]
        x_min, x_max = np.where(cols)[0][[0, -1]]
        
        return (x_min, y_min, x_max, y_max)
    
    def bbox_to_yolo_format(self, bbox: Tuple[int, int, int, int], 
                           img_width: int, img_height: int) -> Tuple[float, float, float, float]:
        """
        Converte bbox absoluto para formato YOLO normalizado
        
        Args:
            bbox: (x_min, y_min, x_max, y_max)
            img_width: Largura da imagem
            img_height: Altura da imagem
        
        Returns:
            (x_center, y_center, width, height) normalizados [0-1]
        """
        x_min, y_min, x_max, y_max = bbox
        
        x_center = (x_min + x_max) / 2.0 / img_width
        y_center = (y_min + y_max) / 2.0 / img_height
        width = (x_max - x_min) / img_width
        height = (y_max - y_min) / img_height
        
        # Garante valores válidos [0-1]
        x_center = max(0.0, min(1.0, x_center))
        y_center = max(0.0, min(1.0, y_center))
        width = max(0.0, min(1.0, width))
        height = max(0.0, min(1.0, height))
        
        return (x_center, y_center, width, height)
    
    def process_annotation(self, annotation_path: Path, image_path: Path) -> List[str]:
        """
        Processa arquivo de anotação e retorna linhas YOLO
        
        Formato YOLO: <class_id> <x_center> <y_center> <width> <height>
        
        Returns:
            Lista de linhas no formato YOLO
        """
        # Este método precisa ser adaptado ao formato real das anotações GynSurge
        # Exemplo para JSON com segmentações:
        
        yolo_lines = []
        
        # Carrega imagem para dimensões
        img = cv2.imread(str(image_path))
        if img is None:
            return []
        
        img_height, img_width = img.shape[:2]
        
        # Exemplo: assume JSON com formato {'annotations': [...]}
        # AJUSTE CONFORME FORMATO REAL
        try:
            with open(annotation_path, 'r') as f:
                data = json.load(f)
            
            # Exemplo de extração (AJUSTAR):
            if 'annotations' in data:
                for ann in data['annotations']:
                    class_name = ann.get('class', 'other')
                    class_id = self.CLASSES.get(class_name, 9)  # 9 = other
                    
                    # Se tiver segmentação (polygon/mask)
                    if 'segmentation' in ann:
                        # Converte para bbox
                        # (implementação específica)
                        pass
                    
                    # Se já tiver bbox
                    elif 'bbox' in ann:
                        bbox = ann['bbox']  # formato?
                        yolo_bbox = self.bbox_to_yolo_format(bbox, img_width, img_height)
                        yolo_lines.append(f"{class_id} {yolo_bbox[0]:.6f} {yolo_bbox[1]:.6f} {yolo_bbox[2]:.6f} {yolo_bbox[3]:.6f}")
        
        except Exception as e:
            print(f"⚠️ Erro ao processar {annotation_path}: {e}")
        
        return yolo_lines
    
    def convert_dataset(self, train_split: float = 0.7, val_split: float = 0.2):
        """
        Converte dataset completo
        
        Estrutura esperada:
        Instrument_Anatomy_Original_Dataset/
        └── insseg/
            ├── INSSEG_01/
            │   ├── 0.mp4_/
            │   ├── 1.mp4_/
            │   └── ...
            ├── INSSEG_02/
            └── ... até INSSEG_10/
        
        Args:
            train_split: % para treino
            val_split: % para validação
            test_split: remainder para teste
        """
        print("=" * 70)
        print("🔄 CONVERTENDO DATASET GYNSURGE PARA FORMATO YOLO")
        print("=" * 70)
        print()
        
        # Estrutura específica do GynSurge
        insseg_dir = self.input_dir / 'insseg'
        
        if not insseg_dir.exists():
            print(f"❌ Erro: Diretório 'insseg' não encontrado em {self.input_dir}")
            print(f"   Estrutura esperada:")
            print(f"   {self.input_dir}")
            print(f"   └── insseg/")
            print(f"       ├── INSSEG_01/")
            print(f"       ├── INSSEG_02/")
            print(f"       └── ...")
            return
        
        print(f"📂 Procurando em: {insseg_dir}")
        
        # Procura subpastas INSSEG_XX
        insseg_folders = sorted([d for d in insseg_dir.iterdir() if d.is_dir() and d.name.startswith('INSSEG_')])
        print(f"📁 Encontradas {len(insseg_folders)} pastas INSSEG")
        
        # Coleta todas as imagens de todas as subpastas
        all_images = []
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        
        for insseg_folder in insseg_folders:
            print(f"   🔍 {insseg_folder.name}...")
            
            # Procura subpastas *.mp4_ dentro de cada INSSEG_XX
            video_folders = sorted([d for d in insseg_folder.iterdir() if d.is_dir() and '.mp4_' in d.name])
            
            for video_folder in video_folders:
                # Procura imagens dentro de cada pasta de vídeo
                for ext in image_extensions:
                    images_in_folder = list(video_folder.glob(f"*{ext}"))
                    all_images.extend(images_in_folder)
                    
                    if images_in_folder:
                        print(f"      • {video_folder.name}: {len(images_in_folder)} imagens")
        
        print()
        print(f"📁 Total de imagens encontradas: {len(all_images)}")
        
        if len(all_images) == 0:
            print("❌ Nenhuma imagem encontrada!")
            print(f"   Verifique o caminho: {self.input_dir}")
            return
        
        # Divide em train/val/test
        np.random.shuffle(all_images)
        n_train = int(len(all_images) * train_split)
        n_val = int(len(all_images) * val_split)
        
        splits = {
            'train': all_images[:n_train],
            'val': all_images[n_train:n_train + n_val],
            'test': all_images[n_train + n_val:]
        }
        
        print(f"📊 Split: train={n_train}, val={n_val}, test={len(splits['test'])}")
        print()
        
        # Processa cada split
        stats = {'train': 0, 'val': 0, 'test': 0}
        
        for split_name, images in splits.items():
            print(f"🔄 Processando {split_name}...")
            
            for img_path in images:
                # Procura anotação correspondente
                # AJUSTAR conforme estrutura do dataset
                ann_path = img_path.with_suffix('.json')  # ou .xml, .txt, etc.
                
                if not ann_path.exists():
                    print(f"   ⚠️ Anotação não encontrada: {ann_path.name}")
                    continue
                
                # Processa anotação
                yolo_lines = self.process_annotation(ann_path, img_path)
                
                if not yolo_lines:
                    continue  # Pula imagens sem anotações válidas
                
                # Copia imagem
                dest_img = self.images_dir / split_name / img_path.name
                shutil.copy(img_path, dest_img)
                
                # Salva label YOLO
                dest_label = self.labels_dir / split_name / f"{img_path.stem}.txt"
                with open(dest_label, 'w') as f:
                    f.write('\n'.join(yolo_lines))
                
                stats[split_name] += 1
            
            print(f"   ✅ Processadas: {stats[split_name]} imagens")
        
        print()
        print("=" * 70)
        print("✅ CONVERSÃO CONCLUÍDA!")
        print("=" * 70)
        print(f"📂 Dataset YOLO salvo em: {self.output_dir}")
        print(f"📊 Total: train={stats['train']}, val={stats['val']}, test={stats['test']}")
        
        # Cria arquivo data.yaml para YOLOv8
        self.create_data_yaml()
    
    def create_data_yaml(self):
        """Cria arquivo data.yaml para treinamento YOLOv8"""
        yaml_content = f"""# GynSurge Dataset Configuration for YOLOv8

# Paths (relative to this file)
path: {self.output_dir.absolute()}
train: images/train
val: images/val
test: images/test

# Classes
nc: {len(self.CLASSES)}  # number of classes
names: {list(self.CLASSES.keys())}  # class names
"""
        
        yaml_path = self.output_dir / 'data.yaml'
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)
        
        print(f"📝 Criado: {yaml_path}")


def main():
    """Função principal"""
    
    print("=" * 70)
    print("🏥 PREPARADOR DE DATASET GYNSURGE")
    print("=" * 70)
    print()
    
    # Configuração
    # AJUSTE ESTES CAMINHOS:
    INPUT_DIR = "C:/dev/TechChallengeF04/datasets/gynsurge"  # Onde você baixou
    OUTPUT_DIR = "C:/dev/TechChallengeF04/medvision-ai/datasets/gynsurge_yolo"
    
    print(f"📥 Input: {INPUT_DIR}")
    print(f"📤 Output: {OUTPUT_DIR}")
    print()
    
    if not Path(INPUT_DIR).exists():
        print("❌ ERRO: Diretório de entrada não encontrado!")
        print(f"   Por favor, baixe o dataset GynSurge e extraia em:")
        print(f"   {INPUT_DIR}")
        print()
        print("🌐 Download: https://ftp.itec.aau.at/datasets/GynSurge/")
        return
    
    # Cria preparador
    preparator = GynSurgePreparator(INPUT_DIR, OUTPUT_DIR)
    
    # Converte dataset
    preparator.convert_dataset(
        train_split=0.7,  # 70% treino
        val_split=0.2,    # 20% validação
        # 10% teste (restante)
    )
    
    print()
    print("🎯 PRÓXIMO PASSO:")
    print("   Execute: python scripts/train_yolov8_gynsurge.py")


if __name__ == '__main__':
    main()
