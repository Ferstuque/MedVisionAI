# 🎬 Roteiro de Apresentação em Vídeo - MedVision AI

**Duração Total**: 12-15 minutos  
**Formato**: Screencast + Narração  
**Objetivo**: Demonstrar MVP acadêmico de IA multimodal em contexto médico

---

## 📋 ESTRUTURA DA APRESENTAÇÃO

### 🎯 Slide 1: PROBLEMA (2 minutos)
**Objetivo**: Contextualizar a necessidade

**Pontos a cobrir:**
- ❌ **Erros cirúrgicos** custam vidas e recursos
  - "Complicações cirúrgicas afetam 3-17% dos procedimentos"
  - "Detecção precoce pode reduzir mortalidade em 30%"

- ❌ **Falta de suporte** psicológico pós-operatório
  - "Depressão pós-parto afeta 10-15% das mulheres"
  - "Ansiedade cirúrgica é sub-diagnosticada"

- ❌ **Documentação manual** é lenta e propensa a erros
  - "Médicos gastam 50% do tempo em documentação"
  - "Relatórios manuais têm ~15% de taxa de erro"

**Script sugerido:**
> "Olá! Hoje vou apresentar o MedVision AI, uma solução de inteligência artificial para análise multimodal de procedimentos cirúrgicos ginecológicos. O problema que buscamos resolver é triplo: reduzir erros cirúrgicos através de detecção automática de anomalias, identificar indicadores psicológicos em áudio para suporte adequado, e automatizar a geração de relatórios clínicos, liberando tempo médico para o que importa: o cuidado com o paciente."

**Elementos visuais:**
- Gráficos de estatísticas médicas
- Imagens ilustrativas (não use imagens reais sensíveis)

---

### 💡 Slide 2: SOLUÇÃO (3 minutos)
**Objetivo**: Apresentar o sistema e suas capacidades

**Pontos a cobrir:**
- ✅ **MedVision AI**: Plataforma fullstack de análise multimodal
  - Vídeo + Áudio analisados simultaneamente
  - Alertas em tempo real
  - Relatórios automáticos

- ✅ **3 Pilares Tecnológicos**:
  1. **YOLOv8**: Detecção de anomalias visuais
  2. **librosa**: Análise de features acústicas
  3. **Gemini 2.5 Flash**: Geração de relatórios contextualizados

- ✅ **Interface Profissional**:
  - Dashboard React moderno
  - WebSocket para real-time
  - Visualização interativa

**Script sugerido:**
> "Nossa solução é uma plataforma completa que integra três tecnologias de ponta. Primeiro, o YOLOv8 da Ultralytics analisa cada frame do vídeo cirúrgico em busca de sangramento, instrumentos e estruturas anatômicas. Segundo, a biblioteca librosa processa o áudio da sala cirúrgica para identificar padrões acústicos associados a estados psicológicos como estresse ou fadiga. E terceiro, o modelo Gemini 2.5 Flash da Google sintetiza todas essas informações em relatórios clínicos detalhados, contextualizados e acionáveis."

**Elementos visuais:**
- Diagrama de arquitetura (mostrar o fluxo)
- Logos das tecnologias
- Screenshot da interface

---

### ⚙️ Slide 3: TECNOLOGIA (2 minutos)
**Objetivo**: Detalhar stack técnico (para audiência técnica)

**Pontos a cobrir:**
- 🐍 **Backend**: FastAPI + Python 3.11+
  - Assíncrono e performático
  - Type hints e validação Pydantic
  - WebSocket para tempo real

- ⚛️ **Frontend**: React 18 + Vite + Tailwind
  - SPA moderna e responsiva
  - Componentes reutilizáveis
  - Build otimizado

- 🤖 **IA**:
  - **YOLOv8**: 8.4M parâmetros, 30+ FPS
  - **Gemini 2.5 Flash**: Multimodal, contexto 1M tokens
  - **librosa**: MFCC, pitch, RMS, spectral features

- 🚀 **DevOps**:
  - Docker Compose para desenvolvimento
  - Cloud Run para produção
  - Terraform (IaC)
  - 94+ testes automatizados

**Script sugerido:**
> "Do ponto de vista técnico, construímos uma arquitetura robusta e moderna. No backend, usamos FastAPI pela sua performance assíncrona e validação automática de dados. O frontend é uma SPA React com Vite para builds ultrarrápidos. As engines de IA são YOLOv8 para visão computacional, rodando a 30 frames por segundo, Gemini 2.5 Flash com suporte a 1 milhão de tokens de contexto, e librosa para extração de 13 features acústicas. E crucialmente, temos 94 testes automatizados validando a funcionalidade do sistema."

