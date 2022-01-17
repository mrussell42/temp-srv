from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import plotly
import pandas as pd


import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


                     
class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dev_datetime = db.Column(db.DateTime, nullable=False)
    submit_time = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    value = db.Column(db.Float, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    device = db.relationship("Device", back_populates="temperatures")

    def __repr__(self):
        # Add device name to this string
        dev_name = self.device.name if self.device else None
        return f'Device {dev_name} Temperature {self.value} at {self.dev_datetime}'


class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nodename = db.Column(db.Integer, nullable=False)  # this is the node key
    name = db.Column(db.String(80), nullable=False)
    temperatures = db.relationship("Temperature", back_populates="device")
    
    
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
    fig = go.Figure()
    if name.lower() == "all":
        for chan in (91,92):
            q = Temperature.query.filter_by(device_id=chan)
            df = pd.read_sql(q.statement, q.session.bind)
            line = go.Scatter(x=df.dev_datetime, y=df.value, mode='lines', name=str(chan))
            fig.add_trace(line)
            
    else:             
        q = Temperature.query.filter_by(device_id=name)
        df = pd.read_sql(q.statement, q.session.bind)
        fig = px.line(df, x='dev_datetime', y='value')
        fig.update_traces(mode='markers+lines')
        
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', name=name, graphJSON=graphJSON)


