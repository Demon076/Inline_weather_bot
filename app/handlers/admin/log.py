from pathlib import Path

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile

from app.utils.root_dir import root_path

router = Router()


@router.message(Command("unload_log"))
async def cmd_unload_log(message: types.Message):
    log = FSInputFile(filename="log.log", path=Path(root_path() / "log.log"))
    await message.answer_document(
        document=log
    )
