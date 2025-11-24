import mysql.connector
import logging
from config import db_config

logging.basicConfig(filename='ddl.log',
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s")

database_name = db_config['database'] 

def create_database(database_name):
    try:
        conn = mysql.connector.MySQLConnection(user=db_config['user'], password=db_config['password'], host=db_config['host'])
        logging.debug('connecting to mysql')
        cur = conn.cursor()
        cur.execute(f" DROP DATABASE IF EXISTS {database_name};")
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
        cur.close()
        conn.close()
        logging.info(f'Database {database_name} created successfully.')
    except Exception as e:
        logging.error(f'Error creating database: {e}')
        
def create_table_user():
    try:
        conn = mysql.connector.MySQLConnection(**db_config)
        cur = conn.cursor()
        cur.execute(" DROP TABLE IF EXISTS USERS;")
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS USERS(
                        `CHAT_ID`       BIGINT UNSIGNED PRIMARY KEY,
                        `NAME`          VARCHAR(150) NOT NULL,
                        `USERNAME`      VARCHAR(255) NOT NULL,
                        `LAST_MSG_TIME` DOUBLE,
                        `SCORE`         TINYINT DEFAULT 0,
                        `IS_SPAM`       BOOLEAN NOT NULL DEFAULT FALSE,
                        `REGISTER_DATE` DATETIME DEFAULT CURRENT_TIMESTAMP,
                        `LAST_UPDATE`   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                        );
                    """)
        conn.commit()
        cur.close()
        conn.close()
        logging.info('users table create successfully.')
    except Exception as e:
        logging.error(f'Error creating database: {e}')
        
        
def create_table_question():
    try:
        conn = mysql.connector.MySQLConnection(**db_config)
        cur = conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS QUESTION(
                        `ID`            INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        `Q_TEXT`        TEXT NOT NULL,
                        `REGISTER_DATE` DATETIME DEFAULT CURRENT_TIMESTAMP,
                        `LAST_UPDATE`   TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                        ); """)   
        conn.commit()
        cur.close()
        conn.close()
        logging.info('question table create successfully.')
    except Exception as e:
        logging.error(f'Error creating database: {e}')
        
def create_table_answer():
    try:
        conn = mysql.connector.MySQLConnection(**db_config)
        cur = conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS ANSWER(
                        `ID`                INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        `OPTION_TEXT`       VARCHAR(255) NOT NULL,
                        `QUESTION_ID`       INT UNSIGNED NOT NULL,
                        `IS_FINAL`          BOOLEAN  NOT NULL DEFAULT FALSE,
                        `NEXT_QUESTION_ID`  INT UNSIGNED ,
                        `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
                        `LAST_UPDATE`       TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (QUESTION_ID) REFERENCES QUESTION (ID),
                        FOREIGN KEY (NEXT_QUESTION_ID) REFERENCES QUESTION (ID)
                        ); """)   
        conn.commit()
        cur.close()
        conn.close()
        logging.info('answer table create successfully.')
    except Exception as e:
        logging.error(f'Error creating database: {e}')
        
def create_table_insurance_result():
    try:
        conn = mysql.connector.MySQLConnection(**db_config)
        cur = conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS INSURANCE_RESULT(
                        `ID`                INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        `RES_TEXT`          TEXT NOT NULL,
                        `ANS_ID`            INT UNSIGNED NOT NULL,
                        `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
                        `LAST_UPDATE`       TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                         FOREIGN KEY (ANS_ID) REFERENCES ANSWER (ID)
                        );""")    
        conn.commit()
        cur.close()
        conn.close()
        logging.info('insurance result table create successfully.')
    except Exception as e:
        logging.error(f'Error creating database: {e}')
        
def create_table_user_answers():
    try:
        conn = mysql.connector.MySQLConnection(**db_config)
        cur = conn.cursor()
        cur.execute(" DROP TABLE IF EXISTS USER_ANSWERS;")
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS USER_ANSWERS(
                        `ID`                INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        `CID`               BIGINT UNSIGNED NOT NULL,
                        `QUESTION_ID`       INT UNSIGNED NOT NULL,
                        `OPTION_ID`         INT UNSIGNED NOT NULL,
                        `REGISTER_DATE`     DATETIME DEFAULT CURRENT_TIMESTAMP,
                        `LAST_UPDATE`       TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (CID) REFERENCES USERS (CHAT_ID),
                        FOREIGN KEY (QUESTION_ID) REFERENCES QUESTION (ID),
                        FOREIGN KEY (OPTION_ID) REFERENCES ANSWER (ID)
                        ); """)   
        conn.commit()
        cur.close()
        conn.close()
        logging.info('user answers table create successfully.')
    except Exception as e:
        logging.error(f'Error creating database: {e}')
        
        
