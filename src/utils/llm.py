
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

def build_llm(provider: str, model: str, temperature: float, max_tokens: int):
    if provider == "groq":
        return ChatGroq(model=model, temperature=temperature, max_tokens=max_tokens)
    if provider == "openai":
        return ChatOpenAI(model=model, temperature=temperature, max_tokens=max_tokens)
    raise ValueError(f"Unsupported LLM provider: {provider}")
