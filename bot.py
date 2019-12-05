from pyrogram import Client, MessageHandler, Filters

from utlis.rank import setrank ,isrank ,remrank ,setsudos ,remsudos ,setsudo
from handlers.callback import updateCallback
from handlers.msg import updateHandlers
from handlers.delete import delete
from utlis.tg import Bot,Del24
from handlers.edit import edit
from handlers.nf import nf
from config import *

import threading, requests, time, random
import redis
import sched, time

R = redis.Redis(charset="utf-8", decode_responses=True)

#app = Client("NB"+BOT_ID,bot_token=TOKEN,api_id = API_ID, api_hash = API_HASH)
session_string = open("session.txt").read()
app = Client(session_string,api_id = API_ID, api_hash = API_HASH)
setsudo(R,SUDO)
R.set("{}Nbot:BOTrank".format(BOT_ID), BOT_ID)

t = threading.Thread(target=Del24,args=("client", "message",R))
t.setDaemon(True)
t.start()

@app.on_message(~Filters.edited & ~Filters.new_chat_title & ~Filters.pinned_message & ~Filters.left_chat_member & ~Filters.new_chat_photo & ~Filters.new_chat_members & ~Filters.delete_chat_photo & ~Filters.channel)
def update(client, message):
    t = threading.Thread(target=updateHandlers,args=(client, message,R))
    t.setDaemon(True)
    t.start()
@app.on_callback_query()
def callback(client, callback_query ):
    t = threading.Thread(target=updateCallback,args=(client, callback_query,R))
    t.setDaemon(True)
    t.start()
@app.on_message(Filters.edited & ~Filters.channel)
def updateEdit(client, message):
    t = threading.Thread(target=edit,args=(client, message,R))
    t.setDaemon(True)
    t.start()
@app.on_message(Filters.new_chat_title | Filters.pinned_message | Filters.left_chat_member | Filters.new_chat_photo | Filters.new_chat_members | Filters.delete_chat_photo & ~Filters.channel)
def updateEdit(client, message):
    t = threading.Thread(target=nf,args=(client, message,R))
    t.setDaemon(True)
    t.start()

app.run()
