from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import aiofiles

from utils.states import Form
from keyboards.builders import profile
from keyboards.reply import rmk
from data.speaking_questions import speaking_task
from keyboards.reply import phone
from datetime import datetime


router = Router()


@router.message(Command("start"))
async def command_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>Вас приветствует школа LinLab 👋</b>\n\n"
        "📝 Выполните письменный тест /quiz\n"
        "🗣 Пройдите устный тест /speaking\n"
        "📞 Для обратной связи заполните анкету /profile",
        reply_markup=rmk,
        parse_mode="HTML"
    )

@router.message(Command("exit"))
async def command_start(message: Message, state: FSMContext):
    data = await state.get_data()
    correct = data.get("Верных ответов (в тесте)", {})
    level = data.get("Уровень", {})
    audio = data.get("Аудио", {})
    await state.clear()
    if correct or level or audio:
        await state.set_data({"Верных ответов (в тесте)": correct, "Уровень": level, "Аудио": audio})
    await message.answer(
        "📝 Выполните письменный тест /quiz\n"
        "🗣 Пройдите устный тест /speaking\n"
        "📞 Для обратной связи заполните анкету /profile",
        reply_markup=rmk,
        parse_mode="HTML"
    )

@router.message(Command("speaking"))
async def test(message: Message, state: FSMContext):
    await state.set_state(Form.speaking_link)
    await message.answer(speaking_task, reply_markup=rmk, parse_mode="HTML")

@router.message(Command("profile"))
async def fill_profile(message: Message, state: FSMContext):
    await state.set_state(Form.name)
    user_name = " ".join(message.from_user.username.split("_"))
    await message.answer(
        "Для выхода 👉 /exit"
        "\nЗаполним анкету обратной связи. "
        "\n\nВведите <b>Ваше имя и фамилию</b> или нажмите на кнопку ниже: ",
        reply_markup=profile(str(user_name)), parse_mode="HTML"
    )


@router.message(Form.speaking_link)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(Аудио=message.text)
    await message.answer("Спасибо!"
                         "\nЕсли Вы не выполнили письменный тест 👉 /exit, потом 👉 /quiz"
                         "\nДля обратной связи заполните анкету 👉 /profile", reply_markup=rmk)



@router.message(Form.name)
async def form_name(message: Message, state: FSMContext):
    await state.update_data(имя=message.text)
    await state.set_state(Form.phone)
    await message.answer("Введите Ваш телефон или нажмите на кнопку ниже:", reply_markup=phone)


@router.message(Form.phone)
async def form_phone(message: Message, state: FSMContext):
    if message.contact:
        num = str(message.contact.phone_number).replace("+", "")
    else:
        num = message.text.replace(" ", "").replace("-", "")
    if num.isdigit() and (len(num) == 10 or len(num) == 11):
        await state.update_data(телефон=num)
        await state.set_state(Form.app_choice)
        await message.answer("Способ связи:", reply_markup=profile(["Звонок", "WhatsApp", "Telegram"]))
    else:
        await message.answer("Извините, введен некорректный номер мобильного телефона. Пожалуйста, введите повторно.")


@router.message(Form.app_choice, F.text.casefold().in_(["звонок", "whatsapp", "telegram"]))
async def form_about(message: Message, state: FSMContext):
    await state.update_data(связь=message.text)
    await state.set_state(Form.about)
    await message.answer(
        "Расскажите, для каких целей Вам необходим английский язык. Выберите одну из кнопок или введите информацию вручную",
        reply_markup=profile(["Путешествия", "Работа", "Учеба"]))


@router.message(Form.app_choice)
async def incorrect_app_choice(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, нажмите на одну из кнопок!", reply_markup=profile(["WhatsApp", "Telegram"]))


@router.message(Form.about)
async def fill_about(message: Message, state: FSMContext):
    if len(message.text) < 5:
        await message.answer("Пожалуйста, введите чуть больше информации о целях изучения английского языка!")
    else:
        await state.update_data(цель=message.text)
        data = await state.get_data()
        formatted_text = []
        [
            formatted_text.append(f"{key.capitalize()}: {value}")
            for key, value in data.items()
        ]
        profile_data = '\n'.join(formatted_text)
        await state.set_state(Form.verified)
        await message.answer(
            f"Проверьте, пожалуйста, правильность информации внизу и <b>нажмите кнопку 'Верно'</b>:"
            f"\n\n{profile_data}"
            f"\n\nЕсли есть ошибка, просим заново заполнить форму 👉 /profile"
            f"\nДля выхода из анкеты без ее отправки 👉 /exit ",reply_markup=profile(["Верно"]), parse_mode="HTML")


@router.message(Form.verified, F.text.casefold().in_(["верно"]))
async def verified_reply(message: Message, state: FSMContext):
    await message.answer("Спасибо за обращение! Свяжемся с Вами в ближайшее время. До свидания!")
    data = await state.get_data()
    path = "data/new_clients"
    submit_date = datetime.today().strftime('%d-%m-%Y')
    name = f"{message.from_user.id}_от_{submit_date}"
    async with aiofiles.open(f'{path}/заявка_{data["имя"]}_{name}.txt', mode='w', encoding="utf-8") as f:
        data_saved = [f"{key}: {value}" for key, value in data.items()]
        await f.write('\n'.join(data_saved))