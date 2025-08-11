import asyncio
import webbrowser
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import (
    KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
)

API_TOKEN = "8410930612:AAFGx_FrZYy-HEtZ-IqDbh_kJ65pZxs5Ass"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Хранилище "перекурщиков"
smokers = []


def show_smokers_on_map(smokers_list):
    """Создаёт HTML-карту с перекурщиками и открывает её."""
    if not smokers_list:
        return None

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>Карта перекуров</title>
        <script src="https://api-maps.yandex.ru/2.1/?lang=ru_RU" type="text/javascript"></script>
        <script type="text/javascript">
            ymaps.ready(init);
            function init() {{
                var map = new ymaps.Map("map", {{
                    center: [{smokers_list[0]['lat']}, {smokers_list[0]['lon']}],
                    zoom: 15
                }});
                {"".join([f"map.geoObjects.add(new ymaps.Placemark([{s['lat']}, {s['lon']}], {{balloonContent: '{s['name']} на перекуре'}}));" for s in smokers_list])}
            }}
        </script>
        <style>
            html, body, #map {{ width: 100%; height: 100%; margin: 0; padding: 0; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
    </body>
    </html>
    """

    filename = "smokers_map.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html_content)

    webbrowser.open(filename)
    return filename


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    # Кнопка для отправки геолокации
    button_geo = KeyboardButton(text="🚬 Выйти на перекур", request_location=True)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[button_geo]],
        resize_keyboard=True
    )
    await message.answer(
        "Нажми кнопку, чтобы выйти на перекур 🚬",
        reply_markup=keyboard
    )


@dp.message(Command("map"))
async def map_handler(message: types.Message):
    if not smokers:
        await message.answer("Пока никто не на перекуре 😢")
    else:
        file = show_smokers_on_map(smokers)
        if file:
            await message.answer("Карта перекурщиков создана! Открой файл smokers_map.html у себя.")


@dp.message()
async def location_handler(message: types.Message):
    if message.location:
        lat = message.location.latitude
        lon = message.location.longitude
        smokers.append({"name": message.from_user.first_name, "lat": lat, "lon": lon})
        await message.answer(
            f"Ты отмечен на перекуре! 🚬\nВсего сейчас на перекуре: {len(smokers)}",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer("Если хочешь выйти на перекур, нажми кнопку с геолокацией!")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
