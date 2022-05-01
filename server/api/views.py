from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

creds = {
    "COUCH_URL": "https://fa3c88f9-b406-4b2a-9dc7-95574334ca93-bluemix.cloudantnosqldb.appdomain.cloud",
    "IAM_API_KEY": "oNT674ZAafCJwgOcsak9Avyd8xEzMDw5XNcm1qxWcwks",
    "COUCH_USERNAME": "fa3c88f9-b406-4b2a-9dc7-95574334ca93-bluemix"
}


# Create your views here.
def dealership(request):
    if request.method == 'GET':
        try:
            state = request.GET.get('state', None)

            client = Cloudant.iam(
                    account_name=creds["COUCH_USERNAME"],
                    api_key=creds["IAM_API_KEY"],
                    connect=True,
                )
            db = client["dealerships"].all_docs(include_docs=True)
            client.disconnect()
            if state:
                result = [i["doc"] for i in db["rows"] if i["doc"]["st"]==state]
            else:
                result = [i["doc"] for i in db["rows"]]

            if state and not result:
                return JsonResponse({"error": "The state does not exist"}, status=404)
            
            if not state and not result:
                return JsonResponse({"error": "The database is empty"}, status=404)

            return JsonResponse(result, safe=False)
        except:
            return JsonResponse({"error": "Something went wrong on the server"}, status=500)

@csrf_exempt
def review(request):
    client = Cloudant.iam(
        account_name=creds["COUCH_USERNAME"],
        api_key=creds["IAM_API_KEY"],
        connect=True,
    )

    if request.method == 'GET':
        try:
            dealerId = request.GET.get('dealerId', None)

            db = client["reviews"].all_docs(include_docs=True)
            client.disconnect()
            if dealerId:
                result = [i["doc"] for i in db["rows"] if str(i["doc"]["dealership"])==dealerId]
            else:
                result = [i["doc"] for i in db["rows"]]

            if dealerId and not result:
                return JsonResponse([], status=404, safe=False)
            
            if not dealerId and not result:
                return JsonResponse([], status=404, safe=False
                )

            return JsonResponse(result, safe=False)
        except:
            return JsonResponse({"error": "Something went wrong on the server"}, status=500)
    
    if request.method == 'POST':
        try:
            doc = json.loads(request.body)["review"]
            db = client["reviews"].create_document(doc)
            return JsonResponse({"success": "Review is uploaded"}, status=200)

        except:
            return JsonResponse({"error": "Something went wrong on the server"}, status=500)