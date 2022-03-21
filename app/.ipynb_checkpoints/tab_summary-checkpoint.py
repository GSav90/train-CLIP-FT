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
import plotly.graph_objects as go
import plotly.express as px

    



    


########################################
############Summary metrics ############
########################################

# def get_summary_metrics(summary_df,drop_lst):
#     if summary_df.shape[0]==0:
#         summary_df=pd.DataFrame({"feedback": drop_list, "count":[0]*len(drop_lst)})
#     fig=px.bar(summary_df, x='feedback', y='count',orientation='h')
#     return fig
    


summary_content = dbc.Container(
    [
        html.H1(children="Summary Metrics"),
        html.Br(),
        # html.Div([dcc.Graph(figure=get_summary_metrics())])
        
    ]
)


