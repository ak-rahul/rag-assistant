
from langchain_community.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings

def build_embeddings(provider: str, model: str, device: str = "auto"):
    if provider == "sentence-transformers":
        return HuggingFaceEmbeddings(model_name=model, model_kwargs={"device": device})
    if provider == "openai":
        return OpenAIEmbeddings(model=model)
    raise ValueError(f"Unsupported embeddings provider: {provider}")
