#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
An example to show running concurrent receivers.
"""

import os
import sys
import time
import logging
import asyncio
import json
from azure.eventhub import Offset, EventHubClientAsync, AsyncReceiver

logger = logging.getLogger("azure")


# Address can be in either of these formats:
# "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
# "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
ADDRESS = "amqps://farmers.servicebus.windows.net/farmer"

# SAS policy and key are not required if they are encoded in the URL
USER = "RootManageSharedAccessKey"
#USER = "root"
KEY = "ItxSR2V5a+XQbEN5kmfQk5SBq390v9A2GZmfRjOmmUg="
CONSUMER_GROUP = "$default"
OFFSET = Offset("-1")

last_offset_value = "-1"

async def pump(client, partition):
    receiver = client.add_async_receiver(CONSUMER_GROUP, partition, OFFSET, prefetch=5)
    await client.run_async()
    total = 0
    start_time = time.time()
    for event_data in await receiver.receive(timeout=10):
        for data in event_data.message.get_data():
            data_json = json.loads(data)
            print(data_json)
        last_offset = event_data.offset
        last_offset_value = last_offset.value
        last_sn = event_data.sequence_number
        print("Received: {}, {}".format(last_offset_value, last_sn))
        total += 1
    end_time = time.time()
    run_time = end_time - start_time
    print("Received {} messages in {} seconds".format(total, run_time))
    #OFFSET = Offset(last_offset_value)

try:
    if not ADDRESS:
        raise ValueError("No EventHubs URL supplied.")

    loop = asyncio.get_event_loop()
    client = EventHubClientAsync(ADDRESS, debug=False, username=USER, password=KEY)

    tasks = [
        asyncio.ensure_future(pump(client, "0")),
        asyncio.ensure_future(pump(client, "1"))]
    loop.run_until_complete(asyncio.wait(tasks))

    loop.run_until_complete(client.stop_async())
    loop.close()

except KeyboardInterrupt:
    pass