from telegram import Update
from core.storage import UserStorage
from core.models import User


def register_user(update: Update) -> User:
    effective_user = update.effective_user
    user = User(id=effective_user.id, username=effective_user.username,
                first_name=effective_user.first_name,
                last_name=effective_user.last_name)
    UserStorage.insert(user)
    return user
