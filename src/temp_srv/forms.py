# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length


class DeviceForm(FlaskForm):
    """Device Form"""

    id = IntegerField(
        'Node ID',
        [DataRequired()]
        )
    
    name = StringField(
        "Device Name",
        [DataRequired()]
        )
    submit = SubmitField('Submit')
    