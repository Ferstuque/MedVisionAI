# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-02-13

### 🎉 Lançamento Inicial

Primeira release pública do **MedVision AI** - Plataforma de Análise Multimodal Cirúrgica com IA.

### ✨ Adicionado

#### Backend
- API REST completa com FastAPI 0.115+
- Análise de vídeo com YOLOv8 (detecção de anomalias, sangramento, instrumentos)
- Análise de áudio com librosa (features psicológicas: MFCC, pitch, RMS, spectral)
- Geração de relatórios com Google Gemini 2.5 Flash
- Sistema de alertas em tempo real via WebSocket
- Validação de dados com Pydantic schemas
- Logging estruturado
- CORS configurado para desenvolvimento e produção
- Armazenamento local de vídeos, áudios e relatórios

#### Frontend
- Dashboard React 18 interativo e responsivo
- Upload de vídeo com drag & drop
- Visualização de análise em tempo real (progress bars)
- Player de vídeo com bounding boxes sobrepostas
- Painel de alertas com severidade (crítico, warning, info)
- Sistema de navegação com React Router
- Integração WebSocket para atualizações live
- Tema dark/light (Tailwind CSS)
- Componentes reutilizáveis (AlertPanel, VideoPlayer, BoundingBoxOverlay)

#### Testes
- 94+ testes automatizados com pytest
- Cobertura de 27% (100% em models críticos)
- 16 testes de schemas Pydantic
- 28 testes de rotas API
- 20 testes de services (business logic)
- 18 testes de edge cases
- 12 testes de integração
- Mocks para YOLO e Gemini
- Coverage HTML report

#### Infraestrutura
- Docker Compose para desenvolvimento local
- Dockerfile multi-stage para produção
- Terraform para Cloud Run (GCP)
- Cloud Build para CI/CD
- Secrets Manager para API keys
- Service Account com IAM policies
- Nginx para servir React em produção

#### Documentação
- README completo com badges, arquitetura e setup
- Guia de testes (README_TESTS.md)
- Guia de deploy GCP (infrastructure/README.md)
- Guia de instalação local (TESTE_LOCAL.md)
- Guia de fine-tuning YOLOv8 (docs/FINE_TUNING_GUIDE.md)
- Colab quickstart (docs/COLAB_QUICKSTART.md)
- Roteiro de apresentação (ROTEIRO_APRESENTACAO.md)
- Guia de publicação GitHub (DEPLOY_GITHUB.md)
- Contributing guidelines (CONTRIBUTING.md)

### 🛠️ Stack Tecnológico

**Backend**
- Python 3.11+
- FastAPI 0.115.6
- YOLOv8 (ultralytics 8.3.0)
- Google Gemini 2.5 Flash
- librosa 0.10.2
- OpenCV 4.10
- pytest 9.0.2

**Frontend**
- React 18.3.1
- Vite 5.3.3
- Tailwind CSS 3.4.10
- React Router 6.26.2
- Axios 1.7.8

**DevOps**
- Docker & Docker Compose
- Terraform 5.0+
- Google Cloud Run
- Cloud Build
- GitHub Actions (CI/CD)

### 📊 Métricas

- **103 arquivos** de código
- **25.818 linhas** adicionadas
- **27% coverage** (100% em schemas/models)
- **94 testes** passando
- **~80MB** tamanho do repositório (após cleanup)

### ⚠️ Avisos Importantes

- ⚠️ **MVP Educacional**: NÃO usar para decisões clínicas reais
- ⚠️ **Modelos não fine-tuned**: YOLOv8 usa pesos genéricos (não treinado em dados cirúrgicos)
- ⚠️ **Requer API Key**: Gemini API necessária (gratuita em https://ai.google.dev/)
- ⚠️ **Dados de teste**: Vídeos de teste NÃO são dados médicos reais

### 🔒 Segurança

- CORS configurado
- API keys em variáveis de ambiente
- Secrets Manager para produção
- .gitignore para excluir credenciais
- HTTPS obrigatório em produção

### 📝 Licença

MIT License - Veja [LICENSE](../LICENSE)

---

## [Unreleased]

### 🛣️ Roadmap v2.0

#### Planejado
- Fine-tuning YOLOv8 com dataset GynsurGE
- Integração com sistemas PACS hospitalares
- App mobile (React Native)
- Dashboard de analytics hospitalar
- Suporte a múltiplos idiomas
- Exportação de relatórios em PDF
- Autenticação e autorização (OAuth2)
- Armazenamento em Cloud Storage (GCS/S3)

#### Em discussão
- Detecção de emoções em tempo real (análise facial)
- Integração com prontuários eletrônicos (FHIR)
- Certificação médica (ANVISA/FDA)
- Sistema de notificações (email/SMS)
- Auditoria e compliance LGPD/HIPAA

---

## 📖 Tipos de Mudanças

- **Added**: Novas funcionalidades
- **Changed**: Mudanças em funcionalidades existentes
- **Deprecated**: Funcionalidades que serão removidas
- **Removed**: Funcionalidades removidas
- **Fixed**: Correções de bugs
- **Security**: Correções de segurança

---

**Última atualização**: 2026-02-13
