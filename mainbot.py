#version 1.0.0

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telebot.util import antiflood
import time
from text import texts
from config import *
from DML import *
from DQL import *

bot = telebot.TeleBot(API_TOKEN)
score_limit = 20
lower_limit = 2
upper_limit = 5
spam_time = 5*60

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            print(f'{m.chat.first_name} [{str(m.chat.id)}]: {m.text}')
        elif m.content_type == 'photo':
            print(f'{m.chat.first_name} [{str(m.chat.id)}]: sent photo')
        else:
            print(f'{m.chat.first_name} [{str(m.chat.id)}]: send another content type: {m.content_type}')    
bot.set_update_listener(listener)   

def send_message(*args,**kwargs):
    try:
        return antiflood(bot.send_message,*args,**kwargs)
    except Exception as e:
        print(f"Error occured: {repr(e)}")
        
def edit_message_text(*args,**kwargs):
    try:
        return antiflood(bot.edit_message_text,*args,**kwargs)
    except Exception as e:
        print(f"Error occured: {repr(e)}")       
        
def user_exist(cid):
    if not user_in_database(cid):
        user_info = bot.get_chat(cid)
        insert_user_data(cid, user_info.first_name, user_info.username,time.time())    
    return True
        
def is_spam_user(cid,msg_time):
    if  check_is_spam(cid):
        last_time = user_in_database(cid).get('LAST_MSG_TIME')
        if time.time()-last_time > spam_time:
            set_is_spam(cid,False)
            return False
        return True
    if user_in_database(cid):
        last_time = user_in_database(cid).get('LAST_MSG_TIME')
        score = user_in_database(cid).get('SCORE')
        print(last_time,score)

        if (msg_time-last_time) <= lower_limit:
            score += 1
            update_user_data(cid,time.time(),score)
            if score >= score_limit:
                set_is_spam(cid,True)
                return True
            return False      
        elif (msg_time-last_time)>upper_limit:
            score = max (score-1 , 0)
            update_user_data(cid,time.time(),score)
            if score>score_limit:
                set_is_spam(cid,True)
                return True
            return False
    else: return False
    
def main_worker():
    while True:
        if spam_list():
            for user in spam_list():
                cid=user['CHAT_ID']
                last_time = user(cid).get('LAST_MSG_TIME')
                if time.time()-last_time > spam_time:
                    set_is_spam(cid,False)
        time.sleep(60)
    
def clean_word(string):
    if string:
        return (string.replace('*', '\\*')
                .replace('_', '\\_').replace('|', '\\|').replace('-', '\\-')
                .replace('.', '\\.').replace(')','\\)').replace('(','\\(')
                .replace('<','\\<').replace('>','\\>').replace('=','\\=')
                .replace(',','\\,').replace('!','\\!').replace('#','\\#'))

def send_question_n_options(cid,qid):
    question = get_question(qid)
    answer = get_options(qid)   
    markup = InlineKeyboardMarkup()
    for ans in answer:
        markup.add(InlineKeyboardButton(ans['OPTION_TEXT'],
                            callback_data = f"options_{str(qid)}_{str(ans['ID'])}"))
    if qid!=1:
        markup.add(InlineKeyboardButton(texts['back'], callback_data='back'))
    send_message(cid,f"♦️ *{clean_word(question['Q_TEXT'])}* ❓",
                     parse_mode="markdownv2", reply_markup=markup)       
    
