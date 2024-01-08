# https://docs.aiogram.dev/en/dev-3.x/dispatcher/finite_state_machine/scene.html#aiogram.fsm.scene.Scene
import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.scene import SceneRegistry
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram.types import BotCommand
from handlers import bot_messages
from data.quiz_scene import QuizScene
from config_reader import config

quiz_router = Router(name=__name__)
# Add handler that initializes the scene
quiz_router.message.register(QuizScene.as_handler(), Command("quiz"))

def create_dispatcher():
    # Event isolation is needed to correctly handle fast user responses
    dispatcher = Dispatcher(
        events_isolation=SimpleEventIsolation(),
    )

    dispatcher.include_router(bot_messages.router)
    dispatcher.include_router(quiz_router)

    # To use scenes, you should create a SceneRegistry and register your scenes there
    scene_registry = SceneRegistry(dispatcher)
    # ... and then register a scene in the registry
    # by default, Scene will be mounted to the router that passed to the SceneRegistry,
    # but you can specify the router explicitly using the `router` argument
    scene_registry.add(QuizScene)

    return dispatcher


async def main():
    dispatcher = create_dispatcher()

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    # меню бота
    async def set_main_menu(bot: Bot):
        main_menu_commands = [
            BotCommand(
                command='/quiz',
                description='Письменный тест'
            ),
            BotCommand(
                command='/speaking',
                description='Устный тест'
            ),
            BotCommand(
                command='/profile',
                description='Обратная связь'
            ),
            BotCommand(
                command="/exit",
                description="Выход"
            ),
            BotCommand(
                command="/start",
                description="Перезапуск бота (обнуляет результаты тестирования)"
            )
        ]
        await bot.set_my_commands(main_menu_commands)

    await set_main_menu(bot)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())