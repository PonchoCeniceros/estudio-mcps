#
# dominio: la logica del negocio, en Python puro.
# No sabe nada de MCP, JSON ni stdio: se puede probar
# y reutilizar sin ninguna de esas capas.
#


def saludar(nombre: str) -> str:
    return f"hola, {nombre}"


def sumar(a: int, b: int) -> int:
    return a + b
