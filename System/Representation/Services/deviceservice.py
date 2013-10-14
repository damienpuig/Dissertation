from bson.objectid import ObjectId

from Objects.device import Device

from Objects.value import Value
from Objects.result import Result
from Services.servicebase import ServiceBase


#Device service
#
#Basic implementation of a service executing queries
#to the mongoDB database.
#Most of the queries are encapsulation in a Result instance.
#Most of the queries are logged through ServiceBase.
class DeviceService(ServiceBase):
    def __init__(self, instancename):
        ServiceBase.__init__(self, instancename)

    def getall(self):
        query = lambda: Device.exclude("values").all()
        result = Result().safe_execute(query)

        if result.isvalid:
            self.logit("getall performed", "{0} entry(ies) found".format(len(result.result)))
        else:
            self.logit("getall performed with error", result.error)
        return result

    def getbylocation(self, locationTuple, limit):
        def query(lt, l):
            builder = Device.objects(location={"type": "Point", "coordinates": lt}, point__max_distance=1000).exclude(
                "values").limit(1)
            if not (limit is None):
                builder.limit(l)
            return builder.all()

        result = Result().safe_execute(query, locationTuple, limit)

        if result.isvalid:
            self.logit("getbylocation performed", "{0} entry(ies) found".format(len(result.result)))
        else:
            self.logit("getbylocation performed with error", result.error)
        return result

    def getbyname(self, name):
        query = lambda n: Device.objects(name=n).exclude("values").first()

        result = Result().safe_execute(query, name)

        if result.isvalid:
            self.logit("getbyname performed", result.result.tojson())
        else:
            self.logit("getbyname performed with error", result.error)
        return result

    def getbyid(self, id):
        query = lambda i: Device.objects(id=ObjectId(i)).exclude("values").first()

        result = Result().safe_execute(query, id)

        if result.isvalid:
            self.logit("getbyid performed", result.result.tojson())
        else:
            self.logit("getbyid performed with error", result.error)
        return result

    def getbyvalue(self, value):

        query = lambda v: Device.objects(values__in=[v]).first()

        result = Result().safe_execute(query, value)

        if result.isvalid:
            self.logit("getbyvalue performed", result.result.tojson())
        else:
            self.logit("getbyvalue performed with error", result.error)
        return result


    def add(self, name, description, location):
        def query(n, d, l):
            newDevice = Device(name=name, description=description, location=location)
            newDevice.save()
            return newDevice


        result = Result().safe_execute(query, name, description, location)

        if result.isvalid:
            self.logit("add performed", "{0} has been added".format(result.result.tojson()))
        else:
            self.logit("add performed with error", result.error)
        return result

        return result

    def delete(self, device):
        device.delete()
        self.logit("removeDevice performed", "{0} has been deleted".format(device.tojson()))
        return device

    def deleteall(self):
        Device.drop_collection()
        self.logit("removeAllDevices performed", "Device collection has been deleted")


    def update(self, device):
        device.save()
        self.logit("updateDevice performed", "{0} has been updated".format(device.tojson()))