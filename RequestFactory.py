from RequestObject import RequestObject
import datetime
import RequestResolverDAO

# A factory for creating Request objects.
class RequestFactory:

    def __init__(self, debug=True):

        self.debug = debug

    def makeIPObj(self, ip, arg):

        try:
            returnObj = RequestObject(ip, datetime.datetime.now(),
                                  arg, self.debug)
            return returnObj

        except Exception as e:

            RequestResolverDAO.setLogsToDatabase("FactoryError", "Failed to make IP Object. Error was: " + str(e))
            return None



