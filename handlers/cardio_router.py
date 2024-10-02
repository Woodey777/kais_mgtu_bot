from aiogram import Router, F
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback, get_user_locale
from datetime import datetime
from keyboards.cardio_kb import cardio_type_kb, is_competition_kb, pay_debt_kb, send_cardio_kb
from states.survey_states import Cardio
from utils.logger import logger

cardio_router = Router()

def check_dist(s):
    try:
        f = float(s)
        if f > 0:
          return True
        else:
          return False
    except ValueError:
        return False


@cardio_router.message(Command(commands=['cardio']))
async def cardio_mes(message: Message, state: FSMContext):
    logger.info("cardio from message handler")
    await cardio(message, state)


@cardio_router.callback_query(Cardio.send, F.data.in_(["cardio_again"]))
async def cardio_mes(callback: CallbackQuery, state: FSMContext):
    logger.info("cardio from callback handler")
    await callback.answer('')
    await cardio(callback, state)


async def cardio(message: CallbackQuery | Message, state: FSMContext):
    logger.info("common cardio handler")
    await state.clear()
    logger.info("state cleared")
    await state.set_state(Cardio.type)
    logger.info("state Cardio.type")

    cardio_description = ("Тренировка засчитывается только если она дольше 1 часа, а пройденное расстояние не меньше:\n"
                          "Бег - 10км\n"
                          "Плавание - 2.5км\n"
                          "Ролики - 15км\n"
                          "Коньки - 15км\n"
                          "Лыжи - 15км\n"
                          "Велосипед - 20км\n"
                          "За минимальное расстояние даётся 1 балл, за большее - пропорционально больше, за меньшее баллы не даются\n"
                          "За участие в соревнованиях баллы увеличиваются в 2\n"
                          "Помните, что если минимальное расстояние за неделю не пройдено, долг увеличивается в 1.5\n"
                          "Для допуска к конкурсу пробежек должно быть минимум 1 в неделю и не больше 8 пропущенных недель за весь период подготовкиКакого типа она была?")

    if isinstance(message, Message):
        logger.info("Message type handling")
        await message.answer(f'Давай добавим кардио тренировку!\n{cardio_description}', parse_mode="MARKDOWN")
        await message.answer('Выбери тип кардио тренировки', reply_markup=cardio_type_kb())
    elif isinstance(message, CallbackQuery):
        logger.info("CallbackQuery type handling")
        await message.message.answer(f'Давай добавим кардио тренировку!\n{cardio_description}', parse_mode="MARKDOWN")
        await message.message.answer('Выбери тип кардио тренировки', reply_markup=cardio_type_kb())

@cardio_router.callback_query(Cardio.type, F.data.in_(["running_type", "swimming_type", "rollers_type", "ice_skates_type", "ski_type", "cycle_type", "running_fac_type", "rogaine_type"]))
async def get_distance(callback: CallbackQuery, state: FSMContext):
    logger.info("get_distance handler")
    await callback.answer('')
    kb = cardio_type_kb().inline_keyboard
    for i in range(0, len(kb)):
        for j in range(0, len(kb[i])):
            if callback.data == kb[i][j].callback_data:
                await state.update_data(cardio_type=kb[i][j].text)
                logger.info(f"got cardio_type: {kb[i][j].text}")

    await state.set_state(Cardio.dist)
    logger.info("state Cardio.dist")
    await callback.message.answer(f'Введите дистанцию(км):')

@cardio_router.message(lambda message: check_dist(message.text), Cardio.dist)
async def get_date(message: Message, state: FSMContext):
    logger.info("get_distance handler")
    await state.update_data(distance=message.text)
    logger.info(f"got distance: {message.text}")
    await state.set_state(Cardio.date)
    logger.info("state Cardio.date")
    calendar = SimpleCalendar(
        locale=await get_user_locale(message.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2024, 10, 1), datetime(2024, 11, 1))
    await message.answer(
        "Выберите дату",
        reply_markup=await calendar.start_calendar(year=2024, month=10)
        )

@cardio_router.message(lambda message: not check_dist(message.text), Cardio.dist)
async def wrong_dist(message: Message):
    logger.info("wrong dist handler")
    await message.answer(f'Дистанция должна быть положительным действительным числом\nПопробуйте еще раз:')

@cardio_router.callback_query(SimpleCalendarCallback.filter(), Cardio.date)
async def is_competition(callback: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    calendar = SimpleCalendar(locale=await get_user_locale(callback.from_user), show_alerts=True)
    selected, date = await calendar.process_selection(callback, callback_data)
    if selected:
        date_str = date.strftime("%d.%m.%Y")
        await state.update_data(date=date_str)
        logger.info(f"got date: {date_str}")
        await state.set_state(Cardio.is_competition)
        logger.info("state Cardio.is_competition")
        await callback.message.answer(f'Участие в рамках кардио соревнований?', reply_markup=is_competition_kb())
    else:
        logger.warning("date is not selected in calendar")
        return    


@cardio_router.callback_query(Cardio.is_competition, F.data.in_(["yes_competition", "no_competition"]))
async def pay_debt(callback: CallbackQuery, state: FSMContext):
    logger.info("pay_debt handler")
    await callback.answer('')
    kb = is_competition_kb().inline_keyboard
    for i in range(0, len(kb)):
        for j in range(0, len(kb[i])):
            if callback.data == kb[i][j].callback_data:
                await state.update_data(is_competition=kb[i][j].text)
                logger.info(f"got is_competition: {kb[i][j].text}")
    await state.set_state(Cardio.pay_debt)
    logger.info("state Cardio.pay_debt")

    description = ("Не списывать имеющийся долг, накопить баллы?\n"
                   "Пользуйтесь с умом: в течение всего периода предлагерной подготовки допускается всего 8 пропусков\n"
                   "Когда может быть полезно: у тебя 7/8 долгов, ты проходишь по требованиям, но находишься низко в рейтинге, поэтому хочешь накопить баллы, а не закрывать долги")
    await callback.message.answer(f'{description}', reply_markup=pay_debt_kb(), parse_mode="MARKDOWN")


@cardio_router.callback_query(Cardio.pay_debt, F.data.in_(["yes_pay_debt", "no_pay_debt"]))
async def end_activity_survey(callback: CallbackQuery, state: FSMContext):
    logger.info("end_activity_survey handler")
    await callback.answer('')
    kb = pay_debt_kb().inline_keyboard
    for i in range(0, len(kb)):
        for j in range(0, len(kb[i])):
            if callback.data == kb[i][j].callback_data:
                await state.update_data(pay_debt=kb[i][j].text)
                logger.info(f"got pay_debt: {kb[i][j].text}")
    data = await state.get_data()
    logger.info("state data received")
    ans = ('Вы ввели следующие данные:\n'
           f'Тип тренировки – *{data["cardio_type"]}*\n'
           f'Дистанция – *{data["distance"]} км*\n' 
           f'Дата – *{data["date"]}*\n' 
           f'Соревнование? – *{data["is_competition"]}*\n'
           f'Списать долг? – *{data["pay_debt"]}*')
    await state.set_state(Cardio.send)
    logger.info("state Cardio.send")
    await callback.message.answer(ans, reply_markup=send_cardio_kb(), parse_mode="MARKDOWN")

@cardio_router.callback_query(Cardio.send, F.data.in_(["send_cardio"]))
async def send_cardio(callback: CallbackQuery, state: FSMContext):
    logger.info("sending_cardio handler")
    await callback.answer('')
    await callback.message.answer("Отправлено! (нет)")
    logger.info("sending cardio")
    pass