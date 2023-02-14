from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_session import Session

from datetime import date, datetime, timedelta
import pytz

db=SQLAlchemy()
ma=Marshmallow()

tz = pytz.timezone('Asia/Yangon')

def getTodayDate():
    dt = datetime.now(tz)
    d_truncated = date(dt.year, dt.month, dt.day)
    return d_truncated

def getTimeWindow(option):
    if(option=='week'):
        return timedelta(weeks=1)
    if(option=='month'):
        return timedelta(days=30)

def getTargetDate(targetMonth=0,targetDay=0):
    dt = datetime.now(tz)
    targetDate_truncated=date(dt.year, dt.month-targetMonth, dt.day-targetDay)
    return targetDate_truncated