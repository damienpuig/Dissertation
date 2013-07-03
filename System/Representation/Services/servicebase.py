from mongoengine import *
from Objects.log import Log

class ServiceBase():

    def logIt(self, content, details):
    	newLog = Log(logType= "SYSTEM", content=content, details=details)
    	newLog.save()

    def getLastLog(self):
    	return Log.objects[:1].order_by('-date').first()


# class Result():
# 	def __init__(self):
#         self.error = None
#         self.result = None
#         self.isvalid = None

# 	def safe_execute(func):
# 		try:
#             self.result = func()
#             self.isvalid = True
#         except Exception, e:
#             self.isvalid = False
#             self.error = e

