#!/usr/bin/env node
//
// transporte stdio: el cliente lanza este programa como proceso hijo
// y le habla por stdin/stdout.
//
// correr: npm run build && npm start
//
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

import { createServer } from "./server.js";

// OJO: stdout es el canal del protocolo. Un console.log lo corromperia;
// para mensajes propios usa console.error (stderr).
console.error("MCP stdio listo, esperando mensajes por stdin");

const server = createServer();
await server.connect(new StdioServerTransport());
