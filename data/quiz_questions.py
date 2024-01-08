from dataclasses import dataclass, field

@dataclass
class Answer:
    """
    Ответ на вопрос
    """

    text: str
    """Текст ответа"""
    is_correct: bool = False
    """Указывает, верен ли ответ"""


@dataclass
class Question:
    """
    Вопрос и список ответов
    """

    text: str
    """Текст вопроса"""
    answers: list[Answer]
    """Список ответов класса Answer"""

    correct_answer: str = field(init=False)

    def __post_init__(self):
        self.correct_answer = next(answer.text for answer in self.answers if answer.is_correct)

#В переменную test записываем данные из файла формата json с вопросами, вариантами ответов и верным ответом
import os
from ujson import loads

path = "data/placement_test.json"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as file:
        test = loads(file.read())

# Создаем список для вопросов и ответов из переменной test
quiz_questions_set = []

for item in range(len(test["Questions"])):
    # записываем в переменные текст 1 вопроса и 3 вариантов ответов
    quest = test["Questions"][str(item)]
    opt1 = test["Option 1"][str(item)]
    opt2 = test["Option 2"][str(item)]
    opt3 = test["Option 3"][str(item)]
    options_list = [opt1, opt2, opt3]
    # сохраняем индекс правильного ответа
    correct_opt_index = test["Correct"][str(item)]
    #создаем список вариантов ответов с отметкой правильного ответа
    answers_list = []
    for i,option in enumerate(options_list):
        if i == correct_opt_index:
            answers_list.append(Answer(option, is_correct=True))
        else:
            answers_list.append(Answer(option))
    quest_container = Question(text=quest, answers=answers_list)
    #добавляем в основной список вопросов и ответов
    quiz_questions_set.append(quest_container)

