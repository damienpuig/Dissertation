from mongoengine import *
from Objects.log import Log

class ServiceBase():
	def __init__(self, instancename):
		self.instancename = instancename

	def logit(self, content, details):
		newLog = Log(logType="SYSTEM", content=content + 'from ' + self.instancename, details=details)
		newLog.save()

	def last(self):
		return Log.objects[:1].order_by('-date').first()


class Result():
	def __init__(self):
		self.error = None
		self.result = None
		self.isvalid = None

	def safe_execute(self, func, *args):
		print 'try execute'
		try:
			self.result = func(*args)
			self.isvalid = True
			print 'try successfully executed'
		except Exception, e:
			self.isvalid = False
			self.error = e
			print 'except executed'
			print self.error
		finally:
			return self


