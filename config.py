import os

db_config = {
    'user':os.environ.get('db_user','root'), 
    'password':os.environ.get('db_password','password'), 
    'host':os.environ.get('db_host','localhost'), 
    'database':os.environ.get('database_name')
}

SUPPORT_CID = int(os.environ.get('SUPPORT_CID'))
API_TOKEN = os.environ.get('BOT_TOKEN')