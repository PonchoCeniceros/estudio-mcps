#
# servidor: la capa MCP. Expone el dominio como tools.
# No sabe por que transporte llegan los mensajes.
#
from mcp.server.fastmcp import FastMCP

import domain
from params import Nombre, NumeroA, NumeroB

mcp = FastMCP(
    "mcp_py",
    instructions="Servidor MCP de prueba: saluda y suma numeros",
    log_level="ERROR",
)


# Recorrido de una llamada, del cable a la función y de vuelta:
#
# 1. Llega un CallToolRequest (tools/call) por el transporte:
#       {"method": "tools/call",
#        "params": {"name": "suma", "arguments": {"a": 2, "b": 3}}}
#
# 2. FastMCP busca "suma" en su registro. Ese es el name= del decorador,
#    no el nombre de la función en Python (tool_suma, que es privado mío).
#
# 3. Pydantic valida los argumentos contra el schema que generó a partir de
#    los type hints. Si "a" no es int, se rechaza aquí y la función NO corre.
#
# 4. Se invoca tool_suma(a=2, b=3). Aquí sí corre mi código.
#
# 5. El return ("5") se serializa como bloque de contenido:
#       {"result": {"content": [{"type": "text", "text": "5"}]}}
#    Por el cable siempre viaja contenido, no tipos.
#
# 6. Se manda el CallToolResult de vuelta al cliente, con el mismo id del
#    request. El cliente se lo entrega a la app, y la app lo mete al historial
#    como tool_result antes de volver a llamar al modelo.
#
# Nota: el description= del decorador y los de cada Field viajan en el
# tools/list y terminan en el contexto del modelo. No son documentación:
# son lo único que Claude tiene para decidir si usar la tool y con qué args.
#
# cada tool solo traduce: params -> dominio -> respuesta
#
@mcp.tool(name="saludo", description="Saluda a una persona por su nombre")
def tool_saludo(nombre: Nombre) -> str:
    return domain.saludar(nombre)


@mcp.tool(name="suma", description="Suma dos numeros enteros")
def tool_suma(a: NumeroA, b: NumeroB) -> str:
    return str(domain.sumar(a, b))
