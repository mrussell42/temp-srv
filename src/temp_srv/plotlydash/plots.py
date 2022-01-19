# -*- coding: utf-8 -*-
import plotly.graph_objects as go
from temp_srv.models import Temperature
import pandas as pd


def make_plot(chan, start=None, stop=None):
    fig = go.Figure()
    if isinstance(chan, str):
        if chan.lower() == "all":
            chan =  (91,92)
        else:
            chan = [chan]
    
    for ch in chan:
        line = make_line(ch, start=start, stop=stop)
        fig.add_trace(line)
            
    
    return fig


def make_line(chan, start=None, stop=None):
    q = Temperature.query.filter_by(device_id=chan)
    if start is not None:
        q = q.filter(Temperature.submit_time>start)
    if stop is not None:
        q = q.filter(Temperature.submit_time<stop)
                
    df = pd.read_sql(q.statement, q.session.bind)
    line = go.Scatter(x=df.dev_datetime, y=df.value, mode='lines', name=str(chan))
    return line