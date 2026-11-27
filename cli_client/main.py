import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
from contextlib import AsyncExitStack

from mcp_client import MCPClient
from core.claude import Claude

from core.cli_chat import CliChat
from core.cli import CliApp

load_dotenv()

# los tres servidores viven junto a cli_client y exponen las mismas tools
# (saludo, suma): son intercambiables, el chat no nota cual esta del otro lado
ROOT = Path(__file__).resolve().parent.parent

# Python: ../mcp_py, con su propio pyproject
PY_DIR = str(ROOT / "mcp_py")
PY_SERVER = str(ROOT / "mcp_py" / "main.py")

# Rust: binario compilado con `cargo build` en ../mcp_rs
RS_SERVER = str(ROOT / "mcp_rs" / "target" / "debug" / "mcp_rs")

# TypeScript: compilado con `npm run build` en ../mcp_ts
TS_SERVER = str(ROOT / "mcp_ts" / "dist" / "index.js")

# como lanzar cada uno: (comando, argumentos)
SERVERS = {
    "py": (
        ("uv", ["run", "--project", PY_DIR, PY_SERVER])
        if os.getenv("USE_UV", "0") == "1"
        else ("python", [PY_SERVER])
    ),
    "rs": (RS_SERVER, []),
    "ts": ("node", [TS_SERVER]),
}

# cual usar: MCP_SERVER=py|rs|ts (uno a la vez, porque las tools se llaman
# igual en los tres y la API de Claude no acepta nombres repetidos)
MCP_SERVER = os.getenv("MCP_SERVER", "py")
assert MCP_SERVER in SERVERS, f"Error: MCP_SERVER debe ser uno de {list(SERVERS)}"

# Anthropic Config
claude_model = os.getenv("CLAUDE_MODEL", "")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")


assert claude_model, "Error: CLAUDE_MODEL cannot be empty. Update .env"
assert anthropic_api_key, (
    "Error: ANTHROPIC_API_KEY cannot be empty. Update .env"
)


async def main():
    claude_service = Claude(model=claude_model)

    server_scripts = sys.argv[1:]
    clients = {}

    command, args = SERVERS[MCP_SERVER]

    async with AsyncExitStack() as stack:
        doc_client = await stack.enter_async_context(
            MCPClient(command=command, args=args)
        )
        clients["doc_client"] = doc_client

        for i, server_script in enumerate(server_scripts):
            client_id = f"client_{i}_{server_script}"
            client = await stack.enter_async_context(
                MCPClient(command="uv", args=["run", server_script])
            )
            clients[client_id] = client

        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            claude_service=claude_service,
        )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
