from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI


class CuentoState(TypedDict):
    tema: str
    cuento: str


def generar_cuento(state: CuentoState) -> dict:
    client = OpenAI()  # se crea aquí, no al importar el archivo
    response = client.responses.create(
        model="gpt-5.6-luna",
        input=f"Escribe una pequeña oración, en español, sobre {state['tema']}.",
    )
    return {"cuento": response.output_text}


builder = StateGraph(CuentoState)
builder.add_node("generar_cuento", generar_cuento)
builder.add_edge(START, "generar_cuento")
builder.add_edge("generar_cuento", END)

cuento_agent = builder.compile()