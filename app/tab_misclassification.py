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


filepath="/home/jupyter/train-CLIP-FT/app/misclassifications_ET90_SN1.csv"
gap=getAppData()
df_out=gap.get_table_data(filepath)
feedback_file="Feedback.csv"


misclassification_content = dbc.Container(
    [
        html.H1(children="Analyze Misclassifications"),
        html.Br(),
        dbc.Table.from_dataframe(df_out, striped=True, bordered=True, hover=True, responsive="lg",size="lg",style = {'margin-right':'10px','margin-left':'10px'})

    ]
)


@app.callback(Output("radio_button_id_out","children"),[Input("feedback_radio_id","value")])
def listen_radio_buttons(value):
    """
    This callback takes in page2-buttons selected value and returns content to display
    in selected-button
    """
    row_id, feedback= value.split('_')
    row=df_out.iloc[row_id]
    row["feedback"]=feedback
    row.to_csv(feedback_file, mode="a", index=False, header=os.path.exists(feedback_file))
    return 