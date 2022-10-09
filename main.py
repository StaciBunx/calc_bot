import logging
from config import TOKEN
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (ApplicationBuilder, CommandHandler, MessageHandler,
                          filters,
                          ConversationHandler
                          )


logging.basicConfig(filename='log.txt',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO
                    )
logger = logging.getLogger(__name__)


GET_NUM, RATIONAL_1, RATIONAL_2, COMPLEX_1, COMPLEX_2, RATIONAL_OPER, COMPLEX_OPER = range(
    7)


async def start(update, _):
    reply_keyboard = [['Рациональные', 'Комплексные', 'Выход']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        'Добро пожаловать в калькулятор рациональных и комплексных чисел. '
        'Выберите с какими числами выполнить вычисления. Или нажмите "Выход", чтобы закончить разговор. \n',
        reply_markup=markup_key)
    return GET_NUM


async def get_num(update, context):
    choice = update.message.text
    if choice == 'Рациональные':
        await update.message.reply_text('Введите первое рациональное число (через точку):', reply_markup=ReplyKeyboardRemove())
        return RATIONAL_1
    elif choice == 'Комплексные':
        await update.message.reply_text('Введите действительную и мнимую часть числа (через пробел): ', reply_markup=ReplyKeyboardRemove())
        return COMPLEX_1
    else:
        return cancel(update, context)


async def rational_1(update, context):
    rational_first = update.message.text
    if rational_first == str(float(rational_first)):
        rational_first = float(rational_first)
        context.user_data['rational_first'] = rational_first
        await update.message.reply_text('Введите второе рациональное число (через точку): ')
        return RATIONAL_2
    else:
        await update.message.reply_text('Неправильный ввод! Попробуйте еще раз: ')
        return RATIONAL_1


async def rational_2(update, context):
    rational_second = update.message.text
    if rational_second == str(float(rational_second)):
        rational_second = float(rational_second)
        context.user_data['rational_second'] = rational_second
        reply_keyboard = [['+', '-', 'х', '/']]
        markup_key = ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text('Нажмите, какая будет операция.', reply_markup=markup_key)
        return RATIONAL_OPER
    else:
        await update.message.reply_text('Неправильный ввод! Попробуйте еще раз: ')
        return RATIONAL_2


async def rational_oper(update, context):
    rational_first = context.user_data.get('rational_first')
    rational_second = context.user_data.get('rational_second')
    choice = update.message.text
    if choice == '+':
        result = rational_first + rational_second
    if choice == '-':
        result = rational_first - rational_second
    if choice == 'х':
        result = rational_first * rational_second
    if choice == '/':
        try:
            result = rational_first / rational_second
        except:
            await update.message.reply_text('Делить на ноль нельзя.')
            await update.message.reply_text('Нажмите /start для запуска Калькулятора.')
            return ConversationHandler.END
    await update.message.reply_text(
        f'Результат: {rational_first} {choice} {rational_second} = {result} \n'
        'Если хотите еще что-то посчитать, нажмите /start')
    return ConversationHandler.END


async def complex_1(update, context):
    complex_num = update.message.text
    complex_num = complex_num.split(' ')
    complex_first = complex(int(complex_num[0]), int(complex_num[1]))
    context.user_data['complex_first'] = complex_first
    await update.message.reply_text('Введите действительную и мнимую часть второго числа (через пробел):')
    return COMPLEX_2


async def complex_2(update, context):
    complex_num = update.message.text
    complex_num = complex_num.split(' ')
    complex_second = complex(int(complex_num[0]), int(complex_num[1]))
    context.user_data['complex_second'] = complex_second
    reply_keyboard = [['+', '-', 'х', '/']]
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text('Нажмите, какая будет операция.', reply_markup=markup_key)
    return COMPLEX_OPER


async def complex_oper(update, context):
    complex_first = context.user_data.get('complex_first')
    complex_second = context.user_data.get('complex_second')
    choice = update.message.text
    if choice == '+':
        result = complex_first + complex_second
    if choice == '-':
        result = complex_first - complex_second
    if choice == 'х':
        result = complex_first * complex_second
    if choice == '/':
        try:
            result = complex_first / complex_second
        except:
            await update.message.reply_text('Делить на 0 нельзя.')
            await update.message.reply_text('Нажмите /start для запуска Калькулятора.')
            return ConversationHandler.END
    await update.message.reply_text(
        f'Результат: {complex_first} {choice} {complex_second} = {result} \n'
        'Если хотите еще что-то посчитать, нажмите /start')
    return ConversationHandler.END


async def cancel(update, context):
    await update.message.reply_text('Хорошо, пока!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


app = ApplicationBuilder().token(TOKEN).build()

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        GET_NUM: [MessageHandler(filters.ALL, get_num)],
        RATIONAL_1: [MessageHandler(filters.ALL, rational_1)],
        RATIONAL_2: [MessageHandler(filters.ALL, rational_2)],
        RATIONAL_OPER: [MessageHandler(filters.ALL, rational_oper)],
        COMPLEX_1: [MessageHandler(filters.ALL, complex_1)],
        COMPLEX_2: [MessageHandler(filters.ALL, complex_2)],
        COMPLEX_OPER: [MessageHandler(filters.ALL, complex_oper)],
    },
    fallbacks=[CommandHandler('cancel', cancel)])


app.add_handler(conversation_handler)

print('server start')
app.run_polling()
