#
# params: el contrato de entrada de cada tool.
# Annotated + Field -> pydantic valida el JSON que manda el modelo
# y genera el esquema que el modelo lee en tools/list.
# (en Rust esto son los structs con Deserialize + JsonSchema)
#
from typing import Annotated

from pydantic import Field

Nombre = Annotated[str, Field(description="nombre de la persona a saludar")]
NumeroA = Annotated[int, Field(description="primer numero")]
NumeroB = Annotated[int, Field(description="segundo numero")]