if __name__ == '__main__':
    logging.critical('Program started')
    create_database(database_name)
    create_table_user()
    create_table_question()
    create_table_answer()
    create_table_insurance_result()
    create_table_user_answers()
    logging.critical('Program ended')
    
    from DML import *
    #questions
#بخش عمرانی
    insert_question_data(' نوع قرارداد ')#q1
    insert_question_data(' سطح قرارداد ')#q2
    insert_question_data('  نوع قرارداد اصلی')#q3
    insert_question_data('  نوع مجری در قرارداد اصلی')#q4
    insert_question_data('  محل اجرای قرارداد')#q5
    insert_question_data(' ملیت کارفرما')#q6
    insert_question_data('  ملیت مجری')#q7
    insert_question_data(' نوع مجری ')#q8
    insert_question_data(' نوع شخصیت مجری')#q9
    insert_question_data(' قرارداد بر اساس ضوابط تیپ سازمان برنامه و بودجه تنظیم گردیده')#q10
    insert_question_data(' تمام یا قسمتی از بودجه عملیات ازمحل طرح تملک داراییهای سرمایه ای (طرحهای عمرانی) دولت میباشد')#q11
    insert_question_data('تامین مصالح به عهده کدامیک از طرفین است ')#q12
    insert_question_data(' قرارداد براساس فهرست بها پایه سازمان برنامه و بودجه منعقد گردیده')#q13
    insert_question_data(' تمام یا قسمتی از بودجه عملیات ازمحل طرح تملک داراییهای سرمایه ای (طرحهای عمرانی) دولت میباشد')#q14
    insert_question_data(' نام کارفرما (واگذارنده‌كار)')#q15
    insert_question_data('موضوع قراراد')#q16
    insert_question_data('موضوع قراراد')#q17
    insert_question_data('موضوع قراراد')#q18
    insert_question_data('تامين اعتبار قرارداد از محل فروش اراضی آماده به متقاضیان و اشخاص است')#q19
    insert_question_data(' نام کارفرما (واگذارنده‌كار)')#20
    insert_question_data('موضوع قراراد')#q21
    insert_question_data('موضوع قراراد')#q22
    insert_question_data('موضوع قراراد')#q23
    insert_question_data('تامين اعتبار قرارداد از محل فروش اراضی آماده به متقاضیان و اشخاص است')#q24
#بخش غیرعمرانی


    
    