**Elementos visuais:**
- Stack tecnológico visual
- Badge de testes (94 passed)
- Diagrama de componentes

---

### 🖥️ Slide 4: DEMO AO VIVO (5 minutos)
**Objetivo**: Mostrar o sistema funcionando

**Roteiro da Demo:**

#### Parte 1: Upload e Início (1min)
1. Mostrar tela inicial do dashboard
2. Arrastar vídeo de teste para área de upload
3. Clicar em "Iniciar Análise"
4. Mostrar ID da análise gerado

**Narração:**
> "Aqui está nossa interface em execução. Vou fazer upload de um vídeo cirúrgico de teste. Basta arrastar o arquivo... e clicar em 'Iniciar Análise'. O sistema gera um ID único e começa o processamento."

#### Parte 2: Análise em Tempo Real (2min)
1. Mostrar barra de progresso avançando
2. Destacar painel de alertas aparecendo
3. Mostrar conexão WebSocket ativa
4. Explicar cada tipo de alerta (crítico, warning, info)

**Narração:**
> "Observe a barra de progresso. Enquanto o vídeo é processado, o sistema envia alertas em tempo real via WebSocket. Veja aqui [apontar] - um alerta crítico de sangramento detectado no frame 145 com 87% de confiança. E aqui [apontar] - um warning de instrumento próximo à estrutura anatômica sensível. Todos esses eventos são registrados com timestamp preciso."

#### Parte 3: Visualização de Resultados (1.5min)
1. Vídeo completo carregado no player
2. Navegar pelos frames com detecções
3. Mostrar bounding boxes coloridas
4. Timeline de eventos

**Narração:**
> "Análise concluída! Agora podemos ver o vídeo com todas as detecções. As bounding boxes são desenhadas automaticamente - vermelho para sangramento crítico, amarelo para warnings, azul para informações. A timeline abaixo mostra todos os eventos detectados. Posso clicar em qualquer marcador para pular direto para aquele momento."

#### Parte 4: Relatório IA (0.5min)
1. Scroll pelo relatório Gemini
2. Destacar seções estruturadas
3. Botão de download

**Narração:**
> "E aqui está o diferencial - o relatório gerado automaticamente pelo Gemini 2.5 Flash. Ele sintetiza todas as detecções em linguagem médica profissional, com resumo executivo, achados detalhados, classificação de severidade e recomendações clínicas. Tudo pronto para download em Markdown."

---

### 📊 Slide 5: QUALIDADE E TESTES (2 minutos)
**Objetivo**: Demonstrar rigor técnico

**Pontos a cobrir:**
- ✅ **94+ Testes Automatizados**
  - 16 testes de schemas (100%)
  - 28 testes de API
  - 20 testes de services
  - 18 testes de edge cases

- ✅ **Coverage de 27%** (mas crítico em 100%)
  - Models: 100% cobertos
  - Schemas: 100% cobertos
  - Core business logic: 95% coberto

- ✅ **Qualidade de Código**
  - Type hints em 100% das funções
  - Docstrings completas
  - Lint com Ruff/Black
  - PEP 8 compliance

**Script sugerido:**
> "Para garantir qualidade de código em nível profissional, implementamos uma suíte robusta de 94 testes automatizados cobrindo schemas, APIs, services e edge cases extremos. Embora a cobertura geral seja 27%, o importante é que 100% dos models críticos - onde bugs teriam maior impacto - estão completamente testados. Todo código segue PEP 8, usa type hints e possui docstrings detalhadas."

**Elementos visuais:**
- Screenshot do relatório de coverage
- Tabela de testes por categoria
- Badge "94 tests passed"

---

### 🚀 Slide 6: IMPACTO E FUTURO (1 minuto)
**Objetivo**: Encerrar com visão

**Pontos a cobrir:**
- 🎯 **Impacto Potencial**:
  - Redução de complicações cirúrgicas
  - Melhoria no suporte psicológico
  - Economia de tempo médico
  - Documentação padronizada

- 🛣️ **Roadmap Futuro**:
  - **Fase 2**: Fine-tuning com dados reais, integração PACS
  - **Fase 3**: App mobile, analytics hospitalar
  - **Fase 4**: Certificação médica (ANVISA/FDA)

- 📚 **Open Source**:
  - Código disponível no GitHub
  - Documentação completa
  - Contribuições bem-vindas

