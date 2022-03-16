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
from app import app
from tab_misclassification import misclassification_content

drop_lst=["GTIN Incorrectly labeled", "Cleanup Enrollment Images","Model Error","Multiple Items","Other"],
filepath="/home/jupyter/train-CLIP-FT/app/misclassifications_ET90_SN1.csv"
df=pd.read_csv(filepath)
drop_list= ["GTIN Incorrectly labeled", "Cleanup Enrollment Images","Model Error","Multiple Items","Other"]


true_gtin_name, predicted_gtin_name, true_img_thumbnail, prediction_thumnails= "","",None,None

df_misclassification=pd.DataFrame()
start=0
n_rows=20
for idx,row in df.iloc[start:start+n_rows].iterrows():
    true_gtin_name, predicted_gtin_name, true_img_thumbnail, prediction_thumnails= get_misclassifications(df)
    row= {"true_img_thumbnail": true_img_thumbnail,\
          "true_gtin_name": true_gtin_name, 
          "predicted_gtin_name": predicted_gtin_name,\
             "pred_sample_1": prediction_thumnails[0],
             "pred_sample_2": prediction_thumnails[1],
             "pred_sample_3": prediction_thumnails[2],
             "pred_sample_4": prediction_thumnails[3],
             "pred_sample_5": prediction_thumnails[4],
              "Refresh": html.A(html.Button('Refresh'),href='/'),
             "feedback_inp": add_radioitems(idx,drop_list),
              "feedback_out": None
            }
    
    df_misclassification=df_misclassification.append(row,ignore_index=True)



@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"),
    Input("store", "data")]
)
def render_tab_content(active_tab,data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab and data is not None:
        if active_tab == "misclassification_id":
            if "misclassification" in data:
                return get_misclassification_content(data["misclassification"])
            else:
                return get_misclassification_content(df_misclassification)
        elif active_tab == "summary_id":

            return get_summary_content(data["summary"])
    return "No tab selected"

@app.callback(
    Output("radio_button_id_out","children"),
    [Input("feedback_radio_id","value")
    Input("feedback_radio_id","value")]
)
def listen_radio_buttons(value):
    """
    This callback takes in page2-buttons selected value and returns content to display
    in selected-button
    """
    row_id= value.split('_')[0]
    feedback = value.split('_')[1]
    df=pd.read_csv(filepath)
    df.loc[df["feedback"]==feedback,["count"]]+=1
    
    return