@bot.callback_query_handler(func=lambda call:True)
def call_back_query(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    call_id = call.id
    mtime = call.message.date
    if not user_exist(cid) : return
    if is_spam_user(cid ,mtime): return
    if data == 'back':
        bot.answer_callback_query(call_id,"بازگشت به مرحله قبل ✅")
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)
        previous = bacK_to_previous(cid)
        if previous:
            qid = previous['QUESTION_ID']
            send_question_n_options(cid,qid)
            delete_last_UserAnswers(cid, previous["ID"])
            
    elif data.startswith('options'):
        bot.answer_callback_query(call_id,"انتخاب گزینه انجام شد✅")
        _,q,ans = data.split('_')
        ans_id = int(ans)
        qid = int(q)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f'{get_ans_data(ans_id)['OPTION_TEXT']} ✔', callback_data='nothing'))
        bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        insert_user_answers_data(cid,qid,ans_id)
        ans = get_ans_data(ans_id)
        if ans['IS_FINAL']:
            result = get_insurance_result(ans_id)
            if result:
                send_message(cid,f"✅*نتیجه:*\n *{clean_word(result['RES_TEXT'])}*",
                                        parse_mode="markdownv2")
                delete_UserAnswers_data(cid)
            else:
                bot.answer_callback_query(call_id,"⚠️نتیجه ای یافت نشد")
        else:
            next_qid = ans["NEXT_QUESTION_ID"]
            if next_qid:
                send_question_n_options(cid,next_qid)
            else:
                bot.answer_callback_query(call_id,"⚠️سوال بعدی یافت نشد")
        
    elif data == 'contact_consultant':
        bot.answer_callback_query(call_id,"درخواست ارتباط با مشاور✅")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('بازگشت⬅️',callback_data='support_menu'))
        edit_message_text (clean_word(texts['consultant_link']),cid,mid, parse_mode = "MarkdownV2",reply_markup=markup)
        
    elif data == 'support':
        bot.answer_callback_query(call_id,"درخواست پشتیبانی✅")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('بازگشت⬅️',callback_data='support_menu'))
        edit_message_text (f"{texts['support_link']}",cid,mid, parse_mode = "MarkdownV2",reply_markup=markup)

    elif data == 'support_menu':
        bot.answer_callback_query(call_id,"بازگشت به مرحله قبل ✅")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('ارسال قرارداد و دریافت مشاوره✍️',callback_data='contact_consultant'),
                   InlineKeyboardButton('پشتیبانی🧑‍💻', callback_data='support'))
        edit_message_text('پشتیبانی یا مشاوره؟',cid,mid,reply_markup =markup)
        
    elif data == 'nothing':
        bot.answer_callback_query(call_id, 'فاقد عملیات!')
        
    elif data == 'cancel':
        bot.answer_callback_query(call_id, 'لغو مشاوره')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    mtime = message.date
    if not user_exist(cid): return
    if is_spam_user(cid ,mtime): return
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(texts['calculate'],texts['help'])
    markup.add(texts['contact_us'],texts['About'])
    markup.add(texts['support'])
    send_message(cid,texts['welcome'],reply_markup=markup)   
    
@bot.message_handler(func=lambda m: m.text == texts['help'])
def show_help_text_handler(message):
    cid = message.chat.id
    mtime = message.date
    if not user_exist(cid): return
    if is_spam_user(cid ,mtime): return
    send_message(cid,texts['help_text'])
    
@bot.message_handler(func=lambda m: m.text == texts['calculate'])
def calculate_insurance_handler(message):
    cid = message.chat.id
    user_info = bot.get_chat(cid)
    username = user_info.username
    name = user_info.first_name
    mtime = message.date
    if not user_exist(cid): return
    if is_spam_user(cid ,mtime): return
    insert_user_data(cid,name,username,mtime)
    send_question_n_options(cid,1)       

@bot.message_handler(func=lambda m: m.text == texts['contact_us'])
def contact_us_handler(message):
    cid = message.chat.id
    mtime = message.date
    if not user_exist(cid): return
    if is_spam_user(cid ,mtime): return
    send_message(cid,f"*{clean_word(texts['contact_txt'])}*" , parse_mode="MarkdownV2")  
    
@bot.message_handler(func=lambda m: m.text == texts['support'])
def support_handler(message):
    cid = message.chat.id
    mtime = message.date
    if not user_exist(cid): return
    if is_spam_user(cid ,mtime): return
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('ارسال قرارداد و دریافت مشاوره✍️',callback_data='contact_consultant'),
                InlineKeyboardButton('پشتیبانی🧑‍💻', callback_data='support'))
    send_message(cid,'پشتیبانی یا مشاوره؟',reply_markup =markup)        
 
@bot.message_handler(func=lambda m: m.text == texts['About'])
def about_bot_handler(message):
    cid = message.chat.id
    mtime = message.date
    if not user_exist(cid): return
    if is_spam_user(cid ,mtime): return
    send_message(cid , f'*{clean_word(texts['about_txt'])}*',parse_mode = "markdownv2")                      
               
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text:
        bot.reply_to(message, message.text)
    else:
        bot.reply_to(message, "پیام بدون متن دریافت شد.")
    
if __name__ == "__main__":
    bot.infinity_polling()

