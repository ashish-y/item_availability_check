
import requests
from datetime import datetime
import time
import random
import boto3
import os
from dotenv import load_dotenv
load_dotenv()

# global vars
is_available = 0
attempts = 0

# update header accordingly
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36', 'authority': 'www.bestbuy.com'}


# send notification
def publish(gpu_name):
    arn = os.environ.get("arn")
    sns_client = boto3.client(
        'sns',
        aws_access_key_id=os.environ.get("aws_access_key_id"),
        aws_secret_access_key=os.environ.get("aws_secret_access_key"),
        region_name=os.environ.get("region_name")
    )
    response = sns_client.publish(
        TopicArn=arn, Message="GPU in Stock! Grab it!" + gpu_name)


while(is_available == 0):
    items = [{
        'item_url': 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442',
        'item_name': "Nvidia FE", 'search_string': 'Sold Out</button>'}, {
        'item_url': 'https://www.bestbuy.com/site/gigabyte-geforce-rtx-3070-8g-gddr6-pci-express-4-0-graphics-card-black/6437912.p?skuId=6437912',
        'item_name': "gigabyte-geforce-rtx-3070",  'search_string': 'Sold Out</button>'}, {
        'item_url': 'https://www.bestbuy.com/site/pny-geforce-rtx-3070-8gb-dual-fan-graphics-card/6432654.p?skuId=6432654',
        'item_name': "pny-geforce-rtx-3070",  'search_string': 'Sold Out</button>'}, {
        'item_url': 'https://www.bestbuy.com/site/gigabyte-geforce-rtx-3070-8g-gddr6-pci-express-4-0-graphics-card-black/6439384.p?skuId=6439384',
        'item_name': "gigabyte-geforce-rtx-3070",  'search_string': 'Coming Soon</button>'}
    ]

    for item in items:
        url = item['item_url']
        name = item['item_name']
        search_string = item['search_string']
        result = requests.get(url, headers=headers)
        result = (result.content.decode())
        search_result = result.find(search_string)
        if search_result != -1:
            print(name+" Out of Stock!")
            print('Time = ' + str(datetime.now()) +
                  " - Attempts = " + str(attempts))
            time.sleep(random.randint(20, 60))  # + some gitter
        else:
            is_available = 1
            print(name+"available - notify")
            publish(name)
    attempts += 1
