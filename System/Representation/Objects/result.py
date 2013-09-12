from mongoengine import *
from Objects.mongoextension import encode_model
import json

class Result(object):
	def __init__(self):
		self.error = None
		self.result = None
		self.isvalid = None

	def safe_execute(self, func, *args):
		print 'try execute'
		try:
			self.result = func(*args)
			self.isvalid = True

			if self.result is None:
				self.isvalid = False
				print 'try successfully executed, but result is None'
				return self

			print 'try successfully executed with result'

		except Exception, e:
			print 'except executed'
			self.isvalid = False
			self.error = e
			print self.error
			
		finally:
			return self