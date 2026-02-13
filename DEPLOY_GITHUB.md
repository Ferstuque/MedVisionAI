# 🚀 Guia de Publicação no GitHub

## Passo a Passo para Publicar o MedVision AI

### 1️⃣ Preparação Local

```powershell
# Navegar para o diretório do projeto
cd C:\dev\TechChallengeF04

# Inicializar repositório Git (se ainda não foi feito)
cd medvision-ai
git init

# Adicionar remote do GitHub (substitua com seu usuário)
git remote add origin https://github.com/SEU-USUARIO/medvision-ai.git

# Verificar status
git status
```

### 2️⃣ Criar Repositório no GitHub

1. Acesse https://github.com/new
2. Configure:
   - **Repository name**: `medvision-ai`
   - **Description**: "🏥 Plataforma de Análise Multimodal Cirúrgica com IA - YOLOv8 + Gemini 2.5 Flash"
   - **Visibility**: Public (ou Private se preferir)
   - ❌ **NÃO** inicialize com README, .gitignore ou LICENSE (já temos)
3. Clique em "Create repository"

### 3️⃣ Adicionar Arquivos ao Git

```powershell
# Adicionar todos os arquivos (respeitando .gitignore)
git add .

# Verificar o que será commitado
git status

# Se aparecer arquivos grandes ou indesejados, adicione ao .gitignore e execute:
# git rm --cached arquivo_grande.mp4
# git add .gitignore

# Fazer commit inicial
git commit -m "feat: Initial commit - MedVision AI MVP

- Backend FastAPI com YOLOv8 e Gemini 2.5 Flash
- Frontend React com visualização em tempo real
- 94+ testes automatizados (coverage 27%)
- Infraestrutura como código (Terraform)
- Deploy automatizado para GCP Cloud Run
- Documentação completa e badges"
```

### 4️⃣ Push para GitHub

```powershell
# Criar e mudar para branch main
git branch -M main

# Enviar para GitHub
git push -u origin main
```

### 5️⃣ Configurar Repositório no GitHub

#### A. Adicionar Topics (Tags)

No repositório GitHub, clique em "⚙️ Settings" > "General" > "Topics":

```
machine-learning
computer-vision
yolov8
fastapi
react
healthcare
medical-ai
deep-learning
object-detection
gemini-api
cloud-run
terraform
```

#### B. Editar About

- **Description**: "🏥 Plataforma de Análise Multimodal Cirúrgica com IA usando YOLOv8, Gemini 2.5 Flash e React"
- **Website**: (URL do Cloud Run após deploy, se tiver)
- ✅ **Releases**
- ✅ **Packages**

#### C. Configurar Branch Protection (Opcional para produção)

Settings > Branches > Add rule:
- Branch name pattern: `main`
- ✅ Require a pull request before merging
- ✅ Require status checks to pass before merging

### 6️⃣ Criar Release v1.0.0

1. No GitHub, vá em "Releases" > "Create a new release"
2. **Tag**: `v1.0.0`
3. **Title**: "🎉 MedVision AI - MVP v1.0.0"
4. **Description**:

```markdown
## 🏥 MedVision AI - MVP v1.0.0

Primeira release pública do MedVision AI, uma plataforma completa de análise multimodal cirúrgica com inteligência artificial.

### ✨ Funcionalidades

- ✅ **Análise de Vídeo** com YOLOv8 (detecção de anomalias)
- ✅ **Análise de Áudio** com librosa (indicadores psicológicos)
- ✅ **Relatórios com IA** usando Gemini 2.5 Flash
- ✅ **Alertas em Tempo Real** via WebSocket
- ✅ **Dashboard Interativo** em React
- ✅ **94+ Testes Automatizados**
- ✅ **Deploy Cloud Run** com IaC (Terraform)

### 📦 Stack Tecnológico

**Backend**: Python 3.11+ | FastAPI | YOLOv8 | Gemini 2.5 Flash | librosa  
**Frontend**: React 18 | Vite | Tailwind CSS | WebSocket  
**DevOps**: Docker | Cloud Run | Terraform | pytest

### 🚀 Quick Start

```bash
git clone https://github.com/SEU-USUARIO/medvision-ai.git
cd medvision-ai
docker-compose up
```

Acesse: http://localhost:5173

### 📚 Documentação

- [README Completo](./README.md)
- [Guia de Instalação](./README.md#instalação)
- [API Documentation](http://localhost:8000/docs)
- [Infraestrutura (IaC)](./infrastructure/README.md)

### ⚠️ Avisos

- MVP educacional - NÃO usar para decisões clínicas reais
- Requer API Key do Gemini (gratuita em https://ai.google.dev/)
- Modelos YOLOv8 não foram fine-tuned com dados cirúrgicos reais

### 🙏 Agradecimentos

Ultralytics (YOLOv8) | Google (Gemini AI) | Comunidade Open Source

---

**⚕️ Desenvolvido para melhorar a segurança cirúrgica com IA**
```

