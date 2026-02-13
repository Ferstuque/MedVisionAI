#!/usr/bin/env python3
"""
Inspeciona estrutura do dataset GynSurge
Mostra organização de pastas, arquivos de anotação, formatos, etc.
"""

from pathlib import Path
import json
import xml.etree.ElementTree as ET


def inspect_gynsurge_dataset(dataset_path: str):
    """Inspeciona estrutura do dataset"""
    
    print("=" * 70)
    print("🔍 INSPEÇÃO DO DATASET GYNSURGE")
    print("=" * 70)
    print()
    
    root = Path(dataset_path)
    
    if not root.exists():
        print(f"❌ Erro: Caminho não encontrado: {dataset_path}")
        return
    
    print(f"📂 Root: {root.absolute()}")
    print()
    
    # Estrutura de diretórios
    print("📁 ESTRUTURA DE DIRETÓRIOS")
    print("-" * 70)
    
    insseg_dir = root / 'insseg'
    
    if not insseg_dir.exists():
        print(f"⚠️ Diretório 'insseg' não encontrado")
        print(f"   Listando conteúdo de {root}:")
        for item in root.iterdir():
            print(f"   • {item.name} {'(pasta)' if item.is_dir() else '(arquivo)'}")
        return
    
    # Lista pastas INSSEG_XX
    insseg_folders = sorted([d for d in insseg_dir.iterdir() if d.is_dir() and d.name.startswith('INSSEG_')])
    print(f"✅ Encontradas {len(insseg_folders)} pastas INSSEG_XX")
    print()
    
    # Analisa primeira pasta como exemplo
    if insseg_folders:
        example_folder = insseg_folders[0]
        print(f"📋 EXEMPLO: {example_folder.name}")
        print("-" * 70)
        
        # Lista subpastas (vídeos)
        video_folders = sorted([d for d in example_folder.iterdir() if d.is_dir()])
        print(f"   Subpastas de vídeo: {len(video_folders)}")
        
        if video_folders:
            example_video = video_folders[0]
            print(f"   Exemplo: {example_video.name}")
            print()
            
            # Lista arquivos dentro
            files = list(example_video.iterdir())
            print(f"   📄 ARQUIVOS em {example_video.name}:")
            
            # Agrupa por extensão
            extensions = {}
            for f in files:
                ext = f.suffix.lower()
                if ext not in extensions:
                    extensions[ext] = []
                extensions[ext].append(f.name)
            
            for ext, filenames in sorted(extensions.items()):
                print(f"      {ext or '(sem extensão)'}: {len(filenames)} arquivos")
                # Mostra primeiros 3 exemplos
                for fname in filenames[:3]:
                    print(f"         • {fname}")
                if len(filenames) > 3:
                    print(f"         ... +{len(filenames) - 3} arquivos")
            
            print()
            
            # Tenta detectar formato de anotação
            print("🔍 FORMATO DE ANOTAÇÕES:")
            print("-" * 70)
            
            # Procura JSON
            json_files = list(example_video.glob('*.json'))
            if json_files:
                print(f"   ✅ Encontrados {len(json_files)} arquivos JSON")
                print(f"      Exemplo: {json_files[0].name}")
                
                # Lê exemplo
                try:
                    with open(json_files[0], 'r') as f:
                        data = json.load(f)
                    
                    print()
                    print("      📋 Estrutura JSON:")
                    print(f"         Keys: {list(data.keys())}")
                    
                    # Mostra primeiras linhas
                    import json as json_module
                    preview = json_module.dumps(data, indent=2)[:500]
                    print("      Preview:")
                    for line in preview.split('\n'):
                        print(f"         {line}")
                    if len(preview) >= 500:
                        print("         ...")
                
                except Exception as e:
                    print(f"      ⚠️ Erro ao ler JSON: {e}")
            
            # Procura XML
            xml_files = list(example_video.glob('*.xml'))
            if xml_files:
                print(f"   ✅ Encontrados {len(xml_files)} arquivos XML")
                print(f"      Exemplo: {xml_files[0].name}")
                
                try:
                    tree = ET.parse(xml_files[0])
                    root_elem = tree.getroot()
                    print(f"      Root tag: <{root_elem.tag}>")
                    print(f"      Children: {[child.tag for child in root_elem][:5]}")
                except Exception as e:
                    print(f"      ⚠️ Erro ao ler XML: {e}")
            
            # Procura máscaras PNG
            mask_patterns = ['*mask*.png', '*label*.png', '*seg*.png']
            masks = []
            for pattern in mask_patterns:
                masks.extend(list(example_video.glob(pattern)))
            
            if masks:
                print(f"   ✅ Encontradas {len(masks)} possíveis máscaras de segmentação")
                print(f"      Exemplo: {masks[0].name}")
            
            # Procura TXT (YOLO format?)
            txt_files = list(example_video.glob('*.txt'))
            if txt_files:
                print(f"   ✅ Encontrados {len(txt_files)} arquivos TXT")
                print(f"      Exemplo: {txt_files[0].name}")
                
                try:
                    with open(txt_files[0], 'r') as f:
                        lines = f.readlines()[:3]
                    print("      Preview:")
                    for line in lines:
                        print(f"         {line.strip()}")
                except Exception as e:
                    print(f"      ⚠️ Erro ao ler TXT: {e}")
            
            if not json_files and not xml_files and not masks and not txt_files:
                print("   ⚠️ Nenhum formato de anotação reconhecido")
    
    print()
    print("=" * 70)
    print("📊 ESTATÍSTICAS GERAIS")
    print("=" * 70)
    
    # Conta total de imagens
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    total_images = 0
    
    for insseg_folder in insseg_folders:
        video_folders = [d for d in insseg_folder.iterdir() if d.is_dir()]
        for video_folder in video_folders:
            for ext in image_extensions:
                total_images += len(list(video_folder.glob(f"*{ext}")))
    
    print(f"📷 Total de imagens: {total_images}")
    print(f"📁 Pastas INSSEG: {len(insseg_folders)}")
    
    # Conta vídeos
    total_videos = 0
    for insseg_folder in insseg_folders:
        video_folders = [d for d in insseg_folder.iterdir() if d.is_dir() and '.mp4_' in d.name]
        total_videos += len(video_folders)
    
    print(f"🎬 Pastas de vídeo: {total_videos}")
    
    print()
    print("🎯 PRÓXIMO PASSO:")
    print("   Com base na estrutura de anotações detectada,")
    print("   adapte o script prepare_gynsurge_dataset.py")
    print("   na função process_annotation()")


def main():
    """Função principal"""
    import sys
    
    print()
    print("=" * 70)
    print("🔬 INSPETOR DE DATASET GYNSURGE")
    print("=" * 70)
    print()
    
    # Verifica se foi passado como argumento
    if len(sys.argv) > 1:
        dataset_path = sys.argv[1]
        print(f"📂 Caminho (argumento): {dataset_path}")
    else:
        # Caminho padrão
        default_path = "C:/dev/TechChallengeF04/Instrument_Anatomy_Original_Dataset"
        
        dataset_path = input(f"Caminho do dataset (Enter={default_path}):\n> ").strip()
        dataset_path = dataset_path or default_path
    
    print()
    inspect_gynsurge_dataset(dataset_path)


if __name__ == '__main__':
    main()
