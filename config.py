import os

db_config = {
    'user':os.environ.get('db_user'), 
    'password':os.environ.get('db_password'), 
    'host':os.environ.get('db_host'), 
    'database':os.environ.get('database_name')
}

SUPPORT_CID = int(os.environ.get('SUPPORT_CID'))
API_TOKEN = os.environ.get('BOT_TOKEN')