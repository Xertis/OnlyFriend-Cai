from googletrans import Translator


__translator__ = Translator()
async def translate(message: str, src: str, dest: str) -> str:
    translated_message = ''

    try:
        translated_message = await __translator__.translate(message, src=src, dest=dest)
        translated_message = translated_message.text
    except Exception as e:
        print(f"Translation error (ru->en): {e}")
        translated_message = message

    return translated_message