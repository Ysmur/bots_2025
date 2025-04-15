# Импортируем необходимые классы.
import logging
import os
import random

from telegram.ext import Application, MessageHandler, filters,CommandHandler
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
TIMER = 30

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
reply_keyboard = [['/dice', '/timer']]
dice_keyboard = [['/6', "/20"],
                 ["/2", "/back"]]
timer_keyboard = [["/30", "/1"], ["/5", "/back"]]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
markup_dice = ReplyKeyboardMarkup(dice_keyboard, one_time_keyboard=False)
markup_timer = ReplyKeyboardMarkup(timer_keyboard, one_time_keyboard=False)

# Определяем функцию-обработчик сообщений.
# У неё два параметра, updater, принявший сообщение и контекст - дополнительная информация о сообщении.
async def echo(update, context):
    # У объекта класса Updater есть поле message,
    # являющееся объектом сообщения.
    # У message есть поле text, содержащее текст полученного сообщения,
    # а также метод reply_text(str),
    # отсылающий ответ пользователю, от которого получено сообщение.
    text = update.message.text
    await update.message.reply_text(update.message.text)

async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот-помощник по играм.",
        reply_markup=markup
    )

async def back(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот-помощник по играм.",
        reply_markup=markup
    )

async def dice(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот-помощник по играм.",
        reply_markup=markup_dice
    )

async def timer(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я бот-помощник по играм.",
        reply_markup=markup_timer
    )

async def kubik(update, context):
    n1 = random.randint(1, 6)
    n2 = random.randint(1, 6)
    await update.message.reply_html(f'{n1} {n2}',
                                    reply_markup=markup_dice
    )

async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")

async def timer30(update, context):
    print('xa')
    await set_timer(update, context)


async def set_timer(update, context):
    """Добавляем задачу в очередь"""
    print('xa-xa')
    chat_id = update.effective_message.chat_id
    # Добавляем задачу в очередь
    # и останавливаем предыдущую (если она была)
    #job_removed = remove_job_if_exists(str(chat_id), context)
    job = context.job_queue.run_once(task, TIMER, chat_id=chat_id, name=str(chat_id), data=TIMER)
    print(job)

    text = f'Вернусь через 30 с.!'

    await update.effective_message.reply_text(text)

async def task(context):
    """Выводит сообщение"""
    await context.bot.send_message(context.job.chat_id, text=f'КУКУ! 30c. прошли!')

def remove_job_if_exists(name, context):
    """Удаляем задачу по имени.
    Возвращаем True если задача была успешно удалена."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("dice", dice))
    application.add_handler(CommandHandler("timer", timer))
    application.add_handler(CommandHandler("30", timer30))
    application.add_handler(CommandHandler("2", kubik))
    application.add_handler(CommandHandler("back", back))


    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()