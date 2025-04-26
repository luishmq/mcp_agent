# MCP Chatbot CLI

This project provides a command-line chatbot client (CLI) that integrates OpenAI language models (LLMs) with MCP (Model Context Protocol) servers for specialized tool execution.

## Features

- Initialize and manage multiple MCP servers (e.g., Puppeteer, GitHub, FileSystem).
- Discover and present available tools from each server to the LLM.
- Generate dynamic prompts guiding the LLM to use tools when necessary.
- Process LLM responses, execute tools via MCP, and return results to the user.
- Retry mechanism for tool calls.
- Proper resource cleanup when ending the session.

## Technologies & Dependencies

- Python 3.12+
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [MCP (Model Context Protocol)](https://pypi.org/project/mcp/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [ruff](https://github.com/charliermarsh/ruff) (linting)

Dependencies are defined in `pyproject.toml`. To install:

```bash
python --version  # should be >= 3.12
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install .
```

## Configuration

1. Create a `.env` file at the project root with your OpenAI API key:

   ```bash
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   ```

2. Define the MCP server(s) in `servers_config.json`. Example:

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

> ⚠️ Do not commit tokens or sensitive credentials to the repository. Consider adding `servers_config.json` to `.gitignore` and maintaining a sample file (`servers_config.example.json`).

## Usage

```bash
python main.py
```

The chatbot will start an interactive session:

```
You: What is the status of my repository checkout?
Assistant: ...
```

- Type your question or command.
- To exit, type `exit` or `quit`.

## Project Structure

```
.
├── app/
│   ├── chat/           # Orchestrates the chat session and flow logic
│   ├── config/         # Loads configuration and environment variables
│   ├── llm/            # Client for LLM (OpenAI) communication
│   ├── server/         # Manages MCP server connections and tool execution
│   └── tools/          # Tool representation and formatting
├── main.py             # Application entrypoint
├── servers_config.json # MCP servers configuration
├── pyproject.toml      # Project metadata and dependencies
├── .gitignore          # Files and folders ignored by Git
└── README.md           # Project documentation
```

## Contributing

Contributions are welcome! Open issues or pull requests for improvements, bug fixes, or new features.