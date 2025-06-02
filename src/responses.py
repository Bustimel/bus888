def greet_user():
    return (
        "👋 Вітаю! Я диспетчер Bus-Timel.\n"
        "Напишіть, будь ласка, звідки і куди хочете їхати — я підкажу маршрут 🚌"
    )

def unknown_request():
    return (
        "😕 Вибач, не зміг розпізнати напрямок.\n"
        "Напишіть два міста (звідки і куди), і я допоможу!"
    )

def confirm_direction(start: str, end: str):
    return f"🔁 Ви маєте на увазі поїздку з <b>{start.title()}</b> до <b>{end.title()}</b>?"

def ask_for_destination(city: str):
    return f"🗺 У яке місто ви хочете їхати з <b>{city.title()}</b>?"

def ask_for_origin(city: str):
    return f"🗺 З якого міста ви хочете їхати до <b>{city.title()}</b>?"

def no_route_found(start: str, end: str):
    return f"🚫 На жаль, не знайшов маршруту з <b>{start.title()}</b> до <b>{end.title()}</b>."

def one_city_mentioned(city: str, intent: str = "to"):
    if intent == "to":
        return ask_for_origin(city)
    return ask_for_destination(city)

def fallback():
    return "🔎 Якщо ви шукаєте маршрут, будь ласка, напишіть два міста: звідки і куди ви хочете їхати."

async def send_route_info(msg, start, end):
    from src.routes import find_route

    route = find_route(start, end)
    if not route:
        await msg.answer(no_route_found(start, end))
        return

    stops = ', '.join([s['city'] for s in route.get("stops", [])]) if "stops" in route else "—"
    answer = (
        f"📍 <b>{start.title()} → {end.title()}</b>\n"
        f"🕐 Відправлення: <b>{route.get('departure_time', '—')}</b>\n"
        f"⏱ Час у дорозі: <b>{route.get('duration', '—')}</b>\n"
        f"💸 Ціна: <b>{route.get('price', '—')}</b>\n"
        f"🚏 Зупинки: {stops}\n"
        f"🔗 <a href=\"https://bus-timel.com.ua/routes/{start}-{end}.html\">Детальніше</a>"
    )
    await msg.answer(answer)