#--------------------------------------------------------------------------------------    
#options
#بخش عمرانی
    insert_answer_data('غیرعمرانی ',1,25)#s1
    insert_answer_data('عمرانی ',1,2)#S2
    insert_answer_data('قرارداد فرعی است ',2,3)#s3
    insert_answer_data('قرارداد اصلی است ',2,5)#s4
    insert_answer_data('قرارداد اصلی غیرعمرانی ',3,None,True)#s5
    insert_answer_data('قرارداد اصلی عمرانی ',3,4)#s6
    insert_answer_data('مهندس مشاور ',4,None,True)#s7
    insert_answer_data('پیمانکار اجرایی ',4,None,True)#s8
    insert_answer_data('کلا خارج از کشور ',5,None,True)#s9
    insert_answer_data('تمام یا بخشی داخل کشور',5,6)#s10
    insert_answer_data('غیرایرانی ',6,None,True)#s11
    insert_answer_data('ایرانی ',6,7)#s12
    insert_answer_data('غیرایرانی ',7,None,True)#s13
    insert_answer_data('ایرانی ',7,8)#s14
    insert_answer_data('پیمانکار اجرایی ',8,12)#s15
    insert_answer_data('مهندس مشاور ',8,9)#s16
    insert_answer_data('حقیقی ',9,None,True)#s17
    insert_answer_data('حقوقی ',9,10)#s18
    insert_answer_data('خیر ',10,None,True)#s19
    insert_answer_data('بلی ',10,11)#s20
    insert_answer_data('خیر ',11,15)#s21
    insert_answer_data('بلی ',11,None,True)#s22
    insert_answer_data('تامین تمام مصالح توسط پیمانکار  ',12,13)#s23
    insert_answer_data('تامین تمام یا بخشی از مصالح توسط کارفرما ',12,None,True)#s24
    insert_answer_data('خیر ',13,None,True)#s25
    insert_answer_data('بلی ',13,14)#s26
    insert_answer_data('خیر ',14,20)#s27
    insert_answer_data('بلی ',14,None,True)#s28
    insert_answer_data('سازمان صنايع دفاع',15,None,True)#s29
    insert_answer_data('آستان قدس رضوی',15,16)#s3
    insert_answer_data('وزارت مسکن و شهرسازی ',15,17)#s31
    insert_answer_data('وزارت دفاع و پشتیبانی نیروهای مسلح',15,18)#s32
    insert_answer_data('سازمان تامین‌اجتماعی',15,18)#s33
    insert_answer_data('ساير ',15,None,True)#s34
    insert_answer_data('طرح توسعه حريم رضوی ',16,None,True)#s35
    insert_answer_data('سایر',16,None,True)#s36
    insert_answer_data('تسطیح و آماده سازی اراضي مي‌باشد',17,19)#s37
    insert_answer_data('سایر',17,None,True)#s38
    insert_answer_data('عملیات ساختماني',18,None,True)#s39
    insert_answer_data('سایر',18,None,True)#s40
    insert_answer_data('خیر',19,None,True)#s41
    insert_answer_data('بلی',19,None,True)#s42
    insert_answer_data('سازمان صنايع دفاع',20,None,True)#s43
    insert_answer_data('آستان قدس رضوی',20,21)#s44
    insert_answer_data('وزارت مسکن و شهرسازی ',20,22)#s45
    insert_answer_data('وزارت دفاع و پشتیبانی نیروهای مسلح',20,18)#s46
    insert_answer_data('سازمان تامین‌اجتماعی',20,23)#s47
    insert_answer_data('ساير ',20,None,True)#s48
    insert_answer_data('طرح توسعه حريم رضوی ',21,None,True)#s49
    insert_answer_data('سایر',21,None,True)#s50
    insert_answer_data('تسطیح و آماده سازی اراضي مي‌باشد',22,24)#s51
    insert_answer_data('سایر',22,None,True)#s52
    insert_answer_data('عملیات ساختماني',23,None,True)#s53
    insert_answer_data('سایر',23,None,True)#s54
    insert_answer_data('خیر',24,None,True)#s55
    insert_answer_data('بلی',24,None,True)#s56
#بخش غیرعمرانی


