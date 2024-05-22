import sqlite3
import logging

logging.basicConfig(filename='logs.txt', level=logging.INFO,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="w")


def create_database():
    try:
        with sqlite3.connect('db.sqlite') as con:
            cursor = con.cursor()

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS dict(
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                word TEXT,
                trans TEXT,
                date INTEGER,
                level INTEGER DEFAULT '0',
                error INTEGER DEFAULT '0')
            ''')
            logging.info('DATABASE: База данных создана')
    except Exception as e:
        logging.error(e)
        return None


def new_word(user_id, full_message):
    try:
        with sqlite3.connect('db.sqlite') as con:
            cur = con.cursor()

            word, trans, date = full_message

            cur.execute(
                '''
                INSERT INTO dict (user_id, word, trans, date)
                VALUES (?, ?, ?, ?) 
                ''',
                (user_id, word, trans, date)
            )
            con.commit()
            logging.info('DATABASE: INSERT INTO dict'
                         f'VALUES ({user_id}, {word}, {trans}, {date})')

            return 'Слово успешно добавлено'

    except Exception as e:
        logging.error(e)
        return 'Ошибка во время добавления слова в БД'


def check_repeat_word(user_id, word):
    try:
        with sqlite3.connect('db.sqlite') as con:
            cur = con.cursor()

            cur.execute('''SELECT EXISTS(SELECT word 
            FROM dict 
            WHERE user_id=? AND word=?)''', (user_id, word))

            exists = cur.fetchone()[0]
            if exists:
                return False, 'Такое слово уже есть в словаре'
            return True, 'Такого слова нет в словаре'
    except Exception as e:
        logging.error(e)
        return False, 'Ошибка при проверке слова'


def select_word(user_id):
    pass
