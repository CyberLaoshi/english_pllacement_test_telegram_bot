from typing import Any
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.fsm.scene import Scene, on
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message, ReplyKeyboardRemove
from data.quiz_questions import quiz_questions_set
from aiogram.utils.formatting import (
    Text,
    Bold,
    as_key_value,
    as_list,
    as_numbered_list,
    as_section,
)
from aiogram import F, html
from utils.level_assessor import level_assessment

QUESTIONS = quiz_questions_set

class QuizScene(Scene, state="quiz"):
    """
    Класс для квиза с логикой игры
    """

    @on.message.enter()
    async def on_enter(self, message: Message, state: FSMContext, step: int | None = 0) -> Any:
        """
        Method triggered when the user enters the quiz scene.

        It displays the current question and answer options to the user.

        :param message:
        :param state:
        :param step: Scene argument, can be passed to the scene using the wizard
        :return:
        """
        if not step:
            # This is the first step, so we should greet the user
            await message.answer("Приступим к письменному тесту. Выберите правильный вариант ответа. Удачи!")

        try:
            quiz = QUESTIONS[step]
        except IndexError:
            # This error means that the question's list is over
            return await self.wizard.exit()

        markup = ReplyKeyboardBuilder()
        markup.add(*[KeyboardButton(text=answer.text) for answer in quiz.answers])

        if step > 0:
            markup.button(text="🔙 Назад")
        markup.button(text="🚫 Завершить")

        await state.update_data(step=step)
        return await message.answer(
            text=QUESTIONS[step].text,
            reply_markup=markup.adjust(2).as_markup(resize_keyboard=True),
        )

    @on.message.exit()
    async def on_exit(self, message: Message, state: FSMContext) -> None:
        """
        Method triggered when the user exits the quiz scene.

        It calculates the user's answers, displays the summary, and clears the stored answers.

        :param message:
        :param state:
        :return:
        """
        data = await state.get_data()
        answers = data.get("answers", {})
        correct = 0
        incorrect = 0
        user_answers = []
        for step, quiz in enumerate(QUESTIONS):
            answer = answers.get(step)
            is_correct = answer == quiz.correct_answer
            if is_correct:
                correct += 1
                icon = "✅"
            else:
                incorrect += 1
                icon = "❌"
            if answer is None:
                answer = "no answer"
            user_answers.append(f"{quiz.text} ({icon} {html.quote(answer)})")

        assessed_level = level_assessment(correct)

        content = as_list(
            as_section(
                Bold("Ваши ответы:"),
                as_numbered_list(*user_answers),
            ),
            "",
            as_section(
                Bold("Итого:"),
                as_list(
                    as_key_value("Верно", correct),
                    as_key_value("Неверно", incorrect),
                ),
            ),
            "",
            as_section(
                Bold("Ваш уровень:"),
                Text(assessed_level)
            ),
            "",
            as_section(
                Text("Пройдите устный тест 👉 /speaking"),
                Text("Нужна помощь? Заполните анкету 👉 /profile")
            )
        )


        await message.answer(**content.as_kwargs(), reply_markup=ReplyKeyboardRemove())
        audio = data.get("Аудио", {})
        await state.set_data({"Уровень": assessed_level, "Верных ответов (в тесте)": correct, "Аудио": audio})

    @on.message(F.text == "🔙 Назад")
    async def back(self, message: Message, state: FSMContext) -> None:
        """
        Method triggered when the user selects the "Back" button.

        It allows the user to go back to the previous question.

        :param message:
        :param state:
        :return:
        """
        data = await state.get_data()
        step = data["step"]

        previous_step = step - 1
        if previous_step < 0:
            # In case when the user tries to go back from the first question,
            # we just exit the quiz
            return await self.wizard.exit()
        return await self.wizard.back(step=previous_step)

    @on.message(F.text == "🚫 Завершить")
    async def exit(self, message: Message) -> None:
        """
        Method triggered when the user selects the "Exit" button.

        It exits the quiz.

        :param message:
        :return:
        """
        await self.wizard.exit()

    @on.message(F.text)
    async def answer(self, message: Message, state: FSMContext) -> None:
        """
        Method triggered when the user selects an answer.

        It stores the answer and proceeds to the next question.

        :param message:
        :param state:
        :return:
        """
        data = await state.get_data()
        step = data["step"]
        answers = data.get("answers", {})
        answers[step] = message.text
        await state.update_data(answers=answers)

        await self.wizard.retake(step=step + 1)

    @on.message()
    async def unknown_message(self, message: Message) -> None:
        """
        Method triggered when the user sends a message that is not a command or an answer.

        It asks the user to select an answer.

        :param message: The message received from the user.
        :return: None
        """
        await message.answer("Please select an answer.")

