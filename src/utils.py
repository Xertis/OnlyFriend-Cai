import random
from PIL import Image, ImageDraw
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

async def child_paint(rate: int=5) -> Image:
    width, height = 256, 256
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    colors = [
        (255, 0, 0),    # Красный
        (0, 0, 255),    # Синий
        (0, 128, 0),    # Зеленый
        (128, 0, 128),  # Фиолетовый
        (255, 165, 0),  # Оранжевый
        (255, 192, 203) # Розовый
    ]

    for _ in range(rate):
        x = random.randint(0, width)
        y = random.randint(0, height)
        
        color = random.choice(colors)
        line_width = random.randint(1, 3)
        
        for _ in range(random.randint(50, 200)):
            new_x = x + random.randint(-20, 20)
            new_y = y + random.randint(-20, 20)
            
            new_x = max(0, min(width, new_x))
            new_y = max(0, min(height, new_y))
            
            draw.line([x, y, new_x, new_y], fill=color, width=line_width)
            x, y = new_x, new_y

    return image