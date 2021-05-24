import requests
import re
import datetime
from bs4 import BeautifulSoup
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '1862096252:AAH-otPTeBwSYugh-x0neqX05IJx8xN3EJA'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# По некоторой причине, страница с расписанием 104 группы выдает с моей стороны Runtime Error
# поэтому id 104 группы (275357) заменен на id 101 группы (276415)

def pars(date):
    url = f'https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/276415/{date}'
    req = requests.get(url)
    src = req.text
    return(src)

# Кнопки
btnToday = KeyboardButton("/today")
btnTomorrow = KeyboardButton("/tomorrow")
start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(btnToday, btnTomorrow)


# Стартовое сообщение
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Hello, please, type the date for which you want to know the schedule', reply_markup=start_kb)


# Расписание на сегодня
@dp.message_handler(commands=['today'])
async def type_schedule(message: types.Message):
    try:
        src = pars(datetime.date.today())
        soup = BeautifulSoup(src, 'lxml')
        today = datetime.date.today().strftime("%A")  # Берем из даты день недели
        day = soup.find(string=re.compile(today))  # Находим его на странице
        list = []  # Список для вывода информации в Телеграм
        list.append(day.strip().capitalize())
        smt = day.find_next(class_='panel-collapse nopadding nomargin')  # Находим блок с расписанием
        sib = day.find_next(class_='common-list-item row')
        for k in smt:
            if sib.find(title='The date/time were changed') is not None:
                Time = sib.find(title='The date/time were changed').text.strip()
            elif sib.find(title='The event was cancelled') is not None:
                sib = sib.find_next_sibling()
                continue
            else:
                Time = sib.find(title='Time').text.strip()
            list.append(Time)
            Subject = sib.find_next(title='Subject').text.strip()
            list.append(Subject)
            Locations = sib.find_next(title='Locations').text.strip()
            list.append(Locations)
            Teachers = sib.find_next(title='Teachers').text.strip()
            list.append(Teachers)
            sib = sib.find_next_sibling()
            if sib is None:
                break
        list_str = '\n'.join(list)  # Вывод
        await message.reply(list_str)
    except:
        await message.reply(f'There are no classes on {today}')


@dp.message_handler(commands=['tomorrow'])
async def type_schedule(message: types.Message):
    try:
        src = pars(datetime.date.today() + datetime.timedelta(days=1))
        soup = BeautifulSoup(src, 'lxml')
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%A")
        day = soup.find(string=re.compile(tomorrow))
        list = []
        list.append(day.strip().capitalize())
        smt = day.find_next(class_='panel-collapse nopadding nomargin')
        sib = day.find_next(class_='common-list-item row')
        for k in smt:
            if sib.find(title='The date/time were changed') is not None:
                Time = sib.find(title='The date/time were changed').text.strip()
            elif sib.find(title='The event was cancelled') is not None:
                sib = sib.find_next_sibling()
                continue
            else:
                Time = sib.find(title='Time').text.strip()
            list.append(Time)
            Subject = sib.find_next(title='Subject').text.strip()
            list.append(Subject)
            Locations = sib.find_next(title='Locations').text.strip()
            list.append(Locations)
            Teachers = sib.find_next(title='Teachers').text.strip()
            list.append(Teachers)
            sib = sib.find_next_sibling()
            if sib is None:
                break
        list_str = '\n'.join(list)
        await message.reply(list_str)
    except:
        await message.reply(f'There are no classes on {tomorrow}')


@dp.message_handler()
async def type_schedule(message: types.Message):
    try:
        src = pars(datetime.datetime.strptime(message.text, '%d.%m.%Y').strftime('%Y-%m-%d'))
        soup = BeautifulSoup(src, 'lxml')
        exday = datetime.datetime.strptime(message.text, '%d.%m.%Y').strftime("%A")
        day = soup.find(string=re.compile(exday))
        list = []
        list.append(day.strip().capitalize())
        smt = day.find_next(class_='panel-collapse nopadding nomargin')
        sib = day.find_next(class_='common-list-item row')
        for k in smt:
            if sib.find(title='The date/time were changed') is not None:
                Time = sib.find(title='The date/time were changed').text.strip()
            elif sib.find(title='The event was cancelled') is not None:
                sib = sib.find_next_sibling()
                continue
            else:
                Time = sib.find(title='Time').text.strip()
            list.append(Time)
            Subject = sib.find(title='Subject').text.strip()
            list.append(Subject)
            Locations = sib.find(title='Locations').text.strip()
            list.append(Locations)
            Teachers = sib.find(title='Teachers').text.strip()
            list.append(Teachers)
            sib = sib.find_next_sibling()
            if sib is None:
                break
        list_str = '\n'.join(list)
        await message.reply(list_str)
    except:
        await message.reply(f'There are no classes on {exday}')


if __name__ == '__main__':
    executor.start_polling(dp)
