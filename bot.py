import json
import random
import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ConversationHandler
import asyncio
import nest_asyncio

# Активируем возможность вложенных циклов событий
nest_asyncio.apply()

# Папка для изображений
IMAGES_DIR = 'images'

# Файл для хранения комплиментов, отправленных за текущий день
SENT_COMPLIMENTS_FILE = 'sent_compliments.json'

# Состояния для ConversationHandler
ADDING_PHOTO = range(1)

# Загрузка комплиментов из файла
def load_compliments():
    with open('compliments.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data['compliments']

# Запись комплиментов в файл
def save_compliment(new_compliment):
    compliments = load_compliments()
    compliments.append(new_compliment)

    with open('compliments.json', 'w', encoding='utf-8') as file:
        json.dump({"compliments": compliments}, file, ensure_ascii=False, indent=4)

# Загрузка отправленных комплиментов за текущий день
def load_sent_compliments():
    if os.path.exists(SENT_COMPLIMENTS_FILE):
        with open(SENT_COMPLIMENTS_FILE, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if data.get('date') != datetime.now().strftime('%Y-%m-%d'):
                return []  # Если дата изменилась, возвращаем пустой список
            return data['compliments']
    return []

# Запись отправленных комплиментов
def save_sent_compliment(compliment):
    sent_compliments = load_sent_compliments()
    sent_compliments.append(compliment)
    with open(SENT_COMPLIMENTS_FILE, 'w', encoding='utf-8') as file:
        json.dump({'date': datetime.now().strftime('%Y-%m-%d'), 'compliments': sent_compliments}, file, ensure_ascii=False)

# Загрузка случайного изображения из папки
def get_random_image():
    images = os.listdir(IMAGES_DIR)
    random_image = random.choice(images)
    return os.path.join(IMAGES_DIR, random_image)

# Функция для отправки случайного комплимента с изображением и инлайн-кнопками
async def send_compliment(update: Update, context):
    compliments = load_compliments()
    sent_compliments = load_sent_compliments()

    # Фильтрация комплиментов, которые еще не отправлялись сегодня
    available_compliments = [c for c in compliments if c not in sent_compliments]

    if not available_compliments:
        sent_compliments = []
        available_compliments = compliments

    compliment = random.choice(available_compliments)
    save_sent_compliment(compliment)
    image_path = get_random_image()

    # Создаем инлайн-кнопки
    keyboard = [
        [InlineKeyboardButton("Получить еще комплимент", callback_data='compliment')],
        [InlineKeyboardButton("Добавить комплимент", callback_data='add_compliment')],
        [InlineKeyboardButton("Добавить фото", callback_data='add_photo')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем изображение и комплимент с инлайн-кнопками
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_path, 'rb'), caption=compliment, reply_markup=reply_markup)

# Функция для отправки списка доступных команд
async def help_command(update: Update, context):
    help_text = (
        "/compliment - получить случайный комплимент с изображением\n"
        "/help - список доступных команд\n"
        "/add_compliment <текст> - добавить новый комплимент\n"
        "/add_photo - отправить фото для добавления в базу"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

# Функция для обработки инлайн-кнопок
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'compliment':
        await send_compliment(update, context)
    elif query.data == 'add_compliment':
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Введите команду /add_compliment с текстом комплимента.")
    elif query.data == 'add_photo':
        await add_photo_start(update, context)

# Функция для добавления нового комплимента
async def add_compliment(update: Update, context):
    new_compliment = ' '.join(context.args)

    if new_compliment:
        save_compliment(new_compliment)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Новый комплимент добавлен!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, добавьте текст комплимента после команды /add_compliment.")

# Функция для начала процесса добавления фото
async def add_photo_start(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Отправьте фото для добавления.")
    return ADDING_PHOTO

# Функция для сохранения нового фото
async def save_photo(update: Update, context):
    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        new_photo_path = os.path.join(IMAGES_DIR, f'photo_{random.randint(1, 10000)}.jpg')
        await photo_file.download_to_drive(new_photo_path)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Фото успешно добавлено!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, отправьте фото.")
    return ConversationHandler.END

# Функция для отмены добавления фото
async def cancel(update: Update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Добавление фото отменено.")
    return ConversationHandler.END

# Функция для отправки стартового меню
async def start_command(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Получить комплимент", callback_data='compliment')],
        [InlineKeyboardButton("Добавить комплимент", callback_data='add_compliment')],
        [InlineKeyboardButton("Добавить фото", callback_data='add_photo')],
        [InlineKeyboardButton("Помощь", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите команду:", reply_markup=reply_markup)

# Настройка и запуск бота
async def main():
    TOKEN = '7636816904:AAEdeNNl7TzqeEI5JDMWEKSD1HTTIJ1U4h0'  # Замените на ваш токен бота

    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(CommandHandler('add_compliment', add_compliment))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('add_photo', add_photo_start)],
        states={
            ADDING_PHOTO: [MessageHandler(filters.PHOTO, save_photo)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)

    await application.run_polling()

if __name__ == '__main__':
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    asyncio.run(main())
