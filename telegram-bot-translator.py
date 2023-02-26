import os
from aiogram import Bot, Dispatcher, types, executor
from translate import Translator

# Create a Telegram bot instance
bot = Bot(token='YOUR_TOKEN_HERE')

# Set up the dispatcher
dp = Dispatcher(bot)

# Define a dictionary of available languages and their corresponding translation options
languages = {
    'en-ru': {'from_lang': 'en', 'to_lang': 'ru', 'text': 'English to Russian'},
    'en-pt': {'from_lang': 'en', 'to_lang': 'pt', 'text': 'English to Portuguese'},
    'en-fr': {'from_lang': 'en', 'to_lang': 'fr', 'text': 'English to France'},
	'en-it': {'from_lang': 'en', 'to_lang': 'it', 'text': 'English to Italia'},
	'ru-en': {'from_lang': 'ru', 'to_lang': 'en', 'text': 'Russian to English'},
	'ru-pt': {'from_lang': 'ru', 'to_lang': 'pt', 'text': 'Russian to Portuguese'},
	'ru-fr': {'from_lang': 'ru', 'to_lang': 'fr', 'text': 'Russian to France'},
}

# Set up the default translator with ru-en option
translator = Translator(from_lang=languages['ru-en']['from_lang'], to_lang=languages['ru-en']['to_lang'])

# Define a handler for incoming messages
@dp.message_handler(commands=['start', 'menu'])
async def start(message: types.Message):
    # Send the user a message with the language options
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for key in languages:
        buttons.append(types.InlineKeyboardButton(text=languages[key]['text'], callback_data=key))
    keyboard.add(*buttons)
    await message.answer("Select a translation direction:", reply_markup=keyboard)

@dp.callback_query_handler()
async def process_callback(callback_query: types.CallbackQuery):
    global translator

    # Set up the translator with the selected language option
    translator = Translator(from_lang=languages[callback_query.data]['from_lang'],
                                to_lang=languages[callback_query.data]['to_lang'])

    # Send the user a message with the selected language option
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Selected translation direction: {languages[callback_query.data]['text']}")

@dp.message_handler()
async def translate_message(message: types.Message):
    global translator

    # Translate the incoming message
    translated_text = translator.translate(message.text)

    # Send the translated text back to the user
    await message.answer(translated_text)


# Start the bot
if __name__ == '__main__':
    executor.start_polling(dp)
