import dash
from dash import html
import base64
import os
from pprintpp import pprint
# from inference_clip import clip_inference
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
from dash import dcc, html, Input, Output, callback, ALL, MATCH
import json

feedback_file=os.path.join("/Users/g0s00lq/Documents/Github_new/NextGen/train-CLIP-FT/app","Feedback.txt")
filepath=os.path.join(os.getcwd(),"misclassifications_ET90_SN1.csv")
gap=getAppData()

st=(1*10)-10
end=st+10
# df_out=gap.get_table_data(filepath,st,end)
seattle = "[![Seattle](/Users/g0s00lq/Documents/Github_new/NextGen/dvc-manual/data/80gtin_allsubfolders/splitfolders/test/00010900003308/171581_1.png#thumbnail)]"
# seattle = "<img src='/Users/g0s00lq/Documents/Github_new/NextGen/dvc-manual/data/80gtin_allsubfolders/splitfolders/test/00010900003308/171581_1.png' height='400' />"
paris = "<img src='https://upload.wikimedia.org/wikipedia/commons/a/a8/Tour_Eiffel_Wikimedia_Commons.jpg' height='400' />"
nyc = "<img src='https://upload.wikimedia.org/wikipedia/commons/d/dd/Lady_Liberty_under_a_blue_sky_%28cropped%29.jpg' height='400' />"

def generate_thumbnail(encoded_image):
    return html.Div(
        [
            html.A(
                [
                    html.Img(
                        src=f"data:image/png;base64,{encoded_image.decode()}",
                        style={
                            "height": "80%",
                            "width": "80%",
                            "float": "left",
                            "position": "relative",
                            "padding-top": 0,
                            "padding-right": 10,
                        },
                    )
                ],
                # href="https://www.google.com",
            ),
        ]
    )



df = pd.DataFrame(
    dict(
        [
            ("temperature", [13, 43, 50]),
            ("city", ["NYC", "Paris", "Seattle"]),
            ("image", [nyc, paris, seattle]),
        ]
    )
)

misclassification_content = html.Div(
    [
        dash_table.DataTable(
            # css=[dict(selector="p", rule="margin: 0px;")],
            css=[{"selector":".dropdown", "rule": "position: static"}],
            data=df.to_dict("records"),
            columns=[
                {"id": "image", "name": "image", "presentation": "markdown"},
                {"id": "city", "name": "city"},
                {"id": "temperature", "name": "temperature"},
            ],
            style_cell_conditional=[{"if": {"column_id": "image"}, "width": "200px"}],
            markdown_options={"html": True},
            style_table={"width": 800},
        )
    ]
)


# misclassification_content = html.Div([
#     html.Button("Add Filter", id="dynamic-add-filter", n_clicks=0),
#     html.Div(id='dynamic-dropdown-container', children=[]),
#     dbc.Table.from_dataframe(df_out, striped=True, bordered=True, hover=True, responsive="lg",size="lg",style = {'margin-right':'2px','margin-left':'2px'}),
# ])