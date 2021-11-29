import telegram.ext
import random

updater=telegram.ext.Updater("2118314851:AAFMhCUDQms42EEHnuAl29jjQlaPhHTLnxs",use_context=True)
a=telegram.Bot("2118314851:AAFMhCUDQms42EEHnuAl29jjQlaPhHTLnxs")
theNumber="0"
messageId=0
guesses=[]

def g_num():
    nums=[i for i in range(1,10)]
    i=random.choice(nums)
    j=random.choice(nums)
    k=random.choice(nums)
    l=random.choice(nums)
    if i==j or i==k or i==l or j==k or j==l or k==l:
        return g_num()
    else:
        return str(i)+str(j)+str(k)+str(l)

    
def eval(update,context,guessNumber):
    global guesses
    i,j,k,l=guessNumber
    a,b,c,d=theNumber
    number=0
    position=0
    if i in theNumber:
        number+=1
    if j in theNumber:
        number+=1
    if k in theNumber:
        number+=1
    if l in theNumber:
        number+=1
    if i == a:
        position+=1
    if j == b:
        position+=1
    if k == c:
        position+=1
    if l == d:
        position+=1
    if number==4 and position==4:
        update.message.reply_text("YOU WON!!!\nNumber={}\nPosition={}".format(number,position))
        update.message.reply_text("type /start_game to start another game")
    else:
        
        # i=update.message.reply_text(f"Guess:{guessNumber}\nNumber={number}\nPosition={position}")
        guesses.append([guessNumber,number,position])
        edit(update,context)
        deli(update,update.message.message_id)
        
    
    
def start_game(update,context) :
    global theNumber,messageId,guesses
    guesses=[]
    update.message.reply_text("the Game is Started:\nRules:\n\tEnter only 4 numbers(no space nedded)\n\tDo not repeat numbers")
    msg=update.message.reply_text("Score:\nGuess\t\tNumber\t\tPositio")
    messageId=msg.message_id
    
    theNumber=g_num()
       
def start(update,context):
    update.message.reply_text("welcome {}, to start a game type /start_game".format(update.message.chat.username))
    print(update.message.chat.username," is playing.")
    
    

def check_num(number):
    if len(number)>4 or len(number)<4:
        return False
    q,w,e,r=number
    if len(set([q,w,e,r]))<4:
        return False 
    return True

def deli(update,iid):
    global a
    a.delete_message(update.message.chat.id, iid)

def edit(update,context):
    global guesses
    
    # context.bot.editMessageText(chat_id=update.message.chat_id,
    #                             message_id=update.message.message_id,text="edited")
    te="Score:\nGuess\t\tNumber\t\tPosition\n"
    for guess,num,pos in guesses:
        te+=str(guess)+"             "+str(num)+"             "+str(pos)+"\n"
    context.bot.edit_message_text(chat_id=update.message.chat_id,message_id=messageId,text=te)
 
def messageHandler(update,context) :
    number=update.message.text
    if check_num(number):
        eval(update,context,number)
    else:
        update.message.reply_text("your input '{}' is incorrect!!! Try again".format(number))
        
def help(update,context):
    update.message.reply_text("This is the help menu\n the goal of the game  is to guess the 4 digit number the computer holds.\n each time you guess a number it will tell you how many numbers you got correct and how many of them are in the right position.\n for ex:    \n if your guess is 1234 and you get number=3 & position=2, this means you git three numbers right and 2 of them are in the right position")  
 
 
disp=updater.dispatcher

disp.add_handler(telegram.ext.CommandHandler('help',help))
disp.add_handler(telegram.ext.CommandHandler("start",start))
disp.add_handler(telegram.ext.CommandHandler("start_game",start_game))

disp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text,messageHandler))

updater.start_polling()
updater.idle()
