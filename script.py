import os
from dotenv import load_dotenv
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
        url= os.getenv('DOMAIN'), 
        consumer_key= os.getenv('CONSUMER_KEY'), 
        consumer_secret= os.getenv('CONSUMER_SECRET'), 
        wp_api=True, 
        version="wc/v3" 
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
    
    match get_parse_result:
        case 502:
            changePrice(raised_price, product_to_sell_id)

        case 800:
            changePrice(lowered_price, product_to_sell_id)

        case _:
            changePrice(regular_price, product_to_sell_id)
    

getWeather()
