# -*- coding: utf-8 -*-
from flask import current_app as app
from . import db

from flask import request, render_template, redirect, url_for
from datetime import datetime, timedelta
import plotly

from .plotlydash.plots import make_plot

import json

from .models import Temperature, Device
from .forms import DeviceForm


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

@app.route('/plot/<name>')
def plot(name=None):
    # df = gen_data(3000)
    fig1 = make_plot(name)
    fig2 = make_plot(name, start=datetime.now() - timedelta(days=1))
    fig1.update_layout(width=2000, height=1000)
    fig2.update_layout(width=2000, height=1000, title="Last 24 Hours")
  
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', 
                           name=name, 
                           graphJSON1=graphJSON1,
                           graphJSON2=graphJSON2)


@app.route('/device', methods=["GET", "POST"])
def device():
    """Standard `device` form."""
    form = DeviceForm()
    if form.validate_on_submit():
        print(f"Submitted {form.name} with id {form.id}")
        existing_dev = Device.query.filter(Device.id == int(form.id.data)).first()
        if existing_dev:
            existing_dev.update({"name":form.name})
            db.session.commit()
            return redirect(url_for("updated"))
        else:
            dev = Device(id=int(form.id.data), 
                         name=form.name.data,
                         nodename="None")
            db.session.add(dev)
            db.session.commit()
            return redirect(url_for("success"))
    
    
        
    return render_template('device.jinja2',
                          form=form,
                          template="form-template"
    )
    

@app.route("/success", methods=["GET", "POST"])
def success():
    """Generic success page upon form submission."""
    return render_template(
        "success.jinja2",
        template="success-template"
    )

@app.route('/devices', methods=["GET"])
def all_devices():
    return render_template(
        'devices.jinja2',
        devices=Device.query.all(),
        title="Show Devices"
        )