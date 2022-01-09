from tkinter import *
import requests
import json
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np


root = Tk()
root.title("Stock Price Lookup")

frame = LabelFrame(root)
frame.pack()

myLabel1 = Label(frame,text='Enter Stock Ticker')
e1 = Entry(frame,width=50,borderwidth=2)
myLabel1.grid(row=0,column=0)
e1.grid(row=1,column=0)


def closing_price():
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')
    five_mons = datetime.now() - relativedelta(months=5)
    past = five_mons.strftime('%Y-%m-%d')
    
    
    try:
        tick = e1.get()
        api_key = 'c3EHhR2wVKRxlfRUvipd3FF4Ggb_ozia'
        ticker = str(tick)
        multiplier = 1
        timespan = 'day'
        start = past
        end = today

        api_url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{start}/{end}?adjusted=true&sort=asc&limit=120&apiKey={api_key}'

        data = requests.get(api_url).json()

        prior_5_months = {}

        for i in range(len(data['results'])):
            ms = data['results'][i]['t']
            ts = ms / 1000.0
            date = datetime.utcfromtimestamp(ts).strftime('%m-%d-%Y')
            prior_5_months[date] = data['results'][i]['c']

        fm_avg = round(np.mean(list(prior_5_months.values())),2)
        last_close = list(prior_5_months.values())[-1]
        
        global myLabel
        myLabel = Label(frame,text=f'Last Close Price: {last_close} , Five Month Average: {fm_avg}')
        myLabel.grid(row=3,column=0,columnspan=3)
        
    except:
        myLabel.destroy()
        myLabel2 = Label(frame,text='Stock Ticker Does Not Exist')
        myLabel2.grid(row=3,column=0,columnspan=3)
    
    
    

myButton = Button(frame,width=20,text="Find Last Closing Price",activebackground='#8af',command=closing_price)
myButton.grid(row=2,column=0)

root.mainloop()