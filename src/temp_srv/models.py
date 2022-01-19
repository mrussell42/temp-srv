# -*- coding: utf-8 -*-


from . import db
from datetime import datetime

                     
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
    

def get_channels_dict():
    q = Device.query.all()
    channels = {ch.id:ch.name for ch in q}
    return channels