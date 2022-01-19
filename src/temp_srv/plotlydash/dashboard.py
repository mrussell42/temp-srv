# -*- coding: utf-8 -*-
import dash
# import dash_core_components as dcc
import dash_html_components as html
import dash_core_components as dcc
from .plots import make_plot
from datetime import datetime, timedelta
from temp_srv.models import Temperature, get_channels_dict
import pandas as pd
from dash.dependencies import Input, Output

def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashapp/',
        external_stylesheets=[
            '/static/dist/css/styles.css',
        ]
    )
    df = get_dataframe(chan=92)
    channels = get_channels_dict()
    print(channels)
    # Create Dash Layout
    #dash_app.layout = html.Div(id='dash-container')
    name = "92"
    fig = make_plot(name, start=datetime.now() - timedelta(days=1))
    fig.update_layout(title="Last 24 Hours")
    dash_app.layout = html.Div(
        children=[
            dcc.Checklist(
                id='chan_chk',
                options=[{'label': v, 'value': k} for k,v in channels.items()],
                labelStyle={'display': 'inline-block'},
                value=list(channels.keys())
                ),
            dcc.Graph(
                id='line-graph',
                figure=fig
                )
            ],
        id="dash-container",
        )
    init_callbacks(dash_app)
    
    return dash_app.server



def init_callbacks(dash_app):
    
    
    @dash_app.callback(
    Output(component_id='line-graph', component_property='figure'),
    Input(component_id='chan_chk', component_property='value')
    )
    def update_graph(names):
        
        fig = make_plot(names, start=datetime.now() - timedelta(days=1))
        fig.update_layout(title="Last 24 Hours")
        return fig



def get_dataframe(chan, start=None, stop=None):
    q = Temperature.query.filter_by(device_id=chan)
    if start is not None:
        q = q.filter(Temperature.submit_time>start)
    if stop is not None:
        q = q.filter(Temperature.submit_time<stop)
                
    df = pd.read_sql(q.statement, q.session.bind)
    return df