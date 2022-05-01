#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

creds = {
    "COUCH_URL": "oNT674ZAafCJwgOcsak9Avyd8xEzMDw5XNcm1qxWcwks",
    "IAM_API_KEY": "oNT674ZAafCJwgOcsak9Avyd8xEzMDw5XNcm1qxWcwks",
    "COUCH_USERNAME": "fa3c88f9-b406-4b2a-9dc7-95574334ca93-bluemix"
}


def main(creds):
    databaseName = "dealerships"

    try:
        client = Cloudant.iam(
            account_name=creds["COUCH_USERNAME"],
            api_key=creds["IAM_API_KEY"],
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return_statement = {"dbs": client.all_dbs()}

    return return_statement

main(creds)