#--------------------------------------------------------------------------------------    
#results
#بخش عمرانی
    insert_result_data('با توجه به نوع قرارداد اصلی برای تعیین ضریب با شروع مجدد ربات، گزینه غیرعمرانی را انتخاب نمایید. ',5)
    insert_result_data('در صورت احراز عمرانی بودن قرارداد اصلی و تایید قرارداد فرعی توسط کارفرمای اصلی، به تبعیت از قرارداد اصلی ضریب قرارداد= 14% (حق بیمه= 14%مبلغ قرارداد وبیمه بیکاری=1.6% مبلغ قرارداد میباشد). ولیکن با توجه به پرداخت حق بیمه در قرارداد اصلی تا سقف 15.6% مبلغ قرارداد، حق بیمه ای دریافت نمیگردد و صرفا در صورتیکه حق بیمه لیستهای ارسالی بیش از حق بیمه طبق ضریب باشد یا لیستها خارج از دوره قرارداد ارسال شده باشد، مابه التفاوت آن اخذ میگردد. ',7)
    insert_result_data('در صورت احراز عمرانی بودن قرارداد اصلی و تایید قرارداد فرعی توسط کارفرمای اصلی، به تبعیت از قرارداد اصلی ضریب قرارداد= 6% (حق بیمه= 6%مبلغ قرارداد وبیمه بیکاری=0.6% مبلغ قرارداد میباشد). ولیکن با توجه به پرداخت حق بیمه در قرارداد اصلی تا سقف 6.6% مبلغ قرارداد، حق بیمه ای دریافت نمیگردد و صرفا در صورتیکه حق بیمه لیستهای ارسالی بیش از حق بیمه طبق ضریب باشد یا لیستها خارج از دوره ارسال شده باشد مابه التفاوت آن اخذ میگردد. ',8)
    insert_result_data('با توجه به محل اجرای قرارداد خارج ازمرزهای کشورمشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',9)
    insert_result_data('با توجه به ملیت کارفرما قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',11)
    insert_result_data('با توجه به ملیت مجری قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',13)
    insert_result_data('شخصیت مهندس مشاور نمیتواند حقیقی باشد. برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',17)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود. ',19)
    insert_result_data('ضریب قرارداد : 14% (حق بیمه= 14% مبلغ قراردادوبیمه بیکاری= 1.6 %مبلغ قرارداد مجموعا 15.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای ارسالی قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 15.6% کارکرد مطالبه و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.ضمنا چنانچه هیچگونه لیستی با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',22)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود. ',24)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود. ',25)
    insert_result_data('ضریب قرارداد : 6% (حق بیمه= 6% مبلغ قراردادوبیمه بیکاری= 0.6 %مبلغ قرارداد مجموعا 6.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 6.6% کارکرد مطالبه میشود و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.چنانچه هیچگونه لیستی  با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه  و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه  میگردد.',28)
    insert_result_data('ضریب قرارداد : 14% (حق بیمه= 14% مبلغ قراردادوبیمه بیکاری= 1.6 %مبلغ قرارداد مجموعا 15.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای ارسالی قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 15.6% کارکرد مطالبه و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.ضمنا چنانچه هیچگونه لیستی با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',29)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',34)
    insert_result_data('ضریب قرارداد : 14% (حق بیمه= 14% مبلغ قراردادوبیمه بیکاری= 1.6 %مبلغ قرارداد مجموعا 15.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای ارسالی قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 15.6% کارکرد مطالبه و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.ضمنا چنانچه هیچگونه لیستی با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',35)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',36)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',38)
    insert_result_data('ضریب قرارداد : 14% (حق بیمه= 14% مبلغ قراردادوبیمه بیکاری= 1.6 %مبلغ قرارداد مجموعا 15.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای ارسالی قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 15.6% کارکرد مطالبه و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.ضمنا چنانچه هیچگونه لیستی با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',39)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',40)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',41)
    insert_result_data('ضریب قرارداد : 14% (حق بیمه= 14% مبلغ قراردادوبیمه بیکاری= 1.6 %مبلغ قرارداد مجموعا 15.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای ارسالی قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 15.6% کارکرد مطالبه و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.ضمنا چنانچه هیچگونه لیستی با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',42)
    insert_result_data('ضریب قرارداد : 6% (حق بیمه= 6% مبلغ قراردادوبیمه بیکاری= 0.6 %مبلغ قرارداد مجموعا 6.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 6.6% کارکرد مطالبه میشود و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.چنانچه هیچگونه لیستی  با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه  و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه  میگردد.',43)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',48)
    insert_result_data('ضریب قرارداد : 6% (حق بیمه= 6% مبلغ قراردادوبیمه بیکاری= 0.6 %مبلغ قرارداد مجموعا 6.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 6.6% کارکرد مطالبه میشود و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.چنانچه هیچگونه لیستی  با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه  و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه  میگردد.',49)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',50)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',52)
    insert_result_data('ضریب قرارداد : 6% (حق بیمه= 6% مبلغ قراردادوبیمه بیکاری= 0.6 %مبلغ قرارداد مجموعا 6.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 6.6% کارکرد مطالبه میشود و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.چنانچه هیچگونه لیستی  با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه  و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه  میگردد.',53)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',54)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای تعیین ضریب با شروع مجدد ربات، ازبخش غیرعمرانی استفاده شود.',55)
    insert_result_data('ضریب قرارداد : 6% (حق بیمه= 6% مبلغ قراردادوبیمه بیکاری= 0.6 %مبلغ قرارداد مجموعا 6.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 6.6% کارکرد مطالبه میشود و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.چنانچه هیچگونه لیستی  با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه  و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه  میگردد.',56)
#بخش غیرعمرانی




