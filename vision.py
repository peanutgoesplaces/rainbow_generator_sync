import pandas as pd
import requests
from database import conn
from pathlib import Path
import os
from dotenv import load_dotenv
from tkinter import messagebox
from datetime import date, timedelta, datetime

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / '.env', override=True)

LISTENER_URL = os.environ.get("LISTENER_URL")
LISTENER_TOKEN = os.environ.get("LISTENER_TOKEN")

# Retrieves WINEPOS current inventory JSON
def retrieve_current_inventory():

    url = "http://192.168.1.223:8081/Inventory.jsp?format=json&db=ICS"


    session = requests.Session()

    # First request obtains the session cookie
    session.get(url, timeout=10)

    cookie = session.cookies.get("JSESSIONID")
    print("JSESSIONID:", "Retrieved" if cookie else "Missing")

    response = requests.get(
        f"{LISTENER_URL}/get_identity",
        headers = {"X-Listener-Token": LISTENER_TOKEN},
        timeout=10
    )

    response.raise_for_status()

    vision_identity = response.json()['identity']

    session.headers.update(
        {
        "X-Tab-Identity": vision_identity
    })

    # Request inventory
    response = session.get(url, timeout=10)

    print("RESPONSE STATUS:", response.status_code)

    response.raise_for_status()

    # Convert JSON into a DataFrame
    data = response.json()
    df = pd.DataFrame(data['rows'])

    df['item_num'] = df['item_num'].astype(str)

    df = df[['sdesc', 'item_num', 'descr', 'qoh']]
    df.columns = ['dept', 'item_num', 'item', 'qoh']

    return df

#retrieve_current_inventory()

#_____________________________________________________________

def generate_weekly_sales_df():
    global start_date
    global end_date

    today=date.today()
    #
    start_date = date.today() - timedelta(days=7)
    end_date = date.today() - timedelta(days=4)
    #
    # #Use these for manual entry
    # # start_date = date(2026,8,31)
    # # end_date = date(2026,9,6)
    #
    #
    # #WINE POS JSON WebReports for Previous Week
    # #Only Works On Order Day Thursday
    # if today.weekday() == 3:
    url = (f"http://192.168.1.223:8081/ItemsSold.jsp?"
           f"format=json&db=ICS&"
           f"start_date={start_date}&"
           f"end_date={end_date}")
    try:

        session = requests.Session()

        session.get(url, timeout=10)

        cookie = session.cookies.get("JSESSIONID")
        print("JSESSIONID:", "Retrieved" if cookie else "Missing")

        response = requests.get(
            f"{LISTENER_URL}/get_identity",
            headers={"X-Listener-Token": LISTENER_TOKEN},
            timeout=10
        )

        response.raise_for_status()

        vision_identity = response.json()['identity']

        session.headers.update(
            {
                "X-Tab-Identity": vision_identity
            })

        # Request inventory
        response = session.get(url, timeout=10)

        print("RESPONSE STATUS:", response.status_code)

        response.raise_for_status()

        # response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data['rows'])
        #print(df[df['descr'].str.contains('MARL')])

        return df


    except requests.exceptions.Timeout:
        messagebox.showinfo("Connection Timed Out")

    except requests.exceptions.ConnectionError:
        messagebox.showinfo("Could N Connect to POS Server")

    except requests.exceptions.HTTPError as e:
        messagebox.showinfo(f"HTTP Error {e}")

        return None
# else:
#     print("Its not Thursday")
#     return None
#     #messagebox.showinfo(f"{datetime.now().strftime('%A')}", "New Weekly Sales Not Updated")

#generate_weekly_sales_df()
