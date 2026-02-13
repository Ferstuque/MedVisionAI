# 🧹 Script de Limpeza do Projeto

## Scripts e Arquivos Removidos

Os seguintes diretórios foram marcados para NÃO serem commitados no GitHub:

### 📁 `scripts_de_teste/` - Scripts de Teste e Desenvolvimento

**Status**: ❌ Não incluir no repositório final

**Arquivos:**
- `create_test_video.py` - Geração de vídeos sintéticos para teste
- `record_webcam_test.py` - Captura de webcam para testes
- `reencode_video.py` - Re-encoding de vídeos
- `test_audio_system.py` - Testes manuais de áudio
- `test_gemini_video.py` - Testes manuais da API Gemini
- `upload_audio.py` - Script de upload para testes

**Motivo**: Scripts auxiliares de desenvolvimento não necessários para produção ou uso do MVP.

### 📁 `arquivos_de_teste/` - Arquivos de Mídia para Teste

**Status**: ❌ Não incluir no repositório final

**Arquivos:**
- `Rachel_PT_BR.mp3` - Áudio de teste
- `Rachel_PT_BR_2.mp3` - Áudio de teste
- `test_video.mp4` - Vídeo de exemplo
- `test_video2.mp4` - Vídeo de exemplo

**Motivo**: Arquivos de mídia grandes (>10MB) que aumentam o tamanho do repositório desnecessariamente.

### 📦 `Instrument_Anatomy_Original_Dataset.zip`

**Status**: ❌ Não incluir no repositório final

**Motivo**: Dataset grande (provavelmente >100MB) que deve ser hospedado externamente ou distribuído via link.

## ✅ Arquivos Mantidos

### Scripts Essenciais

- ✅ `backend/` - Código do backend completo
- ✅ `frontend/` - Código do frontend completo
- ✅ `infrastructure/` - IaC com Terraform
- ✅ `docs/` - Documentação do projeto
- ✅ `notebooks/` - Notebooks de fine-tuning
- ✅ `tests/` - Suíte de testes automatizados

### Arquivos de Configuração

- ✅ `README.md` - Documentação principal
- ✅ `docker-compose.yml` - Configuração Docker
- ✅ `cloudbuild.yaml` - Build do Cloud Run
- ✅ `.gitignore` - Arquivos ignorados
- ✅ `LICENSE` - Licença MIT

## 🚀 Ações Realizadas

1. **.gitignore atualizado** para ignorar:
   - `scripts_de_teste/`
   - `arquivos_de_teste/`
   - `*.zip` (datasets)
   - `*.mp4`, `*.mp3`, `*.wav` (exceto em docs/)
   - Arquivos temporários e caches

2. **README.md atualizado** com:
   - Badges profissionais
   - Nomenclaturas corretas (Gemini 2.5 Flash)
   - Instruções de deploy melhoradas

3. **Infraestrutura criada**:
   - `infrastructure/main.tf` - Terraform config
   - `cloudbuild.yaml` - Cloud Build config
   - Deploy automatizado para Cloud Run

## 📝 Recomendações

### Para Distribuição de Datasets

Se precisar compartilhar datasets ou arquivos de teste:

```bash
# Opção 1: Google Drive
# Upload para Drive e compartilhe link público

# Opção 2: Google Cloud Storage
gsutil cp Instrument_Anatomy_Original_Dataset.zip \
  gs://medvision-public-datasets/

# Opção 3: GitHub Release
# Crie uma release e anexe como asset
```

### Para Testes Futuros

Se precisar de arquivos de teste no CI/CD:

```yaml
# .github/workflows/test.yml
- name: Download test files
  run: |
    wget https://storage.googleapis.com/medvision-test-files/test_video.mp4
    wget https://storage.googleapis.com/medvision-test-files/test_audio.mp3
```

### Estrutura Final do Repositório

```
medvision-ai/
├── backend/              ✅ Incluir
├── frontend/             ✅ Incluir
├── infrastructure/       ✅ Incluir
├── docs/                 ✅ Incluir
├── notebooks/            ✅ Incluir
├── .github/              ✅ Incluir (CI/CD)
├── README.md             ✅ Incluir
├── docker-compose.yml    ✅ Incluir
├── cloudbuild.yaml       ✅ Incluir
├── LICENSE               ✅ Incluir
├── .gitignore            ✅ Incluir
├── scripts_de_teste/     ❌ Ignorado
├── arquivos_de_teste/    ❌ Ignorado
└── *.zip                 ❌ Ignorado
```

## 🎯 Tamanho Estimado do Repositório

- **Antes da limpeza**: ~500-800 MB (com datasets e vídeos)
- **Depois da limpeza**: ~50-80 MB (apenas código)
- **Redução**: ~90% menor!

---

**Nota**: Os arquivos não foram deletados do disco, apenas marcados para serem ignorados pelo Git. Você ainda pode usá-los localmente para desenvolvimento.
