import requests
from src.utils import translate


class AiSession:
    def __init__(self, model: str, context: str=''):
        self.__model = model
        self.context = context

    async def ask(self, message: str) -> str:
        message = await translate(message, src="ru", dest="en")
        self.context += f"[human] {message}\n"

        url = "http://localhost:11434/api/generate"

        data = {
            "model": self.__model,
            "prompt": self.context,
            "stream": False
        }

        response = requests.post(url, json=data)
        out = response.json()["response"]
        self.context += f"{out}\n"

        return await translate(out, src="en", dest="ru")
