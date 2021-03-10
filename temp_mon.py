from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Temperature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dev_datetime = db.Column(db.DateTime, nullable=False)
    submit_time = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    value = db.Column(db.Float, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)

    def _repr_(self):
        # Add device name to this string
        return f'Device {self.device_id} Temperature {self.value} at {delf.datatime}'

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nodename = db.Column(db.Integer, nullable=False)  # this is the node key
    name = db.Column(db.String(80), nullable=False)
    

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == "POST":
        print(request.form.get('temp'))
        print(hello_world())
    else:
        # Do nothing, its a submit url
        pass
    
    return "Success"

@app.route('/plot')
@app.route('/plot/<name>')
def plot(name=None):
    
    #return "I will plot it when I'm ready"
    return render_template('plot.html', name=name)

def hello_world():
    return 'Hello, World!'

