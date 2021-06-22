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
group_number = {
    101: '276415',
    102: '276277',
    103: '275298',
    104: '275357'
}

def to_print(day):
    list = []  # Список для вывода информации в Телеграм
    list.append(day.strip().capitalize())
    smt = day.find_next(class_='panel-collapse nopadding nomargin')  # Находим блок с расписанием
    sib = day.find_next(class_='common-list-item row')
    for k in smt:  # Добавление в список нужных блоков с временем, занятием, локацией и преподавателем
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
        if sib.find(title='One or more locations were changed') is not None:
            Locations = sib.find(title='One or more locations were changed').text.strip()
        else:
            Locations = sib.find(title='Locations').text.strip()
        list.append(Locations)
        Teachers = sib.find_next(title='Teachers').text.strip()
        list.append(Teachers)
        sib = sib.find_next_sibling()
        if sib is None:
            break
    list_str = '\n'.join(list)  # Вывод
    return list_str
# Кнопки
btnToday = KeyboardButton("Today")
btnTomorrow = KeyboardButton("Tomorrow")
start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(btnToday, btnTomorrow)


# Стартовое сообщение
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply(
        'Hello, type /help if you want to know the commands',
        reply_markup=start_kb)
@dp.message_handler(commands=['help'])
async def start(message: types.Message):
    await message.reply(
        'Type \'Setgroup(number)\' to set the group\n'
        'Type \'Today\' to know the schedule for today\n'
        'Type \'Tomorrow\' to know the schedule for tomorrow\n'
        'Type \'dd.mm.yyyy\' to know the schedule for this date'
    )

@dp.message_handler()
async def type_schedule(message: types.Message):
    global url
    if message.text == 'Today':
        try:
            k = url
            url += f'{datetime.date.today()}'
            req = requests.get(url)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            today = datetime.date.today().strftime("%A")
            day = soup.find(string=re.compile(today))
            await message.reply(to_print(day))
            url = k
        except:
            await message.reply(f'There are no classes on {today}')
    elif message.text == 'Tomorrow':
        try:
            k = url
            url += f'{datetime.date.today() + datetime.timedelta(days=1)}'
            req = requests.get(url)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%A")
            day = soup.find(string=re.compile(tomorrow))
            await message.reply(to_print(day))
            url = k
        except:
            await message.reply(f'There are no classes on {tomorrow}')
    elif message.text == 'Setgroup(101)':
        url = f'https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/{group_number[101]}/'
        await message.reply('The group has been set')
    elif message.text == 'Setgroup(102)':
        url = f'https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/{group_number[102]}/'
        await message.reply('The group has been set')
    elif message.text == 'Setgroup(103)':
        url = f'https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/{group_number[103]}/'
        await message.reply('The group has been set')
    elif message.text == 'Setgroup(104)':
        url = f'https://timetable.spbu.ru/AMCP/StudentGroupEvents/Primary/{group_number[104]}/'
        await message.reply('The group has been set')
    else:
        try:
            t = datetime.datetime.strptime(message.text, '%d.%m.%Y').strftime('%Y-%m-%d')
            k = url
            url += f'{t}'
            req = requests.get(url)
            src = req.text
            soup = BeautifulSoup(src, 'lxml')
            exday = datetime.datetime.strptime(message.text, '%d.%m.%Y').strftime("%A")
            day = soup.find(string=re.compile(exday))
            await message.reply(to_print(day))
            url = k
        except:
            await message.reply(f'There are no classes on {exday}')


if __name__ == '__main__':
    executor.start_polling(dp)
