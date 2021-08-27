import requests, json
from random import randrange
from datetime import timedelta
from datetime import datetime
import random
import string
import os
from dotenv import load_dotenv

load_dotenv()

print("Program testujący obciążenie bazy danych na serwerze.")

def main(skipQuestion):
    # Getting count of event and request from user.
    count_events = input("wpisz ile wygenerować zdarzeń (default = 1): ")
    count_request = input("wpisz ile wysłać takich requestów z tą samą ilością zdarzeń. (default = 1): ")

    count_events = checkIsInt(count_events, 1)
    count_request = checkIsInt(count_request, 1)

    data = createNewEvents(count_events)
    if(not skipQuestion):
        passing = askUserBool("Wygenerowano zdarzenia, czy wysłać je na serwer ? (true/ false): ")

        if(passing == 'true'):
            sendRequest(data, count_request)
            again = askUserBool("Czy wysłać zapytanie ponownie ? (true / false): ")
            if(again == 'true'):
                main(True)
            else:
                print("Exited.")
        else:
            print('Exited.')
    else:
        sendRequest(data, count_request)
        again = askUserBool("Czy wysłać zapytanie ponownie ? (true / false): ")
        if(again == 'true'):
            main(True)
        else:
            print("Exited.")

def sendRequest(data, count):
    showFulldata = askUserBool("Czy pokazać odpowiedź serwera na zapytanie? (true / false): ")
    for which in range(count):
        try:
            r = requests.post(os.environ.get('url'), data = data)

            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred {http_err}')
        except Exception as err:
            print(f'Other error occurred {err}')
        else:
            print("Odpowiedz od serwera - Code Status: "+str(r.status_code)+" - Numer zapytania: "+str(which + 1)+" - Czas zapytania: "+str(r.elapsed.total_seconds()))
            if(showFulldata == "true"):
                print(r.json())


def askUserBool(msg):
    while True:
        try:
            passing = str(input(msg))
            if(passing == 'true' or passing == 'false'):
                break
            else:
                print("This command didn't match.")
                continue
        except ValueError:
            print("This command didn't match.")
            continue

    return passing

def createNewEvents(count_events):
    events = []
    # GENERATE A EVENT WITH A RANDOM COMMENT AND A DATETIME.
    for _ in range(count_events):
        temp = {"comment":get_random_string(10),"datetime":random_date(),"gps":"59.2545413;18.1161158","id":8,"location":"Tompol/sköndal","source":6,"status":0,"type":2}
        events.append(temp)

    result = {"password" : str(os.environ.get('password')), "login" : str(os.environ.get('login')), "events" : json.dumps(events)}

    return result

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

def checkIsInt(what, default):
    try:
        what = int(what)
    except ValueError:
        what = default

    return what

if(__name__) == '__main__':
    try:
        main(False)
    except MemoryError:
        sys.stderr.write("Maximum Memory Exceeded")
        sys.exit(-1)