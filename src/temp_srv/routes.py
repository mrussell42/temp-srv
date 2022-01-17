# -*- coding: utf-8 -*-
from flask import current_app as app
from . import db

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import plotly
import pandas as pd


import json

from .models import Temperature


@app.route('/')
def home():
    """Landing page."""
    return render_template(
        'home.html',
        title="Jinja Demo Site",
        description="Smarter page templates with Flask & Jinja."
    )

@app.route('/submit', methods=['POST'])
def submit():
    request_data = request.get_json()
    print(request_data)
    if request_data.get('datatype', None) == "temp":
        dev_datestr = request_data.get('dev_datestr')
        value = request_data.get('value')
        device_id = request_data.get('device_id')
        t = Temperature(dev_datetime=datetime.fromisoformat(dev_datestr), value=value, device_id=device_id)
        db.session.add(t)
        db.session.commit()
    else:
        print("Not a temp submit")
    
    return "Success"


@app.route('/plot')
@app.route('/plot/<name>')
def plot(name=None):
    # df = gen_data(3000)
    fig1 = go.Figure()
    fig2 = go.Figure()
    if name.lower() == "all":
        for chan in (91,92):
            line1 = make_line(chan)
            fig1.add_trace(line1)
            line2 = make_line(chan, start=datetime.now() - timedelta(days=1))
            fig2.add_trace(line2)
            
    else:             
        line1 = make_line(name)
        fig1.add_trace(line1)
        line2 = make_line(name, start=datetime.now() - timedelta(days=1))
        fig2.add_trace(line2)
    
    fig1.update_layout(width=2000, height=1000)
    fig2.update_layout(width=2000, height=1000, title="Last 24 Hours")
    
        
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', 
                           name=name, 
                           graphJSON1=graphJSON1,
                           graphJSON2=graphJSON2)



def make_line(chan, start=None, stop=None):
    q = Temperature.query.filter_by(device_id=chan)
    if start is not None:
        q = q.filter(Temperature.submit_time>start)
    if stop is not None:
        q = q.filter(Temperature.submit_time<stop)
                
    df = pd.read_sql(q.statement, q.session.bind)
    line = go.Scatter(x=df.dev_datetime, y=df.value, mode='lines', name=str(chan))
    return line
    