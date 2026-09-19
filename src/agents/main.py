import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

load_dotenv()  # carga las variables de tu archivo .env

def get_weather(city: str) -> str:
    """Obtiene el clima de una ciudad."""
    return f"¡Siempre hace sol en {city}!"

model = ChatOpenAI(model="gpt-5.6-luna", reasoning_effort="none")

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="Eres un asistente útil.",
)