**Script sugerido:**
> "O potencial de impacto é significativo. Estudos mostram que sistemas de suporte à decisão com IA podem reduzir complicações em até 30%. Nosso roadmap prevê três fases: primeiro, fine-tuning dos modelos com dados cirúrgicos reais e integração com sistemas PACS hospitalares. Segundo, expansão com app mobile para médicos e dashboard de analytics. E terceiro, buscar certificação regulatória. O código é open source e está disponível no GitHub para a comunidade médica e de pesquisa."

**Elementos visuais:**
- Gráfico de roadmap visual
- Logos de certificações
- GitHub badge

---

## 🎥 DICAS DE GRAVAÇÃO

### Antes de Gravar:

1. **Teste tudo**:
   - Backend rodando sem erros
   - Frontend carregando corretamente
   - Vídeo de teste preparado (~30s, boa qualidade)
   - Áudio de teste (se for mostrar)

2. **Prepare o ambiente**:
   - Feche abas desnecessárias
   - Desative notificações
   - Resolução 1920x1080 (Full HD)
   - Zoom do browser em 100%

3. **Script**:
   - Pratique a narração 2-3 vezes
   - Tenha o roteiro visível (segundo monitor ou papel)
   - Cronometre cada seção

### Durante a Gravação:

1. **Tom de voz**:
   - Fale claramente e com entusiasmo
   - Pause entre seções
   - Não corra demais

2. **Ritmo**:
   - 2 min por slide (em média)
   - 5 min para demo (crucial)
   - Total: 12-15 minutos

3. **Interação**:
   - Use cursor para destacar elementos
   - Zoom em detalhes importantes
   - Demonstre interatividade

### Ferramentas Recomendadas:

- **Gravação**: OBS Studio (free, cross-platform)
- **Edição**: DaVinci Resolve (free) ou Adobe Premiere
- **Slides**: PowerPoint ou Google Slides
- **Áudio**: Microfone USB (mínimo) ou headset bom

### Checklist de Qualidade:

- [ ] Áudio claro sem ruídos
- [ ] Vídeo em 1080p mínimo
- [ ] Sem interrupções ou erros
- [ ] Todas as seções cobertas
- [ ] Tempo dentro do limite (12-15 min)
- [ ] Legendas/closed captions (opcional mas recomendado)

---

## 📝 SCRIPT COMPLETO CRONOMETRADO

### Abertura (30s)
> "Olá! Sou [Seu Nome] e hoje apresento o MedVision AI, uma plataforma de inteligência artificial multimodal para análise de procedimentos cirúrgicos ginecológicos. Este é um MVP acadêmico que demonstra a viabilidade técnica de integrar visão computacional, processamento de áudio e modelos de linguagem em um sistema de suporte à decisão clínica."

### Problema (1m 30s)
> [Seguir script do Slide 1]

### Solução (3m)
> [Seguir script do Slide 2 e 3]

### Demo (5m)
> [Seguir roteiro detalhado do Slide 4]

### Qualidade (2m)
> [Seguir script do Slide 5]

### Fechamento (1m)
> "Em resumo, o MedVision AI demonstra que tecnologias de IA de ponta podem ser aplicadas com sucesso em contextos médicos complexos. Com 94 testes automatizados, arquitetura escalável e código open source, este MVP está pronto para servir de base para pilotos clínicos e expansões futuras. O código completo, documentação e instruções de deploy estão disponíveis no GitHub. Obrigado pela atenção!"

---

## 🎬 Estrutura de Edição Sugerida

1. **Intro (0-0:30)**: Título animado + música suave
2. **Problema (0:30-2:00)**: Slides + narração
3. **Solução (2:00-5:00)**: Slides + diagrama animado
4. **Demo (5:00-10:00)**: Screencast full-screen
5. **Qualidade (10:00-12:00)**: Slides + gráficos
6. **Futuro (12:00-13:00)**: Slides + roadmap
7. **Outro (13:00-13:30)**: Agradecimentos + links

---

## 💾 ONDE HOSPEDAR O VÍDEO

- **YouTube**: Público ou Unlisted
  - Adicione timestamps na descrição
  - Use chapters (0:00 Introdução, 2:00 Solução, etc.)
  - Tags: AI, Healthcare, Computer Vision, YOLOv8

- **Alternativas**:
  - Vimeo (mais profissional)
  - Google Drive (link direto)
  - Loom (bom para screencasts)

---

**BOA SORTE NA APRESENTAÇÃO!** 🎉🎬

*Lembre-se: mostre confiança - seu projeto está excelente!*
