# StackSpot Agent API

Uma API Python para interagir com agentes de IA da StackSpot, oferecendo uma interface simplificada para criação, gerenciamento e interação com agentes inteligentes.

## 📚 Links Úteis

- [Documentação Oficial da StackSpot](https://docs.stackspot.com/)
- [Guia de Agentes IA](https://docs.stackspot.com/latest/docs/genai/concepts/agent-intro)
- [API de Inferência](https://docs.stackspot.com/latest/docs/genai/references/api/inference-api)
- [API de Upload](https://docs.stackspot.com/latest/docs/genai/references/api/upload-api)
- [Autenticação OAuth](https://docs.stackspot.com/latest/docs/genai/references/api/auth)

## 🌟 Características

- 🤖 Criação e gerenciamento de agentes IA
- 💬 Interface de chat simplificada
- 🔄 Gerenciamento de sessão e contexto
- � Upload de arquivos via S3 (Novo!)
- �🔐 Autenticação OAuth integrada
- 📝 Logging completo de interações
- ⚙️ Configuração flexível via Dynaconf

## 🛠️ Instalação

```bash
# Usando poetry (recomendado)
poetry install

# Usando pip
pip install -r requirements.txt
```

## 🚀 Início Rápido

### Exemplo Simples de Chat com Arquivos

```python
from pathlib import Path
from src.agents.chat import AgentChat
from src.models.chat_session import ChatSession

# Inicializa sessão de chat
session = ChatSession()

# Configura o chat com um agente existente
chat = AgentChat(
    agent_id="seu_agent_id",
    realm="seu_realm",
    client_id="seu_client_id",
    client_secret="seu_client_secret"
)

# Lista de arquivos para upload
files = [
    Path("documento1.pdf"),
    Path("documento2.txt")
]

# Faz uma pergunta incluindo contexto dos arquivos
response = chat.ask(
    question="Analise os documentos anexados",
    context=session.get_context(),
    files=files,
    streaming=False
)

print(f"Resposta: {response}")
```

### Exemplo de Criação de Agente

```python
from src.agents.stackspot_agent import StackSpotAgent
from src.models.llm import LLMConfig
from src.models.prompt import PromptConfig

# Configura o modelo LLM
llm_config = LLMConfig(
    provider="openai",
    model="gpt-4",
    temperature=0.7
)

# Configura o prompt
prompt_config = PromptConfig(
    content="Seu prompt aqui"
)

# Cria um novo agente
agent = StackSpotAgent(
    name="Meu Agente",
    description="Descrição do agente",
    llm_config=llm_config,
    prompt_config=prompt_config,
    client_id="seu_client_id",
    client_secret="seu_client_secret",
    realm="seu_realm"
)

# Cria o agente na StackSpot
agent.create()
```

## 📚 Documentação

### Estrutura do Projeto

```
stackspot_agent_api/
├── src/
│   ├── agents/
│   │   ├── base_agent.py     # Classe base para agentes
│   │   ├── chat.py           # Interface simplificada de chat
│   │   └── stackspot_agent.py # Implementação principal
│   ├── config/
│   │   ├── config_dynaconf.py # Configuração via Dynaconf
│   │   └── config_logger.py   # Configuração de logging
│   ├── models/
│   │   ├── chat_session.py   # Modelos de sessão de chat
│   │   ├── llm.py           # Configuração de modelos LLM
│   │   └── prompt.py        # Configuração de prompts
│   └── utils/
│       ├── api_client.py    # Cliente API REST
│       ├── url_utils.py     # Utilitários de URL
│       └── file_uploader.py # Upload de arquivos (Novo!)
├── docs/
│   └── diagrams.md         # Diagramas de arquitetura
├── tests/                  # Testes unitários e de integração
└── examples/              # Exemplos de uso
```

### Classes Principais

#### StackSpotAgent

Classe principal para interação com a API da StackSpot:

- Criação de agentes
- Execução de prompts
- Gerenciamento de agentes existentes
- Autenticação OAuth
- Upload de arquivos (Novo!)

#### AgentChat

Interface simplificada para chat:

- Interação conversacional
- Manutenção de contexto
- Streaming de respostas
- Upload de arquivos para contexto (Novo!)
- Integração com conhecimento StackSpot

#### FileUploader (Novo!)

Gerenciamento de uploads:

- Upload seguro via S3
- Geração de formulários pré-assinados
- Gerenciamento automático de recursos
- Upload em lote de múltiplos arquivos

#### ChatSession

Gerenciamento de sessões de chat:

- Identificação única via UUID
- Histórico de mensagens
- Contexto conversacional
- Metadados de sessão

## ⚙️ Configuração

### Variáveis de Ambiente

```toml
# .secrets.toml
[default]
stackspot.client_id = "seu_client_id"
stackspot.client_secret = "seu_client_secret"
stackspot.realm = "seu_realm"

# settings.toml
[default.stackspot]
agent_id = "seu_agent_id"

[default.stackspot.auth]
base_url = "https://idm.stackspot.com"
api_version = "v1"
oidc_resource = "oidc"
oauth_resource = "oauth"
token_resource = "token"

[default.stackspot.inference]
base_url = "https://genai-inference-app.stackspot.com"
api_version = "v1"
agent_resource = "agent"
chat_endpoint = "chat"

[default.stackspot.upload]
base_url = "https://data-integration-api.stackspot.com"
api_version = "v2"
file_upload_resource = "file-upload"
form_endpoint = "form"
```

### Logging

Os logs são salvos em:
- `logs/stackspot_{time}.log` - Todos os logs
- `logs/stackspot_errors_{time}.log` - Apenas erros

## 📐 Arquitetura

Os diagramas abaixo explicam o funcionamento do sistema:

- [Fluxo de Upload de Arquivos](docs/diagrams.md#fluxo-de-upload-de-arquivos)
- [Arquitetura do Sistema](docs/diagrams.md#arquitetura-do-sistema)
- [Fluxo de Autenticação](docs/diagrams.md#fluxo-de-autenticação)
- [Estrutura de Classes](docs/diagrams.md#estrutura-de-classes)

## 🧪 Testes

```bash
# Executa todos os testes
pytest

# Com cobertura
pytest --cov=src
```

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ✨ Agradecimentos

- Time StackSpot pelo suporte e documentação
- Comunidade Python pelos pacotes utilizados
