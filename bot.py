import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from bot_config import TOKEN, owner
import db_config
import keyboards

# Налаштування боту
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# States - заміна вітального повідомлення
class SetMsg(StatesGroup):
	msg_text = State()

# відправка розсилки
class SendAll(StatesGroup):
	msg_text = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    db_config.get_user(message.from_user.id)
    msg = db_config.get_message()
    await message.answer(msg, reply_markup=keyboards.start_kb)

@dp.message_handler(Text(equals=['⭐️Актуальне посилання⭐️']))
async def actual_link(message: types.message):
	await start(message)

# Вхід до админ-панелі
@dp.message_handler(commands=['panel'])
async def panel(message: types.Message):
	if message.from_user.id == owner:
		await message.answer('Ласкаво просимо в панель адміністратора🪄', reply_markup=keyboards.panel_kb)

# Заміна вітального повідомлення
@dp.message_handler(Text(equals=['📨Замінити вітальне повідомлення📨']))
async def add_code(message: types.message):
	if message.from_user.id == owner:
		await message.answer('Надішліть новий текст повідомлення💬', reply_markup=keyboards.back_kb)
		await SetMsg.msg_text.set()

@dp.message_handler(Text(equals=['◀️Меню◀️']))
async def back_n_stop(message: types.message):
	await dp.storage.close()
	await dp.storage.wait_closed()
	await message.answer('Ви скасували дію🪄', reply_markup=keyboards.panel_kb)

# Заміна вітального повідомлення
@dp.message_handler(state=SetMsg.msg_text)
async def send_text(message: types.Message, state: FSMContext):
    if(message.text == '◀️Меню◀️'):
        await back_n_stop(message)
        return
    db_config.set_message(message.text)
    await state.finish()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await message.answer('Ви замінили повідовлення🪄', reply_markup=keyboards.panel_kb)

@dp.message_handler(Text(equals=['🫂Кількисть користувачів🫂']))
async def users_stat(message: types.message):
    if message.from_user.id == owner:
        msg, users = db_config.get_users()
        await message.answer(msg)


@dp.message_handler(Text(equals=['📩Зробити розсилку📩']))
async def send_all(message: types.message):
    if message.from_user.id == owner:
        await message.answer('Надішліть текст повідомлення💬', reply_markup=keyboards.back_kb)
        await SendAll.msg_text.set()

@dp.message_handler(state=SendAll.msg_text)
async def send_all_message(message: types.Message, state: FSMContext):
    if(message.text == '◀️Меню◀️'):
        await back_n_stop(message)
        return
    
    msg, users = db_config.get_users()

    #активні/неактивні юзери
    a_users = 0
    n_users = 0

    for u in users:
        try:
            await bot.send_message(u, message.text)
            a_users += 1
        except:
            n_users += 1

    await state.finish()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await message.answer(f'Розсилка відправлена🪄\n\nВсього відправлено: {a_users + n_users}\nАктивних: {a_users}\nНеактивних: {n_users}', reply_markup=keyboards.panel_kb)


# ---------------------------
if __name__ == '__main__':
	db_config.database_setup()
	executor.start_polling(dp)