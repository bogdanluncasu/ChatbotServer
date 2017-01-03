from aiml import Kernel
from os import listdir
import sys, processing
from flask import Flask, request
from geventwebsocket import WebSocketServer, WebSocketApplication, Resource
from collections import OrderedDict

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

def ask_him(data,index,bot,substs):
    question = data
    question = processing.apply_substitutions(question, substs)
    reply = bot.respond(question)
    return "Bot> "+reply

class EchoApplication(WebSocketApplication):

    def on_open(self):
        print "Connection opened"

        self.bot = Kernel()
        for file in files:
            self.bot.learn('standard/' + file)

        set_personality(self.bot)
        self.substs = processing.get_substitutions()
        self.respon = ' '
        self.ws.send( "Bot> Hello , I am PCH the bot. Good to see you. Type \"bye\" to exit")

    def on_message(self, message):
        if self.bot is None or self.substs is None or message is None:
            return "Hello"
        reply = ask_him(message, 0,self.bot,self.substs)
        self.ws.send(reply)

    def on_close(self, reason):
        print reason
        self.ws.send("Bye")

WebSocketServer(
    ('', 8000),
    Resource(OrderedDict({'/': EchoApplication}))
).serve_forever()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'THISISTHESECRETKEY'





@app.route('/')
def welcome():
    return "Welcome",200



if __name__ == '__main__':
    try:
        app.run()
    except:
        pass