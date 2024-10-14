import json
import random
from telegram import Update
from telegram.ext import Application, CommandHandler

# Загрузка комплиментов из файла
def load_compliments():
    with open('compliments.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data['compliments']

# Функция для отправки случайного комплимента
async def send_compliment(update: Update, context):
    compliments = load_compliments()
    compliment = random.choice(compliments)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=compliment)

# Настройка и запуск бота
async def main():
    # Вставь свой токен, который ты получил от BotFather
    TOKEN = '8102359090:AAFfeQsH6bZS4DDeGIGpOC1GnRJ9sQ-T8Dg'

    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Хендлер для команды /compliment
    application.add_handler(CommandHandler('compliment', send_compliment))

    # Запуск бота (начало обработки обновлений)
    await application.start()

    # Ожидание завершения работы бота (в режиме idle)
    await application.updater.start_polling()

    # Ожидание завершения работы
    await application.stop()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
