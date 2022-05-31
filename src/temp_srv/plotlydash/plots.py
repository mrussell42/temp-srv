# -*- coding: utf-8 -*-
import plotly.graph_objects as go
from temp_srv.models import Temperature, Device
import pandas as pd
import pytz


def make_plot(chan, start=None, stop=None):
    fig = go.Figure()
    if isinstance(chan, str):
        if chan.lower() == "all":
            chan =  (91,92)
        else:
            chan = [chan]
    if isinstance(chan, int):
        chan=[chan]
        
    for ch in chan:
        line = make_line(ch, start=start, stop=stop)
        fig.add_trace(line)
    fig.update_layout(height=1000)
    
    return fig


def make_line(chan, start=None, stop=None):
    dev = Device.query.get(chan)
    
    q = Temperature.query.filter_by(device_id=chan)
    if start is not None:
        q = q.filter(Temperature.submit_time>start)
    if stop is not None:
        q = q.filter(Temperature.submit_time<stop)
    
    df = pd.read_sql(q.statement, q.session.bind, index_col='dev_datetime')
    if len(df) > 0:
        # This fails if there isn't any data in the pandas obj
        df.index = df.index.tz_localize(pytz.utc)
        df.index = df.index.tz_convert('Europe/London')
    line = go.Scatter(x=df.index, y=df.value, mode='lines', name=dev.name)
    return line

def get_live_values(channels):
    live_values = {}
    for ch in channels:
        q = Temperature.query.filter_by(device_id=ch).order_by(Temperature.submit_time.desc()).first()
        if q is not None:
            live_values[ch] = q.value
    return live_values