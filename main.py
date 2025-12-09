#version 1.3.0
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telebot.util import antiflood
import logging
import time
from text import texts
from config import *
from DML import *
from DQL import *

logging.basicConfig(filename='main.log',
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

bot = telebot.TeleBot(API_TOKEN)
score_limit = 30
lower_limit = 0.5
upper_limit = 2
spam_time = 30*60

user_steps = dict() # {cid:"A",}
info_msg_bot = dict() # {cid:[mid]}

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            logging.info(f'{m.chat.first_name} [{str(m.chat.id)}]: {m.text}')
        elif m.content_type == 'photo':
            logging.info(f'{m.chat.first_name} [{str(m.chat.id)}]: sent photo')
        else:
            logging.info(f'{m.chat.first_name} [{str(m.chat.id)}]: send another content type: {m.content_type}')    
bot.set_update_listener(listener)   

def send_message(*args,**kwargs):
    try:
        return antiflood(bot.send_message,*args,**kwargs)
    except Exception as e:
        logging.error(f"Error occured: {repr(e)}",exc_info=True)
        
def edit_message_text(*args,**kwargs):
    try:
        return antiflood(bot.edit_message_text,*args,**kwargs)
    except Exception as e:
        logging.error(f"Error occured: {repr(e)}",exc_info=True)  
        
def  edit_message_reply_markup(*args,**kwargs):
    try:
        return antiflood( bot.edit_message_reply_markup,*args,**kwargs)
    except Exception as e:
        logging.error(f"Error occured: {repr(e)}",exc_info=True)            
        
def delete_message(*args,**kwargs):
    try:
        return antiflood(bot.delete_message,*args,**kwargs)
    except Exception as e:
        logging.error(f"Error occured: {repr(e)}",exc_info=True)    
          
def answer_callback_query(*args,**kwargs):
    try:
        return antiflood(bot.answer_callback_query,*args,**kwargs)
    except Exception as e:
        logging.error(f"Error occured: {repr(e)}",exc_info=True)            
        
def user_exist(cid):
    if not user_in_database(cid):
        user_info = bot.get_chat(cid)
        insert_user_data(cid, user_info.first_name, user_info.username,time.time()) 
        logging.info(f'user {user_info.first_name} by cid {cid} inserted in database successfully')   
    return True
        
def is_spam_user(cid,msg_time):
    if  check_is_spam(cid):
        last_time = user_in_database(cid).get('LAST_MSG_TIME')
        if time.time()-last_time > spam_time:
            set_is_spam(cid,False)
            return False
        logging.info(f'user by cid {cid} add to spam list')
        return True
    if user_in_database(cid):
        last_time = user_in_database(cid).get('LAST_MSG_TIME')
        score = user_in_database(cid).get('SCORE')

        if (msg_time-last_time) < lower_limit:
            score += 1
            update_user_data(cid,time.time(),score)
            if score > score_limit:
                set_is_spam(cid,True)
                logging.info(f'user by cid {cid} add to spam list')
                return True
            return False      
        elif (msg_time-last_time) >= upper_limit:
            score = max (score-1 , 0)
            update_user_data(cid,time.time(),score)
            return False
    else: return False
    
    
def clean_word(string):
    try:
        if string:
            return (string.replace('*', '\\*').replace('+','\\+')
                    .replace('_', '\\_').replace('|', '\\|').replace('-', '\\-')
                    .replace('.', '\\.').replace(')','\\)').replace('(','\\(')
                    .replace('<','\\<').replace('>','\\>').replace('=','\\=')
                    .replace(',','\\,').replace('!','\\!').replace('#','\\#'))
    except Exception as e:
          logging.error(f"Error occured in clean_word function: {repr(e)}",exc_info=True)  

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
                     parse_mode="MarkdownV2", reply_markup=markup)   
  

def result_menu(cid,ans_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(texts['back'],callback_data='back'),
        InlineKeyboardButton('تایید اطلاعات و نمایش نتیجه',callback_data=f"result_{ans_id} "))
    send_message(cid,f'*{clean_word(texts['result_menu'])}*',parse_mode="MarkdownV2", reply_markup=markup)


