import dash
from dash import html
import base64
import os
from pprintpp import pprint
from inference_clip import clip_inference
import pandas as pd
import random
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
from maindash import app
from app_data import getAppData

feedback_file="Feedback.csv"
filepath="/home/jupyter/train-CLIP-FT/app/misclassifications_ET90_SN1.csv"
gap=getAppData()
df_out=gap.get_table_data(filepath,100)
start,end=0,10
misclassification_content = dbc.Container(
    [
        html.H1(children="Analyze Misclassifications"),
        html.Br(),
        dbc.Table.from_dataframe(df_out, striped=True, bordered=True, hover=True, responsive="lg",size="lg",style = {'margin-right':'10px','margin-left':'10px'}),
        dcc.Store(id='intermediate-value')
        
    ]
)

@app.callback(
    Output('dropdown-container-output', 'children'),
    Input({'type': 'filter-dropdown', 'index': ALL}, 'value')
)
def add_radioitems(self,idx,drop_lst=None):
        return dbc.Col(
                            [
                                dcc.RadioItems(
                                                id=radio_id,
                                                options = [
                                                    {'label':'{}'.format(i), 'value':'{}'.format(i) } for i in drop_lst
                                                ]
                                                ),
                                html.Div(id='radio_button_id_out')
                            ]

# @app.callback(Output('intermediate-value', 'data'), Input('dropdown', 'value'))
# def intermediate_data(value):
#     df_out=gap.get_table_data(filepath,10)
#     return json.dumps(df_out)
    
    
    
    
# @app.callback(Output("radio_button_id_out","children"),[Input('intermediate-value', 'data'),])
# def listen_radio_buttons(dataset):
#     """
#     This callback takes in page2-buttons selected value and returns content to display
#     in selected-button
#     """
    
#     row_id, feedback= dataset["fid"].split('_')

#     row=df_out.iloc[row_id]
#     row["feedback"]=feedback
#     row.to_csv(feedback_file, mode="a", index=False, header=os.path.exists(feedback_file))
#     return 




### 