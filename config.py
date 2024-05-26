import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

CUR_USER_DICT = {}
STEP_USER = {}

LEVEL_TIME = {
    0: 1,
    1: 1,
    2: 3,
    3: 7,
    4: 21,
    5: 31,
    6: 93,
    7: 183,
    8: 365,
    9: 1095
}

DONE_USER_DICT = {}