import os
import config
from dotenv import load_dotenv

import neuronet
import markups as nav
import actions
import constants
import paths
import user_settings as settings
from utils import set_default_commands

import markovify
import logging
from gtts import gTTS

import asyncio
from aiogram import Bot, types, Dispatcher, executor



"""ENV"""

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

bot_token = ''

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    bot_token = os.getenv("API_TOKEN")

if bot_token == '': bot_token = config.API_TOKEN


"""Log level"""

logging.basicConfig(format = "%(asctime)s - %(levelname)s - %(message)s", level = logging.INFO)
logger = logging.getLogger(__name__)


"""Bot init"""

bot = Bot(token = bot_token)
dp = Dispatcher(bot)


"""Startup function"""

async def on_startup(dp):
    await set_default_commands(dp)


"""Voice answer generation"""

def generate(text, out_file):

    tts = gTTS(text, lang = "ru")
    tts.save(out_file)


"""Get text model"""

def get_model(filename):

    with open(filename, encoding = "utf-8") as f: text = f.read()
    return markovify.Text(text)


"""Get compliment"""

async def get_compliment():

    generator = get_model(paths.PATH_FEMALE_TEXT_MODEL_ANSWER)
    statement = True

    while statement:

        text = generator.make_sentence()
        if text is not None: statement = False
        
    return text


"""Start function"""

@dp.message_handler(commands = ["start", "hi", "hello"])
async def start(message: types.Message, commands = "start"):

    await bot.send_chat_action(message.from_user.id, types.chat.ChatActions.TYPING)
    await asyncio.sleep(1)
    await message.answer(f"{actions.ANSWER_HI} {message.from_user.full_name}!", 
                        reply_markup = nav.greet_markup)


"""Error function"""

@dp.errors_handler()
async def error(self):
    await logger.warning('update "%s" casused error "%s"', self.exception_name, self.exception_message)


"""On photo"""

@dp.message_handler(content_types = ["photo"])
async def photo(message: types.Message):

    filename = "settings_" + str(message.from_user.id) + ".txt"
    settings_path = paths.PATH_USER_DATA + filename

    is_text = await settings.get_user_settings_text(settings_path)

    tmp_pic_file = paths.PATH_USER_DATA + str(message.from_user.id) + ".jpg"
    await message.photo[-1].download(destination_file=tmp_pic_file)

    result = neuronet.resolve(tmp_pic_file)
    os.remove(tmp_pic_file)

    if is_text == False:
        tmp_audio_file = paths.PATH_USER_DATA + str(message.from_user.id) + ".mp3"
    
    if len(result[0]) == 0:

        text = actions.ANSWER_UNDEFINED

        if is_text == False:
            generate(text, tmp_audio_file)

        await bot.send_chat_action(message.chat.id, types.chat.ChatActions.TYPING)
        await asyncio.sleep(1)

        if is_text == False:
            await message.answer_audio(audio = open(tmp_audio_file, "rb"))
            os.remove(tmp_audio_file)
            return
        else: 
            await message.answer(text)
            return

    text = result[1][0] + ", на мой скромный взгляд."
    
    if result[0][0] == constants.IS_FEMALE: text = f'{actions.ANSWER_FEMALE} {text}'
    elif result[0][0] == constants.IS_MALE: text = f'{actions.ANSWER_MALE} {text}'
    
    print(text)

    await bot.send_chat_action(message.from_user.id, types.chat.ChatActions.TYPING)
    await asyncio.sleep(1)

    if is_text == False:
        generate(text, tmp_audio_file)
        await message.answer_audio(audio = open(tmp_audio_file, "rb"))
        os.remove(tmp_audio_file)
    else: await message.answer(text)

    text = ""
    
    if result[0][0] == constants.IS_FEMALE: text = await get_compliment()
    elif result[0][0] == constants.IS_MALE: text = actions.ANSWER_MALE_WITHOUT_MODEL

    print(text)

    await bot.send_chat_action(message.from_user.id, types.chat.ChatActions.TYPING)
    await asyncio.sleep(1)

    if is_text == False:
        generate(text, tmp_audio_file)
        await message.answer_audio(audio = open(tmp_audio_file, "rb"))
        os.remove(tmp_audio_file)
    else:
        await message.answer(text)


