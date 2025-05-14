import requests
from src.utils import translate


class AiSession:
    def __init__(self, model: str, context: str='', translation: bool=True):
        self.__model = model
        self.__translation = translation
        self.context = context

    async def ask(self, message: str, save: bool = True) -> str:
        message = await translate(message, src="ru", dest="en") if self.__translation else message
        
        prompt = message
        if save:
            self.context += f"[human] {message} [/human]\n"
            prompt = self.context
        
        url = "http://localhost:11434/api/generate"
        data = {
            "model": self.__model,
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(url, json=data)
        out = response.json()["response"]
        
        if save:
            self.context += f"{out}\n"
        
        return await translate(out, src="en", dest="ru") if self.__translation else out
