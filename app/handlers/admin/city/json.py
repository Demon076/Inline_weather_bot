import os
from pathlib import Path

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile

from app.bot.bot import bot
from app.handlers.weather.default_results import DefaultResults
from app.services.weather.data import Cities
from app.utils.root_dir import root_path

router = Router()


class JsonState(StatesGroup):
    json_load = State()


@router.message(Command("json_cities"))
async def json_cities_cmd(message: types.Message):
    json_cities = FSInputFile(
        filename="cities.json",
        path=Path(root_path() / "resources/weather/cities.json")
    )
    await message.answer_document(text='Файл с городами', document=json_cities)


@router.message(Command("load_json_cities"))
async def cmd_upload_csv(message: types.Message, state: FSMContext):
    await message.answer(text="Отправьте файл с городами")
    await state.set_state(JsonState.json_load)


@router.message(JsonState.json_load)
async def fsm_upload_csv(message: types.Message, state: FSMContext):
    if message.document is None:
        await message.answer(text="Попробуйте снова! Документ не отправлен.")
        await state.set_state(JsonState.json_load)
    else:
        document = message.document
        path = Path(root_path() / "resources/weather/cities.json")
        os.remove(path)
        await bot.download(
            document,
            destination=path
        )
        await message.answer(text="Файл загружен!")
        await state.clear()

        Cities.load_cities()
        DefaultResults.reload_default_results()
        await message.answer(text="Данные обновлены!!")