def send_result(cid,mid,ans_id,call_id):
    result = get_insurance_result(ans_id)
    if result:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('خروج',callback_data='end_n_poll'),
                   InlineKeyboardButton('شروع مجدد تعیین ضریب',callback_data='re_calculate'))
        edit_message_text(f"✅*نتیجه:*\n *{clean_word(result['RES_TEXT'])}*",
                          cid,mid,parse_mode="MarkdownV2",reply_markup= markup)
        clean_messages(cid)
        delete_User_Choices(cid)
    else:
        answer_callback_query(call_id,"⚠️نتیجه ای یافت نشد") 
        logging.warning(f' no result for answer Id = {ans_id}') 
        
def clean_messages(cid):
    ans_list = get_user_answers_data(cid)
    for m in ans_list:
        mid = m['MID']
        delete_message(cid,mid)
        
def send_files_to_consultant(cid,markup):
    if not info_msg_bot:
        msg = send_message(cid,f"ارسال فایل/فایلها و ارتباط با مشاور: {clean_word(texts['consultant_link'])}",
                           parse_mode="MarkdownV2",reply_markup=markup)
        mid = msg.message_id
        info_msg_bot[cid]=[mid]
    else:
        for m in info_msg_bot.get(cid):
            delete_message(cid,m)
            info_msg_bot[cid].remove(m)
        msg = send_message(cid,f"ارسال فایل/فایلها و ارتباط با مشاور: {clean_word(texts['consultant_link'])}",
                           parse_mode="MarkdownV2",reply_markup=markup)
        mid = msg.message_id
        info_msg_bot[cid].append(mid)
                
             
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
        answer_callback_query(call_id,"بازگشت به مرحله قبل ✅")
        delete_message(cid,mid)
        previous = bacK_to_previous(cid)
        if previous:
            pre_mid = previous['MID']
            delete_message(cid,pre_mid)
            qid = previous['QUESTION_ID']
            send_question_n_options(cid,qid)
            delete_last_UserAnswers(cid, previous["ID"])
            
    elif data.startswith('options'):
        answer_callback_query(call_id,"انتخاب گزینه انجام شد✅")
        _,q,ans = data.split('_')
        ans_id = int(ans)
        qid = int(q)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f'{get_ans_data(ans_id)['OPTION_TEXT']} ✔', callback_data='nothing'))
        edit_message_reply_markup(cid, mid, reply_markup=markup)
        insert_user_answers_data(cid,mid,qid,ans_id)
        ans = get_ans_data(ans_id)
        if ans['IS_FINAL']:
            result_menu(cid,ans_id)
        else:
            next_qid = ans["NEXT_QUESTION_ID"]
            if next_qid:
                send_question_n_options(cid,next_qid)
            else:
                answer_callback_query(call_id,"⚠️سوال بعدی یافت نشد")
                logging.warning(f' There is no question for answer Id {ans_id}') 
                
    elif data.startswith('result'):
        answer_callback_query(call_id,"انتخاب گزینه انجام شد✅")
        _,ans = data.split('_')
        ans_id = int(ans)
        send_result(cid,mid,ans_id,call_id)
        
    elif data == 're_calculate':
        answer_callback_query(call_id,"انتخاب گزینه انجام شد✅")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('شروع مجدد تعیین ضریب✔️', callback_data='nothing'))
        edit_message_reply_markup(cid, mid, reply_markup=markup)
        send_question_n_options(cid,1)  
        
    elif data == 'end_n_poll':
        answer_callback_query(call_id,"انتخاب گزینه انجام شد✅")
        
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('خروج ✔️', callback_data='nothing'))
        edit_message_reply_markup(cid, mid, reply_markup=markup)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('⭐⭐⭐⭐⭐',callback_data='rate_5'),
                   InlineKeyboardButton('⭐⭐⭐⭐',callback_data='rate_4'),
                   InlineKeyboardButton('⭐⭐⭐',callback_data='rate_3'),
                   InlineKeyboardButton('⭐⭐',callback_data='rate_2'),
                   InlineKeyboardButton('⭐',callback_data='rate_1'))
        send_message(cid,f"*{clean_word(texts['end'])}*", parse_mode = "MarkdownV2",reply_markup=markup)
    
    elif data.startswith('rate_'):
        answer_callback_query(call_id, "امتیاز ثبت شد ✔️")
        _,rate=data.split('_')
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f"{'⭐'*int(rate)}✔️", callback_data='nothing'))
        edit_message_reply_markup(cid, mid, reply_markup=markup)
        send_message(SUPPORT_CID,f"""
ثبت نظر جدید
امتیاز:{rate}
از طرف:
tg://user?id={cid}""")
        
        send_message(cid,f"*{clean_word(texts['thanks'])}*",parse_mode ="MarkdownV2")   
        
    elif data == 'contact_consultant':
        answer_callback_query(call_id,"درخواست ارتباط با مشاور✅")
        user_steps[cid] = "A"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('بازگشت⬅️',callback_data='support_menu'))
        edit_message_text('*جهت مشاوره لطفا کلیه فایلهای قرارداد را بارگذاری و سپس دکمه تایید و ارسال را انتخاب کنید*',
                          cid,mid, parse_mode="MarkdownV2",reply_markup=markup)
        
    elif data == 'support':
        answer_callback_query(call_id,"درخواست پشتیبانی✅")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('بازگشت⬅️',callback_data='support_menu'))
        support_link =f'ارتباط با [پشتیبانی](tg://user?id={SUPPORT_CID})'
        edit_message_text (support_link,cid,mid, parse_mode = "MarkdownV2",reply_markup=markup)

    elif data == 'support_menu':
        answer_callback_query(call_id,"بازگشت به مرحله قبل ✅")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('ارسال قرارداد و دریافت مشاوره✍️',
                                        callback_data= 'contact_consultant'),
                   InlineKeyboardButton('پشتیبانی🧑‍💻',url=texts['consultant_link']))
        edit_message_text('پشتیبانی یا مشاوره؟',cid,mid,reply_markup =markup)
        
    elif data == 'confirm_send':
        answer_callback_query(call_id,"تایید ارسال فایل")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f"تایید و ارسال✔️", callback_data='nothing'))
        edit_message_reply_markup(cid, mid, reply_markup=markup)
        link_sender =f'contact [sender](tg://user?id={cid})'
        result=get_file_info(cid)   
        file_num = len(result)
        for info in result:
            bot.copy_message(SUPPORT_CID,cid,info['MID'],
                caption=f' فایل ارسال شده جهت مشاوره از سوی کاربر{link_sender}',parse_mode="MarkdownV2" )
        send_message(cid,f'*تعداد {file_num} فایل با موفقیت به مشاور ارسال گردید*',parse_mode='MarkdownV2')
        delete_file_after_sending(cid)
        user_steps.pop(cid,None)
        info_msg_bot.pop(cid,None)
               
    elif data == 'nothing':
        answer_callback_query(call_id, 'فاقد عملیات!')
        
    elif data == 'cancel_send':
        answer_callback_query(call_id, 'لغو مشاوره')
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f"لغو مشاوره✔️", callback_data='nothing'))
        msg=bot.edit_message_reply_markup(cid, mid, reply_markup=markup)
        Mid = msg.message_id
        delete_message(cid,Mid)
        delete_file_after_sending(cid)
        user_steps.pop(cid,None) 
        info_msg_bot.pop(cid,None)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    mtime = message.date
    if not user_exist(cid): return
    if is_spam_user(cid ,mtime): return
    markup = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=False)
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
                InlineKeyboardButton('پشتیبانی🧑‍💻',url=texts['consultant_link']))
    send_message(cid,'پشتیبانی یا مشاوره؟',reply_markup =markup)        
 
