import os
import sys
import logging
import time
import json
from azure.eventhub import EventHubClient, Receiver, Offset
from collections import deque
import statistics
import requests
import datetime

logger = logging.getLogger("azure")

# Address can be in either of these formats:
# "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
# "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
# For example:
ADDRESS = "amqps://farmers.servicebus.windows.net/farmer"

# SAS policy and key are not required if they are encoded in the URL
USER = "RootManageSharedAccessKey"
#USER = "root"
KEY = "ItxSR2V5a+XQbEN5kmfQk5SBq390v9A2GZmfRjOmmUg="
CONSUMER_GROUP = "$default"
OFFSET = Offset("652248")
PARTITION = "0"
q = deque()

# requests
url = "https://api.amazonalexa.com/v1/proactiveEvents/stages/development"

payload = {
    "timestamp": "2019-05-14T05:35:30Z",
    "referenceId": "orangetango2221800f44-436a-4c47-8d9f-e14356bb010c",
    "expiryTime": "2019-05-14T05:45:30Z",
    "event": {
      "name": "AMAZON.MessageAlert.Activated",
      "payload": {
        "state": {
          "status": "UNREAD",
          "freshness": "NEW"
        },
        "messageGroup": {
          "creator": {
            "name": "Farm House"
          },
          "count": 1,
          "urgency": "URGENT"
        }
      }
    },
    "relevantAudience": {
        "type": "Unicast",
        "payload": {
            "user": "amzn1.ask.account.AGLOQ7EQHZ4K57TCWI4C4UOMG4KOR2GZ7ODYZTGLLZVPYIBWCGSBUJ3V77IQ3VEFWCG2HCFXNH2DN46FN7Q4PVD6MF6EHLP2NDL6PZDGWGUNDL5E2IEV4LQ55L42EYNATILU34766AKHKOWO25EIEQ5JVCGQ7GA75DUQFP5WLPVSG2HH5QXN46JKQUA363YDEVNBW2HQ4UKQNYI"
        }
    }
}

headers = {
    'Authorization': "Bearer Atc|MQEBIJC84-kQrS8AckoHZtQBeAsf6b1wTCX692gAfqXO3BLyPL9t-jKyPTf7X7MpHyQ8RNQsKAt0fq8naozLLcjU476k1lfJChOEqCfPQ7LArwwiahrfJ8UeDPDyn6SftplR3Ydna55W33lP0rpigb3OB_3xXdMR9FDswRlHOPTQbM2N6w-2_2PcFX7NCGYkzRJhcU3J5_9sED_qyywmxxOXHVIyHMXpAXp_0QCZW62FIiZDojqRkDnZswEDR_-kx1HDUoA4TOrFDeSgCEWLIGtiBkDcOu0a9s1PPlWHzT7h-mxSVQ",
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "e68ac593-305d-4254-97b0-a6394473f1ba"
    }


# payload = "{\n    \"timestamp\": \"{}\",\n    \"referenceId\": \"orangetango2221800f44-436a-4c47-8d9f-e14356bb010c\",\n    \"expiryTime\": \"2019-05-14T05:45:30Z\",\n    \"event\": {\n      \"name\": \"AMAZON.MessageAlert.Activated\",\n      \"payload\": {\n        \"state\": {\n          \"status\": \"UNREAD\",\n          \"freshness\": \"NEW\"\n        },\n        \"messageGroup\": {\n          \"creator\": {\n            \"name\": \"Andy\"\n          },\n          \"count\": 5,\n          \"urgency\": \"URGENT\"\n        }\n      }\n    },\n    \"relevantAudience\": {\n        \"type\": \"Unicast\",\n        \"payload\": {\n        \t\"user\": \"amzn1.ask.account.AGLOQ7EQHZ4K57TCWI4C4UOMG4KOR2GZ7ODYZTGLLZVPYIBWCGSBUJ3V77IQ3VEFWCG2HCFXNH2DN46FN7Q4PVD6MF6EHLP2NDL6PZDGWGUNDL5E2IEV4LQ55L42EYNATILU34766AKHKOWO25EIEQ5JVCGQ7GA75DUQFP5WLPVSG2HH5QXN46JKQUA363YDEVNBW2HQ4UKQNYI\"\n        }\n    }\n}"


# response = requests.request("POST", url, data=payload, headers=headers)

# print(response.text)


total = 0
last_sn = -1
last_offset = "-1"
client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)
try:
    receiver = client.add_receiver(CONSUMER_GROUP, PARTITION, prefetch=5000, offset=OFFSET)
    client.run()
    start_time = time.time()
    while True:
        for event_data in receiver.receive():
            last_offset = event_data.offset
            OFFSET = Offset(last_offset)
            last_sn = event_data.sequence_number
            for data in event_data.message.get_data():
                data_json = json.loads(data)
                print(data_json)
                if 'moisture' in data_json.keys():
                    moisture_data = float(data_json['moisture'])
                    q.append(moisture_data)
                    #print("Moisture: {}".format(data_json['moisture']))

                    if len(q) < 10:
                        continue

                    if len(q) > 10:
                        q.popleft()

                    queue_list = list(q)
                    avg = sum(queue_list)/(len(q)*1.0)
                    std = statistics.stdev(queue_list)

                    if moisture_data < avg - 2 * std:
                        print("moisture data: {}".format(moisture_data))
                        print("average: {}".format(avg))
                        print("under irrigation!!!")

                        ts = datetime.datetime.now(datetime.timezone.utc)
                        payload['timestamp'] = ts.strftime('%Y-%m-%dT%H:%M:%SZ')

                        ts2 = ts + datetime.timedelta(minutes = 20)
                        payload['expiryTime'] = ts2.strftime('%Y-%m-%dT%H:%M:%SZ')

                        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
                        print(response.text)

                    elif moisture_data > avg + 2 * std:
                        print("moisture data: {}".format(moisture_data))
                        print("average: {}".format(avg))
                        print("over irrigation!!!")

                        ts = datetime.datetime.now(datetime.timezone.utc)
                        payload['timestamp'] = ts.strftime('%Y-%m-%dT%H:%M:%SZ')

                        ts2 = ts + datetime.timedelta(minutes = 20)
                        payload['expiryTime'] = ts2.strftime('%Y-%m-%dT%H:%M:%SZ')

                        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
                        print(response.text)

                    else:
                        print("moisture data: {}".format(moisture_data))
                        print("average: {}".format(avg))
                        print("normal irrigation")                        

            total += 1
            print(last_offset.value)

    end_time = time.time()
    client.stop()
    run_time = end_time - start_time
    print("Received {} messages in {} seconds".format(total, run_time))

except KeyboardInterrupt:
    pass
finally:
    client.stop()