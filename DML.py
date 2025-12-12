import mysql.connector
from config import db_config

database_name = db_config['database']

def insert_question_data(text):
    conn = mysql.connector.MySQLConnection(**db_config)
    cur = conn.cursor()
    SQL_QUERY = "INSERT INTO QUESTION (Q_TEXT) VALUES (%s);"
    cur.execute(SQL_QUERY, (text,))
    conn.commit()
    ID=cur.lastrowid
    cur.close()
    conn.close()
    return ID
    
def insert_answer_data(text, qid, next_qid = None, is_final = False):
    conn = mysql.connector.MySQLConnection(**db_config)
    cur=conn.cursor()
    SQL_QUERY ="INSERT INTO ANSWER (OPTION_TEXT,QUESTION_ID,NEXT_QUESTION_ID,IS_FINAL) VALUES (%s,%s,%s,%s);"
    cur.execute(SQL_QUERY, (text,qid,next_qid,is_final))
    conn.commit()
    ID=cur.lastrowid
    cur.close()
    conn.close()
    return ID
    
def insert_result_data(text,ans_id):
    conn = mysql.connector.MySQLConnection(**db_config)
    cur=conn.cursor()
    SQL_QUERY = "INSERT INTO INSURANCE_RESULT (RES_TEXT,ANS_ID) VALUES (%s,%s);"
    cur.execute(SQL_QUERY, (text,ans_id))
    conn.commit()
    ID=cur.lastrowid
    cur.close()
    conn.close()
    return ID
        
def insert_user_data(cid,name,username,Time,score=0):
    conn = mysql.connector.MySQLConnection(**db_config)
    cur = conn.cursor()
    try:
        SQL_QUERY = "INSERT IGNORE INTO USERS (CHAT_ID,NAME, USERNAME,LAST_MSG_TIME,SCORE) VALUES (%s, %s, %s,%s,%s);"
        cur.execute(SQL_QUERY, (cid, name, username,Time,score))
        conn.commit()
    finally:
        cur.close()
        conn.close()
        
def insert_file_info(cid,mid,fid):
    conn = mysql.connector.MySQLConnection(**db_config)
    cur = conn.cursor()
    try:
        SQL_QUERY = "INSERT IGNORE INTO FILE_INFO (CID,MID,FID) VALUES (%s, %s, %s) ;"
        cur.execute(SQL_QUERY, (cid,mid,fid))
        conn.commit()
    finally:
            cur.close()
            conn.close()
            
    
            
def update_user_data(cid,Time,score):
    conn = mysql.connector.MySQLConnection(**db_config)
    cur = conn.cursor()
    try:
        SQL_QUERY = "UPDATE USERS SET LAST_MSG_TIME=%s , SCORE=%s WHERE CHAT_ID=%s ;"
        cur.execute(SQL_QUERY, (Time,score,cid))
        conn.commit()
    finally:
            cur.close()
            conn.close()
            
def set_is_spam(cid,T=False)-> None:
    conn = mysql.connector.MySQLConnection(**db_config)
    cur = conn.cursor()
    try:
        SQL_QUERY = "UPDATE USERS SET IS_SPAM=%s,SCORE=%s WHERE CHAT_ID=%s;"
        cur.execute(SQL_QUERY, (T,0,cid))
        conn.commit()
    finally:
        cur.close()
        conn.close()

def insert_user_answers_data( cid, mid, qid, ans_id):
    conn = mysql.connector.MySQLConnection(**db_config)
    cur = conn.cursor()
    try:
        SQL_QUERY = "INSERT INTO USER_ANSWERS (CID, MID, QUESTION_ID, OPTION_ID) VALUES (%s, %s,%s, %s)"
        cur.execute(SQL_QUERY,(cid, mid, qid, ans_id))
        conn.commit()
    finally:
            cur.close()
            conn.close()
