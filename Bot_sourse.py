from cgitb import text
from sunau import Au_read
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler


bot = Bot(token="5578165526:AAFAePrUyZ1bgy5gH0KqdJHIaDjZzc4MDzg")
updater = Updater(token='5578165526:AAFAePrUyZ1bgy5gH0KqdJHIaDjZzc4MDzg')
dispatcher = updater.dispatcher



def start(update, context):
    global area
    area = [["*", "*", "*"], ["*", "*", "*"], ["*", "*", "*"]]
    context.bot.send_message(update.effective_chat.id, "Начало новой игры в крестики-нолики!")


def info(update, context):
    context.bot.send_message(update.effective_chat.id, "Игра в крестики-нолики")

def check_winner(field):
    for i in field:
        if i == ['X','X','X'] or i == ['0','0','0']:
            return True
    if (field[0][0] == field[1][1] == field[2][2] or field[0][2] == field[1][1] == field[2][0]) and not field[1][1] == '*':
        return True
    for e in range(3):
        if(field[0][e] == field[1][e] == field[2][e]) and not field[0][e] == '*':
            return True
    return False            

def message(update, context):
    global area
    for turn in range(1, 10):
        context.bot.send_message(update.effective_chat.id,f"Ход: {turn}")
        if turn % 2 == 0:
            turn_char = "0"
            context.bot.send_message(update.effective_chat.id,'Ходят нолики')
        else:
            turn_char = "X"
            context.bot.send_message(update.effective_chat.id,'Ходят крестики')
        context.bot.send_message(update.effective_chat.id, 'Введите номер строки(0,1 или 2):')
        text = update.message.text
        row = int(text)
        context.bot.send_message(update.effective_chat.id, 'Введите номер столбца(0,1 или 2):')
        text = update.message.text
        column = int(text)
        if area[row][column] == "*":
            area[row][column] = turn_char
        else:
            context.bot.send_message(update.effective_chat.id,"Ячейка уже занята, вы пропускаете ход")
        if turn == 9:
            context.bot.send_message(update.effective_chat.id,'Ничья!')
            continue
        for cell in area:
            context.bot.send_message(update.effective_chat.id, cell)
        
        if check_winner(area) and turn % 2 == 1: 
            context.bot.send_message(update.effective_chat.id,"Победа крестиков!")
            break
        if check_winner(area) and turn % 2 == 0: 
            context.bot.send_message(update.effective_chat.id,"Победа ноликов!")
            break



start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', info)
message_handler = MessageHandler(Filters.text, message)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(message_handler)

print('server started')
updater.start_polling()
updater.idle()
