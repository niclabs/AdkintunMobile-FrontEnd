from datetime import datetime

from app.importation.monthly_importation import monthly_import
from apscheduler.schedulers.background import BackgroundScheduler


def start_scheduler():
    scheduler = BackgroundScheduler()
    start_date = get_first_day()
    scheduler.add_job(monthly_import, "cron", id="importacion mensual", replace_existing=True,
                      day="2", hour="0", minute="0", start_date=start_date)
    scheduler.start()


def get_first_day():
    return datetime.now().replace(day=2, hour=0, minute=0, second=0, microsecond=0)