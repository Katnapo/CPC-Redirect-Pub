import datetime
import requests
import json
import RequestResolverDAO
class RequestObject:


    def __init__(self, ip, time, uuid, debug=True):


        # IP is given in request
        self.ip = ip

        # Json will start off empty until a get request is performed.
        self.json = {}
        self.json_str = None

        # Time is passed in as a string
        self.time = time

        # Arguments from initial user request
        self.uuid = uuid
        self.arg = ""
        
        self.debug = debug
        self.url = "https://www.childsplayclothing.com/wo/en"
        self.iteration = 0
        self.fail = False


    def run(self):

        # Run performs the regular process for each IP that comes in. It will first get the JSON from IPRegistry,
        # then it will get the URL from the database, then it will construct the final URL,
        # and then it will return the final URL.

        if self.getRequestForApiUsingIp() is None:
            self.Fail = True
        self.logObjectToDatabase()
        self.getURLFromObject()
        self.constructFinalUrlFromArg()


    def getRequestForApiUsingIp(self):


        # Send the IP to the HTTPS Requester, which will query IPRegistry and return two JSON entities
        import RequestHTTPS

        # TODO: Figure out what json_str is for
        self.json, self.json_str = RequestHTTPS.getIPRegistryDataForIp(self.ip)


        # If the JSON is empty, then the request failed. Return None.
        if self.json is None or self.json_str is None:
            self.iteration = self.iteration + 1
            if self.iteration > 5:
                return None
            else:
                return self.getRequestForApiUsingIp()

        # Test to see if the JSON is valid. If it is not, then the request failed. Raise an exception
        try:
            p = json.loads(json.dumps(self.json))
            self.json = p
            return 1

        # Error catching for true JSON from IPRegistry. If the JSON is not true JSON, then the request will fail (Although this is retried twice)
        # TODO: Figure out what causes either error

        except ValueError as f:
            RequestResolverDAO.setLogsToDatabase("RequestJSONError", "Attempt " + str(self.iteration) + ", failed to convert JSON given from request to JSON, ValueError caught is: " + str(f))
            self.iteration = self.iteration + 1
            if self.iteration > 2:
                return None
            else:
                return self.getRequestForApiUsingIp()

        except Exception as g:

            RequestResolverDAO.setLogsToDatabase("RequestJSONError", "Attempt " + str(self.iteration) + ", failed to convert JSON given from request to JSON, regular error caught is: " + str(g))
            self.iteration = self.iteration + 1
            if self.iteration > 2:
                return None
            else:
                return self.getRequestForApiUsingIp()


    # Logs the request data to the database
    def logObjectToDatabase(self):

        RequestResolverDAO.setRequestDataToLog([self.ip, self.json_str, self.time, self.uuid])


    # Dissects the JSON from IPRegistry to get a country code and returns the respective URL from the database
    def getURLFromObject(self):

        try:
            code = self.json["location"]["country"]["code"]
            RequestResolverDAO.setLogsToDatabase("RequestObject", "A country code of " + str(code) + " was found for IP: " + str(
                self.ip) + " with UUID: " + str(self.uuid) + " and time: " + str(self.time))

        except Exception as e:

            RequestResolverDAO.setLogsToDatabase("RequestCountryError", "Response from IPRegistry likely did not have good"
                                                                        "formatting or didnt have a country. IP Was: "
                                                 + str(self.ip) + " with UUID: " + str(self.uuid) + " and time: " +
                                                 str(self.time) + ". Proceeding to default to XX. Error was: " + str(e))
            code = "XX"

        try:
            url = RequestResolverDAO.getFrontUrlFromDatabase(code)
            if not url or url == "" or url == " ":
                url = "https://www.childsplayclothing.com/wo/en"

        except Exception as f:
            RequestResolverDAO.setLogsToDatabase("RequestCountryError", "Request for URL from database failed. "
                                                                        "Defaulting to world. IP Was: "
                                                 + str(self.ip) + " with UUID: " + str(self.uuid) + " and time: " +
                                                 str(self.time) + ". Proceeding to default to XX. Error was: " + str(f))
            url = "https://www.childsplayclothing.com/wo/en"

        self.url = url

    # Get the argument corresponding to the given UUID from the database and then add it to the URL. Return this as the final URL.
    def constructFinalUrlFromArg(self):


        try:
            self.arg = RequestResolverDAO.getArgumentByUUID(self.uuid)[0]

        except Exception as f:

            RequestResolverDAO.setLogsToDatabase("RequestArgumentError", "Failed at getting UUID, defaulting to zero arguments. Error was " + str(f) + " with an IP of " + str(self.ip))
            self.arg = ""


        self.finalUrl = self.url + self.arg

        try:
            import RequestHTTPS
            result = RequestHTTPS.checkUrlForOk(self.finalUrl)
            if result is False:
                RequestResolverDAO.setLogsToDatabase("RequestUrlWarning", "Final URL is not responding with a 200. URL is: " + str(self.finalUrl) + " for IP: " + str(self.ip))

        except Exception as e:
            RequestResolverDAO.setLogsToDatabase("RequestUrlError", "Final URL failed to even be checked. URL is: " + str(self.finalUrl) + " for IP: " + str(self.ip) + " with error: " + str(e))
            self.finalUrl = "https://www.childsplayclothing.com/wo/en"

    def getFailState(self):

        return self.fail

    def getFinalUrl(self):

        return self.finalUrl









