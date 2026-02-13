# 🏥 MedVision AI

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3+-61dafb.svg)](https://reactjs.org/)
[![Tests](https://img.shields.io/badge/tests-94%20passed-success.svg)](./backend/tests)
[![Coverage](https://img.shields.io/badge/coverage-27%25-yellow.svg)](./backend/htmlcov)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](./docker-compose.yml)
[![Cloud Run](https://img.shields.io/badge/GCP-Cloud%20Run-4285F4.svg)](https://cloud.google.com/run)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-optional-lightgrey.svg)](./.github/workflows/README_WORKFLOWS.md)

**Plataforma de Análise Multimodal Cirúrgica com Inteligência Artificial**

Sistema fullstack para análise em tempo real de vídeos e áudios cirúrgicos ginecológicos, utilizando **YOLOv8** para detecção de anomalias visuais, **librosa** para análise de indicadores psicológicos de áudio, e **Google Gemini 2.5 Flash** para geração de relatórios clínicos detalhados com inteligência artificial.

> 🎓 **MVP Acadêmico** - Projeto desenvolvido como estudo de viabilidade técnica de IA multimodal em contexto médico. Demonstra integração de visão computacional, processamento de áudio e modelos de linguagem em um sistema de suporte à decisão clínica.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Uso](#uso)
- [Deploy](#deploy)
- [API Documentation](#api-documentation)
- [Limitações](#limitações)
- [Contribuição](#contribuição)
- [Licença](#licença)

---

## 🎯 Visão Geral

O **MedVision AI** é uma solução completa para análise assistida por IA de procedimentos cirúrgicos ginecológicos, oferecendo:

- **Análise de Vídeo**: Detecção automática de sangramento, instrumentos, estruturas anatômicas e eventos procedimentais usando YOLOv8.
- **Análise de Áudio**: Identificação de indicadores psicológicos de áudio (estresse, fadiga, ansiedade, depressão) através de análise de características acústicas com librosa.
- **Relatórios Clínicos**: Geração automática de relatórios detalhados e contextualizados com **Google Gemini 2.5 Flash**, modelo de última geração com capacidades avançadas de análise multimodal.
- **Alertas em Tempo Real**: Sistema de notificações via WebSocket para eventos críticos durante análise com priorização inteligente.
- **Dashboard Interativo**: Interface React moderna com visualização de bounding boxes sobre frames, timeline de eventos e painel de alertas.

---

## 🏗️ Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  React 18 + Vite + Tailwind CSS + WebSocket Client         │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ VideoPlayer │  │ AlertPanel   │  │ ReportViewer │       │
│  │ + BBoxLayer │  │ (Real-time)  │  │              │       │
│  └─────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP + WebSocket
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                        BACKEND                               │
│  FastAPI + Uvicorn + Python 3.11+                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  API Routes: /video, /audio, /reports, /ws          │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ YOLO Service │  │ Audio Service│  │ Gemini AI    │      │
│  │ (YOLOv8)     │  │ (librosa)    │  │ (Reports)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Video Utils  │  │ Storage      │  │ WebSocket    │      │
│  │ (OpenCV)     │  │ (Local/S3)   │  │ Manager      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   INFRASTRUCTURE                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Redis        │  │ Docker       │  │ GitHub       │      │
│  │ (Cache/Jobs) │  │ Compose      │  │ Actions      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 🔄 Fluxo de Análise de Vídeo

1. **Upload**: Usuário envia vídeo via interface React
2. **Validação**: Backend valida formato, tamanho e codec
3. **Extração**: Frames extraídos com OpenCV (sampling adaptativo)
4. **Detecção**: YOLOv8 analisa cada frame e detecta anomalias
5. **Classificação**: Sistema classifica severidade (critical/warning/info)
6. **Alertas**: WebSocket notifica frontend em tempo real
7. **Relatório**: Gemini 2.0 Flash gera análise clínica contextualizada
8. **Visualização**: React exibe bounding boxes sincronizadas com vídeo

---

## ✨ Funcionalidades

### 🎥 Análise de Vídeo

- **Detecção Multi-classe**: Sangamento, instrumentos, estruturas anatômicas, eventos procedimentais, riscos ao paciente
- **Bounding Boxes**: Visualização com cores por tipo e espessura por severidade
- **Timeline Interativa**: Navegação por frames com detecções
- **Classificação de Severidade**: Automática baseada em heurísticas (ex: sangramento >70% confiança = crítico)
- **Metadados Completos**: FPS, resolução, duração, codec

### 🎵 Análise de Áudio

- **Extração de Features**: MFCC, pitch, RMS energy, zero-crossing rate, spectral centroid
- **Indicadores Psicológicos**: Estresse, fadiga, ansiedade, depressão, estado normal
- **Segmentação**: Janelas de 5 segundos com overlap de 2.5s
- **Detecção de Silêncio**: Identifica pausas anormais na comunicação
- **Waveform Visualization**: Forma de onda com marcadores de eventos

### 📊 Relatórios com IA

- **Google Gemini 2.5 Flash**: Modelo de última geração com capacidades multimodais avançadas
- **Contexto Médico Especializado**: Prompts otimizados para análise ginecológica e obstétrica
- **Estrutura Clínica Padronizada**: Resumo executivo, achados detalhados, severidade, recomendações
- **Exportação Flexível**: Download em Markdown e JSON
- **Retry Logic Inteligente**: Backoff exponencial com fallback para resiliência

### 🚨 Alertas em Tempo Real

- **WebSocket**: Comunicação bidirecional de baixa latência
- **Priorização**: Crítico (vermelho), Warning (amarelo), Info (azul)
- **Timestamp**: Sincronizado com frame e segundo do vídeo
- **Notificações**: Toast notifications com react-hot-toast
- **Persistência**: Histórico completo de alertas

---

## 🛠️ Tecnologias

### Backend

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **Python** | 3.11+ | Linguagem principal |
| **FastAPI** | 0.115.0 | Framework web assíncrono |
| **YOLOv8** | 8.3.0 (ultralytics) | Detecção de objetos |
| **Google Gemini** | 2.5 Flash | API de LLM multimodal para relatórios |
| **librosa** | 0.10.2 | Análise de áudio |
| **OpenCV** | 4.10.0 | Processamento de vídeo |
| **Pydantic** | 2.9.2 | Validação de dados |
| **Redis** | 7.x | Cache e gerenciamento de jobs |
| **pytest** | 8.3.3 | Framework de testes |

### Frontend

| Tecnologia | Versão | Uso |
|------------|--------|-----|
| **React** | 18.3.1 | Biblioteca UI |
| **Vite** | 5.3.3 | Build tool |
| **Tailwind CSS** | 3.4.4 | Estilização |
| **axios** | 1.7.2 | Cliente HTTP |
| **react-router-dom** | 6.24.1 | Roteamento |
| **wavesurfer.js** | 7.7.14 | Visualização de áudio |
| **react-hot-toast** | 2.4.1 | Notificações |
| **lucide-react** | 0.263.1 | Ícones |

### DevOps

- **Docker** + **Docker Compose**: Containerização
- **GitHub Actions**: CI/CD
- **Nginx**: Servidor web (produção)
- **Google Cloud Run**: Deploy serverless

---

## 🚀 Instalação

### Pré-requisitos

- **Python 3.11+**
- **Node.js 20+**
- **Docker** e **Docker Compose** (opcional, mas recomendado)
- **Chave API Google Gemini**: https://ai.google.dev/

### 1. Clonar Repositório

```bash
git clone https://github.com/seu-usuario/medvision-ai.git
cd medvision-ai
```

### 2. Configurar Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env e adicionar GEMINI_API_KEY
```

**Arquivo `.env` mínimo:**

```env
GEMINI_API_KEY=sua-chave-aqui
ENVIRONMENT=development
LOG_LEVEL=DEBUG
YOLO_MODEL_PATH=./data/models/yolov8n.pt
STORAGE_TYPE=local
STORAGE_LOCAL_PATH=./data/uploads
```

### 3. Configurar Frontend

```bash
cd ../frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env
```

**Arquivo `.env` mínimo:**

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### 4. Executar com Docker Compose (Recomendado)

```bash
# Na raiz do projeto
docker-compose up --build
```

Serviços disponíveis:
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Redis**: localhost:6379

### 5. Executar Manualmente (Desenvolvimento)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

---

## 📖 Uso

### 1. Upload de Vídeo/Áudio

1. Acesse http://localhost:5173
2. Arraste ou selecione arquivo (MP4, AVI, MOV, WAV, MP3)
3. Clique em "Iniciar Análise"

### 2. Monitorar Análise

- **Barra de progresso**: Mostra porcentagem completa
- **Painel de alertas**: Alertas em tempo real (lado direito)
- **WebSocket status**: Indicador de conexão

### 3. Visualizar Resultado

- **Player de vídeo**: Navegue pelos frames
- **Bounding boxes**: Desenhadas automaticamente sobre detecções
- **Relatório Gemini**: Análise clínica completa
- **Download**: Exporte relatório em Markdown

### 4. Exemplo de Chamada API (cURL)

```bash
# Upload vídeo
curl -X POST "http://localhost:8000/api/v1/video/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@video_cirurgico.mp4"

# Resposta:
# {"analysis_id": "abc123", "status": "processing", "message": "..."}

# Obter status
curl "http://localhost:8000/api/v1/video/status/abc123"

# Obter resultado
curl "http://localhost:8000/api/v1/video/result/abc123"
```

---

## 🌐 Deploy

### Google Cloud Run

1. **Pré-requisitos:**
   - Conta GCP com billing ativado
   - `gcloud` CLI instalado e configurado
   - Secret Manager criado com `gemini-api-key`

2. **Configurar Secrets:**

```bash
echo -n "SUA_CHAVE_GEMINI" | gcloud secrets create gemini-api-key --data-file=-
```

3. **Deploy via GitHub Actions:**

> ⚠️ **Nota**: Os workflows de CI/CD estão **desabilitados temporariamente** para o MVP. Para habilitá-los, configure as secrets do GCP e siga o guia em [`.github/workflows/README_WORKFLOWS.md`](./.github/workflows/README_WORKFLOWS.md).

- Fork do repositório
- Adicione secrets no GitHub:
  - `GCP_PROJECT_ID`
  - `GCP_SA_KEY` (Service Account JSON)
  - `GEMINI_API_KEY` (para production)

- Habilite workflows em `.github/workflows/cd.yml`
- Push na branch `main` ativa deploy automático

4. **Deploy Manual:**

```bash
# Backend
gcloud run deploy medvision-backend \
  --source ./backend \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --set-secrets GEMINI_API_KEY=gemini-api-key:latest

# Frontend
gcloud run deploy medvision-frontend \
  --source ./frontend \
  --region us-central1 \
  --memory 512Mi
```

### Docker Compose Produção

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📚 API Documentation

### Endpoints Principais

#### **POST** `/api/v1/video/analyze`
Upload e análise de vídeo.

**Request:**
```
Content-Type: multipart/form-data
Body: file (video file)
```

**Response:**
```json
{
  "analysis_id": "uuid",
  "status": "processing",
  "message": "Análise iniciada"
}
```

#### **GET** `/api/v1/video/result/{analysis_id}`
Obtém resultado completo.

**Response:**
```json
{
  "result": {
    "analysis_id": "uuid",
    "total_frames": 300,
    "frames_with_anomalies": 45,
    "frames_analysis": [
      {
        "frame_number": 10,
        "timestamp": 0.33,
        "bounding_boxes": [
          {
            "x_min": 100, "y_min": 150,
            "x_max": 200, "y_max": 250,
            "class_name": "bleeding",
            "confidence": 0.87,
            "anomaly_type": "bleeding",
            "severity": "critical"
          }
        ]
      }
    ],
    "gemini_report": "# Relatório de Análise...",
    "metadata": {
      "duration": 10.0,
      "fps": 30,
      "width": 1920,
      "height": 1080
    }
  }
}
```

#### **WebSocket** `/ws/analysis/{analysis_id}`
Stream de eventos em tempo real.

**Mensagens:**
```json
{
  "type": "progress",
  "data": {"progress_percentage": 45.2, "message": "Frame 136/300"}
}

{
  "type": "alert",
  "data": {
    "severity": "critical",
    "anomaly_type": "bleeding",
    "message": "Sangramento detectado com alta confiança",
    "frame_number": 10,
    "frame_timestamp": 0.33,
    "confidence": 0.87,
    "timestamp": "2024-01-15T10:30:00Z"
  }
}

{
  "type": "completed",
  "data": {"message": "Análise concluída"}
}
```

**Documentação Interativa:** http://localhost:8000/docs

---

## ⚠️ Limitações

### Técnicas

- **Modelos YOLOv8**: Treinados em datasets gerais (COCO), requerem fine-tuning com imagens cirúrgicas reais para produção
- **Classificação de Áudio**: Usa heurísticas simples; modelo ML dedicado aumentaria precisão
- **Armazenamento**: Sistema atual usa memória local; produção requer banco de dados (PostgreSQL) e storage cloud (S3/GCS)
- **Concorrência**: Análises CPU-intensive podem sobrecarregar servidor; considere queue system (Celery) para produção
- **WebSocket**: Sem persistência; reconexões perdem histórico não salvo

### Regulatórias

- ⚠️ **Este sistema é apenas demonstrativo e NÃO deve ser usado para decisões clínicas reais**
- Não certificado para uso médico (ISO 13485, FDA 510(k), CE mark)
- Requer validação clínica extensiva antes de deployment hospitalar
- Dados sensíveis necessitam criptografia end-to-end e compliance HIPAA/LGPD

### Performance

- **Vídeos grandes (>500 MB)**: Considere streaming chunked upload
- **Latência Gemini**: API externa pode adicionar 5-15s; fallback para relatórios locais recomendado
- **Cold Start**: Primeira requisição carrega modelo YOLOv8 (~2GB RAM)

---

## 🧪 Testes

### Backend

```bash
cd backend

# Todos os testes
pytest tests/ -v

# Com cobertura
pytest tests/ --cov=app --cov-report=html

# Teste específico
pytest tests/test_video_service.py::test_process_video_success -v
```

### Frontend

```bash
cd frontend

# Lint
npm run lint

# Build test
npm run build
```

---

## 🤝 Contribuição

1. Fork o projeto
2. Crie branch de feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para branch (`git push origin feature/nova-funcionalidade`)
5. Abra Pull Request

**Diretrizes:**

- Código Python: PEP 8, type hints, docstrings
- Código JavaScript: ESLint, comentários em português
- Testes: Cobertura mínima 80%
- Commits: Conventional Commits (feat, fix, docs, etc.)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja arquivo [LICENSE](LICENSE) para detalhes.

---

## 👥 Autores

- **Equipe MedVision AI** - Projeto Tech Challenge F04

---

## 🙏 Agradecimentos

- **Ultralytics** pelo YOLOv8
- **Google** pelo Gemini API
- **librosa** team pela biblioteca de análise de áudio
- Comunidade open-source de FastAPI e React

---

## 📞 Contato

- **Email**: contato@medvision.ai
- **GitHub**: https://github.com/seu-usuario/medvision-ai
- **Issues**: https://github.com/seu-usuario/medvision-ai/issues

---

**⚕️ Desenvolvido com ❤️ para melhorar a segurança cirúrgica com IA**
