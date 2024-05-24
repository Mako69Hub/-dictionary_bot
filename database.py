import sqlite3
import logging

logging.basicConfig(filename='logs.log', level=logging.INFO,
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


def insert_new_word(user_id, full_message):
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

            return ''

    except sqlite3.IntegrityError as e:
        logging.error(e)
        return 'Ошибка во время добавления слова в БД'


def check_repeat_word(user_id, word):
    try:
        with sqlite3.connect('db.sqlite') as con:
            cur = con.cursor()

            cur.execute(f'''SELECT EXISTS(SELECT word 
            FROM dict 
            WHERE user_id={user_id} AND word='{word}')''')

            exists = cur.fetchone()[0]
            if exists:
                return False, f'Слово {word} уже есть в словаре\n'
            return True, ''

    except Exception as e:
        logging.error(e)
        return False, 'Ошибка при проверке слова'


def select_word(user_id):
    try:
        with sqlite3.connect('db.sqlite') as con:
            cur = con.cursor()

            cur.execute(f'''SELECT word, trans 
            FROM dict 
            WHERE user_id={user_id}''')

            result = cur.fetchall()
            if not result:
                return 'Словарь пуст'
            return result
    except Exception as e:
        logging.error(e)
        return 'Возникла ошибки при обращении к словарю'


def update_word(user_id, word, translation):
    try:
        with sqlite3.connect('db.sqlite') as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE dict SET trans = ? WHERE user_id = ? AND word = ?", (translation, user_id, word))
            logging.info(f"DATABASE: UPDATE words SET translation = {translation} WHERE user_id = {user_id} AND word = {word}")
            conn.commit()
    except Exception as e:
        logging.error(e)
        return None


def bd_update_lvl():
    pass