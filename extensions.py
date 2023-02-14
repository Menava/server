from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_socketio import SocketIO
from flask_session import Session

from datetime import date, datetime, timedelta
import pytz

db=SQLAlchemy()
ma=Marshmallow()

tz = pytz.timezone('Asia/Myanmar')
# socketio = SocketIO()
# sess=Session()

def getTodayDate():
    dt = datetime.now()
    myanmar_now = datetime.now(tz)
    print(pytz.all_timezones)
    d_truncated = date(dt.year, dt.month, dt.day)
    return d_truncated

def getTimeWindow(option):
    if(option=='week'):
        return timedelta(weeks=1)
    if(option=='month'):
        return timedelta(days=30)

def getTargetDate(targetMonth=0,targetDay=0):
    print(targetMonth,targetDay)
    dt = datetime.now()
    targetDate_truncated=date(dt.year, dt.month-targetMonth, dt.day-targetDay)
    return targetDate_truncated