#
# transporte stdio: el cliente lanza este programa como proceso hijo
# y le habla por stdin/stdout.
#
# correr: uv run main.py
#
from server import mcp

# OJO: stdout es el canal del protocolo. Un print() lo corromperia;
# para mensajes propios usa sys.stderr.
if __name__ == "__main__":
    mcp.run(transport="stdio")
