from Objects.mongoextension import encode_model

#Abstraction of each result coming from the database.
#The result class encapsulate the queries, execute them, 
#assignate them in the result property, and give
#a boolean response.
#If the value is not valid, the error is also encalsulated.
#
#This encalsulation is very useful since the system does not crach
#on database query, and could be extended on every action needed.
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