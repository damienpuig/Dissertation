from mongoengine import *
from bson.objectid import ObjectId

from Objects.device import Device
from Objects.value import Value
from Objects.result import Result
from Objects.qoc import QoC
from Services.servicebase import ServiceBase


#Value service
#
#Basic implementation of a service executing queries
#to the mongoDB database.
#Most of the queries are encapsulation in a Result instance.
#Most of the queries are logged through ServiceBase.
class ValueService(ServiceBase):
    def __init__(self, instancename):
        ServiceBase.__init__(self, instancename)

    def getbyid(self, id):
        query = lambda x: Value.objects(id=ObjectId(x)).first()

        result = Result().safe_execute(query, id)

        if result.isvalid:
            self.logit("getbyid performed", result.result.tojson())
        else:
            self.logit("getbyid performed with error", result.error)
        return result

    def getbydevice(self, device, limit):
        query = lambda i: Device.objects.get(id=ObjectId(i)).values

        result = Result().safe_execute(query, device.id)

        if result.isvalid:
            if not (limit is None) and result.result:
                result.result = result.result[:limit]
            self.logit("getbydevice performed", "{0} entry(ies) found".format(len(result.result)))
        else:
            self.logit("getbydevice performed with error", result.error)

        return result

    def getbytime(self, limit, date):
        def query(date, l):
            builder = Value.objects.filter(Q(date__gt=date))
            if not (limit is None):
                builder.limit(l)
            return builder

        result = Result().safe_execute(query, date, limit)

        if result.isvalid:
            self.logit("getbytime performed", "{0} entry(ies) found".format(len(result.result)))
        else:
            self.logit("getbytime performed with error", result.error)
        return result

    def add(self, device, valuetype, value, location, comment, completeness, significance):
        newValue = Value(valueType=valuetype, value=value, location=location)

        if not ((completeness is None) and (significance is None)):
            newValue.qoc = QoC(completeness=completeness, significance=significance)

        if not (comment is None):
            newValue.comments = [comment]

        newValue.save()

        self.logit("add performed", "{0} has been added".format(newValue.tojson()))

        device.update(add_to_set__values=[newValue])

        self.logit("update performed", "{0} has been updated".format(device.tojson()))

        return newValue

    def delete(self, value):
        value.delete()
        self.logit("delete performed", value.tojson() + " has been deleted")
        return value

    def deleteallbydevice(self, device):
        lenght = len(device.values)
        device.values = None
        device.save()
        self.logit("deleteallbydevice performed", "device: {0}, entry(ies):{1}".format(device.tojson(), lenght))
        return device

    def deleteall(self):
        Value.drop_collection()
        self.logIt("deleteall performed", "Value collection has been deleted")
