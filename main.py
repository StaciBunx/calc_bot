from config import TOKEN
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler
from operations import *

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
    fallbacks=[MessageHandler('Выход', cancel)])


app.add_handler(conversation_handler)

print('server start')
app.run_polling()
