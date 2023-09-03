from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

start_btn = KeyboardButton('⭐️Актуальне посилання⭐️')
start_kb = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb.add(start_btn)

send_all_btn = KeyboardButton('📩Зробити розсилку📩')
get_all_users_btn = KeyboardButton('🫂Кількисть користувачів🫂')
set_msg_btn = KeyboardButton('📨Замінити вітальне повідомлення📨')
panel_kb = ReplyKeyboardMarkup(resize_keyboard=True)
panel_kb.add(send_all_btn).row(get_all_users_btn, set_msg_btn)

back_btn = KeyboardButton('◀️Меню◀️')
back_kb = ReplyKeyboardMarkup(resize_keyboard=True)
back_kb.add(back_btn)
