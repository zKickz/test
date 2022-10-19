from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

help_mssg = "Для того что бы пригласить друга введи команду /invite после введи id аккаунта, кому хочешь отправить приглашение"
info_mssg = """
Создатели бота\n
Василевский Александр\n
Губченко Максим\n
Лопатин Иван\n
Павлов Валерий\n
Спасибо за использование бота.
"""
error_mssg = "Я не знаю как обработать этот запрос"
ivite_mssg = "Введите id пользователя с которым хотите поиграть"
links = """
Ссылки бота:
/start
/help
/invite
/info
/random
/game
"""
button_help = KeyboardButton('/help')
button_info = KeyboardButton('/info')
button_invite = KeyboardButton('/invite')

kb_start = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(button_help, button_invite, button_info)
