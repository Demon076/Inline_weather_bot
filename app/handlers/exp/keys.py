from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.database.core.redis import redis_conn
from app.filters.role_filters import AdminFilter

router = Router()
router.message.filter(AdminFilter())


class ValueState(StatesGroup):
    value = State()


@router.message(Command("key"))
async def key_cmd(
        message: types.Message,
        command: CommandObject
):
    value = await redis_conn.get(command.args)

    if value is None:
        await message.answer(text="По этому ключу ничего не лежит ((")
        return

    await message.answer(text=value)


@router.message(Command("value"))
async def value_cmd(
        message: types.Message,
        command: CommandObject,
        state: FSMContext
):
    if command.args is None:
        await message.answer(text="Введите что-то чтобы добавить ключ")
        return

    await state.set_data(data={'key': command.args})
    await message.answer(text="Ключ запомнен. Теперь введите значение!!")
    await state.set_state(ValueState.value)


@router.message(ValueState.value)
async def value_cmd(
        message: types.Message,
        state: FSMContext
):
    if message.text is None:
        await message.answer(text="Введите что-то чтобы добавить значение!!")
        return

    key = (await state.get_data())['key']
    await redis_conn.set(name=key, value=str(message.text))

    await message.answer(text=f'Добавлено!!\n\n'
                              f'Ключ: {key}\n'
                              f'Значение: {(await redis_conn.get(key))}')

    await state.clear()
