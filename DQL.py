import mysql.connector
from config import db_config

database_name = db_config['database']

def user_in_database(cid):
    conn = mysql.connector.MySQLConnection(**db_config)
    cur = conn.cursor(dictionary=True)
    SQL_QUERY = "SELECT * FROM USERS WHERE CHAT_ID = %s"
    cur.execute(SQL_QUERY, (cid,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def check_is_spam(cid):
    conn = mysql.connector.MySQLConnection(**db_config)
    cur = conn.cursor(dictionary=True)
    SQL_QUERY = "SELECT * FROM USERS WHERE CHAT_ID = %s"
    cur.execute(SQL_QUERY, (cid,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result['IS_SPAM']
    

# def spam_list():
#     conn = mysql.connector.MySQLConnection(**db_config)
#     cur = conn.cursor(dictionary=True)
#     cur.execute( "SELECT * FROM USERS WHERE IS_SPAM = True")
#     result = cur.fetchall()
#     cur.close()
#     conn.close()
#     return result


def bacK_to_previous(cid):
    conn = mysql.connector.MySQLConnection(**db_config)
    curr = conn.cursor(dictionary=True) 
    try:
        curr.execute("""SELECT ID, QUESTION_ID, OPTION_ID FROM USER_ANSWERS 
                     WHERE CID = %s ORDER BY ID DESC LIMIT 1 """,(cid,))
        previous = curr.fetchone()
        if not previous:
            return None
        return previous
    finally:
        curr.close()
        conn.close()
        
def get_question(qid):
    conn = mysql.connector.MySQLConnection(**db_config)
    curr = conn.cursor(dictionary=True)
    curr.execute("SELECT * FROM QUESTION WHERE ID = %s",(qid,))
    question = curr.fetchone()
    curr.close()
    conn.close()
    if not question:
        print ("❌ Question Id doesn't exist.")
        return
    return question


def get_options(qid):
    conn = mysql.connector.MySQLConnection(**db_config)
    curr = conn.cursor(dictionary=True)
    curr.execute("SELECT * FROM ANSWER WHERE QUESTION_ID = %s", (qid,))
    options = curr.fetchall()
    curr.close()
    conn.close()
    if not options:
        print (f"❌ No option Id for {qid}.")
    return options

def get_ans_data(ans_id):
    conn = mysql.connector.MySQLConnection(**db_config)
    curr = conn.cursor(dictionary=True)
    curr.execute("SELECT * FROM ANSWER WHERE ID = %s",(ans_id,))
    res = curr.fetchone()
    curr.close()
    conn.close() 
    return res

def get_insurance_result(ans_id):
    conn = mysql.connector.MySQLConnection(**db_config)
    curr = conn.cursor(dictionary=True)
    curr.execute("SELECT * FROM INSURANCE_RESULT WHERE ANS_ID = %s",(ans_id,))
    res = curr.fetchone()
    curr.close()
    conn.close() 
    return res

def delete_last_UserAnswers(cid,ID):
    conn = mysql.connector.MySQLConnection(**db_config)
    curr = conn.cursor()
    curr.execute("DELETE FROM USER_ANSWERS WHERE CID = %s and ID = %s",
            (cid , ID))
    conn.commit()
    curr.close()
    conn.close()
    
def delete_UserAnswers_data(cid):
    conn = mysql.connector.MySQLConnection(**db_config)
    curr = conn.cursor()
    curr.execute("DELETE FROM USER_ANSWERS WHERE CID=%s",(cid,))
    conn.commit()
    curr.close()
    conn.close()   