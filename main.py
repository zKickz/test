import logging
import random
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from aiogram.utils import executor
from aiogram import Bot, types, Dispatcher
from app.sq_statement import get_users, set_user, get_username, get_users2
from app.answers import kb_start, help_mssg, info_mssg, error_mssg, ivite_mssg, links
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = '5472254968:AAG3DSHV91GI1DwO2VsBXL7tgSBSMSrdMVM'

DB_FILE = 'db_users.db'

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    user_id = message.from_user.id
    result = get_users(DB_FILE)
    for i in result:
        if user_id == i[0]:
            break
    else:
        first_name = message.from_user.first_name
        username = message.from_user.username
        logging.info(f"New user: {first_name}")
        set_user(DB_FILE, user_id, first_name, username)
    await message.reply(
        f"Привет, <b>{message.from_user.first_name}, \n"
        f"твой ид: {message.from_user.id}</b>",
        reply_markup=kb_start)


class StateInv(StatesGroup):
    choosing_state = State()


@dp.message_handler(Command(commands=["invite"]))
async def invite_command(message: Message, state: FSMContext):
    await message.answer(
        text=ivite_mssg
    )
    # Устанавливаем пользователю состояние "ввод ИД"
    await state.set_state(StateInv.choosing_state)


@dp.message_handler(state=StateInv.choosing_state)
async def id_command(message: Message, state: FSMContext):
    data = state.get_state()
    print(data)
    result = get_users(DB_FILE)
    proove = 0
    resultat = get_username(DB_FILE, int(message.text))
    for i in result:
        if int(message.text) == i[0]:
            proove = +1
    if proove == 1:
        await bot.send_message(chat_id=int(message.text), text='Приглашаем поиграть с нами, для игры введи /game')
        await message.reply(f"Вы успешно пригласили игрока: {resultat}")
    else:
        await message.answer(
            text="такого id не знаю, пригласи его в ко мне (https://t.me/Kick59Rus_bot) и начни с начала",
            )
    await state.finish()


@dp.message_handler(Command(commands=["cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено"
    )


@dp.message_handler(commands="help")
async def help_command(message: types.Message):
    await message.reply(help_mssg)


@dp.message_handler(commands="info")
async def info_command(message: types.Message):
    await message.answer(info_mssg)


@dp.message_handler(commands="links")
async def links_command(message: types.Message):
    await message.reply(links)


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def other_command(message: types.Message):
    await message.reply(error_mssg)


@dp.message_handler(commands="game")
async def game_start(message: types.Message):
    await bot.send_game(chat_id=message.chat.id, game_short_name='Kick_Game')


@dp.callback_query_handler(lambda call: call.game_short_name == 'kick_game')
async def game(call):
    await bot.answer_callback_query(callback_query_id=call.id, url='https://6f5e-77-236-87-98.eu.ngrok.io/')


@dp.message_handler(commands="random")
async def random_command(message: types.Message):
    result = get_users2(DB_FILE)
    await message.answer(f'Выбор случайного игрока - "{random.choice(result)}"')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s](%(levelname)s): \"%(filename)s\", line:%(lineno)d, %(funcName)s - %(message)s",
        filename='botLogs.log')
    print('Бот онлайн')
    executor.start_polling(dp, skip_updates=True)
