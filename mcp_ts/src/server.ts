//
// servidor: la capa MCP. Expone el dominio como tools.
// No sabe por que transporte llegan los mensajes.
//
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

import { saludar, sumar } from "./domain.js";
import { saludoParams, sumaParams } from "./params.js";

//
// cada tool solo traduce: params -> dominio -> respuesta
//
export function createServer(): McpServer {
  const server = new McpServer(
    { name: "mcp_ts", version: "0.1.0" },
    { instructions: "Servidor MCP de prueba: saluda y suma numeros" }
  );

  server.registerTool(
    "saludo",
    { description: "Saluda a una persona por su nombre", inputSchema: saludoParams },
    async ({ nombre }) => ({
      content: [{ type: "text", text: saludar(nombre) }],
    })
  );

  server.registerTool(
    "suma",
    { description: "Suma dos numeros enteros", inputSchema: sumaParams },
    async ({ a, b }) => ({
      content: [{ type: "text", text: String(sumar(a, b)) }],
    })
  );

  return server;
}