5. Clique em "Publish release"

### 7️⃣ Configurar Secrets para CI/CD (Se for usar GitHub Actions)

Settings > Secrets and variables > Actions > New repository secret:

- `GCP_PROJECT_ID`: ID do projeto GCP
- `GCP_SA_KEY`: JSON completo da Service Account
- `GEMINI_API_KEY`: Chave da API Gemini

### 8️⃣ Adicionar Badge ao README

O README já está com badges! Verifique se aparecem corretamente no GitHub.

### 9️⃣ Criar Documentação Adicional (Opcional)

#### A. CONTRIBUTING.md

```markdown
# 🤝 Contribuindo para o MedVision AI

Obrigado por considerar contribuir! Este guia ajudará você a começar.

## 📋 Como Contribuir

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 🧪 Testes

Execute os testes antes de abrir PR:

```bash
cd backend
pytest tests/ -v
```

## 📝 Convenções

- **Commits**: Use Conventional Commits (feat, fix, docs, etc.)
- **Código Python**: PEP 8, type hints, docstrings
- **Código JavaScript**: ESLint, Prettier

## 🐛 Reportar Bugs

Abra uma issue com:
- Descrição clara do problema
- Passos para reproduzir
- Comportamento esperado vs atual
- Screenshots (se aplicável)

## 💡 Sugerir Features

Abra uma issue com tag `enhancement`:
- Descrição da feature
- Justificativa (por que é útil?)
- Exemplos de uso

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a MIT License.
```

#### B. CHANGELOG.md

```markdown
# Changelog

Todas as mudanças notáveis neste projeto serão documentadas aqui.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2026-02-13

### Adicionado
- Análise de vídeo com YOLOv8
- Análise de áudio com librosa
- Geração de relatórios com Gemini 2.5 Flash
- Sistema de alertas em tempo real (WebSocket)
- Dashboard React interativo
- 94+ testes automatizados
- Infraestrutura como código (Terraform)
- Deploy automatizado para Cloud Run
- Documentação completa

### Tecnologias
- Backend: FastAPI + Python 3.11+
- Frontend: React 18 + Vite + Tailwind
- IA: YOLOv8, Gemini 2.5 Flash, librosa
- DevOps: Docker, Cloud Run, Terraform
```

### 🎯 Checklist Final

Antes de considerar o projeto "pronto para publicação":

- [x] README.md atualizado com badges
- [x] .gitignore configurado corretamente
- [x] Nomenclaturas corretas (Gemini 2.5 Flash)
- [x] Infraestrutura como código (Terraform)
- [x] Cloud Build configurado
- [x] Testes documentados com coverage
- [x] Documentação de deploy completa
- [ ] LICENSE file presente (MIT)
- [ ] Screenshots na documentação
- [ ] Vídeo demo (opcional mas recomendado)
- [ ] First commit feito
- [ ] Repositório no GitHub criado
- [ ] Remote adicionado e push realizado
- [ ] Release v1.0.0 criada
- [ ] Topics/tags configuradas

### 📸 Adicionar Screenshots

Tire screenshots e adicione ao README:

```bash
# Criar diretório para imagens
mkdir docs/images

# Adicionar screenshots:
# - docs/images/dashboard.png
# - docs/images/video-analysis.png
# - docs/images/report.png
# - docs/images/architecture.png
```

Atualize o README com:

```markdown
## 📸 Screenshots

### Dashboard Principal
![Dashboard](./docs/images/dashboard.png)

### Análise de Vídeo em Tempo Real
![Video Analysis](./docs/images/video-analysis.png)

### Relatório Gerado por IA
![Report](./docs/images/report.png)
```

### 🎥 Vídeo Demo (Recomendado)

Grave um screencast de 2-3 minutos mostrando:
1. Upload de vídeo
2. Análise em tempo real
3. Visualização de bounding boxes
4. Relatório final

Ferramentas recomendadas:
- **Windows**: Xbox Game Bar (Win + G)
- **Mac**: QuickTime
- **Cross-platform**: OBS Studio

Upload no YouTube como unlisted e adicione link no README.

### 🔗 Links Úteis

- **GitHub Markdown**: https://guides.github.com/features/mastering-markdown/
- **Badges**: https://shields.io/
- **Conventional Commits**: https://www.conventionalcommits.org/pt-br/
- **Keep a Changelog**: https://keepachangelog.com/pt-BR/

---

**Pronto! Seu projeto está preparado para o GitHub!** 🚀
