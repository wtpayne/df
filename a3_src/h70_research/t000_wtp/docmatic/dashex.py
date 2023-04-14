# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

import pprint

def run():

    print('DCC')
    print('===')

    # url_base_pathname = '/127.0.0.1:8050'
    app = dash.Dash()
    app.scripts.config.serve_locally = False
    app.css.config.serve_locally = False
    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),
    ])
    app.run_server(debug=True)


        # html.Div(children='''
        #     Dash: A web application framework for Python.
        # '''),

        # dcc.Graph(
        #     id='example-graph',
        #     figure={
        #         'data': [
        #             {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
        #             {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
        #         ],
        #         'layout': {
        #             'title': 'Dash Data Visualization'
        #         }
        #     }
        # )
