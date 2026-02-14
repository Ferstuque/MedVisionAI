#  MedVision AI

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3+-61dafb.svg)](https://reactjs.org/)
[![Azure](https://img.shields.io/badge/Azure-Container%20Apps-0078D4.svg)](https://azure.microsoft.com/products/container-apps)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](./docker-compose.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

**Plataforma de Análise Multimodal Cirúrgica com Inteligência Artificial**

Sistema fullstack para análise em tempo real de vídeos e áudios cirúrgicos ginecológicos, utilizando **YOLOv8** para detecção de instrumentos e anomalias visuais, **librosa** para análise de indicadores psicológicos de áudio, e **Google Gemini 2.5 Flash** para geração de relatórios clínicos detalhados.

>  **MVP Acadêmico** - Projeto desenvolvido como estudo de viabilidade técnica de IA multimodal em contexto médico. Demonstra integração de visão computacional, processamento de áudio e modelos de linguagem avançados em um sistema de suporte à decisão clínica.

---

##  Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura](#-arquitetura)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação Local](#-instalação-local)
- [Deploy no Azure Container Apps](#-deploy-no-azure-container-apps)
- [Documentação Adicional](#-documentação-adicional)
- [Limitações](#-limitações-e-disclaimers)
- [Licença](#-licença)

---

##  Visão Geral

O **MedVision AI** é uma solução completa para análise assistida por IA de procedimentos cirúrgicos ginecológicos, oferecendo:

###  Análise de Vídeo Cirúrgico
- **Detecção de Instrumentos**: Identificação automática de 23 classes de instrumentos cirúrgicos ginecológicos usando YOLOv8 customizado
- **Detecção de Anomalias**: Sangramento, perfurações, queimaduras, obstruções, má visualização
- **Bounding Boxes Interativas**: Visualização em tempo real com cores por tipo e espessura por severidade
- **Classificação de Risco**: Automática (crítico/warning/info) baseada em confiança e tipo de anomalia
- **Timeline de Eventos**: Navegação frame-by-frame com detecções sincronizadas

###  Análise de Áudio de Consultas
- **Extração de Features Acústicas**: MFCC, pitch, energia RMS, zero-crossing rate, spectral centroid
- **Indicadores Psicológicos**: Detecção de estresse, fadiga, ansiedade, depressão, trauma
- **Segmentação Temporal**: Janelas de 5 segundos com overlap de 2.5s
- **Transcrição Automática**: Conversão de fala para texto (formatos MP3, WAV, OGG, M4A)
- **Relatórios Especializados**: Contextualizados por tipo de consulta (ginecológica, pré-natal, pós-parto)

###  Relatórios com IA Generativa
- **Google Gemini 2.5 Flash**: Modelo multimodal de última geração
- **Análise Contextual**: Interpretação inteligente das detecções do YOLOv8 e features de áudio
- **Recomendações Clínicas**: Sugestões baseadas em padrões detectados
- **Formato Estruturado**: Markdown com emojis para melhor legibilidade

---

##  Arquitetura

```mermaid
graph TB
    subgraph "Camada de Apresentação"
        USER["👤 Usuário<br/>Navegador Web"]
    end

    subgraph "Azure Container Apps Environment"
        subgraph "Frontend Container"
            REACT["⚛️ React 18<br/>Vite 5<br/>TailwindCSS<br/>Nginx"]
        end
        
        subgraph "Backend Container"
            API["⚡ FastAPI + Uvicorn<br/>WebSocket Server"]
            YOLO["🔍 YOLOv8 Custom<br/>Detecção de Instrumentos"]
            AUDIO["🎵 Librosa<br/>Análise de Áudio"]
            CV["📹 OpenCV<br/>Processamento de Vídeo"]
        end
        
        ACR["📦 Azure Container Registry<br/>Imagens Docker"]
        LOGS["📊 Log Analytics<br/>Monitoramento"]
    end
    
    subgraph "Serviços Externos"
        GEMINI["🤖 Gemini 2.5 Flash<br/>Relatórios + Transcrição"]
    end
    
    USER -->|"Upload Vídeo/Áudio"| REACT
    REACT -->|"API REST<br/>+ WebSocket"| API
    API -->|"Frames"| YOLO
    API -->|"Arquivo"| AUDIO
    API -->|"Extração"| CV
    API -->|"Análise"| GEMINI
    GEMINI -->|"Relatório"| API
    API -->|"Alertas"| REACT
    REACT -->|"Resultados"| USER
    
    ACR -.->|"Pull"| REACT
    ACR -.->|"Pull"| API
    API -.->|"Logs"| LOGS
    REACT -.->|"Logs"| LOGS
    
    style USER fill:#e1f5ff
    style REACT fill:#61dafb
    style API fill:#009688
    style YOLO fill:#ff6b6b
    style AUDIO fill:#9b59b6
    style CV fill:#3498db
    style GEMINI fill:#f39c12
    style ACR fill:#0078d4
    style LOGS fill:#00bcd4
```

### Fluxo de Processamento
