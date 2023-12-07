import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

WASTON_URL = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/645a9d07-99f5-400a-8517-4fcd7a3fd13f"
WATSON_API = "3vnDt-j-J0axqCXaz7eyCjuH6274sFysPswYVMJmYXCb"
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data



def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, dealerId=kwargs["dealerId"])
    if json_result:
        reviews = json_result
        print(reviews)
        for review in reviews:
            dealer_review = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                review=review["review"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment="",
                id=review["id"],
            )
            dealer_review.sentiment = analyze_review_sentiments(dealer_review.review)
            results.append(dealer_review)
            print(dealer_review)
    return results

def analyze_review_sentiments(dealerreview):
    body = {"text": dealerreview, "features": {"sentiment": {"document": True}}}
    print(dealerreview)
    response = requests.post(
        WASTON_URL + "/v1/analyze?version=2022-04-07",
        headers={"Content-Type": "application/json"},
        json=body,  # Use json parameter for automatic conversion
        auth=HTTPBasicAuth("apikey", WATSON_API),
    )

    # Check if request was successful
    if response.status_code == 200:
        sentiment = response.json()["sentiment"]["document"]["label"]
        return sentiment
    return "N/A"

def post_requests(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(
            url, headers={"Content-Type": "application/json"}, json=json_payload
        )
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_review(url, review_json_payload):
    response = post_requests(url, review_json_payload)
    return response

