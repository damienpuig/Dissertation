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

	def __str__(self):
		return "{{\"error\": \"{0}\", \"result\": \"{1}\", \"isvalid\": \"{2}\"}}".format(str(self.error), str(self.result), str(self.isvalid))