import datetime, time, requests
from datetime import date
from math import ceil
import pandas as pd
import os
import matplotlib.pyplot as plt
from fbprophet import Prophet
import io


def getdata(arg, years):
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
    data = data[
        ["Date", "Close"]
    ]  # select Date and Price# Rename the features: These names are NEEDED for the model fitting
    data = data.rename(columns={"Date": "ds", "Close": "y"})
    m = Prophet(daily_seasonality=True)  # the Prophet class (model)
    m.fit(data)
    future = m.make_future_dataframe(
        periods=365
    )  # we need to specify the number of days in future
    prediction = m.predict(future)
    df = prediction[["ds", "yhat", "trend"]]
    df["ds"] = df["ds"].astype(str)
    data_list = df.values.tolist()
    return data_list
