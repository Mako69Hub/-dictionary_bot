import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

CUR_USER_DICT = {}
STEP_USER = {}