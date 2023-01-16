from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from flask_socketio import SocketIO
from flask_session import Session

import datetime

db=SQLAlchemy()
ma=Marshmallow()

# socketio = SocketIO()
# sess=Session()

def getTodayDate():
    dt = datetime.datetime.now()
    d_truncated = datetime.date(dt.year, dt.month, dt.day)
    return d_truncated


def getTargetDate(targetMonth=0,targetDay=0):
    dt = datetime.datetime.now()
    targetDate_truncated=datetime.date(dt.year, dt.month-targetMonth, dt.day-targetDay)
    return targetDate_truncated