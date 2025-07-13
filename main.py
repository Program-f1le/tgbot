from aiogram import *
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from comands import *
from datetime import *
from asyncio import *
from data_name import tg_token
from sqlalchemy import text
from database import engine


bot = Bot(token=tg_token)
dp = Dispatcher()
ans = []

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.first_name}, команды бота /help')
    await timer_(message)

@dp.message(Command('help'))
async def start(message: Message):
    await message.answer('Команды бота: '
                          '\n/start - начать\n'
                          '/today - расписание событий на сегодня\n'
                          '/tomorrow - расписание событий на завтра\n'
                          '/week - расписание событий на неделю\n'
                          '/add - добавить событие\n'
                          '/schedule - инструкция, как добавить событие\n'
                          '/help - команды бота')

@dp.message(Command('schedule'))
async def schedule(message: Message):
    await message.answer('Чтобы добавить событие введите:\n/add Событие год-месяц-день часы:минуты')

@dp.message(Command('add'))
async def add(message):
    if len(str(message.text)) < 16:
        await message.answer(
                         f'Дата введена неправильно, чтобы добавить событие введите:\n/add Событие год-месяц-день часы:минуты')
        await message.answer(f'Пример /add Лекция 2025-12-12 15:30')
    else:
        event, time, t = str(message.text)[5::].split(' ')
        time += ' ' + t
        if check_data(time) == False:
            await message.answer(f'Дата введена не правильно, чтобы добавить событие введите /add Событие год-месяц-день часы:минуты')
            await message.answer(f'Пример /add Лекция 2025-12-12 15:30')
        elif insert_data(time, event, message.from_user.id) == False:
            await message.answer(f'Дата {time} уже прошла')
        else:
            await message.answer(f'Добавлено {event} на {time}')


@dp.message(Command('today'))
async def today(message):
    if today_all(int(datetime.now().day)) == '' and today_user(int(datetime.now().day), message.from_user.id) == '':
        await message.answer(f'На сегодня нет задач!')
    else:
        a = '\n'.join([today_all(int(datetime.now().day)), today_user(int(datetime.now().day), message.from_user.id)])
        await message.answer(f'Сегодня:\n{a}')




@dp.message(Command('tomorrow'))
async def tomorrow(message):
    if today_all(int(datetime.now().day) + 1) == '' and today_user(int(datetime.now().day) + 1, message.from_user.id) == '':
        await message.answer(f'На Завтра нет событий!')
    else:
        a = '\n'.join([today_all(int(datetime.now().day) + 1), today_user(int(datetime.now().day) + 1, message.from_user.id)])
        await message.answer(f'Завтра:\n{a}')


@dp.message(Command('week'))
async def week(message):
    res = []
    day = date.today()
    a = int(datetime.now().day)
    i = 0
    while i != 7:
        if today_all(a) == '' and today_user(a, message.from_user.id) == '':
            break
        b = str(today_all(a)) + ', ' + str(today_user(a, message.from_user.id))
        res.append(f'{day}: {b}')
        day = day + timedelta(days=1)
        a += 1
        i += 1
    if res == []:
        await message.answer(f'На эту неделю нет событий!')
    else:
        await message.answer(f'События на неделю:\n{'\n'.join(res)}.')

async def timer_(message):
    print(1)
    user = message.from_user.id
    day = datetime.now().day
    year = datetime.now().year
    month = datetime.now().month
    global ans
    with engine.connect() as conn:
        a = conn.execute(text(f'''select id from {table_name} where day='{day}' and year= '{year}' and month= '{month}' and for_who= '{user}';''')).all()
        a += conn.execute(text(f'''select id from {table_name} where day='{day}' and year= '{year}' and month= '{month}' and for_who= 'all';''')).all()
        for j in a:
            j = str(j)
            b = ''
            for i in range(1, len(j)):
                if j[i] == ',':
                    break
                else:
                    b += str(j[i])
            b = int(b)
            if b in ans:
                ...
            else:
                t = str(conn.execute(text(f'''select time from {table_name} where id='{b}';''')).first())
                event = str(conn.execute(text(f'''select event from {table_name} where id='{b}';''')).first())
                u = ''
                for i in range(2, len(t)):
                    if t[i] == "'":
                        break
                    else:
                        u += str(t[i])
                t = u
                u = ''
                for i in range(2, len(event)):
                    if event[i] == "'":
                        break
                    else:
                        u += str(event[i])
                event = u
                if len(t) == 4:
                    h = int(t[0])
                else:
                    h = int(t[:2])
                if datetime(year, month, day, h, int(t[3::])) - datetime.now() <= timedelta(minutes=60):
                    e = str(datetime(year, month, day, h, int(t[3::])) - datetime.now()).split(':')[1]
                    await message.answer(f'ВНИМАНИЕ! До события {event} {e} мин!')
                    ans.append(b)

    await sleep(60)
    await timer_(message)

async def main():
    await dp.start_polling(bot)

run(main())
