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
    global turn
    turn = 1
    context.bot.send_message(update.effective_chat.id, "Начало новой игры в крестики-нолики!")
    context.bot.send_message(update.effective_chat.id, "На игровом поле 3 строки и 3 столбца")
    for cell in area:
        context.bot.send_message(update.effective_chat.id, cell)
    context.bot.send_message(update.effective_chat.id, "Первые ходят крестики")
    context.bot.send_message(update.effective_chat.id, "По очереди вводите свои ходы в формате *номер строки*,*номер колонны*")


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
    global turn
    global area
    if turn > 9:
        context.bot.send_message(update.effective_chat.id,"Игра окончена")
    else:
        context.bot.send_message(update.effective_chat.id,f"Ход: {turn}")
        if turn % 2 == 0:
            turn_char = "0"
        else:
            turn_char = "X"
        text = update.message.text
        text = text.split(',')
        row = int(text[0]) - 1
        column = int(text[1]) - 1
        if area[row][column] == "*":
            area[row][column] = turn_char
        else:
            context.bot.send_message(update.effective_chat.id,"Ячейка уже занята, вы пропускаете ход")
        if turn == 9:
            context.bot.send_message(update.effective_chat.id,'Ничья!')
       
        for cell in area:
            context.bot.send_message(update.effective_chat.id, cell)
        
        if check_winner(area) and turn % 2 == 1: 
            context.bot.send_message(update.effective_chat.id,"Победа крестиков!")
            
        if check_winner(area) and turn % 2 == 0: 
            context.bot.send_message(update.effective_chat.id,"Победа ноликов!")
        turn += 1    
    



start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', info)
message_handler = MessageHandler(Filters.text, message)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(message_handler)

print('server started')
updater.start_polling()
updater.idle()
