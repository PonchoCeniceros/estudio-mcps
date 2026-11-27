//
// transporte Streamable HTTP: el servidor MCP como una ruta de express.
// El mismo servidor de src/server.ts; solo cambia por donde llegan los mensajes.
//
// correr: npm run http
//
import { randomUUID } from "node:crypto";
import type { Request, Response } from "express";
import { createMcpExpressApp } from "@modelcontextprotocol/sdk/server/express.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { isInitializeRequest } from "@modelcontextprotocol/sdk/types.js";

import { createServer } from "../src/server.js";

// una sesion por cliente, cada una con su transporte y su propio servidor
// (lo mismo que hace LocalSessionManager en el ejemplo de Rust)
const sessions = new Map<string, StreamableHTTPServerTransport>();

async function handleMcp(req: Request, res: Response) {
  const sessionId = req.header("mcp-session-id");
  const existing = sessionId ? sessions.get(sessionId) : undefined;
  if (existing) {
    await existing.handleRequest(req, res, req.body);
    return;
  }

  // sin sesion, lo unico valido es el saludo inicial (initialize)
  if (req.method !== "POST" || !isInitializeRequest(req.body)) {
    res.status(400).json({
      jsonrpc: "2.0",
      error: { code: -32000, message: "sesion invalida o ausente" },
      id: null,
    });
    return;
  }

  // sesion nueva: transporte nuevo + servidor nuevo
  const transport: StreamableHTTPServerTransport = new StreamableHTTPServerTransport({
    sessionIdGenerator: () => randomUUID(),
    onsessioninitialized: (id) => {
      sessions.set(id, transport);
    },
  });
  transport.onclose = () => {
    if (transport.sessionId) sessions.delete(transport.sessionId);
  };
  await createServer().connect(transport);
  await transport.handleRequest(req, res, req.body);
}

// express ya configurado por el SDK: escucha en 127.0.0.1, valida el header
// Host (proteccion contra DNS rebinding) y parsea el JSON del body
const app = createMcpExpressApp();

// el MCP es una ruta mas dentro de express: POST para los mensajes,
// GET para el stream de notificaciones, DELETE para cerrar la sesion
app.all("/mcp", handleMcp);

app.listen(8000, "127.0.0.1", () => {
  // aqui console.log si se puede: stdout ya no es el canal del protocolo
  console.log("MCP escuchando en http://127.0.0.1:8000/mcp");
});
