from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from core.config import PollCfg
from core.utils import list_to_columns
from tg.context import PollContext


def get_keyboard_markup(ctx: PollContext) -> InlineKeyboardButton | None:
    if ctx.answered_all:
        return None

    buttons = []
    for index, answer in enumerate(ctx.current_question.answers):
        button = InlineKeyboardButton(answer, callback_data=index)
        buttons.append(button)
    keyboard = list_to_columns(buttons, PollCfg.max_columns)

    return InlineKeyboardMarkup(keyboard)

def get_poll_message(ctx: PollContext) -> str:
    if ctx.answered_all:
        return 'Ураа, вы все'

    progress = f'{ctx.current_question_index + 1}/{len(ctx.questions)}'
    question_title = ctx.questions[ctx.current_question_index].title.strip()
    question_mark = '?' if not question_title.endswith('?') else ''
    return f'{progress}\n{question_title}{question_mark}'
