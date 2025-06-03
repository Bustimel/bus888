import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext

from src.routes import extract_cities_from_text
from src.responses import greet_user, unknown_request, confirm_direction
from src.kb import yes_no_kb
from src.states import BookingForm

API_TOKEN = "8011978121:AAEKgT0bCuM5bkb4pm8ddUaWQMKEJGyjFYs"

ADMIN_ID = 6132154171

# === Логування ===
logging.basicConfig(level=logging.INFO)

# === Ініціалізація бота і диспетчера ===
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())


@dp.message(commands=["start", "help"])
async def cmd_start(msg: Message):
    await msg.answer(greet_user())


@dp.message()
async def handle_message(msg: Message, state: FSMContext):
    text = msg.text.strip()
    user_id = msg.from_user.id
    current_state = await state.get_state()

    if current_state == BookingForm.waiting_for_name.state:
        await state.update_data(name=text)
        await msg.answer("📞 Введіть ваш номер телефону:")
        await state.set_state(BookingForm.waiting_for_phone)
        return

    if current_state == BookingForm.waiting_for_phone.state:
        await state.update_data(phone=text)
        await msg.answer("📅 Введіть дату поїздки (день місяць рік):")
        await state.set_state(BookingForm.waiting_for_date)
        return

    if current_state == BookingForm.waiting_for_date.state:
        await state.update_data(date=text)
        data = await state.get_data()

        name = data.get("name")
        phone = data.get("phone")
        date = data.get("date")
        start = data.get("start")
        end = data.get("end")

        application = (
            f"🚍 <b>Нова заявка:</b>\n"
            f"👤 Ім’я: <b>{name}</b>\n"
            f"📞 Телефон: <b>{phone}</b>\n"
            f"🗓 Дата: <b>{date}</b>\n"
            f"🧭 Маршрут: <b>{start} → {end}</b>"
        )

        await bot.send_message(ADMIN_ID, application)
        await msg.answer("✅ Дякуємо! Заявку прийнято. Наш диспетчер зв’яжеться з вами найближчим часом.")
        await state.clear()
        return

    cities = extract_cities_from_text(text.lower())

    if len(cities) == 2:
        start, end = cities
        await state.update_data(start=start, end=end)
        await msg.answer(confirm_direction(start, end), reply_markup=yes_no_kb(start, end))

    elif len(cities) == 1:
        if any(word in text.lower() for word in ["в", "до"]):
            await msg.answer(f"З якого міста ви хочете їхати до <b>{cities[0]}</b>?")
        elif any(word in text.lower() for word in ["з", "із"]):
            await msg.answer(f"У яке місто ви хочете їхати з <b>{cities[0]}</b>?")
        else:
            await msg.answer("Будь ласка, вкажіть два міста — звідки і куди 🧭")
    else:
        await msg.answer(unknown_request())


@dp.callback_query(lambda c: c.data.startswith("confirm:"))
async def process_confirm(call: CallbackQuery, state: FSMContext):
    _, start, end = call.data.split(":")
    await state.update_data(start=start, end=end)
    await call.message.answer("🧾 Введіть ваше ім’я:")
    await state.set_state(BookingForm.waiting_for_name)
    await call.answer()


@dp.callback_query(lambda c: c.data.startswith("reverse:"))
async def process_reverse(call: CallbackQuery, state: FSMContext):
    _, start, end = call.data.split(":")
    await state.update_data(start=end, end=start)
    await call.message.answer("🧾 Введіть ваше ім’я:")
    await state.set_state(BookingForm.waiting_for_name)
    await call.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
