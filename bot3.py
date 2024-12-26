from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


kb = ReplyKeyboardMarkup()
button = KeyboardButton(text= 'Рассчитать')
button2 = KeyboardButton(text= 'Информация')
kb.add(button)
kb.add(button2)

class UserState(StatesGroup):
    pol = State()
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью. Если хочешь узнать какая для тебя существует норма калорий то нажми на 'Рассчитать'", reply_markup= kb )

@dp.message_handler(text=['Рассчитать'])
async def set_age(message):
    await message.answer("Введите свой пол (мужчина/женщина)")
    await UserState.pol.set()

@dp.message_handler(state=UserState.pol)
async def set_growth(message, state):
    await state.update_data(pol=message.text)
    await message.answer("Введите свой возраст")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    if data['pol'] == 'женщина':
        col = (655.1 + (9.563 * float(data['weight'])) + (1.85 * float(data['growth'])) + (4.676 * float(data['age'])))
        await message.answer(f"Ваша норма калорий {col}")
    else:
        col = (66.5 + (13.75 * float(data['weight'])) + (5.003 * float(data['growth'])) + (6.775 * float(data['age'])))

        await message.answer(f"Ваша норма калорий {col}")
    await state.finish()
@dp.message_handler()
async def start(message):
    await message.answer("Привет! Нажми на команду /start, чтобы бот заработал", reply_markup= kb)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)