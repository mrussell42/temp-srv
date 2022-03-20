# -*- coding: utf-8 -*-
import dash
# import dash_core_components as dcc
import dash_html_components as html
import dash_core_components as dcc
from .plots import make_plot, get_live_values
from datetime import datetime, timedelta, date
from temp_srv.models import get_channels_dict
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
    ch_names = list(channels.keys())
    fig1 = make_plot(ch_names, start=datetime.now() - timedelta(days=7))
    fig2 = make_plot(ch_names, start=datetime.now() - timedelta(days=1))
    fig2.update_layout(title="Last 24 Hours")
    _lv =  get_live_values(ch_names)
    default_live_display = [html.H1(f"{channels[ch]}: {round(_lv[ch],2)}", id=f"live_val{ch}") for ch in ch_names]
    layout = html.Div(
        children=[
            html.H1('Walnuts Temperature', style={
                'textAlign': 'center',
                'color': '#7FDBFF'
                }),
            # *default_live_display_H1s,
            html.Div(default_live_display, id="live_vals"),
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
                        value=list(ch_names),
                        style={'flex':1}
                        ),
                    dcc.DatePickerSingle(
                        id='start-date-picker',
                        min_date_allowed=date(2022, 1, 1),
                        max_date_allowed=date.today(),
                        initial_visible_month=date.today(),
                        date=date.today() - timedelta(days=7),
                        style={'flex':1}
                        )
                    ],
                style={'padding': 10, 'display': 'flex', 'flex-direction': 'row'},
                ),
            dcc.Graph(
                id='line-graph1',
                figure=fig1
                ),
            dcc.Graph(
                id='line-graph2',
                figure=fig2
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
    Output(component_id='line-graph1', component_property='figure'),
    Input(component_id='chan_chk', component_property='value'),
    Input(component_id='start-date-picker', component_property='date'),
    Input(component_id= 'interval-component', component_property='n_intervals')
    )
    def update_graph1(names, start, reloads):
        fig1 = make_plot(names, start)
        return fig1

    # Live Update of plot 
    @dash_app.callback(
    Output(component_id='line-graph2', component_property='figure'),
    Input(component_id='chan_chk', component_property='value'),
    Input(component_id='start-date-picker', component_property='date'),
    Input(component_id= 'interval-component', component_property='n_intervals')
    )
    def update_graph2(names, start, reloads):
        fig2 = make_plot(names, start=datetime.now() - timedelta(days=1))
        fig2.update_layout(title="Last 24 Hours")
        return fig2
    
    # Live update of Temperature values
    @dash_app.callback(
    Output(component_id='live_vals', component_property='children'),
    Input(component_id= 'interval-component', component_property='n_intervals')
    )
    def update_live_values(reloads):
        channels = get_channels_dict()
        lvs = get_live_values([channels.keys()])
        #txt = "<br>".join([f"{channels[ch]}: {lvs[ch]}" for ch in channels.keys()])
        return [html.H1(round(lvs[ch],2), id=f"live_val{ch}") for ch in channels.keys()]
        
