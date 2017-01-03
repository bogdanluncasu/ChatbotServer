# Hatter command line version, This doesn't require Flask
from aiml import Kernel
from os import listdir
import sys, processing
from flask import Flask, request
from flask.ext.socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'THISISTHESECRETKEY'
socketio = SocketIO(app)

def set_personality(bot):
    bot.setBotPredicate("name", "PCH")
    bot.setBotPredicate("gender", "robot")
    bot.setBotPredicate("master", "B2Group")
    bot.setBotPredicate("birthday", "21.12.2016")
    bot.setBotPredicate("birthplace", "Iasi")
    bot.setBotPredicate("boyfriend", "you")
    bot.setBotPredicate("favoritebook", "Dont't read me")
    bot.setBotPredicate("favoritecolor", "transparent")
    bot.setBotPredicate("favoriteband", "B.U.G Mafia")
    bot.setBotPredicate("favoritesong", "your voice")
    bot.setBotPredicate("forfun", "talktoyou")
    bot.setBotPredicate("friends", "you")
    bot.setBotPredicate("girlfriend", "you")
    bot.setBotPredicate("language", "english")
    bot.setBotPredicate("email", "pch@bot.romania")


files = listdir('standard')
bot = substs = None
bots=[]

@app.route('/')
def welcome():
    return "Welcome",200

@socketio.on('init')
def init(message):
    global bot,substs,respon
    bot = Kernel()
    for file in files:
        bot.learn('standard/' + file)

    if len(bots)==0:
        bots.append(bot)
    else:
        assigned=false
        for i in range(len(bots)):
            if bots[i] is None:
                bots[i]=bot
                assigned=true
                break
        if not assigned:
            bots.append(bot)

    set_personality(bot)
    substs = processing.get_substitutions()
    respon = ' '
    emit("reply",{"data":"Bot> Hello , I am PCH the bot. Good to see you. Type \"bye\" to exit","index":bots.index(bot)})

@socketio.on('ask')
def asking(message):
    reply = ask_him(message['data'],message['index'])
    emit('reply', {"data":reply})


@socketio.on('disconnect')
def disconnect(message={}):
    if("index" in message):
        if message["index"]!=-1:
            bots[message["index"]]=None;
    print('Client disconnected')


def ask_him(data,index):
    question = data
    question = processing.apply_substitutions(question, substs)
    reply = bots[index].respond(question)
    return "Bot> "+reply

if __name__ == '__main__':
    print "Holla"
    try:
        socketio.run(app)
    except:
        pass