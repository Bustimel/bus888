from aiogram.fsm.state import StatesGroup, State

class BookingForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_date = State()
    confirming = State()