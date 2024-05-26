from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from config import LEVEL_TIME

scheduler = BackgroundScheduler()


def send_remind(user_id, bot):
    bot.send_message(user_id, 'Время повторить')
    


def create_job(bot, user_id, time_to_repeat_in_hours=3):
    trigger_date = datetime.now() + timedelta(hours=time_to_repeat_in_hours)

    scheduler.add_job(send_remind,
                      id=str(user_id),
                      trigger='date',
                      args=(user_id, bot),
                      run_date=trigger_date,
                      replace_existing=True
                      )


def check_interval_word(dict):

    level_word, date_word = dict[2], dict[3]
    day_level = LEVEL_TIME[level_word]

    date_now = datetime.now()

    interval_word = datetime.strptime(date_word, "%Y-%m-%d") + timedelta(days=day_level)

    interval_word_ymd = datetime.strftime(interval_word, "%Y-%m-%d")
    date_now_ymd = datetime.strftime(date_now,"%Y-%m-%d")

    if date_now_ymd > interval_word_ymd:
        return True
    return False
