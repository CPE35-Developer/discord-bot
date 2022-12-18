import requests
import json

url = "https://discord.com/api/webhooks/876803540373356554/7WamQ19zryaLvSNPK-W95aK8gd5htJhVYqYZsMczKRgv5GjoP0p5Jjt4HlzjclQugBnX/messages/876809715118637116"

with open('scripts/info_offline.json', "r", encoding='utf-8') as json_file:
    data = json.load(json_file)

result = requests.patch(url, json=data)

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print("Payload delivered successfully, code {}.".format(result.status_code))
