from characterai import aiocai


class CaiSession:
    def __init__(self, char: str, chat_id: str, token: str):
        self.char = char
        self.chat_id = chat_id,
        self.client = aiocai.Client(token)

    async def ask(self, message: str) -> str:
        async with await self.client.connect() as chat:
            message = await chat.send_message(self.char, self.chat_id, message)
            return message.text
