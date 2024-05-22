from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

scheduler = BackgroundScheduler()


def send_remind(user_id, bot):
    bot.send_message(user_id, 'Время повторить')


def create_job(bot, user_id, time_to_repeat_in_hours=3):
    trigger_date = datetime.now() + timedelta(hours=time_to_repeat_in_hours)

    scheduler.add_job(send_remind,
                      id=str(user_id),
                      trigger='date',
                      args=(user_id, bot),
                      run_date=trigger_date
                      )
