import os
import requests

class GroqClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not provided")

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 512) -> str:
        url = "https://api.groq.ai/v1/generate"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("text", "")
