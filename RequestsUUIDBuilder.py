import datetime
import RequestResolverDAO
# UUID Tools kept separate from main code base for simplicity.
class UUIDTools:

    def getNewUUID(self):

        # Returns a new UUID.
        import uuid
        return uuid.uuid4()

    def setArgAndUUIDToDatabase(self, arg):

        uuid = self.getNewUUID()

        # Set the UUID and the argument to the database. If a UUID is already in the database,
        # the old UUID will be returned.
        try:
            uuid = RequestResolverDAO.setArgumentAndUUIDOrReturnUUID(arg, str(uuid))
            return uuid

        except Exception as e:
            RequestResolverDAO.setLogsToDatabase("UUIDError", "Failed to set UUID to database. Error was: " + str(e))
            return None

    # Methods for dissecting a URL given by CPC staff.
    def dissectURLByStyle(self, url):

        # Regex here just looks for the word "Style" then separates the URL by that.
        splitUrl = url.split("style")
        endUrl = "/style" + splitUrl[1]
        return endUrl

    def dissectURLByRegex(self, url):

        import re
        # TODO: Maybe upgrade the regex to recognize not just the .co.uk/ line but also lines such as /wo/en/

        # Regex here looks for .[WORDS]/
        splitUrl = re.split("\\.[a-zA-Z]+/", url)
        endUrl = "/" + splitUrl[1]
        return endUrl




