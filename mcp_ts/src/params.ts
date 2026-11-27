//
// params: el contrato de entrada de cada tool.
// zod valida el JSON que manda el modelo y el SDK genera con el
// el esquema que el modelo lee en tools/list.
// (en Rust esto son los structs con Deserialize + JsonSchema)
//
import { z } from "zod";

export const saludoParams = {
  nombre: z.string().describe("nombre de la persona a saludar"),
};

export const sumaParams = {
  a: z.number().int().describe("primer numero"),
  b: z.number().int().describe("segundo numero"),
};
