from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END


class MazeState(TypedDict):
    laberinto: list[str]
    cola: list[str]                      # posiciones como "x,y"
    visitados: list[str]
    padre: dict[str, Optional[str]]      # llaves y valores como "x,y"
    meta: str
    encontrado: bool
    ruta: list[str]


def pos_a_str(x: int, y: int) -> str:
    return f"{x},{y}"


def str_a_pos(s: str) -> tuple[int, int]:
    x, y = s.split(",")
    return int(x), int(y)


def encontrar_celda(grid, caracter):
    for y, fila in enumerate(grid):
        for x, c in enumerate(fila):
            if c == caracter:
                return pos_a_str(x, y)
    return None


def vecinos(grid, pos_str):
    x, y = str_a_pos(pos_str)
    candidatos = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    resultado = []
    for cx, cy in candidatos:
        if 0 <= cy < len(grid) and 0 <= cx < len(grid[cy]) and grid[cy][cx] != "#":
            resultado.append(pos_a_str(cx, cy))
    return resultado


def explorar(state: MazeState) -> dict:
    cola = state["cola"].copy()
    visitados = state["visitados"].copy()
    padre = state["padre"].copy()

    actual = cola.pop(0)

    if actual == state["meta"]:
        return {"encontrado": True}

    for vecino in vecinos(state["laberinto"], actual):
        if vecino not in visitados:
            visitados.append(vecino)
            padre[vecino] = actual
            cola.append(vecino)

    return {"cola": cola, "visitados": visitados, "padre": padre}


def decidir_siguiente(state: MazeState) -> str:
    if state.get("encontrado"):
        return "reconstruir"
    if not state["cola"]:
        return "reconstruir"
    return "explorar"


def reconstruir(state: MazeState) -> dict:
    ruta = []
    actual = state["meta"]
    padre = state["padre"]
    while actual is not None:
        ruta.append(actual)
        actual = padre.get(actual)
    ruta.reverse()
    return {"ruta": ruta}


builder = StateGraph(MazeState)

builder.add_node("explorar", explorar)
builder.add_node("reconstruir", reconstruir)

builder.add_edge(START, "explorar")
builder.add_conditional_edges(
    "explorar",
    decidir_siguiente,
    {"explorar": "explorar", "reconstruir": "reconstruir"},
)
builder.add_edge("reconstruir", END)

maze_agent = builder.compile()