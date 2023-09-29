import datetime
import RequestResolverDBCore as DBCon

## TODO: MERGE THIS WITH THE DBCon File


def setArgumentAndUUIDOrReturnUUID(arg, uuid):
    UUID = DBCon.DBConnection.execute_query("SELECT uuid FROM argument_uuid WHERE argument = %s", arg)
    if not UUID:
        DBCon.DBConnection.execute_query("INSERT INTO argument_uuid (argument, uuid) VALUES (%s, %s)", [arg, uuid], False)
        UUID = DBCon.DBConnection.execute_query("SELECT uuid FROM argument_uuid WHERE argument = %s", arg)
    return UUID[0]


def getArgumentByUUID(uuid):
    return DBCon.DBConnection.execute_query("SELECT argument FROM argument_uuid WHERE uuid = %s", uuid, True, False)[0]


def getFrontUrlFromDatabase(countryCode):
    # Returns the URL for the given country code.
    return DBCon.DBConnection.execute_query("SELECT url FROM urls WHERE country_code = %s", countryCode)[0]


def setRequestDataToLog(dataArray):
    # Send the request data to the database. Includes its time of entry, the ip address it came from with the arg used and the data.
    DBCon.DBConnection.execute_query(
        "INSERT INTO ip_log_table (ip_address, json_data, entry_time, argument) VALUES (%s, %s, %s, %s)", dataArray,
        False)


def getEventIdOrSetEventIDIfExists(event):

    # I initally built this function with recursion - unfortunatley, this caused too many bugs.
    # Now, a check takes place if the ID exists. if the check returns nothing, the new event
    # is built and its id is got.

    ID = DBCon.DBConnection.execute_query("SELECT id FROM event_type WHERE event_type = %s", event)
    if not ID:
        DBCon.DBConnection.execute_query("INSERT INTO event_type (event_type) VALUES (%s)", event)
        ID = DBCon.DBConnection.execute_query("SELECT id FROM event_type WHERE event_type = %s", event)

    return ID[0] # Database doing database things and returning arrays


def setLogsToDatabase(eventName, content):

    # Check which table is passed in as a parameter, push the event to the database.

    DBCon.DBConnection.execute_query("INSERT INTO event_logs (event_id, time, content) VALUES (%s, %s, %s)",
                         [getEventIdOrSetEventIDIfExists(eventName), str(datetime.datetime.now()), content], False)

def logTableTruncater():

    sql = "TRUNCATE TABLE event_logs"
    DBCon.DBConnection.execute_query(sql, None, False)
    
    

