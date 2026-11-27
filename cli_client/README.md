# MCP Chat

MCP Chat is a command-line interface application that enables interactive chat capabilities with AI models through the Anthropic API. The application supports document retrieval, command-based prompts, and extensible tool integrations via the MCP (Model Control Protocol) architecture.

## Prerequisites

- Python 3.9+
- Anthropic API Key

## Setup

### Step 1: Configure the environment variables

1. Create or edit the `.env` file in the project root and verify that the following variables are set correctly:

```
ANTHROPIC_API_KEY=""  # Enter your Anthropic API secret key
```

### Step 2: Install dependencies

#### Option 1: Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. Install uv, if not already installed:

```bash
pip install uv
```

2. Create and activate a virtual environment:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Run the project

```bash
uv run main.py
```

#### Option 2: Setup without uv

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install anthropic python-dotenv prompt-toolkit "mcp[cli]==1.8.0"
```

3. Run the project

```bash
python main.py
```

## Usage

### Basic Interaction

Simply type your message and press Enter to chat with the model.

### Choosing the MCP server

The chat connects to one MCP server at a time. All three expose the same tools
(`saludo`, `suma`), so they are interchangeable:

```bash
MCP_SERVER=py uv run main.py   # ../mcp_py (default)
MCP_SERVER=rs uv run main.py   # ../mcp_rs, build first: cargo build
MCP_SERVER=ts uv run main.py   # ../mcp_ts, build first: npm install && npm run build
```

Only one at a time: the tool names are the same in all three, and the Claude
API rejects duplicate tool names.

## Development

### Implementing MCP Features

The document features (`@doc` mentions and `/` commands) depend on resources
and prompts that the servers don't expose yet. To add them:

1. Add resources and prompts to the servers
2. Implement `read_resource`, `list_prompts` and `get_prompt` in `mcp_client.py`

### Linting and Typing Check

There are no lint or type checks implemented.
