import os
from dotenv import load_dotenv
#from itertools import product
import requests
import json
from woocommerce import API

load_dotenv()
product_to_sell_id = "1736"
raised_price = "12"
lowered_price = "8"
regular_price = "10"

def changePrice(price, idProduct):

    wcapi = API(
        url= os.getenv('DOMAIN'), # Your store URL
        consumer_key= os.getenv('CONSUMER_KEY'), # Your consumer key
        consumer_secret= os.getenv('CONSUMER_SECRET'), # Your consumer secret
        wp_api=True, # Enable the WP REST API integration
        version="wc/v3" # WooCommerce WP REST API version
    )

    data = {
        "regular_price": price
    }

    wcapi.put("products/" + idProduct, data).json()
    
    print("New price set to " + data["regular_price"])


def getWeather():

    url = os.getenv('API_BASEURL')

    headers = {
    "Accept": "application/json"
    }
    
    payload = {
    "key": os.getenv('API_KEY'),
    "city": os.getenv('API_CITY'),
    "country": os.getenv('API_COUNTRY')
    }
    

    response = requests.request(
    "GET",
    url,
    params=payload,
    headers=headers  
    )

    data = response.text

    parse_json = json.loads(data)

    get_parse_result = parse_json["data"][0]["weather"]["code"]
    #get_parse_result = 502
    
    #Use switch statement in Python 3.10
    if (get_parse_result == 502):
        changePrice(raised_price, product_to_sell_id)
    elif(get_parse_result == 800):
        changePrice(lowered_price, product_to_sell_id)
    else:
        changePrice(regular_price, product_to_sell_id)


getWeather()