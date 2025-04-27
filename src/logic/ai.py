import requests


class AiSession:
    def __init__(self, model: str):
        self.model = model
        self.context = ''

    async def ask(self, message: str) -> str:
        self.context += f"[human] {message}\n"

        url = "http://localhost:11434/api/generate"

        data = {
            "model": self.model,
            "prompt": self.context,
            "stream": False
        }

        response = requests.post(url, json=data)
        out = response.json()["response"]
        self.context += f"[you] {out}\n"

        return out
