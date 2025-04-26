# MCP Chatbot CLI

Este projeto fornece um cliente de linha de comando (CLI) de chatbot que integra modelos de linguagem (LLMs) da OpenAI com servidores MCP (Model Context Protocol) para execução de ferramentas especializadas.

## Funcionalidades

- Inicializa e gerencia múltiplos servidores MCP (ex.: Puppeteer, GitHub, FileSystem).
- Descobre e apresenta as ferramentas disponíveis de cada servidor ao LLM.
- Gera prompts dinâmicos para o LLM, orientando-o a usar ferramentas quando necessário.
- Processa respostas do LLM, executa ferramentas via MCP e retorna resultados ao usuário.
- Mecanismo de retry para chamadas de ferramenta.
- Limpeza adequada de recursos ao encerrar a sessão.

## Tecnologias e Dependências

- Python 3.12+
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [MCP (Model Context Protocol)](https://pypi.org/project/mcp/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [ruff](https://github.com/charliermarsh/ruff) (linting)

As dependências estão definidas no `pyproject.toml`. Para instalar:

```bash
python --version  # deve ser >= 3.12
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install .
```

## Configuração

1. Crie um arquivo `.env` na raiz do projeto com sua chave da OpenAI:

   ```bash
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

2. Defina o(s) servidor(es) MCP em `servers_config.json`. Exemplo:

   ```json
   {
     "mcpServers": {
       "puppeteer": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
       },
       "github": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-github"],
         "env": {
           "GITHUB_PERSONAL_ACCESS_TOKEN": "your_github_token_here"
         }
       },
       "filesystem": {
         "command": "npx",
         "args": [
           "-y", "@modelcontextprotocol/server-filesystem", "<source_dir>", "<target_dir>"
         ]
       }
     }
   }
   ```

> **⚠️ Atenção**: Nunca comite tokens ou credenciais sensíveis no repositório. Considere adicionar `servers_config.json` ao `.gitignore` e manter um modelo de configuração (`servers_config.example.json`).

## Como usar

```bash
python main.py
```

O chatbot iniciará uma sessão interativa:

```
You: Qual é o status da minha cópia do repositório?
Assistant: ...
```

- Digite sua pergunta ou comando.
- Para sair, digite `exit` ou `quit`.

## Estrutura do Projeto

```
.
├── app/
│   ├── chat/           # Orquestra a sessão de chat e lógica de fluxo
│   ├── config/         # Carrega configurações e variáveis de ambiente
│   ├── llm/            # Cliente para comunicação com o LLM (OpenAI)
│   ├── server/         # Gerencia conexões e execução de ferramentas MCP
│   └── tools/          # Representação e formatação de ferramentas
├── main.py             # Ponto de entrada da aplicação
├── servers_config.json # Configuração dos servidores MCP
├── pyproject.toml      # Metadados e dependências do projeto
├── .gitignore          # Arquivos e pastas ignorados pelo Git
└── README.md           # Documentação do projeto
```

## Contribuição

Contribuições são bem-vindas. Abra issues ou pull requests para melhorias, correções ou novas funcionalidades.