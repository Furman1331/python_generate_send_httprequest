import requests, json
from random import randrange
from datetime import timedelta
from datetime import datetime
import random
import string
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    data = createNewEvents(1)
    r = requests.post('URL', data = data)

def createNewEvents(count):
    events = []
    # GENERATE A EVENT WITH A RANDOM COMMENT AND A DATETIME.
    for _ in range(count):
        events.append(json.dumps('{"comment":"'+get_random_string(10)+'","datetime":"'+random_date()+'","gps":"59.2545413;18.1161158","id":9,"location":"Tompol/sköndal","source":6,"status":0,"type":2}'))

    result = [
        {
            "key": "password",
            "value": "YOUR PASSWORD",
            "type": "text"
        },
        {
            "key": "login",
            "value": "YOUR LOGIN",
            "type": "text"
        },
        {
            "key": "events",
            "value": json.dumps(events),
            "type": "text"
        }
    ]

    return json.dumps(result)

def random_date():
    delta = datetime.strptime('1/1/2025 4:50 AM', '%m/%d/%Y %I:%M %p') - datetime.strptime('1/1/2022 1:30 PM', '%m/%d/%Y %I:%M %p')
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return (datetime.strptime('1/1/2022 4:50 AM', '%m/%d/%Y %I:%M %p') + timedelta(seconds=random_second)).strftime("%Y/%m/%d %H:%M:%S")

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

if(__name__) == '__main__':
    try:
        main()
    except MemoryError:
        sys.stderr.write("Maximum Memory Exceeded")
        sys.exit(-1)