@bot.message_handler(func=lambda m: m.text == texts['About'])
def about_bot_handler(message):
    cid = message.chat.id
    mtime = message.date
    if not user_exist(cid): return
    if is_spam_user(cid ,mtime): return
    send_message(cid , f'*{clean_word(texts['about_txt'])}*',parse_mode="MarkdownV2")  
    
@bot.message_handler(content_types=['document', 'photo'])
def file_handler(message):
    cid = message.chat.id  
    mid = message.message_id       

    if user_steps.get(cid) == 'A':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("تایید و ارسال", callback_data="confirm_send"),
                InlineKeyboardButton("لغو مشاوره", callback_data="cancel_send"))
        
        if message.content_type == 'document':
            file_id = message.document.file_id
            insert_file_info(cid,mid,file_id)
            send_files_to_consultant(cid,markup)
                
        elif message.content_type == 'photo':     
            file_id = message.photo[-1].file_id
            insert_file_info(cid,mid,file_id)
            send_files_to_consultant(cid,markup)
                
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.text:
        bot.reply_to(message, message.text)
    else:
        bot.reply_to(message, "پیام بدون متن دریافت شد.")
    
if __name__ == "__main__":
    logging.critical('Program started')
    bot.infinity_polling()
    logging.critical('Program ended')
