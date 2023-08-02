import requests
import json
import random
import string


async def create_client(name, phone, address):
    url = "https://sunrise.salesdoc.io/api/v2/"

    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choices(characters, k=15))

    client_data = {
        "auth": {
            "userId": "d0_67",
            "token": "7218bd59fa2a4eda570b887191db8343"
        },
        "method": "setClient",
        "filial": {
            "filial_id": ""
        },
        "data": {
            "client": [
                {
                    "code_1C": f"{unique_id}",
                    "shortName": f"{name}",
                    "firmName": f"{name}",
                    "address": f"{address}",
                    "tel": f"{phone}",
                    "clientCategory": {
                        "CS_id": "d0_15",
                        "SD_id": "d0_15",
                        "code_1C": "client_cat_1690617537_912"
                    },
                    "active": "Y",
                    "agent": {
                        "CS_id": "f1-d0_3",
                        "SD_id": "d0_3"
                    }
                }
            ]
        }
    }

    payload = json.dumps(client_data)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    client_id = response.json()["result"]["data"]["client"][0]["SD_id"]
    return client_id


async def create_order(client_id, total, products):
    url = "https://sunrise.salesdoc.io/api/v2/"

    payload = json.dumps({
        "auth": {
            "userId": "d0_67",
            "token": "7218bd59fa2a4eda570b887191db8343"
        },
        "method": "setOrder",
        "data": {
         "order": [
          {
           "code_1C": f"{client_id}",
           "totalSumma": total,
           "comment": "Заказ из бота",
           "status": 1,
           "client": {
            "SD_id": f"{client_id}"
           },
           "agent": {
            "CS_id": "f1-d0_3",
            "SD_id": "d0_3"
           },
           "priceType": {
            "CS_id": "d0_5",
            "SD_id": "d0_5"
           },
           "warehouse": {
            "CS_id": "f1-d0_1",
            "SD_id": "d0_1"
           },
           "orderProducts": products
          }
         ]
        }
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response
