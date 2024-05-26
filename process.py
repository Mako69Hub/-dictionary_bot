from database import check_repeat_word, select_word
from datetime import datetime, timedelta
from config import LEVEL_TIME
from scheduler import check_interval_word

def str_in_list_dict(text):
    dict = text.split('\n')
    list_words = []
    report_int = ''

    for element in dict:
        word, translation = map(str.strip, element.split('='))
        if word.isalnum():
            list_words.append([word, translation])
        else:
            report_int += f'Слово {word}={translation} должно состоять из букв.\n'

    return list_words, report_int


def list_in_str_dict(text):
    count = 1
    str_words = ''
    for element in text:
        str_words += f'{count}. {element[0]} - {element[1]}\n'
        count += 1
    return str_words


def remove_double_word(user_id, dict_user):
    report_check = ''
    double = []
    for element in dict_user:
        status, cur_report_check = check_repeat_word(user_id, element[0])
        if not status:
            double.append(element)
            report_check += cur_report_check

    for elem in double:
        dict_user.remove(elem)
    return dict_user, report_check

# def passivation_dict(user_id, date, dict_user):
#     for element in dict_user:









