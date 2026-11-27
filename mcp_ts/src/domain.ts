//
// dominio: la logica del negocio, en TypeScript puro.
// No sabe nada de MCP, JSON ni stdio: se puede probar
// y reutilizar sin ninguna de esas capas.
//

export function saludar(nombre: string): string {
  return `hola, ${nombre}`;
}

export function sumar(a: number, b: number): number {
  return a + b;
}
