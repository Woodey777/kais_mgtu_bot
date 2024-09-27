from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.activity_kb import trainings_kb, cardio_type_kb, is_competition_kb, pay_debt_kb
from states.survey_states import Cardio
from aiogram.fsm.context import FSMContext

activity_router = Router()

def check_dist(s):
    try:
        f = float(s)
        if f > 0:
          return True
        else:
          return False
    except ValueError:
        return False

@activity_router.message(F.text == "Добавить активность")
async def add_activity(message: Message):
    await message.answer('Какую активность хотите добавить?', reply_markup=trainings_kb())


@activity_router.callback_query(F.data == 'add_cardio')
async def cardio_type(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(Cardio.type)

    await callback.answer('')
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

    await callback.message.answer(f'Давай добавим кардио тренировку!\n{cardio_description}')
    await callback.message.answer('Выбери тип кардио тренировки', reply_markup=cardio_type_kb())


@activity_router.callback_query(Cardio.type, F.data.in_(["running_type", "swimming_type", "rollers_type", "ice_skates_type", "ski_type", "cycle_type", "running_fac_type", "rogaine_type"]))
async def get_distance(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    kb = cardio_type_kb().inline_keyboard
    for i in range(0, len(kb)):
        for j in range(0, len(kb[i])):
            if callback.data == kb[i][j].callback_data:
                await state.update_data(cardio_type=kb[i][j].text)
    await state.set_state(Cardio.dist)
    await callback.message.answer(f'Введите дистанцию:')

@activity_router.message(lambda message: check_dist(message.text), Cardio.dist)
async def is_competition(message: Message, state: FSMContext):
    await state.update_data(distance=message.text)
    await state.set_state(Cardio.is_competition)
    await message.answer(f'Участие в рамках кардио соревнований?', reply_markup=is_competition_kb())

@activity_router.message(lambda message: not check_dist(message.text), Cardio.dist)
async def wrong_dist(message: Message):
    await message.answer(f'Дистанция должна быть положительным действительным числом\nПопробуйте еще раз:')

@activity_router.callback_query(Cardio.is_competition, F.data.in_(["yes_competition", "no_competition"]))
async def pay_debt(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    kb = is_competition_kb().inline_keyboard
    for i in range(0, len(kb)):
        for j in range(0, len(kb[i])):
            if callback.data == kb[i][j].callback_data:
                await state.update_data(is_competition=kb[i][j].text)
    await state.set_state(Cardio.pay_debt)
    description = ("Не списывать имеющийся долг, накопить баллы?\n"
                   "Пользуйтесь с умом: в течение всего периода предлагерной подготовки допускается всего 8 пропусков\n"
                   "Когда может быть полезно: у тебя 7/8 долгов, ты проходишь по требованиям, но находишься низко в рейтинге, поэтому хочешь накопить баллы, а не закрывать долги")
    await callback.message.answer(f'{description}', reply_markup=pay_debt_kb())


@activity_router.callback_query(Cardio.pay_debt, F.data.in_(["yes_pay_debt", "no_pay_debt"]))
async def end_activity_survey(callback: CallbackQuery, state: FSMContext):
    await callback.answer('')
    kb = pay_debt_kb().inline_keyboard
    for i in range(0, len(kb)):
        for j in range(0, len(kb[i])):
            if callback.data == kb[i][j].callback_data:
                await state.update_data(pay_debt=kb[i][j].text)
    data = await state.get_data()
    ans = ('Введенные данные:\n'
           f'тип {data["cardio_type"]}\n'
           f'дистанция {data["distance"]}\n' 
           f'соревнование? {data["is_competition"]}\n'
           f'списать? {data["pay_debt"]}')
    await callback.message.answer(ans)
    await state.clear()
