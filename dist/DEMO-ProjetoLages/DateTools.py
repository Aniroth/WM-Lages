from PyQt5 import QtCore

#SINGLETON#
class DateToolsMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DateTolls(metaclass=DateToolsMeta):

    today = QtCore.QDate.currentDate()

    def GetDate(self, sTime):
        tempDate = str(sTime).split('/')
        date = QtCore.QDate(int(tempDate[2]), int(tempDate[1]), int(tempDate[0]))
        return date