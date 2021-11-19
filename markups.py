
from aiogram.types import ReplyKeyboardRemove, \
                            ReplyKeyboardMarkup, KeyboardButton, \
                            InlineKeyboardMarkup, InlineKeyboardButton

import actions


"""Buttons"""

button_hi = KeyboardButton(actions.QUERY_GREETING)

#button_bye = KeyboardButton(actions.QUERY_BYE)

button_get_compliment = KeyboardButton(actions.QUERY_GET_COMPLIMENT)

button_settngs = KeyboardButton(actions.QUERY_SETTINGS)

button_main_menu = KeyboardButton(actions.QUERY_MAIN_MENU)

button_text_answer = KeyboardButton(actions.QUERY_TEXT_ANSWER)

button_voice_answer = KeyboardButton(actions.QUERY_VOICE_ANSWER)

button_start_auto_compliments = KeyboardButton(actions.QUERY_START_AUTO_COMPLIMENTS)

button_stop_auto_compliments = KeyboardButton(actions.QUERY_STOP_AUTO_COMPLIMENTS)


"""Markups"""

greet_markup = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True
).add(button_hi)


main_markup = ReplyKeyboardMarkup(
                    resize_keyboard=True
                ).add(button_get_compliment
                ).add(button_start_auto_compliments
                ).add(button_settngs)
                #).add(button_bye)

settings_markup = ReplyKeyboardMarkup(
                    resize_keyboard=True
                ).add(button_text_answer
                ).add(button_voice_answer
                ).add(button_main_menu)

auto_compliments_markup = ReplyKeyboardMarkup(
                    resize_keyboard=True
                ).add(button_stop_auto_compliments)


# inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
# inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)