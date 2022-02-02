# -*- coding: utf-8 -*-
import dash
# import dash_core_components as dcc
import dash_html_components as html
import dash_core_components as dcc
from .plots import make_plot, get_live_values
from datetime import datetime, timedelta, date
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
    dash_app.layout = make_layout
    init_callbacks(dash_app)
    
    return dash_app.server



def make_layout():
    """
    Make the Dash Layout.
    
    This is in a function so it gets the live data when the layout is initially
    created. Subsequent updates are handled with the callbacks below.
    """


    channels = get_channels_dict()
    def_name = 92
    fig = make_plot(def_name, start=datetime.now() - timedelta(days=1))
    fig.update_layout(title="Last 24 Hours")
    _lv =  get_live_values(92)
    default_live_value = _lv if _lv is not None else 0
    layout = html.Div(
        children=[
            html.H1('Walnuts Temperature', style={
                'textAlign': 'center',
                'color': '#7FDBFF'
                }),
            html.H1(round(default_live_value,2), id="live_val1"),
            html.Div(
                children=[
                    dcc.Interval(
                        id='interval-component',
                        interval=5*60*1000, # in milliseconds
                        n_intervals=0
                        ),
                    dcc.Checklist(
                        id='chan_chk',
                        options=[{'label': v, 'value': k} for k,v in channels.items()],
                        labelStyle={'display': 'inline-block'},
                        value=[def_name],
                        style={'flex':1}
                        ),
                    dcc.DatePickerSingle(
                        id='start-date-picker',
                        min_date_allowed=date(2022, 1, 1),
                        max_date_allowed=date.today(),
                        initial_visible_month=date.today(),
                        date=date.today() - timedelta(days=1),
                        style={'flex':1}
                        )
                    ],
                style={'padding': 10, 'display': 'flex', 'flex-direction': 'row'},
                ),
            dcc.Graph(
                id='line-graph',
                figure=fig
                )
            
            ],
        id="dash-container",
        style={'padding': 10, 'flex-direction': 'row'},
        )
    return layout

def init_callbacks(dash_app):
    """
    Initalise the callbacks for the layout

    """
    
    # Live Update of plot 
    @dash_app.callback(
    Output(component_id='line-graph', component_property='figure'),
    Input(component_id='chan_chk', component_property='value'),
    Input(component_id='start-date-picker', component_property='date'),
    Input(component_id= 'interval-component', component_property='n_intervals')
    )
    def update_graph(names, start, reloads):
        fig = make_plot(names, start=start)
        fig.update_layout(title="Last 24 Hours")
        return fig
    
    # Live update of Temperature values
    @dash_app.callback(
    Output(component_id='live_val1', component_property='children'),
    Input(component_id= 'interval-component', component_property='n_intervals')
    )
    def update_live_values(reloads):
        return f"Inside Temperature: {get_live_values(92)}"
