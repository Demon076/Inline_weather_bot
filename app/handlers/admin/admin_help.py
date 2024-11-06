from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("admin_help"))
async def admin_help_cmd(message: types.Message):
    await message.answer(f'Мои команды:\n'
                         f'/admin_help - Помощь по командам\n'
                         f'/city_coordinates - Получить координаты города по имени (Устарело)\n'
                         f'/unload_log - Выгрузить лог\n'
                         f'/add_city - Добавить город через запятую: название города, русское название, часовой пояс\n'
                         f'/delete_city - Удалить город по названию или id\n'
                         f'/info_city - Получить информацию по городу по названию или id\n'
                         f'/setting_city - '
                         f'Настроить город через запятую: название города, русское название, часовой пояс\n'
                         f'/json_cities - Выгрузить json файл с городами\n'
                         f'/load_json_cities - Загрузить файл json с городами\n'
                         )
