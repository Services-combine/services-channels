import os
import logging
from dotenv import load_dotenv


dotenv_path = '../services-backend/.env'
load_dotenv(dotenv_path)

FOLDER_CHANNELS = os.getenv("FOLDER_CHANNELS")
URL_DB = os.getenv("MONDO_DB_URL")

if not os.path.exists('logs'):
	os.mkdir('logs')

logging.basicConfig(filename="logs/info.log", format = u'[%(levelname)s][%(asctime)s] %(funcName)s:%(lineno)s: %(message)s', level='INFO')
logger = logging.getLogger()
