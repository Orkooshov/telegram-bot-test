from telegram import Update
from telegram.ext import ContextTypes

from tg import builders
from tg.context import PollContext
from tg import utils
from core.storage import QuestionStorage, UserAnswerStorage, UserStorage
from core.models import UserAnswer


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Пишите /start чтобы начать")

async def start_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''Starts the application'''
    utils.register_user(update)

    poll_ctx = PollContext(questions=QuestionStorage.get_all(), current_question_index=0)
    context.user_data['poll_ctx'] = poll_ctx

    message = builders.get_poll_message(poll_ctx)
    markup = builders.get_keyboard_markup(poll_ctx)
    await update.effective_chat.send_message(message, reply_markup=markup)

async def button_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()

    poll_ctx = context.user_data['poll_ctx']
    user = UserStorage.get_by_username(update.effective_user.username)

    # save answer
    ua = UserAnswer(user, poll_ctx.current_question, int(query.data))
    UserAnswerStorage.insert(ua)

    poll_ctx.current_question_index += 1
    message = builders.get_poll_message(poll_ctx)
    markup = builders.get_keyboard_markup(poll_ctx)
    await query.edit_message_text(text=message, reply_markup=markup)

async def show_questions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = 'Вопросы:\n'

    questions = QuestionStorage.get_all()
    counter = 0
    for q in questions:
        counter += 1
        msg += f'{counter}. {q.title.capitalize()}\n'
        for answer in q.answers:
            msg += f'  - {answer}\n'

    await update.effective_chat.send_message(msg)

async def show_answers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    utils.register_user(update)

    user = UserStorage.get_by_username(update.effective_user.username)
    msg = 'Ваши ответы:\n'
    counter = 0
    for user_answer in UserAnswerStorage.get_by_user(user):
        counter += 1
        msg += f'{counter}. {user_answer.question.title}\n'
        for answer in user_answer.question.answers:
            msg += f'  - {answer}\n'
        msg += f'Ваш ответ: {user_answer.answer_text}\n\n'
        if counter == 0:
            msg += 'Пусто'

    await update.effective_chat.send_message(msg)

# async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     member = await update.get_bot().get_chat_member()
#     member = update.effective_user.get_bot()
    

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # await update.effective_message.edit_text('asdf')
    await update.effective_chat.send_message('Не пон')
    