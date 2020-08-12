from PyQt5 import QtCore

#SINGLETON#
class ToolsMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Tools(metaclass=ToolsMeta):

    today = QtCore.QDate.currentDate()

    def GetDate(self, sTime):
        tempDate = str(sTime).split('/')
        date = QtCore.QDate(int(tempDate[2]), int(tempDate[1]), int(tempDate[0]))
        return date
    
    def FormatData(self, data):
        
        if (data == None):
            data = ''
        elif (data == 1):
            data = 'Sim'
        elif (data == 0):
            data = 'Não'
        else:
            data = str(data)
        
        return data