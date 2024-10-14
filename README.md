Compliment Bot
Описание
Compliment Bot — это Telegram-бот, разработанный для отправки случайных комплиментов с изображениями. 
Он поддерживает отправку комплиментов на каждый день, управление набором комплиментов и изображений, 
а также позволяет пользователю добавлять новые комплименты и фотографии для отправки.

Основные функции
Отправка случайного комплимента с изображением. /n
Ведение учета отправленных комплиментов и изображений за день, чтобы они не повторялись.
Возможность добавления новых комплиментов через команду /add_compliment.
Возможность добавления фотографий через команду /add_photo.
Простое меню с доступом к основным командам.
Команда /help для получения списка доступных команд.

Используемые технологии

Язык программирования: Python

Библиотеки:
python-telegram-bot — для взаимодействия с Telegram API.
json — для хранения и обработки комплиментов.
asyncio — для обработки асинхронных операций.
os и random — для работы с изображениями и выбора случайных файлов.

Команды:

/start — Открыть меню с командами.
/compliment — Получить случайный комплимент с изображением.
/add_compliment <текст> — Добавить новый комплимент в список.
/add_photo — Добавить новое изображение для комплиментов.
/help — Получить список доступных команд.

Примечания:

Бот автоматически сохраняет отправленные комплименты и изображения за текущий день, чтобы не отправлять повторяющиеся сообщения.
Все данные о комплиментах хранятся в формате JSON.
