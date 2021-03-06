import datetime, time, requests
from datetime import date
from math import ceil
import pandas as pd
import os
import io
import matplotlib.pyplot as plt

# from fbprophet import Prophet


def get_chartdata(arg, years):
    today = date.today()
    now_str = today.strftime("%d/%m/%Y")
    DD = datetime.timedelta(days=ceil(7 * 52.177457 * years))
    earlier = today - DD
    earlier_str = earlier.strftime("%d/%m/%Y")
    n_tmstp = int(
        time.mktime(datetime.datetime.strptime(now_str, "%d/%m/%Y").timetuple())
    )
    e_tmstp = int(
        time.mktime(datetime.datetime.strptime(earlier_str, "%d/%m/%Y").timetuple())
    )

    url = f"https://query1.finance.yahoo.com/v7/finance/download/{arg}.NS?period1={e_tmstp}&period2={n_tmstp}&interval=1d&events=history&includeAdjustedClose=true"

    r = requests.get(url)

    data = pd.read_csv(io.StringIO(r.content.decode("utf-8")))
    data = data.dropna(axis=0)
    data["Date"] = data["Date"].astype(str)
    mylist = data.loc[:, ["Date", "Low", "Open", "Close", "High"]]
    data_list = mylist.values.tolist()
    return data_list