@dp.message_handler()
async def answers(message: types.Message):

    filename = "settings_" + str(message.from_user.id) + ".txt"
    settings_path = paths.PATH_USER_DATA + filename

    if message.text == actions.QUERY_GREETING:
        await message.answer(actions.ANSWER_GREETING, reply_markup = nav.main_markup)

    elif message.text == actions.QUERY_SETTINGS:
        await message.answer(actions.ANSWER_SETTINGS, reply_markup = nav.settings_markup)

    elif message.text == actions.QUERY_TEXT_ANSWER:

        is_text = True
        await settings.set_user_settings_text(settings_path, is_text)

        await message.answer(actions.ANSWER_TEXT_ANSWER)

    elif message.text == actions.QUERY_VOICE_ANSWER:

        is_text = False
        await settings.set_user_settings_text(settings_path, is_text)

        await message.answer(actions.ANSWER_VOICE_ANSWER)

    elif message.text == actions.QUERY_MAIN_MENU:
        await message.answer(actions.ANSWER_MAIN_MENU, reply_markup = nav.main_markup)

    elif message.text == actions.QUERY_GET_COMPLIMENT:

        is_text = await settings.get_user_settings_text(settings_path)

        if is_text:

            text = await get_compliment()
            
            print(text)
            
            await bot.send_chat_action(message.from_user.id, types.chat.ChatActions.TYPING)
            await asyncio.sleep(1)
            await message.answer(text)

        else:

            tmp_audio_file = paths.PATH_USER_DATA + str(message.from_user.id) + ".mp3"

            text = await get_compliment()

            print(text)

            await bot.send_chat_action(message.from_user.id, types.chat.ChatActions.TYPING)
            await asyncio.sleep(1)
            generate(text, tmp_audio_file)
            await message.answer_audio(audio = open(tmp_audio_file, "rb"))
            os.remove(tmp_audio_file)
    
    elif message.text == actions.QUERY_START_AUTO_COMPLIMENTS:
        
        is_run = True
        await settings.set_user_settings_text(settings_path, is_run)

        await asyncio.sleep(1)
        await message.answer(actions.ANSWER_START_AUTO_COMPLIMENTS, 
                                reply_markup = nav.auto_compliments_markup)

        while is_run == True: 
            
            is_run = await settings.get_user_settings_text(settings_path)
            text = await get_compliment()
            print(text)
            
            await bot.send_chat_action(message.from_user.id, types.chat.ChatActions.TYPING)
            await asyncio.sleep(3)
            await message.answer(text)

    elif message.text == actions.QUERY_STOP_AUTO_COMPLIMENTS:
        
        is_run = False
        await settings.set_user_settings_text(settings_path, is_run)

        await bot.send_chat_action(message.from_user.id, types.chat.ChatActions.TYPING)
        await asyncio.sleep(1)
        await message.answer(actions.ANSWER_STOP_AUTO_COMPLIMENTS, 
                                reply_markup = nav.main_markup)
           

"""Exit function"""

@dp.message_handler(commands = ["exit", "cancel", "bye"])
async def exit(message: types.Message, commands = "exit"):
    
    await bot.send_chat_action(message.from_user.id, types.chat.ChatActions.TYPING)
    await asyncio.sleep(1)
    await message.answer(f"{actions.ANSWER_BYE} {message.from_user.full_name}!")


"""Run long-polling"""

def main():
    executor.start_polling(dp, on_startup=on_startup, skip_updates = True)

if __name__ == "__main__": main()
