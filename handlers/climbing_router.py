from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, get_user_locale
from datetime import datetime
from keyboards.climbing_kb import climb_type_kb, is_competition_kb, send_climbing_kb
from states.survey_states import Climbing
from utils.logger import logger

climbing_router = Router()

@climbing_router.message(Command(commands=['climbing']))
async def climbing_mes(message: Message, state: FSMContext):
    logger.info("climbing from message handler")
    await climbing(message, state)


@climbing_router.callback_query(Climbing.send, F.data.in_(["climbing_again"]))
async def climbing_mes(callback: CallbackQuery, state: FSMContext):
    logger.info("climbing from callback handler")
    await callback.answer('')
    await climbing(callback, state)


async def climbing(message: CallbackQuery | Message, state: FSMContext):
    logger.info("common climbing handler")
    await state.clear()
    logger.info("state cleared")
    await state.set_state(Climbing.type)
    logger.info("state Climbing.type")

    if isinstance(message, Message):
        logger.info("Message type handling")
        await message.answer('Выбери тип лазательной тренировки', reply_markup=climb_type_kb())
    elif isinstance(message, CallbackQuery):
        logger.info("CallbackQuery type handling")
        await message.message.answer('Выбери тип лазательной тренировки', reply_markup=climb_type_kb())

@climbing_router.callback_query(Climbing.type, F.data.in_(["climb_low_type", "climb_high_type", "bouldering_type", "drytool_type", "ice_climb_type"]))
async def get_date(callback: CallbackQuery, state: FSMContext):
    logger.info("get_date handler")
    await callback.answer('')
    kb = climb_type_kb().inline_keyboard
    for i in range(0, len(kb)):
        for j in range(0, len(kb[i])):
            if callback.data == kb[i][j].callback_data:
                await state.update_data(climbing_type=kb[i][j].text)
                logger.info(f"got climbing_type: {kb[i][j].text}")

    await state.set_state(Climbing.date)
    logger.info("state Climbing.date")

    calendar = SimpleCalendar(
        locale=await get_user_locale(callback.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2024, 10, 1), datetime(2024, 11, 1))  #TODO: на основе текущей даты
    await callback.message.answer(
        "Выберите дату",
        reply_markup=await calendar.start_calendar(year=2024, month=10)
        )
    
    
@climbing_router.callback_query(SimpleCalendarCallback.filter(), Climbing.date)
async def is_competition(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(locale=await get_user_locale(callback.from_user), show_alerts=True)
    selected, date = await calendar.process_selection(callback, callback_data)
    if selected:
        date_str = date.strftime("%d.%m.%Y")
        await state.update_data(date=date_str)
        logger.info(f"got date: {date_str}")
        await state.set_state(Climbing.is_competition)
        logger.info("state Climbing.is_competition")
        await callback.message.answer(f'Участие в рамках лазательных соревнований?', reply_markup=is_competition_kb())
    else:
        logger.warning("date is not selected in calendar")
        return  

@climbing_router.callback_query(Climbing.is_competition, F.data.in_(["yes_competition", "no_competition"]))
async def end_activity_survey(callback: CallbackQuery, state: FSMContext):
    logger.info("end_activity_survey handler")
    await callback.answer('')
    kb = is_competition_kb().inline_keyboard
    for i in range(0, len(kb)):
        for j in range(0, len(kb[i])):
            if callback.data == kb[i][j].callback_data:
                await state.update_data(is_competition=kb[i][j].text)
                logger.info(f"got pay_debt: {kb[i][j].text}")

    data = await state.get_data()
    logger.info("state data received")
    ans = ('Вы ввели следующие данные:\n'
           f'Тип тренировки – *{data["climbing_type"]}*\n'
           f'Дата – *{data["date"]}*\n' 
           f'Соревнование? – *{data["is_competition"]}*\n'
    )
    await state.set_state(Climbing.send)
    logger.info("state Climbing.send")
    await callback.message.answer(ans, reply_markup=send_climbing_kb(), parse_mode="MARKDOWN")

@climbing_router.callback_query(Climbing.send, F.data.in_(["send_climbing"]))
async def send_cardio(callback: CallbackQuery, state: FSMContext):
    logger.info("sending_climbing handler")
    await callback.answer('')
    await callback.message.answer("Отправлено! (нет)")
    logger.info("sending climbing")
    pass