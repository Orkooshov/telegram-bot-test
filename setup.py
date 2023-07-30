from core.storage import QuestionStorage
from core.models import Question
from core.config import RESOURCES_FOLDER
from database import connection
import json


questions_json = RESOURCES_FOLDER / 'questions.json'

if __name__ == '__main__':
    connection.initialize_database()
    with questions_json.open(encoding='utf-8') as f:
        questions = json.load(f)
        for q in questions:
            question = Question(title=q['title'], answers=q['answers'])
            QuestionStorage.insert(question)
