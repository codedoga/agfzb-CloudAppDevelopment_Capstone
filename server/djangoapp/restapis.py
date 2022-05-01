import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from djangoapp.models import CarDealer
from djangoapp.models import DealerReviw
import urllib


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(**kwargs):
    results = []
    # Call get_request with a URL parameter
    url="http://codedoga-cloudapp.eu-gb.mybluemix.net/api/dealership"
    json_result = requests.get(url).json()
    if json_result:
        # For each dealer object
        for dealer_doc in json_result:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"], state=dealer_doc["state"], 
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    url = f"http://codedoga-cloudapp.eu-gb.mybluemix.net/api/reviews"
    json_result = requests.get(url).json()
    for review in json_result:
        if str(review["dealership"]) == dealerId:
            sentiment = analyze_review_sentiments(review["review"])
            review_obj = DealerReviw(dealership=review["dealership"], name=review["name"], purchase=review["purchase"], review=review["review"], purchase_date=review["purchase_date"], car_make=review["car_make"], car_model=review["car_model"],car_year=review["car_year"], sentiment=sentiment)

            
            results.append(review_obj)
    return results


# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    try:
        analyze_dict = {"version":"2022-04-07","text":dealerreview, "features":"keywords","keywords.emotion":"true","keywords.sentiment":"true", "language":"en"}
        params = urllib.parse.urlencode(analyze_dict)

        auth=HTTPBasicAuth('apikey', 'GfHwVoCJ2jMvLgK1G2f2cyIiTFslWR9z2ga4dqVM98ed')
        sentiment = requests.Session().get(f"https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/38b98698-dbf0-4d66-8ba0-76918e65e325/v1/analyze?{params}", auth=auth).json()

        emotion = sentiment["keywords"][0]["sentiment"]["label"]
    except:
        emotion = "not determined"

    return emotion



