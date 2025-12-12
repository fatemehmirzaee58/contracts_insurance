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
        
def create_table_file_info():
    try:
        conn = mysql.connector.MySQLConnection(**db_config)
        cur = conn.cursor()
        cur.execute(" DROP TABLE IF EXISTS FILE_INFO;")
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS FILE_INFO(
                        `ID`                  INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        `CID`                 BIGINT UNSIGNED,
                        `MID`                 INT UNSIGNED,
                        `FID`                 VARCHAR(255),
                        `REGISTER_DATE`       DATETIME DEFAULT CURRENT_TIMESTAMP,
                        `LAST_UPDATE`         TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (CID) REFERENCES USERS (CHAT_ID)
                        );
                    """)
        conn.commit()
        cur.close()
        conn.close()
        logging.info('table FILE_INFO create successfully.')
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
                        `MID`               INT UNSIGNED,
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
    create_table_file_info()
    create_table_question()
    create_table_answer()
    create_table_insurance_result()
    create_table_user_answers()
    logging.critical('Program ended')

    from DML import *

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

    insert_question_data('محل اجراي عمليات')#q25
    insert_question_data('نوع شخصیت مجری')#q26
    insert_question_data('نوع شخصیت مجری')#q27
    insert_question_data(' دسته بندی بر اساس نحوه اجرای عملیات')#28
    insert_question_data(' دسته بندی بر اساس نحوه اجرای عملیات')#29
    
    insert_question_data('موضوع قرارداد')#30
    insert_question_data('موضوع قرارداد')#31
    insert_question_data(' ماهیت مقاطعه کار ')#32
    insert_question_data('موضوع قرارداد')#33
    insert_question_data('موضوع قرارداد')#34
    insert_question_data('موضوع قرارداد')#35
    insert_question_data(' ماهیت مقاطعه کار ')#36
    insert_question_data('موضوع قرارداد')#37
    insert_question_data('موضوع قرارداد')#38
    
    insert_question_data('کلیه مفاد قرارداد بیانگر اجرای قرارداد به تنهایی و توسط شخص مجری میباشد')#39
    insert_question_data('کارفرما انجام قرارداد به تنهایی توسط مجری را گواهی نموده است')#40
    insert_question_data('متوسط دستمزد روزانه(نسبت ناخالص کارکرد به روزهای کارکرد دوره قرارداد) بیش از حداکثر دستمزد روزانه سالهای دوره قرارداد می‌باشد')#41   
    insert_question_data('تامین محل انجام کار به عهده پیمانکاراست ؟«ملکی یا استیجاری» ')#42
    insert_question_data(' در دوره قرارداد هم لیست حق بیمه پرسنل همه ماهه ارسال شده و هم محل اجرای قرارداد مورد بازرسی قرار گرفته است')
    insert_question_data('اسامی اشخاص حقیقی مجری قرارداد در متن قرارداد ذکر شده')#44
    insert_question_data('کارفرما اجرای عملیات منحصرا توسط شخص پیمانکار و یا پیمانکاران مندرج در متن قرارداد را گواهی نموده')#45
    
    insert_question_data('کارگاه ثابت قبل از انعقاد قرارداد و پس از اتمام قرارداد فعال بوده')#46
    insert_question_data('تامین محل انجام کار به عهده پیمانکاراست ؟«ملکی یا استیجاری» ')#47
    insert_question_data('کارگاه دارای پروانه فعالیت  مرتبط و  منطبق با موضوع قرارداد و معتبر در دوره اجرای پیمان میباشد')#48
    insert_question_data('کارگاه در دوره قرارداد در کد کارگاه ثابت، دارای لیست و بازرسی میباشد')#49
    insert_question_data(' کل عملیات اجرایی پروژه توسط کارکنان شاغل در  کارگاه ثابت انجام میشود')#50
    
    insert_question_data('کارگاه دارای پروانه فعالیت  مرتبط و  منطبق با موضوع قرارداد و معتبر در دوره اجرای پیمان میباشد')#51
    insert_question_data('تامین محل انجام کار به عهده پیمانکاراست ؟«ملکی یا استیجاری» ')#52
    insert_question_data(' در دوره قرارداد هم لیست حق بیمه پرسنل همه ماهه ارسال شده و هم محل اجرای قرارداد مورد بازرسی قرار گرفته است')#53
    
    insert_question_data(' کارگاه ثابت قبل از انعقاد قرارداد و پس از اتمام قرارداد فعال بوده؟')#54
    insert_question_data('تامین محل انجام کار به عهده پیمانکاراست ؟«ملکی یا استیجاری» ')#55
    insert_question_data(' موضوع فعالیت طبق اساسنامه (یا آگهی تغییرات)  با موضوع قرارداد انطباق دارد')#56  
    insert_question_data(' کارگاه دارای پروانه فعالیت  مرتبط و  منطبق با موضوع قرارداد و معتبر در دوره اجرای پیمان می‌باشد')#57
    insert_question_data(' در دوره قرارداد هم لیست حق بیمه پرسنل همه ماهه ارسال شده و هم محل اجرای قرارداد مورد بازرسی قرار گرفته است')#58
    insert_question_data(' وضعيت بازرسي از دفاتر قانوني')#59
    insert_question_data(' شماره قرارداد در صورت وجوه درآمدی فهرست شده ')#60
    insert_question_data(' کل عملیات اجرایی پروژه توسط کارکنان شاغل در کارگاه ثابت انجام میشود  ')#61
    
    insert_question_data(' مجري قرارداد دانشگاهها یا مراکز علمی و پژوهشی اعم از دولتی و غیردولتی ميباشند')#62
    insert_question_data('مجری داراي مجوز قطعي تحقيقاتي و پژوهشي از وزارت علوم،تحقیقات و فناوری يا وزارت بهداشت درمان و آموزش پزشکی يا شورای عالی حوزه های علمیه میباشد ')#63
    insert_question_data(' در دوره قرارداد هم لیست حق بیمه پرسنل همه ماهه ارسال شده و هم محل اجرای قرارداد مورد بازرسی قرار گرفته است')#64
    insert_question_data(' وضعيت بازرسي از دفاتر قانوني')#65
    insert_question_data(' شماره قرارداد در صورت وجوه درآمدی فهرست شده ')#66
    insert_question_data(' آيا قرارداد ادامه دارد؟(درخواست مفاصاحساب بصورت مقطعی بوده)')#67
    insert_question_data('آيا مبلغ قرارداد در فهرست وجوه درآمدي بيش ازمبلغ ناخالص كاركرد اعلام شده از سوي کارفرما میباشد ')#68
    
    insert_question_data('مجري قرارداد وزارتخانه ها و موسسات دولتي مي باشند ')#s69
    insert_question_data(' كل عمليات موضوع قرارداد توسط کارکنان مشمول نظام حمایتی خاص غير از تامین اجتماعی انجام گرفته است  ')#70
    insert_question_data(' وضعيت بازرسي از دفاتر قانوني')#71
    insert_question_data(' شماره قرارداد در صورت وجوه درآمدی فهرست شده ')#72
    insert_question_data(' آيا قرارداد ادامه دارد؟(درخواست مفاصاحساب بصورت مقطعی بوده)')#73
    insert_question_data('آيا مبلغ قرارداد در فهرست وجوه درآمدي بيش ازمبلغ ناخالص كاركرد اعلام شده از سوي کارفرما میباشد ')#74
    
    insert_question_data('جزئیات موضوع قرارداد')#75
    insert_question_data('موضوع فعالیت مجری در اساسنامه یا آگهی تغییرات با موضوع قرارداد انطباق دارد')#76
    insert_question_data('پيمانكار دارای مجوز فعالیت  مرتبط و  منطبق با موضوع قرارداد و معتبر در دوره اجرای پیمان میباشد')#77
    insert_question_data('عمليات توسط پرسنل دفترمركزي (كارگاه ثابت) انجام شده')#78
    insert_question_data('در دوره قرارداد داراي  لیست و بازرسی میباشد')#79
    
    insert_question_data('قرارداد مورد تاييد معاونت علمي و فناوري رياست جمهوري ميباشد و داراي تاييديه از معاونت مزبور ميباشد')#80
    insert_question_data('تامین محل انجام کار به عهده پیمانکاراست ؟«ملکی یا استیجاری» ')#81
    
    insert_question_data(' نام کارفرما')#82
    
    insert_question_data('جزئیات موضوع قرارداد')#83
    insert_question_data('جزئیات موضوع قرارداد')#84
    insert_question_data('جزئیات موضوع قرارداد')#85
    insert_question_data('جزئیات موضوع قرارداد')#86
    
    insert_question_data(' دسته بندی بر اساس نام کارفرما یا مجوز مجری')#87
    insert_question_data(' نام گروه و دسته پیمانکار')#88
    insert_question_data('نحوه خريد یرق')#89
    insert_question_data('تامین محل انجام کار به عهده پیمانکاراست ؟«ملکی یا استیجاری» ')#90
    insert_question_data('آیا مبلغ هر بخش تفكيك شده')#91
    insert_question_data(' نام کارفرما')#92
    insert_question_data(' نام کارفرما')#93
    insert_question_data('تامین مصالح به عهده کدامیک از طرفین است ')#94
     
    insert_question_data('تامین دكل و تجهیزات و مصالح مصرفی با پیمانکاراست')#95
    insert_question_data('تامین دكل و تجهیزات و مصالح مصرفی با پیمانکاراست')#96
    
    insert_question_data('پیمانکار دارای کارگاه ثابت تولیدی بوده و ساخت تجهیزات در کارگاه انجام شده')#97
    insert_question_data('تامین کلیه تجهیزات و مصالح با پیمانکاراست')#98
    insert_question_data('مبلغ تجهیزات در قرارداد، صورت‌وضعیتهای موقت و قطعی و گواهی واگذارنده(کارفرما) به تفکیک از مبلغ مصالح و اجرا اعلام شده ')#99
    insert_question_data('آیا مبلغ تجهیزات بیش از 50 درصد مبلغ اولیه و کارکرد نهایی قرارداد می‌باشد')#100
    insert_question_data('افزایش مبلغ تجهیزات در کارکرد نهایی نسبت به مبلغ اولیه بیش از 10 درصد می‌باشد ')#101
    insert_question_data('در اجراي عمليات از مقاطعه‌كار فرعي استفاده شده که موضوع، دوره و مبلغ آنها با قرارداد اصلی تطابق داشته و مفاصاحساب آنهاصادر شده ')#102
    insert_question_data('تمام یا برخی از  قراردادهای فرعی مشمول ماده 47 قانون بوده ')#103
    
    insert_question_data(' نوع بیمه پردازی رانندگان')#104
    insert_question_data('رانندگان خودمالک دارای سابقه بیمه‌پردازی ازطریق بیمه‌رانندگان میباشند')#105
    insert_question_data('رانندگان خودمالک دارای سابقه بیمه‌پردازی ازطریق بیمه‌رانندگان میباشند')#106
    insert_question_data('مبلغ کارکرد رانندگان در استخدام  (A) از کارکرد رانندگان مشمول بیمه‌رانندگان(B) تفکیک شده')#107
    
    insert_question_data('راننده خودمالک و اجرای عملیات به تنهایی توسط شخص راننده بوده')#108
    insert_question_data('راننده در دوره قرارداد دارای سابقه بر اساس بیمه رانندگان می‌باشد')#109
    
    insert_question_data(' نوع بیمه پردازی رانندگان')#110
    insert_question_data('رانندگان خودمالک دارای سابقه بیمه‌پردازی ازطریق بیمه‌رانندگان میباشند')#111
    insert_question_data('رانندگان خودمالک دارای سابقه بیمه‌پردازی ازطریق بیمه‌رانندگان میباشند')#112
    insert_question_data('مبلغ کارکرد رانندگان در استخدام  (A) از کارکرد رانندگان مشمول بیمه‌رانندگان(B) تفکیک شده')#113
    insert_question_data('موضوع قرارداد')#114
    insert_question_data(' کارفرما')#115
    insert_question_data(' کارفرما')#116
    
    insert_question_data(' مالکیت کشتی')#117
    insert_question_data(' موضوع قرارداد')#118
    insert_question_data('تامین تجهیزات، مصالح مصرفی و سوخت با کدامیک از طرفین است')#119
    
    insert_question_data(' موضوع قرارداد')#120
    insert_question_data('آیادرصد مکانیکی و دستی توسط واگذارنده گواهی شده')#121
    
    insert_question_data('نحوه ساخت یا تهیه تجهیزات')#122
    insert_question_data('آیا بابت خرید خارجی اوراق گمرکی مرتبط  به نام پیمانکار و حداکثر تا میزان کارکرد موجود میباشد و مورد تایید کارفرما قرار گرفته ')#123
    
    insert_question_data('نحوه ساخت یا تهیه تجهیزات')#124
    insert_question_data('آیا بابت خرید خارجی اوراق گمرکی مرتبط  به نام پیمانکار و حداکثر تا میزان کارکرد موجود میباشد و مورد تایید کارفرما قرار گرفته ')#125
    
    insert_question_data('نحوه ساخت یا تهیه تجهیزات')#126
    insert_question_data('آیا بابت خرید خارجی اوراق گمرکی مرتبط  به نام پیمانکار و حداکثر تا میزان کارکرد موجود میباشد و مورد تایید کارفرما قرار گرفته ')#127
 
    insert_question_data('تامین نیروی انسانی به عهده کدامیک از طرفین است')#128
    insert_question_data('آیا کارکرد اجاره خودرو با راننده از کل کارکرد تفکیک شده')#129
    insert_question_data('یررسی سوابق کارکنان در استخدام کارفرما')#130
    insert_question_data(' سوابق کارکنان در استخدام کارفرما در ليستهاي ارسالي و عنوان شغلي آنها ')#131
    insert_question_data('وضعیت تامین مصالح')#132
    insert_question_data(' نسبت مصالح به کل کارکرد ')# 133
    insert_question_data('نوع مصالح واگذاري به پيمانكار')#134
    insert_question_data(' نسبت مصالح تهیه شده توسط پیمانکار به کل کارکرد ')# 135
    insert_question_data('ارزش ریالی مصالح واگذاري به پيمانكار،گواهي شده')#136
    
    insert_question_data('تامين كليه ماشين‌آلات با پيمانكار')#137
    insert_question_data('نوع ارائه خدمات')#138
    
    insert_question_data(' وضعیت اوراق گمرکی و سایر مستندات مرتبط باتجهیزات خارجی')#139
    insert_question_data('عملیات دارای تجهیزات خریداری شده از داخل کشور و یا مصالح تامین شده توسط پیمانکار میباشد ')#140
    insert_question_data('نسبت ( تجهیزات داخلی و مصالح مصرفی) به(مبلغ تجهیزات داخلی و مصالح مصرفی+ مبلغ عملیات اجرا) ')#141
    insert_question_data('در اجرای عملیات از ماشین‌آلات استفاده شده و تامین آن با پیمانکار بوده')#142
    
    insert_question_data('عملیات دارای تجهیزات خریداری شده از داخل کشور و یا مصالح تامین شده توسط پیمانکار میباشد ')#143
    insert_question_data('نسبت ( تجهیزات و مصالح مصرفی) به(مبلغ تجهیزات و مصالح مصرفی+ مبلغ عملیات اجرا) ')#144
    insert_question_data('در اجرای عملیات از ماشین‌آلات استفاده شده و تامین آن با پیمانکار بوده')#145
    
    insert_question_data('قرارداد حائز شرایط لازم برای موضوع انتخابی نمیباشد.در ادامه نسبت به تعیین دسته بندی بر اساس نوع، موضوع و جزئیات و شرح کار قرارداد اقدام نمایید.')#146
    insert_question_data(' دسته بندی بر اساس موضوع')#147
    insert_question_data('تامین ماشین‌آلات و ابزار مکانیکی با پیمانکاراست')#148
    
    insert_question_data('تامین ابزار و ماشین‌آلات با پیمانکاراست')#149
    
    insert_question_data(' نوع مواد معدنی و محل اجرا')#150
    insert_question_data('تامین و نگهداری ماشین آلات و تجهیزات سنگین(از قبیل شاول-دامپراکت- دستگاههای حفاری)  به عهده کدامیک از طرفین است')#151
    insert_question_data(' تامین مصالح اختصاصی(مانند دینامیت و آنفو) به عهده کدامیک از طرفین است')#152
    insert_question_data('نام کارفرما(واگذارنده)') #153
    
    insert_question_data('نوع جایگاه')#154
    insert_question_data('نحوه پرداختی به بیمارستان')#155
    
    insert_question_data('تامین تجهیزات و مواد مصرفی به عهده کدام یک از طرفین است')#156
    insert_question_data('تامین تجهیزات و مواد مصرفی به عهده کدام یک از طرفین است')#157
    
    
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

    insert_answer_data('کلا داخل کشور ',25,26)#S57
    insert_answer_data('تمام یا بخشی خارج از كشور',25,27)#S58
    
    insert_answer_data('حقوقی ',26,28)#S59
    insert_answer_data('حقیقی ',26,29)#S60

    insert_answer_data('حقوقی ',27,32)#S61
    insert_answer_data('حقیقی ',27,35)#S62
    
    insert_answer_data('به صورت متمرکز در دفترمرکزی یا کارگاه ثابت و قابل بازرسی طبق ماده 47 قانون',28,31)#S63
    insert_answer_data(' به صورت پراکنده در سطح شهر،استان یا کشور(مشمول ماده 41 قانون)',28,36)#s64
    
    insert_answer_data('به صورت متمرکز در دفترمرکزی یا کارگاه ثابت و قابل بازرسی طبق ماده 47 قانون',29,30)#s65
    insert_answer_data('به صورت پراکنده در سطح شهر،استان یا کشور(مشمول ماده 41 قانون)',29,114)#s66
    insert_answer_data('به صورت انفرادی توسط مجری',29,39)#s67
    
    insert_answer_data('ارائه خدمات مراقبت هاي اوليه بهداشتي و سلامت محور در پايگاههاي سلامت ',30,42)#s68
    insert_answer_data(' تحقيقاتي وپژوهشي',30,44) #s69
    insert_answer_data('انجام عملیات در کارگاه صنعتی،خدماتی،تولیدی،فنی و مهندسی ثابت متعلق به پیمانکار',30,46)#S70
    insert_answer_data(' قراردادهاي مورد اجراي دفاتر پيشخوان دولت',30,51)#s71
    insert_answer_data(' عمليات بيمه گري مورد اجراي نمايندگي و كارگزاري شركت هاي بيمه',30,51)#s72
    insert_answer_data(' اعطای نمايندگي فروشگاههاي زنجيره اي',30,51)#s73
    insert_answer_data(' فروش محصولات با نمايندگيهاي مجاز فروش و خدمات پس از فروش',30,51)#s74
    insert_answer_data('نگهداري كالاو مركبات و غلات در انبارها و سردخانه ها و سيلوهاي مكانيزه ',30,51)#s75
    insert_answer_data(' پورسانت فروش',30,51)#s76
    insert_answer_data(' ارائه خدمات توسط هتلها',30,51)#s77
    
    insert_answer_data('انجام عملیات در کارگاه صنعتی،خدماتی،تولیدی،فنی و مهندسی ثابت متعلق به پیمانکار',31,54)#s78
    insert_answer_data(' تحقيقاتي وپژوهشي',31,62) #s79
    insert_answer_data(' مجری قرارداد مشمول نظام حمايتي خاص',31,69) #s80
    insert_answer_data(' فن آوري اطلاعات و ارتباطات ',31,75) #s81
    insert_answer_data(' دانش بنیان',31,80) #s82
    insert_answer_data(' مشاوره مديريت',31,76) #s83
    insert_answer_data(' قراردادهاي مورد اجراي دفاتر پيشخوان دولت',31,81) #s84
    insert_answer_data('  قراردادهاي مورد اجراي كارگزاري رسمي تامين اجتماعي',31,82) #s85
    insert_answer_data(' عمليات بيمه گري مورد اجراي نمايندگي و كارگزاري شركت هاي بيمه',31,76) #s86
    insert_answer_data(' خدمات فروش بليط توسط نمايندگيهاي شركتهاي حمل ونقل هوايي،ريلي و زميني',31,76) #s87
    insert_answer_data('حسابرسی',31,83) #s88
    insert_answer_data('شركت‌هاي تامين سرمايه',31,84) #s89
    insert_answer_data('شركت‌هاي كارگزاري بورس',31,85) #s90
    insert_answer_data('هواپيمايي و بالگردي',31,86) #s91
    insert_answer_data(' اعطای نمايندگي فروشگاههاي زنجيره اي',31,81) #s92
    insert_answer_data(' فروش محصولات با نمايندگيهاي مجاز فروش و خدمات پس از فروش',31,81)#s93
    insert_answer_data('نگهداري كالاو مركبات و غلات در انبارها و سردخانه ها و سيلوهاي مكانيزه ',31,81)#s94
    insert_answer_data(' پورسانت فروش',31,81)#s95
    insert_answer_data(' موسسات فرهنگي با موضوع انتشارات و تبليغات در فضاي مجازي',31,81)#s96
    insert_answer_data(' ارائه خدمات توسط هتلها',31,76)#s97
    insert_answer_data(' خريد و فروش  تضميني برق ',31,87)#s98
    insert_answer_data(' ارائه خدمات مراقبت هاي اوليه بهداشتي و سلامت محور در پايگاههاي سلامت',31,90)#s99
    
    
    insert_answer_data('مهندس مشاور',32,33)#s100
    insert_answer_data('پیمانکار',32,34)#s101
    
    insert_answer_data('نقشه برداری ',33,None,True)#s102
    insert_answer_data('خدمات مشاوره ژئوتکنیک و مقاومت مصالح ',33,None,True)#s103
    insert_answer_data('طراحی ',33,None,True)#s104
    insert_answer_data('نظارت عالیه و کارگاهی ',33,None,True)#s105
    insert_answer_data('تركيبي از طراحي ،نظارت عاليه ،نقشه برداري ، خدمات ژئوتكنيك و ساير موضوعات مشاوره',33,91)#s106
    insert_answer_data('خدمات مدیریت طرح، بهره برداری و نگهداری و ساير موضوعات مشاوره',33,None,True)#s107
    #حقوقی 41 بخشی خارج    
    insert_answer_data(' هواپيمايي و بالگردي ',34,86)#s108
    insert_answer_data(' نقشه‌برداري ',34,None,True)#s109
    insert_answer_data('تامین دکلهای حفاری چاههای نفت و گاز دریایی به همراه خدمه  ',34,95)#s110
    insert_answer_data(' تامین دکلهای حفاری چاههای نفت و گاز در مناطق خشکی به همراه خدمه ',34,96)#s111
    insert_answer_data(' قراردادهای غیرعمرانی منعقده به روش   EPC وPC  ',34,97)#s112
    insert_answer_data(' حمل و نقل مواد نفتی',34,104)#s113
    insert_answer_data(' حمل و نقل بار و کالای بین شهری',34,104)#s114
    insert_answer_data(' جابه‌جایی مسافر بین شهری و درون شهری',34,110)#s115
    insert_answer_data(' بازار یابی و جذب پیامهای بازرگانی',34,115)#s116
    insert_answer_data(' حمل و نقل ریلی',34,116)#s117
    insert_answer_data(' خدمات دریایی ',34,117)#s118
    insert_answer_data(' خن‌کاری در بنادر ',34,121)#s119
    insert_answer_data(' قراردادهای اجرایی ژئوتکنیک ',34,None,True)#s120
    insert_answer_data(' خرید یا فروش(تهیه، تامین و تحویل تجهیزات بدون کار اضافی)',34,122)#s121
    insert_answer_data(' اجاره خودرو/ ماشین آلات',34,128)#s122
    insert_answer_data('پیمان مدیریت ',34,None,True)#s123
    insert_answer_data('قرارداد دستمزدي',34,None,True)#s124
    insert_answer_data('قرارداد با مصالح',34,132)    #s125
    insert_answer_data('قرارداد ارائه خدمات با استفاده از ماشين‌آلات',34,137)#s126
    insert_answer_data('قرارداد داراي تجهيزات خريداري شده از خارج از كشور',34,139)  #s127
    #خارج 41 حقیقی
    insert_answer_data(' نقشه‌برداري ',35,None,True)#s128
    insert_answer_data(' تامین دکلهای حفاری چاههای نفت و گاز دریایی به همراه خدمه ',35,95)#s129
    insert_answer_data(' تامین دکلهای حفاری چاههای نفت و گاز در مناطق خشکی به همراه خدمه ',35,96)#130
    insert_answer_data(' قراردادهای غیرعمرانی منعقده به روش   EPC وPC  ',35,97)#s131
    insert_answer_data(' حمل و نقل مواد نفتی',35,108)#s132
    insert_answer_data(' حمل و نقل بار و کالای بین شهری',35,104)#s133
    insert_answer_data(' جابه‌جایی مسافر بین شهری و درون شهری',35,110)#s134
    insert_answer_data(' بازار یابی و جذب پیامهای بازرگانی',35,115)#s135
    insert_answer_data(' حمل و نقل ریلی',35,116)#s136
    insert_answer_data(' خدمات دریایی  ',35,117)#s137
    insert_answer_data(' خن‌کاری در بنادر ',35,121)#s138
    insert_answer_data(' قراردادهای اجرایی ژئوتکنیک ',35,None,True)#s139
    insert_answer_data(' خرید یا فروش(تهیه، تامین و تحویل تجهیزات بدون کار اضافی)',35,122)#s140
    insert_answer_data(' اجاره خودرو/ ماشین آلات',35,128)#s141
    insert_answer_data('پیمان مدیریت  ',35,None,True)#s142
    insert_answer_data('قرارداد دستمزدي',35,None,True)#s143
    insert_answer_data('قرارداد با مصالح',35,132)    #s144
    insert_answer_data('قرارداد ارائه خدمات با استفاده از ماشين‌آلات',35,137)#s145
    insert_answer_data('قرارداد داراي تجهيزات خريداري شده از خارج از كشور',35,139)  #s146
    insert_answer_data('اجرای عملیات  به صورت انفرادی توسط مجری',35,39)#s147
    
    insert_answer_data('مهندس مشاور',36,37)#s148
    insert_answer_data('پیمانکار',36,38)#s149
    
    
    insert_answer_data('نقشه برداری ',37,None,True)#150
    insert_answer_data('خدمات مشاوره ژئوتکنیک و مقاومت مصالح ',37,None,True)#s151
    insert_answer_data('طراحی ',37,None,True)#s152
    insert_answer_data('نظارت عالیه و کارگاهی ',37,None,True)#s153
    insert_answer_data('تركيبي از طراحي، نظارت عاليه، نقشه برداري، خدمات ژئوتكنيك و ساير موضوعات مشاوره',37,91)#s154
    insert_answer_data('خدمات مدیریت طرح، بهره برداری و نگهداری و ساير موضوعات مشاوره',37,None,True)#s155
    insert_answer_data(' قراردادهای مشاوره با بنیاد مسکن انقلاب اسلامی  ',37,92)#s156

    # حقوقی 41 داخل 
    insert_answer_data(' نقشه‌برداري ',38,None,True)#s157
    insert_answer_data('قراردادهاي اجرایی منعقده با بنیاد مسکن انقلاب اسلامی ',38,93)#s158
    insert_answer_data(' تامین دکلهای حفاری چاههای نفت و گاز دریایی به همراه خدمه  ',38,95)#s159
    insert_answer_data('تامین دکلهای حفاری چاههای نفت و گاز در مناطق خشکی به همراه خدمه ',38,96)#s160
    insert_answer_data('قراردادهای غیرعمرانی منعقده به روش   EPC وPC   ',38,97)#s161
    insert_answer_data('قراردادهاي خدمات شهری و نگهداری فضای سبز',38,147)#s162
    insert_answer_data('تنظیفات ساختمانهای اداری،تجاری،بیمارستانها،مراکزآموزشی ونگهداری تاسیسات',38,149) #s163   
    insert_answer_data(' حمل و نقل مواد نفتی',38,104) #s164
    insert_answer_data(' حمل و نقل بار و کالای بین شهری ',38,104) #s165
    insert_answer_data(' جابه‌جایی مسافر بین شهری و درون شهری ',38,110) #s166
    insert_answer_data(' باطله برداری ، استخراج و تحویل مواد معدنی ',38,150) #s167
    insert_answer_data(' بازار یابی و جذب پیامهای بازرگانی',38,115) #s168
    insert_answer_data(' حمل و نقل ریلی',38,116) #s169
    insert_answer_data(' اجاره فضا و ارایه خدمات تبلیغاتی ',38,153) #s170
    insert_answer_data(' خدمات دریایی ',38,117) #s171
    insert_answer_data(' خن‌کاری در بنادر  ',38,121) #s172
    insert_answer_data(' قراردادهای اجرایی ژئوتکنیک',38,None,True) #s173
    insert_answer_data(' بهره برداری جایگاه سوخت ',38,154) #s174
    insert_answer_data(' خرید یا فروش(تهیه، تامین و تحویل تجهیزات بدون کار اضافی)',38,124) #s175
    insert_answer_data('قرارداد مراکز تعویض پلاک و نقل و انتقال خودرو ',38,None,True) #s176
    insert_answer_data(' اجاره خودرو/ ماشین آلات',38,128) #s177
    insert_answer_data(' پیمان مدیریت',38,None,True) #s178
    insert_answer_data('واگذاری بخشهای مختلف بیمارستان ',38,155) #179
    insert_answer_data(' قرارداد دستمزدي',38,None,True)#s180
    insert_answer_data('قرارداد با مصالح ',38,132)#s181
    insert_answer_data(' قرارداد ارائه خدمات(با استفاده از ماشين‌آلات)',38,137)#s182
    insert_answer_data(' قرارداد داراي تجهيزات خريداري شده از خارج از كشور',38,139)#s183
    insert_answer_data('بلی',39,40)#s184
    insert_answer_data('خیر',39,146)#s185**
    insert_answer_data('بلی',40,41)#s186
    insert_answer_data('خیر',40,146)#s187**
    insert_answer_data('بلی',41,None,True)#s188
    insert_answer_data('خیر',41,None,True)#s189
    insert_answer_data('بلی',42,43)#s190
    insert_answer_data('خیر',42,None,True)#s191
    insert_answer_data('بلی',43,None,True)#s192
    insert_answer_data('خیر',43,None,True)#s193
    insert_answer_data('بلی',44,45)#s194
    insert_answer_data('خیر',44,None,True)#s195
    insert_answer_data('بلی',45,None,True)#s196
    insert_answer_data('خیر',45,None,True)#s197
    insert_answer_data('بلی',46,47)#s198
    insert_answer_data('خیر',46,146)#s199**
    insert_answer_data('بلی',47,48)#s200
    insert_answer_data('خیر',47,146)#s201**
    insert_answer_data('بلی',48,49)#s202
    insert_answer_data('خیر',48,146)#s203***
    insert_answer_data('بلی',49,50)#s204
    insert_answer_data('خیر',49,146)#s205**
    insert_answer_data('بلی',50,None,True)#s206
    insert_answer_data('خیر',50,None,True)#s207
    insert_answer_data('بلی',51,52)#s208
    insert_answer_data('خیر',51,146)#s209***
    insert_answer_data('بلی',52,53)#s210
    insert_answer_data('خیر',52,146)#s211**
    insert_answer_data('بلی',53,None,True)#s212
    insert_answer_data('خیر',53,146)#s213**
    
    insert_answer_data('بلی',54,55)#s214
    insert_answer_data('خیر',54,146)#s215**
    insert_answer_data('بلی',55,56)#s216
    insert_answer_data('خیر',55,146)#s217**
    insert_answer_data('بلی',56,57)#s218
    insert_answer_data('خیر',56,146)#s219**
    insert_answer_data('بلی',57,58)#s220
    insert_answer_data('خیر',57,146)#s221**
    insert_answer_data('بلی',58,59)#s222
    insert_answer_data('خیر',58,146)#s223**
    insert_answer_data('از اسناد مالی و دفاتر قانونی کل سال  دوره اجرای قرارداد بازرسي انجام شده',59,60)#s224
    insert_answer_data('از اسناد مالی و دفاتر قانونی بخشی  از سال  دوره اجرای قرارداد بازرسي انجام شده',59,60)#s225
    insert_answer_data('اسناد مالی و دفاتر قانونی كل دوره قرارداد هنوز بازرسي  نشده',59,61)#s226
    insert_answer_data('دارای دفاتر سفید و نانویس یا عدم همکاری در تمام یا بخشی از سالهای دوره قرارداد',59,146)#s227**
    insert_answer_data('بلی',60,61)#s228
    insert_answer_data('خیر',60,146)#s229**
    insert_answer_data('بلی',61,None,True)#s230
    insert_answer_data('خیر',61,None,True)#s231
    insert_answer_data('بلی',62,63)#s232
    insert_answer_data('خیر',62,146)#s233**
    insert_answer_data('بلی',63,64)#s234
    insert_answer_data('خیر',63,146)#s235**
    insert_answer_data('بلی',64,65)#s236
    insert_answer_data('خیر',64,None,True)#s237
    insert_answer_data('از اسناد مالی و دفاتر قانونی کل سال  دوره اجرای قرارداد بازرسي انجام شده',65,66)#s238
    insert_answer_data('از اسناد مالی و دفاتر قانونی بخشی  از سال  دوره اجرای قرارداد بازرسي انجام شده',65,66)#s239
    insert_answer_data('اسناد مالی و دفاتر قانونی كل دوره قرارداد هنوز بازرسي  نشده',65,None,True)#s240
    insert_answer_data('دارای دفاتر سفید و نانویس یا عدم همکاری در تمام یا بخشی از سالهای دوره قرارداد',65,None,True)#s241
    insert_answer_data('بلی',66,67)#s242
    insert_answer_data('خیر',66,None,True)#s243
    insert_answer_data('بلی',67,None,True)#s244
    insert_answer_data('خیر',67,68)#s245
    insert_answer_data('بلی',68,None,True)#s246
    insert_answer_data('خیر',68,None,True)#s247
    
    insert_answer_data('بلی',69,70)#s248
    insert_answer_data('خیر',69,146)#s249**
    insert_answer_data('بلی',70,71)#s250
    insert_answer_data('خیر',70,146)#s251**
    insert_answer_data('از اسناد مالی و دفاتر قانونی کل سال  دوره اجرای قرارداد بازرسي انجام شده',71,72)#s252
    insert_answer_data('از اسناد مالی و دفاتر قانونی بخشی  از سال  دوره اجرای قرارداد بازرسي انجام شده',71,72)#s253
    insert_answer_data('اسناد مالی و دفاتر قانونی كل دوره قرارداد هنوز بازرسي  نشده',71,None,True)#s254
    insert_answer_data('دارای دفاتر سفید و نانویس یا عدم همکاری در تمام یا بخشی از سالهای دوره قرارداد',71,146)#s255**
    insert_answer_data('بلی',72,73)#s256
    insert_answer_data('خیر',72,146)#s257**
    insert_answer_data('بلی',73,None,True)#s258
    insert_answer_data('خیر',73,74)#s259
    insert_answer_data('بلی',74,None,True)#s260
    insert_answer_data('خیر',74,None,True)#s261
    
    insert_answer_data('طراحي شبكه: مطالعات اوليه و طراحي شبكه هاي رايانه اي  شامل : شبكه داخلي LAN ؛ شبكه گسترده  WANو شبكه بيسيم محلي',75,76)
    insert_answer_data('نصب و راه اندازي شبكه شامل:شبكه(داخلي، گسترده، بيسیم محلي)،كابلكشي شبكه،راه اندازي سرويس نرم افزاري،تجهيزات ActiveوPassiveوامنيت شبكه',75,76)
    insert_answer_data(' نگهداري شبكه: مديريت كاربري شبكه، نگهداري وبه روزرساني سرويسهاي نرم افزاري شبكه،خدمات حفاظـت وامنيت شبكه',75,76)  
    insert_answer_data(' خدمات دسترسي به اينترنت:تامين پهناي باند،ارائه سـرويسهاي امنيتي ،فيلترينگ،كنترل دسترسي،مديريت كاربري',75,76)  
    insert_answer_data('ارائه خدمات كاربردي(ASP) :ميزباني وب، اجاره خدمات نرم افزارهاي كاربردي از طريق وب',75,76)
    insert_answer_data('تجزيه وتحليل سيستمهاي اطلاعاتي كه منجربه توليدمدلها ومسـتندات تحليـل نيازمنديهاي سيستم ميگردد',75,76)
    insert_answer_data(' طراحي نرم افزارهاي سفارشي اعـم از سيسـتمهاي اطلاعاتي كاربردي،نرم افزارهاي عمومي يااختصاصي، سايتهاي وب ',75,76)
    insert_answer_data('ساخت نرم افزارهاي سفارشي اعم از سيستمهاي اطلاعاتي كاربردي،نرم افزارهـاي عمومي يااختصاصي،سايت هاي وب ',75,76)
    insert_answer_data('انتقال نرم افزار سفارشي به محيط مشتري شامل:انتقال اطلاعات،جراي آزمايشي وموازي،آموزش كاربري وراهبري ومواردلازم براي آماده سازي محيط',75,76)
    insert_answer_data('ارائه خدمات پشتيباني فني نرم افزارسفارشي شامل:رفع اشـكال نرم افزار،مديريت تغييرات در دوران بهره برداري،راهبري و مديريت كاربران',75,76)
    insert_answer_data('توليد محتواي ديجيتالي: طراحي و توليد مطالب و محتوا براي ارائه در محيط وب',75,76)
    insert_answer_data(' خدمات آموزشی شامل:شبكه،سيستم عامل،سخت افزار،نرم افزار،امنيت،خدمات زيرساخت وديتاسنتر،مجازي سازي وذخيره سازي،رايانش ابري،IT ',75,76)
    insert_answer_data('مشاوره،امكان سنجي، طراحي، توليد، نصب و پياده سازي سرويسهاي آموزش الكترونيكي',75,76)
    insert_answer_data('نظارت بر پروژه هاي فاوا: ارائه همه يا بخشي از خدمات نظارت بر اجراي پروژه هاي فاوا',75,76)
    insert_answer_data('مديريت طرح پروژه فاواشامل تعريف پروژه ومـديريت فرآينـدارجاع كار،نظارت ،كنترل كمي و كيفي فرآيند تحويـل و يكپارچه سازي نتايج',75,76)
    insert_answer_data('استانداردسازي: تهيه و تدوين استانداردها، دستورالعمل‌ها و ضوابط فني و مديريتي فاوا',75,76)
    insert_answer_data('تهيه طرح جامع فاوا،تدوين معماري سازماني فناوري اطلاعات،برنامه ريزي استراتژيك سيستم اطلاعاتي،تدوين استراتژي فناوري اطلاعات،تهيه طرح استراتژيك در زمينه فاوا ',75,76)
    insert_answer_data('امكان سنجي ومشاوره پروژه فاوا: امكان سنجي،انتخاب تكنولوژي، تهيه شـرح خدمات وارجـاع كـار (RFP ) براي پروژه هاي فاوا',75,76)
    insert_answer_data('طراحـي نظامها و فرآيندهاي مديريت فـاوا، شـامل نظام مديريت امنيت، نظامهاي تضمين كيفيت، نظامهاي مديريت اسناد در سازمانها',75,76)
    insert_answer_data('پياده سازي نظامها و فرآيندهاي مديريت فاوا شامل: نظامهاي مـديريت امنيـت، نظامهاي تضمين كيفيت، نظامهاي مديريت اسناد در سازمانها',75,76)
    insert_answer_data('پايش،ارزيابي و مميزي نظامهاو فرآيندهاي مديريت فـاوا شـامل:نظامهاي مديريت امنيت، نظامهاي تضمين كيفيت، نظامهاي مديريت اسناد در سازمانها',75,76)
    insert_answer_data('خدمات امنيت اطلاعات:ارتقاءامنيت،ارزيابي واجـراي آزمونهاي امنيتـي زيرسـاخت،شـبكه،سيستمهاونرم افزارها،قفلهاي نرم افزاري وسخت افزاري',75,76)
    insert_answer_data('خدمات مركز داده:مشاوره،طراحي،نظارت،تدوين مستندات، تجهيز، پياده سازي، پشتيباني، نگهداري و آمـوزش مراكز داده',75,76)
    insert_answer_data('تعمیر ونگهداری سخت افزار:تعمیر،نگهداری وپشتیبانی فنی انواع تجهیزات وقطعات سخت افزاری،سرور،سوئیچ و ذخیره ساز',75,76)
    insert_answer_data('تدوين استانداردها،صدور گواهينامه خدمات كيفيت و خدمات تست و آزمون نرم افزار و سخت افزار',75,76)
    insert_answer_data('طراحي وتوسعه وب،طراحي وپياده سازي بانك اطلاعاتي وب،گرافيك وب،بهينه سازي وب سايتهاي ويژه موتور جستجو،پشتيباني وبسايت،نگهداري ومديريت وبسايت',75,76)
    insert_answer_data('طراحي و توليد نرم افزارهاي موبايل و پشتيباني نرم افزارهاي موبايل',75,76)
    insert_answer_data('مشاوره رايانش ابري و داده هاي كلان در حوزه فناوري اطلاعات و ارتباطات',75,76)
    insert_answer_data('شبكه بيسيم: طراحي، تامين تجهيزات، نصب و راه اندازي، پشتيباني و نگهداري شبكه بيسيم محلي',75,76)
    insert_answer_data('امنيت شبكه: نصب، راه اندازي و نگهداري سخت افزار و نرم افزارهاي امنيت شبكه',75,76)
    insert_answer_data('سایر',75,146)#s292**
    insert_answer_data('بلی',76,77)#s293
    insert_answer_data('خیر',76,146)#s294**
    insert_answer_data('بلی',77,78)#s295
    insert_answer_data('خیر',77,146)#s296**
    insert_answer_data('بلی',78,79)#s297
    insert_answer_data('خیر',78,146)#s298**
    insert_answer_data('بلی',79,71)#s299
    insert_answer_data('خیر',79,146)#s300**
    
    insert_answer_data('بلی',80,76)#s301
    insert_answer_data('خیر',80,146)#s302**
    
    insert_answer_data('بلی',81,76)#s303
    insert_answer_data('خیر',81,146)#s304**
    
    insert_answer_data('سازمان تامین اجتماعی',82,76)#305
    insert_answer_data('سایر',82,146)#s306**
    
    insert_answer_data('حسابرسي مالي',83,76)
    insert_answer_data('حسابرسي داخلي و عملياتي',83,76)
    insert_answer_data('بازرسی از دفاتر قانونی',83,76)
    insert_answer_data('خدمات تنظیم صورتهای مالی',83,76)
    insert_answer_data('اصلاح حساب و حسابداری',83,76)
    insert_answer_data('طرح و اجرای سیستمهای مالی اعم از دستی یا مکانیزه',83,76)
    insert_answer_data('تعیین ارزش سهام شرکتها و تعهدپذیره نویسی اوراق مشارکت',83,76)
    insert_answer_data('سایر',83,146)#314**
    
    insert_answer_data('تعهد پذیره نویسی و بازار‌گردانی اوراق بهادار',84,76)
    insert_answer_data('ارائه خدمات مدیریت دارایی‌ها',84,76)
    insert_answer_data('خدمات مرتبط باصندوق‌های سرمایه‌گذاری واداره آنها و سرمایه‌گذاری در آن‌ها',84,76)
    insert_answer_data('سبدگردانی',84,76)
    insert_answer_data('ارائه خدمات مشاوره پذیرش',84,76)
    insert_answer_data('مشاوره سرمایه‌گذاری',84,76)
    insert_answer_data('مشاوره عرضه',84,76)
    insert_answer_data('پشتیبانی و پردازش اطلاعات مالی',84,76)
    insert_answer_data('طراحی شیوه تامین مالی از طریق انتشاراوراق بهاداروفروش محصولات در بورس کالای ایرانی',84,76)
    insert_answer_data('سایر',84,146)#324**
    
    insert_answer_data('کارگزاری،معامله گری وبازارگردانی شامل معامله اوراق بهادار،معامله کالای پذیرفته شده،بازارسازی وبازارگردانی اوراق بهادار ',85,76)
    insert_answer_data('خدمات مالی و مشاوره‌ای شامل مدیریت صندوق‌ سرمایه‌گذاری،نمایندگی ناشر برای ثبت اوراق بهادار و دریافت مجوز عرضه',85,76)
    insert_answer_data('بازاریابی برای فروش اوراق بهادار، سبد گردانی اوراق بهادار',85,76)
    insert_answer_data('مشاوره واموراجرایی برای پذیرش اوراق بهادار یا کالا در بورس‌ یا بازارهای خارج از بورس به نمایندگی از ناشر یا عرضه کننده کالا',85,76)
    insert_answer_data('مشاوره درزمینه‌های قیمت گذاری و روش فروش و عرضه اوراق بهادار',85,76)
    insert_answer_data('طراحی اوراق',85,76)
    insert_answer_data('خرید و فروش یا نگهداری اوراق',85,76)
    insert_answer_data('سرمايه گذاري',85,76)
    insert_answer_data('مدیریت ریسک',85,76)
    insert_answer_data('ادغام، تملک، تغییر و تجدید ساختار سازمانی و مالی شرکت‌ها ',85,76)
    insert_answer_data('طراحي و تشکیل نهادهای مالی',85,76)
    insert_answer_data('سایر',85,146)#336**
    
    insert_answer_data('حمل بار و یا مسافرتوسط هواپیما و بالگرد',86,76)
    insert_answer_data('حق بهره برداری از تعدادی صندلی در هرپرواز',86,76)
    insert_answer_data('اجاره هواپیما و بالگرد',86,76)
    insert_answer_data('سایر',86,146)#340**
    
    insert_answer_data('کارفرما شرکتهای تابعه وزارت نیرو(برق منطقه‌ای،انرژی‌های تجدیدپذیر وبهره‌وری انرژی،شرکت تولید نیروی برق حرارتی) مي‌باشد.',87,88)
    insert_answer_data('مقاطعه کار دارای مجوز رسمی و يا پروانه بهره برداری تولید برق مي‌باشد.',87)
    insert_answer_data('مقاطعه کار دارای پروانه خرده‌فروشی برق می‌باشد.',87,89)
    insert_answer_data('نیروگاه بخش دولتی یا خصوصی',88,76)
    insert_answer_data('سایر',88,146)#345**
    insert_answer_data('خريد از بورس يا نيروگاه انجام شده',89,76)
    insert_answer_data('سایر',89,146)#347**
    
    insert_answer_data('بلی',90,79)#s348
    insert_answer_data('خیر',90,146)#s349**
    
    insert_answer_data('بلی',91,None,True)#350
    insert_answer_data('خیر',91,None,True)#351
    
    insert_answer_data('بنیاد مسکن انقلاب اسلامی',92,None,True)#352
    insert_answer_data('سایر',92,None,True)#353
    insert_answer_data('بنیاد مسکن انقلاب اسلامی',93,94)#354
    insert_answer_data('سایر',93,None,True)#355
    insert_answer_data(' به عهده پیمانکار',94,None,True)#356
    insert_answer_data('به عهده کارفرما',94,None,True)#357
    insert_answer_data('بلی',95,None,True)#358
    insert_answer_data('خیر',95,146)#359**
    insert_answer_data('بلی',96,None,True)#360
    insert_answer_data('خیر',96,146)#361**
    
    insert_answer_data('بلی',97,54)#362
    insert_answer_data('خیر',97,98)#363
    insert_answer_data('بلی',98,99)#364
    insert_answer_data('خیر',98,146)#365 
    insert_answer_data('بلی',99,100)#366
    insert_answer_data('خیر',99,146)#367 ****
    insert_answer_data('بلی',100,101)#368
    insert_answer_data('خیر',100,146)#369 ****
    insert_answer_data('بلی',101,146)#370 ****
    insert_answer_data('خیر',101,102)#371 
    insert_answer_data('بلی',102,103)#372 ***
    insert_answer_data('خیر',102,None,True)#373
    insert_answer_data('بلی',103,146)#374 ****
    insert_answer_data('خیر',103,None,True)#375
    
    insert_answer_data(' کلیه رانندگان خودمالک و مشمول بیمه رانندگان بوده و کارگاه فاقد لیست در ردیف پیمان میباشد',104,105)
    insert_answer_data('تعدادی از  رانندگان خودمالک و تعدادی در استخدام پیمانکار می‌باشند(در ردیف پیمان لیست ارسال شده) ',104,106)
    insert_answer_data('کلیه رانندگان در استخدام می‌باشندو لیست آنها در ردیف پیمان ارسال شده',104,None,True)#378
    insert_answer_data('بلی',105,None,True)#379
    insert_answer_data('خیر',105,None,True)#380
    insert_answer_data('بلی',106,107)#381
    insert_answer_data('خیر',106,None,True)#382
    insert_answer_data('بلی',107,None,True)#383
    insert_answer_data('خیر',107,None,True)#384
    insert_answer_data('بلی',108,109)#385
    insert_answer_data('خیر',108,104)#386
    insert_answer_data('بلی',109,None,True)#387
    insert_answer_data('خیر',109,None,True)#388
    
    insert_answer_data(' کلیه رانندگان خودمالک و مشمول بیمه رانندگان بوده و کارگاه فاقد لیست در ردیف پیمان میباشد',110,111)
    insert_answer_data('تعدادی از  رانندگان خودمالک و تعدادی در استخدام پیمانکار می‌باشند(در ردیف پیمان لیست ارسال شده) ',110,112)
    insert_answer_data('کلیه رانندگان در استخدام می‌باشندو لیست آنها در ردیف پیمان ارسال شده',110,None,True)#391
    insert_answer_data('بلی',111,None,True)#392
    insert_answer_data('خیر',111,None,True)#393
    insert_answer_data('بلی',112,113)#394
    insert_answer_data('خیر',112,None,True)#395
    insert_answer_data('بلی',113,None,True)#396
    insert_answer_data('خیر',113,None,True)#397
    #حقیقی  41 داخل 
    insert_answer_data(' نقشه‌برداري ',114,None,True)#s398
    insert_answer_data('قراردادهاي اجرایی منعقده با بنیاد مسکن انقلاب اسلامی ',114,93)#399
    insert_answer_data(' قراردادهاي تامین دکلهای حفاری چاههای نفت و گاز دریایی به همراه خدمه  ',114,95)#400
    insert_answer_data('تامین دکلهای حفاری چاههای نفت و گاز در مناطق خشکی به همراه خدمه ',114,96)#s401
    insert_answer_data('قراردادهای غیرعمرانی منعقده به روش   EPC وPC   ',114,97)#s402
    insert_answer_data('قراردادهاي خدمات شهری و نگهداری فضای سبز',114,147)#s403
    insert_answer_data('تنظیفات ساختمانهای اداری،تجاری،بیمارستانها،مراکزآموزشی ونگهداری تاسیسات',114,149) #s404
    insert_answer_data(' قراردادهای حمل و نقل مواد نفتی',114,108) #s405
    insert_answer_data('قراردادهای حمل و نقل بار و کالای بین شهری ',114,104) #s406
    insert_answer_data('قراردادهای جابه‌جایی مسافر بین شهری و درون شهری ',114,110) #s407
    insert_answer_data(' قراردادهاي باطله برداری ، استخراج و تحویل مواد معدنی ',114,150) #s408
    insert_answer_data(' قراردادهاي بازار یابی و جذب پیامهای بازرگانی',114,115) #s409
    insert_answer_data(' قراردادهاي حمل و نقل ریلی',114,116) #s410
    insert_answer_data('قراردادهاي اجاره فضا و ارایه خدمات تبلیغاتی  ',114,153) #s411
    insert_answer_data(' قراردادهاي خدمات دریایی ',114,117) #s412
    insert_answer_data('قراردادهاي خن‌کاری در بنادر  ',114,121) #s413
    insert_answer_data(' قراردادهای اجرایی ژئوتکنیک',114,None,True) #s414
    insert_answer_data(' قراردادهای بهره برداری جایگاه سوخت ',114,154) #s415
    insert_answer_data(' قرارداد خرید  فروش(تهیه، تامین و تحویل تجهیزات بدون کار اضافی)',114,126) #s416
    insert_answer_data('قرارداد مراکز تعویض پلاک و نقل و انتقال خودرو ',114,None,True) #s417
    insert_answer_data(' اجاره خودرو/ ماشین آلات',114,128) #s418
    insert_answer_data(' پیمان مدیریت',114,None,True) #s419
    insert_answer_data('واگذاری بخشهای مختلف بیمارستان ',114,155) #420
    insert_answer_data(' قرارداد دستمزدي',114,None,True)#s421
    insert_answer_data('قرارداد با مصالح ',114,132)#s422
    insert_answer_data(' قرارداد ارائه خدمات(با استفاده از ماشين‌آلات)',114,137)#s423
    insert_answer_data(' قرارداد داراي تجهيزات خريداري شده از خارج از كشور',114,139)#s424
    
    insert_answer_data('صدا و سیما',115,None,True)#425
    insert_answer_data('سایر',115,None,True)#s426
    
    insert_answer_data('شرکت راه‌آهن جمهوری اسلامی',116,None,True)#427
    insert_answer_data('سایر',116,None,True)#s428
    
    insert_answer_data('کشتی متعلق به کارفرما(واگذارنده)',117,118)
    insert_answer_data('کشتی متعلق به پیمانکار',117,120)
    insert_answer_data('راهبری به همراه نگهداری و تعمیرات کشتی ',118,119)
    insert_answer_data('تامین نیروی انسانی ',118,None,True)#432
    insert_answer_data('پیمانکار',119,None,True)#433
    insert_answer_data('کارفرما(واگذارنده)',119,None,True)#434
    
    insert_answer_data(' واگذاری کشتی به همراه خدمه مورد نیاز ',120,None,True)#435
    insert_answer_data('سایر',120,None,True)#436
    
    insert_answer_data('بلی',121,None,True)#437
    insert_answer_data('خیر',121,None,True)#438
    
    insert_answer_data('خرید از خارج کشور',122,123)#439
    insert_answer_data('خرید از سایر فروشندگان داخلی',122,None,True)#440
    
    insert_answer_data('بلی',123,None,True)#441
    insert_answer_data('خیر',123,None,True)#442
    
    insert_answer_data(' ساخت داخل کارگاه ثابت تولیدی، فنی، صنعتی و مهندسی',124,54)#443
    insert_answer_data('خرید از خارج کشور',124,125)#444
    insert_answer_data('خرید از سایر فروشندگان داخلی',124,None,True)#445
    
    insert_answer_data('بلی',125,None,True)#446
    insert_answer_data('خیر',125,None,True)#447
    
    insert_answer_data(' ساخت داخل کارگاه ثابت تولیدی، فنی، صنعتی و مهندسی',126,46)#448
    insert_answer_data('خرید از خارج کشور',126,127)#449
    insert_answer_data('خرید از سایر فروشندگان داخلی',126,None,True)#450
    
    insert_answer_data('بلی',127,None,True)#451
    insert_answer_data('خیر',127,None,True)#452
    
    insert_answer_data('تامین  كل نیروی انسانی مورد نیاز با پیمانکار',128,None,True)#453
    insert_answer_data('تامین بخشی از نیروی انسانی مورد نیاز با پیمانکار',128,129)#454
    insert_answer_data('تامین کل نیروی انسانی مورد نیاز با کارفرما',128,131)#455
    
    insert_answer_data('بلی',129,130)#456
    insert_answer_data('خیر',129,None,True)#457
    insert_answer_data('دارای سابقه مرتبط در دوره قرارداد',130,None,True)#458
    insert_answer_data('فاقد سابقه مرتبط در دوره قرارداد',130,None,True)#459
    insert_answer_data('دارای سابقه مرتبط در دوره قرارداد',131,None,True)#460
    insert_answer_data('فاقد سابقه مرتبط در دوره قرارداد',131,None,True)#461
    
    insert_answer_data('تامين كليه مصالح با پيمانكار',132,133)#462
    insert_answer_data('تامين كليه مصالح با کارفرما',132,None,True)#463
    insert_answer_data('تامين بخشي از مصالح با کارفرما و بخشي با پیمانکار',132,134)#464
    
    insert_answer_data('بزرگتر یا مساوی 50%',133,None,True)#465
    insert_answer_data('کمتر از 50%',133,None,True)#466
    
    insert_answer_data('مصالح انحصاري و اختصاصي در قراردادهاي آسانسور و تاسیسات ',134,135)#467
    insert_answer_data('آهن آلات در قراردادهای سوله سازی ',134,135)#468
    insert_answer_data('پارچه در قراردادهای دوخت و دوز ',134,135)#469
    insert_answer_data('آسفالت در قراردادهای جاده سازی و آسفالت كاري',134,135)#470
    insert_answer_data('موکت و کف پوش و کابینت ',134,135)#471
    insert_answer_data('ساير مصالح',134)#472
    
    insert_answer_data('بزرگتر یا مساوی 50%',135,None,True)#473
    insert_answer_data('کمتر از 50%',135,None,True)#474
    
    insert_answer_data('بلی',136,None,True)#475
    insert_answer_data('خیر',136,None,True)#476
    
    insert_answer_data('بلی',137,138)#477
    insert_answer_data('خیر',137,None,True)#478
    
    insert_answer_data('ارائه خدمات به صورت كاملا مكانيكي ',138,None,True)#479
    insert_answer_data('بخشی از قرارداد مکانیکی و بخشی دستمزدی ',138,None,True)#480
    
    insert_answer_data('به نام پیمانکارو مورد تایید کارفرما (واگذارنده) ',139,140)#481
    insert_answer_data('به نام کارفرما (واگذارنده) ',139,143)#482
    
    insert_answer_data('بلی',140,141)#483
    insert_answer_data('خیر',140,142)#484
    
    insert_answer_data('بزرگتر یا مساوی 50%',141,None,True)#485
    insert_answer_data('کمتر از 50%',141,None,True)#486
    
    insert_answer_data('بلی',142,None,True)#487
    insert_answer_data('خیر',142,None,True)#488
    
    insert_answer_data('بلی',143,144)#489
    insert_answer_data('خیر',143,145)#490
    
    insert_answer_data('بزرگتر یا مساوی 50%',144,None,True)#491
    insert_answer_data('کمتر از 50%',144,None,True)#492
    
    insert_answer_data('بلی',145,138)#493
    insert_answer_data('خیر',145,None,True)#494
    
    insert_answer_data('قرارداد دستمزدي',146,None,True)#495
    insert_answer_data('قرارداد با مصالح ',146,132)
    insert_answer_data(' قرارداد ارائه خدمات(با استفاده از ماشين‌آلات)',146,137)
    insert_answer_data(' قرارداد داراي تجهيزات خريداري شده از خارج از کشور',146,139)
    
    insert_answer_data(' خدمات شهری :تنظیفات، جمع آوری و حمل پسماند ',147,148)
    insert_answer_data('نگهداری فضای سبز ',147,148)
    insert_answer_data('سایر',147,146)#501
    
    insert_answer_data('بلی',148,None,True)#502
    insert_answer_data('خیر',148,None,True)#503
    
    insert_answer_data('بلی',149,None,True)#504
    insert_answer_data('خیر',149,None,True)#505
    
    insert_answer_data('معادن سنگ آهنِ (چادر ملو، چغارت، مرکزی، گلگهر) ',150,151)
    insert_answer_data('معادن مسِ (اهر، میدوک، سرچشمه)',150,151)
    insert_answer_data('معادن رویِ (انگوران، مهدی آباد، کالسیمین) ',150,151)
    insert_answer_data('سایر معادن',150,146)
    insert_answer_data('به عهده پیمانکار',151,152)
    insert_answer_data('به عهده کارفرما(واگذارنده)',151,146)
    insert_answer_data('به عهده پیمانکار',152,None,True)#512
    insert_answer_data('به عهده کارفرما(واگذارنده)',152,146)
    
    insert_answer_data(' شهرداری',153,None,True)#514
    insert_answer_data('سازمان زیباسازی',153,None,True)#515
    insert_answer_data('وزارت مسکن و شهرسازی',153,None,True)#516
    insert_answer_data('سایر',153,None,True)#517
    
    insert_answer_data('جایگاه CNG  ',154,None,True)#518
    insert_answer_data('جایگاه بنزین',154,None,True)#519
    
    insert_answer_data('مبلغی از قرارداد بابت اجاره محل به بیمارستان پرداخت میشود',155,156)
    insert_answer_data('از محل درآمد درصدي سهم  بیمارستان می باشد',155,157)
    insert_answer_data('به عهده پیمانکار',156,None,True)#522
    insert_answer_data('به عهده کارفرما(واگذارنده)',156,None,True)#523
    insert_answer_data('به عهده پیمانکار',157,None,True)#524
    insert_answer_data('به عهده کارفرما(واگذارنده)',157,None,True)#525
    
    

#--------------------------------------------------------------------------------------    
#results
#بخش عمرانی
    insert_result_data('با توجه به نوع قرارداد اصلی برای ادامه با شروع مجدد تعیین ضریب، گزینه غیرعمرانی را انتخاب نمایید. ',5)
    insert_result_data('در صورت احراز عمرانی بودن قرارداد اصلی و تایید قرارداد فرعی توسط کارفرمای اصلی، به تبعیت از قرارداد اصلی ضریب قرارداد= 14% (حق بیمه= 14%مبلغ قرارداد وبیمه بیکاری=1.6% مبلغ قرارداد میباشد). ولیکن با توجه به پرداخت حق بیمه در قرارداد اصلی تا سقف 15.6% مبلغ قرارداد، حق بیمه ای دریافت نمیگردد و صرفا در صورتیکه حق بیمه لیستهای ارسالی بیش از حق بیمه طبق ضریب باشد یا لیستها خارج از دوره قرارداد ارسال شده باشد، مابه التفاوت آن اخذ میگردد. ',7)
    insert_result_data('در صورت احراز عمرانی بودن قرارداد اصلی و تایید قرارداد فرعی توسط کارفرمای اصلی، به تبعیت از قرارداد اصلی ضریب قرارداد= 6% (حق بیمه= 6%مبلغ قرارداد وبیمه بیکاری=0.6% مبلغ قرارداد میباشد). ولیکن با توجه به پرداخت حق بیمه در قرارداد اصلی تا سقف 6.6% مبلغ قرارداد، حق بیمه ای دریافت نمیگردد و صرفا در صورتیکه حق بیمه لیستهای ارسالی بیش از حق بیمه طبق ضریب باشد یا لیستها خارج از دوره ارسال شده باشد مابه التفاوت آن اخذ میگردد. ',8)
    insert_result_data('با توجه به محل اجرای قرارداد خارج ازمرزهای کشورمشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',9)
    insert_result_data('با توجه به ملیت کارفرما قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',11)
    insert_result_data('با توجه به ملیت مجری قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',13)
    insert_result_data('شخصیت مهندس مشاور نمیتواند حقیقی باشد. برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',17)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود. ',19)
    insert_result_data('ضریب قرارداد : 14% (حق بیمه= 14% مبلغ قراردادوبیمه بیکاری= 1.6 %مبلغ قرارداد مجموعا 15.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای ارسالی قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 15.6% کارکرد مطالبه و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.ضمنا چنانچه هیچگونه لیستی با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',22)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود. ',24)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود. ',25)
    insert_result_data('ضریب قرارداد : 6% (حق بیمه= 6% مبلغ قراردادوبیمه بیکاری= 0.6 %مبلغ قرارداد مجموعا 6.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 6.6% کارکرد مطالبه میشود و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.چنانچه هیچگونه لیستی  با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه  و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه  میگردد.',28)
    insert_result_data('ضریب قرارداد : 14% (حق بیمه= 14% مبلغ قراردادوبیمه بیکاری= 1.6 %مبلغ قرارداد مجموعا 15.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای ارسالی قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 15.6% کارکرد مطالبه و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.ضمنا چنانچه هیچگونه لیستی با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',29)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',34)
    insert_result_data('ضریب قرارداد : 14% (حق بیمه= 14% مبلغ قراردادوبیمه بیکاری= 1.6 %مبلغ قرارداد مجموعا 15.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای ارسالی قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 15.6% کارکرد مطالبه و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.ضمنا چنانچه هیچگونه لیستی با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',35)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',36)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',38)
    insert_result_data('ضریب قرارداد : 14% (حق بیمه= 14% مبلغ قراردادوبیمه بیکاری= 1.6 %مبلغ قرارداد مجموعا 15.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای ارسالی قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 15.6% کارکرد مطالبه و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.ضمنا چنانچه هیچگونه لیستی با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',39)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',40)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',41)
    insert_result_data('ضریب قرارداد : 14% (حق بیمه= 14% مبلغ قراردادوبیمه بیکاری= 1.6 %مبلغ قرارداد مجموعا 15.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای ارسالی قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 15.6% کارکرد مطالبه و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.ضمنا چنانچه هیچگونه لیستی با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',42)
    insert_result_data('ضریب قرارداد : 6% (حق بیمه= 6% مبلغ قراردادوبیمه بیکاری= 0.6 %مبلغ قرارداد مجموعا 6.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 6.6% کارکرد مطالبه میشود و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.چنانچه هیچگونه لیستی  با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه  و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه  میگردد.',43)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',48)
    insert_result_data('ضریب قرارداد : 6% (حق بیمه= 6% مبلغ قراردادوبیمه بیکاری= 0.6 %مبلغ قرارداد مجموعا 6.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 6.6% کارکرد مطالبه میشود و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.چنانچه هیچگونه لیستی  با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه  و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه  میگردد.',49)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',50)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',52)
    insert_result_data('ضریب قرارداد : 6% (حق بیمه= 6% مبلغ قراردادوبیمه بیکاری= 0.6 %مبلغ قرارداد مجموعا 6.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 6.6% کارکرد مطالبه میشود و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.چنانچه هیچگونه لیستی  با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه  و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه  میگردد.',53)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',54)
    insert_result_data('قرارداد مشمول ضوابط طرحهای عمرانی  نبوده لذا برای ادامه با شروع مجدد تعیین ضریب، ازبخش غیرعمرانی استفاده شود.',55)
    insert_result_data('ضریب قرارداد : 6% (حق بیمه= 6% مبلغ قراردادوبیمه بیکاری= 0.6 %مبلغ قرارداد مجموعا 6.6% مبلغ قرارداد).\n لازم به توضیح است در هنگام محاسبه ابتدا مجموع لیستهای قرارداد اصلی و پیمانکاران فرعی با ضریب قرارداد مقایسه میگردد چنانچه ضریب بیشتر باشد معادل 6.6% کارکرد مطالبه میشود و درصورتیکه لیست بیشتر باشد مبنای محاسبه لیستهای ارسالی میباشد.چنانچه هیچگونه لیستی  با ردیف پیمان ارسال نشده باشد ، مبلغی معادل 10% مجموع حق بیمه  و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه  میگردد.',56)

#بخش غیرعمرانی

    insert_result_data('اجرای انفرادی قرارداد منوط به انجام بازرسی تحقیقی و تایید مراتب توسط بازرسان سازمان میباشد.\n بدیهی است در صورت تایید اجرای پیمان به صورت انفرادی قرارداد مشمول ماده 38 قانون نمیباشد.',188)
    insert_result_data('قرارداد مشمول ماده 38 قانون نمی‌باشد',189)
    insert_result_data('با توجه به تامین محل توسط کارفرما قرارداد از مصادیق ماده 47 قانون نبوده و مشمول ضریب میگردد.\nضريب= 15درصد (حق بيمه طبق ضريب = 15 درصد ناخالص كاركرد وبيمه بيكاري طبق ضریب =  1/9 حق بيمه)\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد بوده و معادل 16.67% کارکرد مورد مطالبه قرار میگیرد درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',191)
    insert_result_data('با توجه به ارسال لیست حق بیمه پرسنل در بازه زمانی قرارداد و انجام بازرسی از محل اجرای قرارداد، بابت قرارداد ضریبی اعمال نمیگردد و صرفا با پرداخت بدهي قطعی سال  دوره اجرای قرارداد، مفاصاحساب صادر میگردد.',192)
    insert_result_data('با توجه به عدم ارسال لیست پرسنل به صورت کامل یا عدم بازرسی در بازه زمانی قرارداد:\n حق بيمه طبق ضريب= 40 درصد ناخالص كاركرد با ماخذ7%و 60 درصد ناخالص كاركرد با ماخذ 15% و بيمه بيكاري طبق ضريب= 1/9 حق بيمه\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',193)
    insert_result_data('ضريب= 7درصد (حق بيمه طبق ضريب = 7 درصد ناخالص كاركرد وبيمه بيكاري طبق ضریب =   1/9 حق بيمه)\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد بوده و معادل 7.8% کارکرد مورد مطالبه قرار میگیرد درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',195)    
    insert_result_data('قرارداد مشمول ماده 38 قانون نمیباشد',196)
    insert_result_data('ضريب= 7درصد (حق بيمه طبق ضريب = 7 درصد ناخالص كاركرد وبيمه بيكاري طبق ضریب =   1/9 حق بيمه)\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد بوده و معادل 7.8% کارکرد مورد مطالبه قرار میگیرد درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',197)
    insert_result_data('با تفکیک مبلغ ناخالص كاركرد به (عمليات كارگاه ثابت و حمل وعمليات  خارج از كارگاه ثابت):\n1- نسبت به مجموع كاركرد کار در كارگاه ثابت و خارج از كارگاه ثابت ضریب اعمال نمیگردد. \n2- صرفا ضریب 7% نسبت به مبلغ  حمل اعمال میگردد. (حق بیمه =  7% مبلغ حمل و بيمه بيكاري = 1/9 حق بیمه) \nضمنا جهت صدور مفاصاحساب میبایست بدهي قطعی سال  دوره اجرای قرارداد، پرداخت گردد.',206)
    insert_result_data('با تفکیک مبلغ ناخالص كاركرد به (عمليات كارگاه ثابت و حمل وعمليات  خارج از كارگاه ثابت) :\n1-نسبت به كاركرد کار در كارگاه ثابت ضریب اعمال نمیگردد\n. 2- ضریب 7% نسبت به مبلغ  حمل اعمال میگردد\n. 3- جهت کارکرد عملیات خارج از کارگاه ثابت میبایست با شروع مجدد تعیین ضریب، با توجه به موضوع عملیات خارج از کارگاه (دستمزدی،با مصالح و ارائه خدمات با ماشین آلات و..) ضریب تعیین گردد.\n ضمنا جهت صدور مفاصاحساب میبایست بدهي قطعی سال  دوره اجرای قرارداد، پرداخت گردد.',207)
    insert_result_data('با توجه به ارسال لیست حق بیمه پرسنل در بازه زمانی قرارداد و انجام بازرسی از محل اجرای قرارداد، بابت قرارداد ضریبی اعمال نمیگردد و صرفا با پرداخت بدهي قطعی سال  دوره اجرای قرارداد، مفاصاحساب صادر میگردد.',212) 

    insert_result_data('1-در صورت عدم بازرسی از دفاتر قانونی در تمام یا بخشی از سالهای دوره قرارداد: اخذ تعهدنامه بازرسی از دفاتر قانونی بابت سالهای فاقد بازرسی \n2-با تفکیک مبلغ ناخالص كاركرد به (عمليات كارگاه ثابت و حمل وعمليات  خارج از كارگاه ثابت):\n- نسبت به مجموع كاركرد کار در كارگاه ثابت و کار خارج از كارگاه ثابت ضریب اعمال نمیگردد \n- صرفا ضریب 7% نسبت به مبلغ  حمل اعمال میگردد. (حق بیمه =  7% مبلغ حمل و بيمه بيكاري = 1/9 حق بیمه) \nضمنا جهت صدور مفاصاحساب میبایست در سال دوره اجرای  قرارداد بدهي قطعی سال  دوره اجرای قرارداد كليه كارگاهها اعم از دفترمركزي،نمايندگي،شعبه وانبار پرداخت گردد.',230)
    insert_result_data('1-در صورت عدم بازرسی از دفاتر قانونی در تمام یا بخشی از سالهای دوره قرارداد: اخذ تعهدنامه بازرسی از دفاتر قانونی بابت سالهای فاقد بازرسی \n2-با تفکیک مبلغ ناخالص كاركرد به (عمليات كارگاه ثابت و حمل وعمليات  خارج از كارگاه ثابت):\n- نسبت به كاركرد کار در كارگاه ثابت ضریب اعمال نمیگردد \n- ضریب 7% نسبت به مبلغ  حمل اعمال میگردد  \n-جهت کارکرد عملیات خارج از کارگاه ثابت میبایست با شروع مجدد تعیین ضریب، با توجه به موضوع عملیات خارج از کارگاه (دستمزدی،با مصالح و ارائه خدمات با ماشین آلات و..) ضریب تعیین گردد - \nضمنا جهت صدور مفاصاحساب میبایست در سال دوره اجرای  قرارداد بدهي قطعی سال  دوره اجرای قرارداد كليه كارگاهها اعم از دفترمركزي،نمايندگي،شعبه وانبار پرداخت گردد.',231)
 
    insert_result_data(' با توجه به عدم ارسال لیست و یا عدم بازرسی مشمول ضریب میگردد: \nضريب= 7درصد (حق بيمه طبق ضريب = 7 درصد ناخالص كاركرد وبيمه بيكاري طبق ضریب =   1/9 حق بيمه)\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد بوده و معادل 7.8% کارکرد مورد مطالبه قرار میگیرد درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',237)
    insert_result_data('با اخذ تعهدنامه بازرسی از دفاتر قانونی بابت سالهای فاقد بازرسی، بابت قرارداد ضریبی اعمال نمیگردد و جهت صدور مفاصاحساب میبایست در سال دوره اجرای  قرارداد بدهي قطعی سال  دوره اجرای قرارداد كليه كارگاهها اعم از دفترمركزي،نمايندگي،شعبه وانبار پرداخت گردد.',240)
    insert_result_data('با توجه به وضعیت دفاتر قانونی مشمول ضریب میگردد: \nضريب= 7درصد (حق بيمه طبق ضريب = 7 درصد ناخالص كاركرد وبيمه بيكاري طبق ضریب =   1/9 حق بيمه)\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد بوده و معادل 7.8% کارکرد مورد مطالبه قرار میگیرد درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',241)
    insert_result_data('با توجه به عدم درج قرارداد در فهرست وجوه درآمدی مشمول ضریب میگردد: \nضريب= 7درصد (حق بيمه طبق ضريب = 7 درصد ناخالص كاركرد وبيمه بيكاري طبق ضریب =   1/9 حق بيمه)\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد بوده و معادل 7.8% کارکرد مورد مطالبه قرار میگیرد درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',243)
    insert_result_data('با اخذ تعهدنامه بازرسی از دفاتر قانونی بابت سالهای فاقد بازرسی، بابت قرارداد ضریبی اعمال نمیگردد و جهت صدور مفاصاحساب میبایست در سال دوره اجرای  قرارداد بدهي قطعی سال  دوره اجرای قرارداد كليه كارگاهها اعم از دفترمركزي،نمايندگي،شعبه وانبار پرداخت گردد.',244)
    insert_result_data('1-نسبت به مابه التفاوت مبلغ   صورت وجوه درآمدي ومبلغ ناخالص كاركرد میبایست با شروع مجدد تعیین ضریب، با توجه به موضوع عملیات (دستمزدی،با مصالح و ارائه خدمات با ماشین آلات و..) ضریب تعیین گردد\n2- به مبلغ ناخالص كاركرد ضریبی اعمال نمیگردد.\n3- جهت صدور مفاصاحساب میبایست در سال دوره اجرای  قرارداد بدهي قطعی سال  دوره اجرای قرارداد كليه كارگاهها اعم از دفترمركزي،نمايندگي،شعبه وانبار و همچنین حق بیمه مابه التفاوت مبلغ  صورت وجوه درآمدي ومبلغ ناخالص كاركرد پرداخت گردد.',246)
    insert_result_data('بابت قرارداد ضریبی اعمال نمیگردد و جهت صدور مفاصاحساب میبایست در سال دوره اجرای  قرارداد بدهي قطعی سال  دوره اجرای قرارداد كليه كارگاهها اعم از دفترمركزي،نمايندگي،شعبه وانبار پرداخت گردد.',247)
 
    insert_result_data('با اخذ تعهدنامه بازرسی از دفاتر قانونی بابت سالهای فاقد بازرسی، بابت قرارداد ضریبی اعمال نمیگردد و جهت صدور مفاصاحساب میبایست در سال دوره اجرای  قرارداد بدهي قطعی سال  دوره اجرای قرارداد كليه كارگاههای مرتبط پرداخت گردد.',254)

    insert_result_data('بابت قرارداد ضریبی اعمال نمیگردد و جهت صدور مفاصاحساب میبایست در سال دوره اجرای  قرارداد بدهي قطعی سال  دوره اجرای قرارداد كليه كارگاههای مرتبط پرداخت گردد.',258)
    insert_result_data('1-نسبت به مابه التفاوت مبلغ   صورت وجوه درآمدي ومبلغ ناخالص كاركرد میبایست با شروع مجدد تعیین ضریب، با توجه به موضوع عملیات (دستمزدی،با مصالح و ارائه خدمات با ماشین آلات و..) ضریب تعیین گردد.\n2- به مبلغ ناخالص كاركرد ضریبی اعمال نمیگردد.\n3- جهت صدور مفاصاحساب میبایست در سال دوره اجرای  قرارداد بدهي قطعی سال  دوره اجرای قرارداد كليه كارگاههای مرتبط وهمچنین حق بیمه مابه التفاوت مبلغ  صورت وجوه درآمدي ومبلغ ناخالص كاركرد پرداخت گردد.',260)
    insert_result_data('با اخذ تعهدنامه بازرسی از دفاتر قانونی بابت سالهای فاقد بازرسی، بابت قرارداد ضریبی اعمال نمیگردد و جهت صدور مفاصاحساب میبایست در سال دوره اجرای  قرارداد بدهي قطعی سال  دوره اجرای قرارداد كليه كارگاههای مرتبط پرداخت گردد.',261)
   
    insert_result_data('حق بيمه طبق ضريب= 70 درصد ناخالص كاركرد با ماخذ7%و 30 درصد ناخالص كاركردبا ماخذ 15% \n بيمه بيكاري طبق ضريب= 1/9 حق بيمه\n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قراردادهای فرعی با اصلی و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',102)
    insert_result_data('حق بيمه طبق ضريب= 60 درصد ناخالص كاركرد با ماخذ7% و 40 درصد ناخالص كاركردبا ماخذ 15% \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قراردادهای فرعی با اصلی و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',103)
    insert_result_data('حق بيمه طبق ضريب= 60 درصد ناخالص كاركرد با ماخذ7% و 40 درصد ناخالص كاركردبا ماخذ 15% \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قراردادهای فرعی با اصلی و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',104)
    insert_result_data('حق بيمه طبق ضريب= 20 درصد ناخالص كاركرد با ماخذ7% و 80 درصد ناخالص كاركردبا ماخذ 15% \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قراردادهای فرعی با اصلی و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',105)
    insert_result_data('1)كاركرد بخش نقشه برداري =A \n2)كاركرد بخش خدمات مشاوره ژئوتكنيك و مقاومت مصالح=B \n3)كاركرد بخش طراحي =C \n4)كاركرد بخش نظارت عاليه و كارگاهي =D \n5)ساير موضوعات مشاوره=E \nحق بيمه طبق ضريب=( 70 درصدA با ماخذ7% و 30 درصد A با ماخذ% 15)+(60 درصدB با ماخذ7% و 40 درصد B با ماخذ% 15)+ (60 درصدC با ماخذ7% و 40 درصد C با ماخذ% 15)+( 20 درصدD با ماخذ7% و 80 درصد D با ماخذ% 15 )+(  100 درصدE  با ماخذ% 15 ) \n بيمه بيكاري طبق ضریب= 1/9 حق بيمه\n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قراردادهای فرعی با قرارداد اصلی و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',350)
    insert_result_data('ضريب= 15 % \nحق بيمه طبق ضريب = 15 درصد ناخالص كاركرد\nبيمه بيكاري طبق ضریب=1/9 حق بيمه\n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قرارداد و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',351)
    insert_result_data('ضريب= 15 % \nحق بيمه طبق ضريب = 15 درصد ناخالص كاركرد\nبيمه بيكاري طبق ضریب=1/9 حق بيمه\n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قرارداد و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',107)
    insert_result_data('حق بيمه طبق ضريب= 70 درصد ناخالص كاركرد با ماخذ7%و 30 درصد ناخالص كاركردبا ماخذ %15 \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه\n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قرارداد و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',150)
    insert_result_data('حق بيمه طبق ضريب= 60 درصد ناخالص كاركرد با ماخذ7% و 40 درصد ناخالص كاركردبا ماخذ 15% \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قرارداد و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',151)
    insert_result_data('حق بيمه طبق ضريب= 60 درصد ناخالص كاركرد با ماخذ7% و 40 درصد ناخالص كاركردبا ماخذ 15% \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قرارداد و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',152)
    insert_result_data('حق بيمه طبق ضريب= 20 درصد ناخالص كاركرد با ماخذ7% و 80 درصد ناخالص كاركردبا ماخذ 15% \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قرارداد و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است.',153)
    insert_result_data('ضريب= 15 % \nحق بيمه طبق ضريب = 15 درصد ناخالص كاركرد\nبيمه بيكاري طبق ضریب=1/9 حق بيمه\n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قرارداد و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است ',155)
    insert_result_data('ضريب= 14 % \nحق بيمه طبق ضريب = 14 درصد ناخالص كاركرد\nبيمه بيكاري طبق ضریب=1/9 حق بيمه\n بدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضم در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است ',352)
    insert_result_data('ضريب= 15 % \nحق بيمه طبق ضريب = 15 درصد ناخالص كاركرد\nبيمه بيكاري طبق ضریب=1/9 حق بيمه\n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قرارداد و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ولیکن چنانچه  ليست  " به صورت متمرکز در دفتر مركزي" ارسال شده باشد محاسبه جریمه ليست منتفی است ',353)
    insert_result_data('حق بيمه طبق ضريب= 70 درصد ناخالص كاركرد با ماخذ7%و 30 درصد ناخالص كاركردبا ماخذ %15 \n بيمه بيكاري طبق ضريب= 1/9 حق بيمه\n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قراردادهای فرعی با اصلی و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',109)
    insert_result_data('حق بيمه طبق ضريب= 70 درصد ناخالص كاركرد با ماخذ7%و 30 درصد ناخالص كاركردبا ماخذ %15 \n بيمه بيكاري طبق ضريب= 1/9 حق بيمه\n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قراردادهای فرعی با اصلی و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',128)
    insert_result_data('حق بيمه طبق ضريب= 70 درصد ناخالص كاركرد با ماخذ7%و 30 درصد ناخالص كاركردبا ماخذ %15 \n بيمه بيكاري طبق ضريب= 1/9 حق بيمه\n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قراردادهای فرعی با اصلی و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',157)
    insert_result_data('ضريب= 6  درصد\nحق بيمه طبق ضريب = 6 درصد ناخالص كاركرد\nبيمه بيكاري طبق ضریب= 1/9 حق بيمه\n بدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد',356)
    insert_result_data('ضريب= 14  درصد\nحق بيمه طبق ضريب = 14 درصد ناخالص كاركرد\nبيمه بيكاري طبق ضریب= 1/9 حق بيمه\n بدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد',357)
    insert_result_data('ضريب= 3  درصد\nحق بيمه طبق ضريب = 3 درصد ناخالص كاركرد\nبيمه بيكاري طبق ضریب= 1/9 حق بيمه\n ضریب مذکور با لحاظ اشتغال اتباع بیگانه در قرارداد اتخاذ شده و بدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',358)
 
    insert_result_data('ضريب= 6  درصد\nحق بيمه طبق ضريب = 6 درصد ناخالص كاركرد\nبيمه بيكاري طبق ضریب= 1/9 حق بيمه\n بدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',360)
   
    insert_result_data('ضريب= 4  درصد\nحق بيمه طبق ضريب = 4 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\n بدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',373)
    insert_result_data('ضريب= 4  درصد\nحق بيمه طبق ضريب = 4 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nدر خصوص مفاصاحساب قراردادهای فرعی صادره طبق ماده 41 قانون، در صورت انطباق موضوع و دوره و مبلغ با بخش اجرایی قرارداد اصلی و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',375)
    insert_result_data('ضريب= 7درصد\nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد بوده و معادل 7.8% کارکرد مورد مطالبه قرار میگیرد درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',378)
    insert_result_data('ضريب= 4درصد\nحق بيمه طبق ضريب = 4 درصد ناخالص كاركرد\nبيمه بيكاري= 7/36 حق بيمه\n بدیهی است ضریب فوق بدون لحاظ کارکرد بارگیری، انبارداری،جابجایی و سایر اموری که در حمل و نقل بار مدخلیت ندارد، میباشد و برای تعیین حق بیمه کارکرد بارگیری، انبارداری؛ جابجایی و سایر امور میبایست با شروع مجدد تعیین ضریب و انتخاب گزینه مشمول ماده 41 قانون با توجه به موضوع قرارداد یکی از موارد (دستمزدی، و ارائه خدمات با ماشین آلات و..) را انتخاب نمایید',379)    
    insert_result_data('ضريب= 7درصد\nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد',380)   
    insert_result_data('ضريب= 7درصد\nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد',382)   
    insert_result_data('مبلغ کارکرد رانندگان در استخدام (A)  \nکارکرد رانندگان مشمول بیمه‌رانندگان(B) \n\n ضريب= مبلغ B با ماخذ4% و مبلغ A با ماخذ7% \nحق بیمه طبق ضریب: (A*7%)+(B*4%) \n بیمه بیکاری طبق ضریب: ((A*7%)*1/9) + ((B*4%)*7/36)\n بدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',383)   
    insert_result_data('محاسبه علی الراس میزان کارکرد رانندگان در استخدام طبق لیستهای ارسالی به شرح ذیل: \n 7%/(مجموع دستمزد طبق لیستهای ارسالی* 27%)  = A \nالباقی ناخالص کارکرد= B \n ضريب= مبلغ B با ماخذ4% و مبلغ A با ماخذ7% \nحق بیمه طبق ضریب: (A*7%)+(B*4%) \nبیمه بیکاری طبق ضریب: ((A*7%)*1/9)+((B*4%)*7/36) \n بدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',384)  
    insert_result_data('قرارداد مشمول ماده 38 قانون نمی‌باشد',387)   
    insert_result_data('ضريب= 7درصد\nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد',388)    
    insert_result_data('ضريب= 7درصد\nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد بوده و معادل 7.8% کارکرد مورد مطالبه قرار میگیرد درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',391)
    insert_result_data('ضريب= 5درصد\nحق بيمه طبق ضريب = 5 درصد ناخالص كاركرد\nبيمه بيكاري= 7/45 حق بيمه',392)
    insert_result_data('ضريب= 7درصد\nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد',393)
    insert_result_data('ضريب= 7درصد\nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد ',395)
    insert_result_data('مبلغ کارکرد رانندگان در استخدام (A)  \nکارکرد رانندگان مشمول بیمه‌رانندگان(B) \n\n ضريب= مبلغ B با ماخذ5% و مبلغ A با ماخذ7% \nحق بیمه طبق ضریب: (A*7%)+(B*5%) \n بیمه بیکاری طبق ضریب: ((A*7%)*1/9) + ((B*5%)*7/45)\n بدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد و در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگرد',396)
    insert_result_data('محاسبه علی الراس میزان کارکرد رانندگان در استخدام طبق لیستهای ارسالی به شرح ذیل: \n 7%/(مجموع دستمزد طبق لیستهای ارسالی* 27%)  = A \nالباقی ناخالص کارکرد= B \n ضريب= مبلغ B با ماخذ5% و مبلغ A با ماخذ7% \nحق بیمه طبق ضریب: (A*7%)+(B*5%) \nبیمه بیکاری طبق ضریب: ((A*7%)*1/9)+((B*4%)*7/45) \n بدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود و در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگرد',397)
    
    insert_result_data('حق بيمه طبق ضريب= 70 درصد ناخالص كاركرد با ماخذ7%و 30 درصد ناخالص كاركردبا ماخذ %15 \n بيمه بيكاري طبق ضريب= 1/9 حق بيمه\n چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب قراردادهای فرعی طبق ماده 41 قانون، انطباق موضوع و دوره و مبلغ قراردادهای فرعی با اصلی و تایید کارفرمای اصلی؛ به میزان حق بیمه پرداختی در قراردادهای فرعی از حق بیمه طبق ضریب کسر خواهد شد.\nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',398)
    insert_result_data('سهم پیمانکار = حداقل 13.6 % از کارکرد \nسهم صدا و سیما = الباقی کارکرد\nحق بيمه طبق ضريب = سهم پیمانکار با ماخذ 7% و سهم صدا و سیما معاف\nبيمه بيكاري= 1/9 حق بيمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',425)
    insert_result_data('ضريب= 7درصد\nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',426)
    insert_result_data('سهم شرکت راه‌آهن: 60 الی  80 درصد ناخالص کارکرد\n سهم پیمانکار: الباقی کارکرد \nبا توجه به اینکه 60 الی 80 درصد از دریافتی پیمانکار بابت استفاده از امکانات ریلی و نیروی کششی به راه آهن پرداخت میگردد با تایید شرکت راه آهن مبلغ مذکور معاف از محاسبه حق بیمه میباشد \nحق بيمه طبق ضريب = سهم پیمانکار با ماخذ 7% \nبيمه بيكاري= 1/9 حق بيمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',427)
    insert_result_data('ضريب= 7درصد\nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',428)
    insert_result_data('ضريب= 15 درصد \nحق بيمه طبق ضريب = 15 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',432)
    insert_result_data('حق بيمه طبق ضريب= 70 درصد ناخالص كاركرد با ماخذ7% و 30 درصد ناخالص كاركردبا ماخذ 15% \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',433)
    insert_result_data('ضريب= 15 درصد \nحق بيمه طبق ضريب = 15 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',434)
    insert_result_data('ضريب= 3درصد\nحق بيمه طبق ضريب = 3 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',435)
    insert_result_data('ضريب= 7 درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',436)
    
    insert_result_data('حق بيمه طبق ضريب= کارکرد مکانیکی با ماخذ 7 درصد و کارکرد غیرمکانیکی (دستی) با ماخذ 15 درصد\nبيمه بيكاري= 1/9 حق بيمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',437)
    insert_result_data('حق بيمه طبق ضريب= 80 درصد ناخالص كاركرد با ماخذ7% و 20 درصد ناخالص كاركردبا ماخذ 15% \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود',438)
    
    insert_result_data('ضريب= 7 درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',120)
    insert_result_data('ضريب= 7 درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',139)
    insert_result_data('ضريب= 7 درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',173)
    insert_result_data('ضريب= 7 درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',414)
    insert_result_data('92 درصد از کارکرد معاف از پرداخت حق بیمه\nحق بيمه طبق ضریب = 8 درصد از ناخالص کارکرد با ماخذ 15 درصد \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',440) 
    insert_result_data('تا میزان مبلغ مبنای محاسبه در اوراق گمرکی معاف از پرداخت حق بیمه\n حق بیمه الباقی ناخالص کارکرد= 15 درصد\nبیمه بیکاری = 1/9 حق بیمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',441) 
    insert_result_data('92 درصد از کارکرد معاف از پرداخت حق بیمه\nحق بيمه طبق ضریب = 8 درصد از ناخالص کارکرد با ماخذ 15 درصد \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',442) 
   
    insert_result_data('92 درصد از کارکرد معاف از پرداخت حق بیمه\nحق بيمه طبق ضریب = 8 درصد از ناخالص کارکرد با ماخذ 15 درصد \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',445) 
    insert_result_data('تا میزان مبلغ مبنای محاسبه در اوراق گمرکی معاف از پرداخت حق بیمه\n حق بیمه الباقی ناخالص کارکرد= 15 درصد\nبیمه بیکاری = 1/9 حق بیمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',446) 
    insert_result_data('92 درصد از کارکرد معاف از پرداخت حق بیمه\nحق بيمه طبق ضریب = 8 درصد از ناخالص کارکرد با ماخذ 15 درصد \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',447) 
    
    insert_result_data('92 درصد از کارکرد معاف از پرداخت حق بیمه\nحق بيمه طبق ضریب = 8 درصد از ناخالص کارکرد با ماخذ 15 درصد \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',450) 
    insert_result_data('تا میزان مبلغ مبنای محاسبه در اوراق گمرکی معاف از پرداخت حق بیمه\n حق بیمه الباقی ناخالص کارکرد= 15 درصد\nبیمه بیکاری = 1/9 حق بیمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',451) 
    insert_result_data('92 درصد از کارکرد معاف از پرداخت حق بیمه\nحق بيمه طبق ضریب = 8 درصد از ناخالص کارکرد با ماخذ 15 درصد \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',452) 
    
    insert_result_data('ضريب= 7 درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',453)
    insert_result_data('ضريب= 7 درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',457)
    insert_result_data('مبلغ کارکرد اجاره خودرو بدون راننده (A) معاف از حق بیمه و کارکرد اجاره خودرو با راننده (B)با ماخذ 7% \nضریب= B*7% \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',458)
    insert_result_data('ضريب= 7 درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',459)
    insert_result_data('قرارداد مشمول ماده 38 قانون نمی‌باشد',460)
    insert_result_data('ضريب= 7 درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\nبدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود.',461)
    
    insert_result_data('ضريب= 15درصد \nحق بيمه طبق ضريب = 15 درصد سهم مدیر پیمان \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nشایان ذکر است پرداخت حق بیمه کارکرد بخش اجرایی با واگذارنده کار (کارفرما) بوده و جداگانه محاسبه میگردد.',123)
    insert_result_data('ضريب= 15درصد \nحق بيمه طبق ضريب = 15 درصد سهم مدیر پیمان \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nشایان ذکر است پرداخت حق بیمه کارکرد بخش اجرایی با واگذارنده کار (کارفرما) بوده و جداگانه محاسبه میگردد.',142)
    insert_result_data('ضريب= 15درصد \nحق بيمه طبق ضريب = 15 درصد سهم مدیر پیمان \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nشایان ذکر است پرداخت حق بیمه کارکرد بخش اجرایی با واگذارنده کار (کارفرما) بوده و جداگانه محاسبه میگردد.',178)
    insert_result_data('ضريب= 15درصد \nحق بيمه طبق ضريب = 15 درصد سهم مدیر پیمان \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nشایان ذکر است پرداخت حق بیمه کارکرد بخش اجرایی با واگذارنده کار (کارفرما) بوده و جداگانه محاسبه میگردد.',419)
    
    insert_result_data('1-ضریب = 15% \nحق بيمه طبق ضريب= 15% کل ناخالص كاركرد \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n 2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ',124)
    insert_result_data('1-ضریب = 15% \nحق بيمه طبق ضريب= 15% کل ناخالص كاركرد \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n 2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ',143)
    insert_result_data('1-ضریب = 15% \nحق بيمه طبق ضريب= 15% کل ناخالص كاركرد \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n 2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ',180)
    insert_result_data('1-ضریب = 15% \nحق بيمه طبق ضريب= 15% کل ناخالص كاركرد \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n 2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ',421)
    insert_result_data('1-ضریب = 15% \nحق بيمه طبق ضريب= 15% کل ناخالص كاركرد \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n 2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ',463)
    insert_result_data('1-ضریب = 7% \nحق بيمه طبق ضريب= 7% کل ناخالص كاركرد \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n 2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ',465)
    insert_result_data('1-حق بيمه طبق ضريب = 2 برابر مبلغ مصالح (بشرطيكه بيشتر از ناخالص كاركرد نباشد) با ماخذ 7 درصد و الباقي ناخالص كاركرد با ماخذ 15 درصد \nبيمه بيكاري= 1/9 حق بيمه \n2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',466)
    insert_result_data('1-ضریب = 7% \nحق بيمه طبق ضريب= 7% کل ناخالص كاركرد \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n 2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ',473)
    insert_result_data('1-حق بيمه طبق ضريب = 2 برابر مبلغ مصالح (بشرطيكه بيشتر از ناخالص كاركرد نباشد) با ماخذ 7 درصد و الباقي ناخالص كاركرد با ماخذ 15 درصد \nبيمه بيكاري= 1/9 حق بيمه \n2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',474)
    
    insert_result_data('1-حق بيمه طبق ضريب = 7 درصد(ناخالص كاركرد+مصالح واگذارشده به پيمانكار) \nبيمه بيكاري= 1/9 حق بيمه \n2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',475)
    insert_result_data('1-ضریب = 15% \nحق بيمه طبق ضريب= 15% کل ناخالص كاركرد \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n 2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ',476)
    
    insert_result_data('1-ضریب = 7% \nحق بيمه طبق ضريب= 7% کل ناخالص كاركرد \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n 2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ',479)
    insert_result_data('1-درصد مكانيكي= A \nدرصد غيرمكانيكي= B \nحق بيمه طبق ضريب = (7%*A*ناخالص کارکرد) + (15%*B*ناخالص کارکرد) \nبيمه بيكاري= 1/9 حق بيمه \n2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',480)
    
    insert_result_data('1-تا میزان مبلغ مبنای محاسبه اوراق گمرکی =معاف\nحق بیمه الباقی ناخالص کارکرد= 7 درصد\nبیمه بیکاری = 1/9 حق بیمه\n2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',485)
    insert_result_data('1-تا میزان مبلغ مبنای محاسبه اوراق گمرکی =معاف\nدو برابر مبلغ تجهیزات داخلی و مصالح مصرفی(بشرطيكه از باقيمانده کارکرد بيشتر نباشد)با ماخذ 7 درصد و الباقي ناخالص كاركرد با ماخذ 15 درصد\nبيمه بيكاري= 1/9 حق بيمه\n2-2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',486)
    insert_result_data('1-\nA=درصد مكانيكي بخش اجرا \nB=درصد غيرمكانيكي بخش اجرا\nتا میزان مبلغ مبنای محاسبه اوراق گمرکی =معاف\nA*7% *(کارکرداجرا) + 15% * B *(کارکرداجرا) +15 % *(الباقی کارکرد) \nبيمه بيكاري= 1/9 حق بيمه\n2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',487)
    insert_result_data('1-تا میزان مبلغ مبنای محاسبه اوراق گمرکی =معاف\nحق بیمه الباقی ناخالص کارکرد=15 درصد\nبیمه بیکاری = 1/9 حق بیمه\n2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',488)
    
    insert_result_data('1-ضریب = 7% \nحق بيمه طبق ضريب= 7% کل ناخالص كاركرد \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n 2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ',491)
    insert_result_data('1-حق بيمه طبق ضريب = 2 برابر مبلغ تجهیزات و مصالح (بشرطيكه بيشتر از ناخالص كاركرد نباشد) با ماخذ 7 درصد و الباقي ناخالص كاركرد با ماخذ 15 درصد \nبيمه بيكاري= 1/9 حق بيمه \n2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد.',492)
    insert_result_data('1-ضریب = 15% \nحق بيمه طبق ضريب= 15% کل ناخالص كاركرد \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n 2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ',494)
    insert_result_data('1-ضریب = 15% \nحق بيمه طبق ضريب= 15% کل ناخالص كاركرد \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه \n 2-چنانچه در اجرای قرارداد از پیمانکار فرعی استفاده شده باشد در صورت صدور مفاصاحساب  بابت آنها و انطباق موضوع و دوره و مجموع مبالغ قراردادهای فرعی با قرارداد اصلی و تایید مراتب استفاده از قرارداد فرعی توسط کارفرمای اصلی؛ به ترتیب زیر عمل خواهد شد: \n -چنانچه کلیه قراردادهای فرعی مشمول ماده 41 قانون باشند: حق بیمه پرداختی در قراردادهای فرعی از ضریب قرارداد اصلی کسر خواهد شد. \n - چنانچه کلیه قراردادهای فرعی مشمول ماده 47 قانون باشند: معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس طبق ضریب محاسبه می گردد.\n-چنانچه برخی از قراردادهای فرعی مشمول ماده 41 و برخی مشمول ماده 47 قانون باشد معادل کارکرد پیمانکاران فرعی از ناخالص کارکرد قرارداد اصلی کسر و سپس ضریب قرارداد اعمال میگردد و سپس از باقیمانده بدهی حق بیمه پرداختی پیمانکاران فرعی مشمول ماده 41 قانون کسر خواهد شد \nبدیهی است در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه حق بیمه طبق ضریب قرارداد بوده درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. \nضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد و در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد. ',495)
    
    insert_result_data('حق بيمه طبق ضريب= 70 درصد ناخالص كاركرد با ماخذ7% و 30 درصد ناخالص كاركردبا ماخذ 15% \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه  \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',502)
    insert_result_data('ضريب= 15درصد \nحق بيمه طبق ضريب = 15 درصد ناخالص کارکرد \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',503)
    
    insert_result_data('حق بيمه طبق ضريب= 25 درصد ناخالص كاركرد با ماخذ7% و 75 درصد ناخالص كاركردبا ماخذ 15% \nبيمه بيكاري طبق ضريب= 1/9 حق بيمه  \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',504)
    insert_result_data('ضريب= 15درصد \nحق بيمه طبق ضريب = 15 درصد ناخالص کارکرد \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',505)
    insert_result_data('ضريب=4.5 درصد\nحق بيمه طبق ضريب = 4.5 درصد ناخالص كاركرد\nبيمه بيكاري= 1/9 حق بيمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',512)
    
    insert_result_data('ضريب= 7درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص کارکرد \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',514)
    insert_result_data('ضريب= 7درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص کارکرد \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',514)
    insert_result_data('ضريب= 7درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص کارکرد \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',514)
    insert_result_data('ضريب= حداکثر تا 80 درصد کارکرد( بابت پرداخت اجاره به شهرداری،سازمان زیباسازی یا وزارت مسکن و شهرسازی معاف از بیمه) و الباقی کارکرد (بابت چاپ، طراحی،نصب، اجرا، نگهداری و تامین روشنایی بیلبورد تبلیغاتی) با ماخذ 15 درصد\nحق بيمه طبق ضريب = حداقل 20 درصد کارکرد (مبلغ چاپ، طراحی،نصب، اجرا، نگهداری و تامین روشنایی) با ماخذ 15 درصد\nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',514)
    
    insert_result_data('ضريب= 7درصد \nحق بيمه طبق ضريب = 7 درصد ناخالص کارکرد \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',518)
    insert_result_data('ضريب= 7درصد \nحق بيمه طبق ضريب = 7%*(ناخالص كاركرد به کسر حق تبخیر)   \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',519)
    
    insert_result_data('ضريب= 15درصد \nحق بيمه طبق ضريب = 15%*ناخالص کارکرد   \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',175)
    insert_result_data('ضريب= 15درصد \nحق بيمه طبق ضريب = 15%*ناخالص کارکرد   \nبيمه بيكاري= 1/9 حق بيمه \n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',417)
    insert_result_data('مبلغ اجاره محل = معاف\nحق بیمه طبق ضريب  = 7 درصدالباقی کارکرد\nبيمه بيكاري= 1/9 حق بيمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',522)
    insert_result_data('مبلغ اجاره محل = معاف \nحق بیمه طبق ضريب = 15 درصد الباقی ناخالص  کارکرد \nبيمه بيكاري= 1/9 حق بيمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',523)
    
    insert_result_data('سهم بیمارستان  = معاف\nحق بیمه طبق ضريب = 7 درصد کارکرد سهم پیمانکار \nبيمه بيكاري= 1/9 حق بيمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',524)
    insert_result_data('سهم بیمارستان  = معاف \n حق بیمه طبق ضريب = 15 درصد کارکرد سهم پیمانکار \nبيمه بيكاري= 1/9 حق بيمه\n بدیهی است در صورت عدم ارسال لیست طی دوره قرارداد،  مبلغی معادل 10% مجموع حق بیمه و بیمه بیکاری بعنوان جریمه عدم ارسال لیست محاسبه و مطالبه میگردد  و در صورتیکه حق بيمه طبق ضريب بیش از حق بيمه طبق ليستهای ارسالی باشد مبناي محاسبه ضریب قرارداد و درغیر اینصورت مبنای محاسبه و مطالبه لیستهای ارسالی خواهد بود. ضمنا در صورت ارسال لیست خارج از دوره قرارداد، به میزان حق بیمه لیستهای خارج از دوره به ضریب قرارداد اضافه میگردد.',525)
    
