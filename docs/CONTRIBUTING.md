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

Para coverage report:

```bash
pytest tests/ --cov=app --cov-report=html
```

## 📝 Convenções

### Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/pt-br/):

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `test:` Testes
- `refactor:` Refatoração
- `chore:` Manutenção

### Código Python

- **PEP 8**: Seguir guia de estilo Python
- **Type Hints**: Sempre usar anotações de tipo
- **Docstrings**: Documentar funções públicas
- **Testing**: Mínimo 80% de coverage em código novo

Exemplo:

```python
def analyze_video(video_path: str, config: AnalysisConfig) -> VideoAnalysisResult:
    """
    Analisa vídeo cirúrgico usando YOLOv8.
    
    Args:
        video_path: Caminho para o arquivo de vídeo
        config: Configurações de análise
        
    Returns:
        Resultado da análise com detecções e métricas
        
    Raises:
        FileNotFoundError: Se o vídeo não existir
        InvalidVideoError: Se o formato for inválido
    """
    # Implementation
```

### Código JavaScript/React

- **ESLint**: Seguir configuração do projeto
- **Prettier**: Formatação automática
- **Componentes**: Preferir componentes funcionais
- **Hooks**: Usar hooks do React

Exemplo:

```jsx
import { useState, useEffect } from 'react';

/**
 * Componente para análise de vídeo em tempo real
 */
export const VideoAnalyzer = ({ videoId }) => {
  const [progress, setProgress] = useState(0);
  
  useEffect(() => {
    // Implementation
  }, [videoId]);
  
  return (
    <div className="video-analyzer">
      {/* JSX */}
    </div>
  );
};
```

## 🐛 Reportar Bugs

Abra uma [issue](https://github.com/Ferstuque/MedVisionAI/issues/new) com:

- **Descrição clara** do problema
- **Passos para reproduzir**:
  1. Passo 1
  2. Passo 2
  3. Erro ocorre
- **Comportamento esperado** vs **atual**
- **Screenshots** (se aplicável)
- **Ambiente**:
  - OS: Windows/Mac/Linux
  - Python: 3.11+
  - Node: 18+
  - Browser: Chrome/Firefox/Safari

**Template de Issue:**

```markdown
## Descrição
[Descreva o bug claramente]

## Reprodução
1. [Primeiro passo]
2. [Segundo passo]
3. [Veja o erro]

## Esperado
[O que deveria acontecer]

## Atual
[O que está acontecendo]

## Ambiente
- OS: Windows 11
- Python: 3.11.5
- Browser: Chrome 120

## Screenshots
[Cole imagens se relevante]
```

## 💡 Sugerir Features

Abra uma [issue](https://github.com/Ferstuque/MedVisionAI/issues/new) com tag `enhancement`:

- **Descrição da feature**
- **Justificativa** (por que é útil?)
- **Exemplos de uso**
- **Mockups** (se aplicável)

**Template de Feature:**

```markdown
## Feature
[Nome/descrição da funcionalidade]

## Motivação
[Por que isso é necessário?]

## Proposta
[Como deveria funcionar?]

## Exemplos
```python
# Código de exemplo
```

## Alternativas
[Outras abordagens consideradas]
```

## 🏗️ Estrutura do Projeto

```
medvision-ai/
├── backend/          # API FastAPI
│   ├── app/
│   │   ├── api/     # Rotas
│   │   ├── core/    # Config, security
│   │   ├── models/  # Schemas Pydantic
│   │   ├── services/ # Business logic
│   │   └── utils/   # Helpers
│   └── tests/       # Pytest tests
├── frontend/        # React SPA
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── hooks/
│       └── services/
├── infrastructure/  # Terraform IaC
└── docs/           # Documentação
```

## 🔄 Workflow de Desenvolvimento

### Setup Local

```bash
# Clone
git clone https://github.com/Ferstuque/MedVisionAI.git
cd MedVisionAI

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install

# Docker (alternativa)
docker-compose up
```

### Criar Feature Branch

```bash
git checkout -b feature/minha-feature
```

### Desenvolver

1. Escreva código
2. Adicione testes
3. Execute testes localmente
4. Commit com mensagem clara

### Push e PR

```bash
git push origin feature/minha-feature
```

Abra PR no GitHub com:
- **Título descritivo**
- **Descrição** do que foi feito
- **Issues relacionadas** (#123)
- **Screenshots** (se UI)
- **Checklist**:
  - [ ] Testes passam
  - [ ] Documentação atualizada
  - [ ] Sem breaking changes
  - [ ] Code review solicitado

## 📚 Recursos

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [YOLOv8 Docs](https://docs.ultralytics.com/)
- [Gemini API](https://ai.google.dev/docs)
- [PEP 8](https://peps.python.org/pep-0008/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## 🙏 Código de Conduta

- Seja respeitoso
- Aceite críticas construtivas
- Foque no melhor para a comunidade
- Empatia com outros contribuidores

## 📧 Contato

- Abra uma [issue](https://github.com/Ferstuque/MedVisionAI/issues)
- Discussões no [GitHub Discussions](https://github.com/Ferstuque/MedVisionAI/discussions)

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a [MIT License](../LICENSE).

---

**Obrigado por contribuir para o MedVision AI!** 🏥🤖
