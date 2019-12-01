from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks

import threading, requests, time, random, re,json
from config import *
import importlib
from utlis.tg import Bot
from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from utlis.send import Name

def delete(client, message,redis):
  #print(message)
  type = message.chat.type
  userID = message.from_user.id
  userFN = message.from_user.first_name
  chatID = message.chat.id
  rank = isrank(redis,userID,chatID)
  if message.text :
    text = message.text
  elif message.caption:
    text = message.caption
  else:
    text = 0
  if redis.sismember("{}Nbot:lang:ar".format(BOT_ID),chatID):
    lang = "ar"
  elif redis.sismember("{}Nbot:lang:en".format(BOT_ID),chatID):
    lang = "en"
  else :
    lang = "ar"
  moduleCMD = "lang."+lang+"-cmd"
  moduleREPLY = "lang."+lang+"-reply"
  c = importlib.import_module(moduleCMD)
  r = importlib.import_module(moduleREPLY)
  if redis.sismember("{}Nbot:restricteds".format(BOT_ID),userID):
    Bot("restrictChatMember",{"chat_id": chatID,"user_id": userID,"can_send_messages": 0,"can_send_media_messages": 0,"can_send_other_messages": 0,"can_send_polls": 0,"can_change_info": 0,"can_add_web_page_previews": 0,"can_pin_messages": 0,})
  if redis.sismember("{}Nbot:bans".format(BOT_ID),userID):
    Bot("kickChatMember",{"chat_id":chatID,"user_id":userID})

  if text :
    if text == c.kickme and not redis.sismember("{}Nbot:kickme".format(BOT_ID),chatID):
      GetGprank = GPranks(userID,chatID)
      if GetGprank == "member":
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.yes,callback_data=json.dumps(["kickme-yes","",userID])),InlineKeyboardButton(r.no,callback_data=json.dumps(["kickme-no","",userID])),]])
        Bot("sendMessage",{"chat_id":chatID,"text":r.kickme,"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":reply_markup})

      
    #if re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text):
    if re.findall("[Hh][Tt][Tt][Pp][Ss]:/|[Hh][Tt][Tt][Pp]://|.[Ii][Rr]|.[Cc][Oo][Mm]|.[Oo][Rr][Gg]|.[Ii][Nn][Ff][Oo]|[Ww][Ww][Ww]|.[Tt][Kk]|.[Mm][Ee]", text):
      if redis.sismember("{}Nbot:Llink".format(BOT_ID),chatID): #1
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

    if re.findall('@', text):
      if redis.sismember("{}Nbot:Lusername".format(BOT_ID),chatID):#2
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

    if re.findall('#', text):
      if redis.sismember("{}Nbot:Ltag".format(BOT_ID),chatID):#3
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

    if re.findall("[a-zA-Z0-9$@$!%*?&#^-_. +]+", text):
      if redis.sismember("{}Nbot:Lenglish".format(BOT_ID),chatID):#4
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
  
    if re.findall("[ا-ي٠-٩]", text):
      if redis.sismember("{}Nbot:Larabic".format(BOT_ID),chatID):#5
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
    if re.findall('@', text):
      if redis.sismember("{}Nbot:Lusername".format(BOT_ID),chatID):#2
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
    Nlongtext = (redis.get("{}Nbot:Nlongtext".format(BOT_ID)) or 250)
    if len(text) >= Nlongtext:
      if redis.sismember("{}Nbot:Llongtext".format(BOT_ID),chatID):#2
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
    li = redis.smembers("{}Nbot:{}:blockTEXTs".format(BOT_ID,chatID))
    for word in li:
      if re.findall(word, text):
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
        break
        
# text ^


  if message.entities :
    if redis.sismember("{}Nbot:Lmarkdown".format(BOT_ID),chatID):#6
      for entitie in message.entities:
        if entitie.type is "text_link":
          Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
          break

  if message.via_bot:
    if redis.sismember("{}Nbot:Linline".format(BOT_ID),chatID):#7
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if message.reply_markup:
    if redis.sismember("{}Nbot:Linline".format(BOT_ID),chatID):
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if message.sticker:
    if redis.sismember("{}Nbot:Lsticker".format(BOT_ID),chatID):#8
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
    elif redis.sismember("{}Nbot:{}:blockSTICKERs".format(BOT_ID,chatID),message.sticker.file_id):
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if message.animation:
    if redis.sismember("{}Nbot:Lgifs".format(BOT_ID),chatID):#9
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
    elif redis.sismember("{}Nbot:{}:blockanimations".format(BOT_ID,chatID),message.animation.file_id):
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if message.audio:
    if redis.sismember("{}Nbot:Lmusic".format(BOT_ID),chatID):#10
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if message.voice:
    if redis.sismember("{}Nbot:Lvoice".format(BOT_ID),chatID):#11
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if message.video:
    if redis.sismember("{}Nbot:Lvideo".format(BOT_ID),chatID):#12
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if message.video:
    if redis.sismember("{}Nbot:Lfiles".format(BOT_ID),chatID):#13
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if message.photo:
    if redis.sismember("{}Nbot:Lphoto".format(BOT_ID),chatID):#14
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
    elif redis.sismember("{}Nbot:{}:blockphotos".format(BOT_ID,chatID),message.photo.file_id):
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if message.contact:
    if redis.sismember("{}Nbot:Lcontact".format(BOT_ID),chatID):#15
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if message.new_chat_members:
    if message.new_chat_members[0].is_bot:
      if redis.sismember("{}Nbot:Lbots".format(BOT_ID),chatID):#16
        first_name = message.new_chat_members[0].first_name
        username = message.new_chat_members[0].username
        Bot("kickChatMember",{"chat_id":chatID,"user_id":message.new_chat_members[0].id})
        Bot("sendMessage",{"chat_id":chatID,"text":r.kickbotadd.format(username,first_name),"reply_to_message_id":message.message_id,"parse_mode":"html"})
    if redis.sismember("{}Nbot:Ljoin".format(BOT_ID),chatID):#17
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if message.forward_from:
    if redis.sismember("{}Nbot:Lfwd".format(BOT_ID),chatID):#18
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if message.video_note:
    if redis.sismember("{}Nbot:Lnote".format(BOT_ID),chatID):#19
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})

  if redis.sismember("{}Nbot:Lflood".format(BOT_ID),chatID) :#20
    Max_msg = int((redis.hget("{}Nbot:max_msg".format(BOT_ID),chatID) or 10))
    Time_ck = int((redis.hget("{}Nbot:time_ck".format(BOT_ID),chatID) or 3))
    User_msg = int((redis.get("{}Nbot:{}:{}:flood".format(BOT_ID,chatID,userID)) or 1))
    if User_msg > Max_msg:
      GetGprank = GPranks(userID,chatID)
      if GetGprank == "member":
        Bot("restrictChatMember",{"chat_id": chatID,"user_id": userID,"can_send_messages": 0,"can_send_media_messages": 0,"can_send_other_messages": 0,"can_send_polls": 0,"can_change_info": 0,"can_add_web_page_previews": 0,"can_pin_messages": 0,})
        redis.sadd("{}Nbot:{}:restricteds".format(BOT_ID,chatID),userID)
        BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,Name(userFN))
        Bot("sendMessage",{"chat_id":chatID,"text":r.TKflood.format(BY,Max_msg,Time_ck),"parse_mode":"html"})
    redis.setex("{}Nbot:{}:{}:flood".format(BOT_ID,chatID,userID), Time_ck, User_msg+1)