from Objects.result import Result
from Objects.log import Log

#base of all service
#
#the ServiceBase is inherited in every service
#to log, or retreive the last log emited.
class ServiceBase():
    def __init__(self, instancename):
        self.instancename = instancename

    def logit(self, content, details):
        newLog = Log(logType="SYSTEM", content=content + " from " + self.instancename, details=str(details))
        newLog.save()
        return newLog

    def last(self):
        query = lambda: Log.objects[:1].order_by('-date').first()
        return Result().safe_execute(query)