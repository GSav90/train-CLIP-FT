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
from tab_misclassification import misclassification_content
from tab_summary import summary_content
from maindash import app



app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Classification Evaluation"),
        html.Hr(),
        
        dbc.Tabs(
            [
                dbc.Tab(label="Analyze Misclassifications", tab_id="misclassification_id"),
                dbc.Tab(label="Summary Metrics", tab_id="summary_id"),
            ],
            id="tabs",
            active_tab="misclassification_id",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")]
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab == "misclassification_id":
        return misclassification_content
    elif active_tab == "summary_id":
        return summary_content
    return "No tab selected"    

    
    
# images = []
# d = "/home/jupyter/dvc-manual/gtin_60/data/prep/subsets/enrollment_size_30_SN_1/10900003308"
# for path in os.listdir(d):
#     full_path = os.path.join(d, path)
#     if os.path.isfile(full_path):
#         images.append(full_path)


# images_div = []
# for i in images:
#     encoded_image = base64.b64encode(open(i, "rb").read())
#     images_div.append(generate_thumbnail(encoded_image))

# app.layout = html.Div(images_div)

if __name__ == "__main__":
    # app.run_server(debug=True)
    app.server.run(port=8000, host="127.0.0.1", debug=True)

    
    ## port forwarding to local
#     gcloud compute ssh gaurav.savlani@enrollment-eval-v3 --project wmt-892b8050ebef7b873b51427a84 --tunnel-through-iap  --zone "us-west1-b" -- -NL 8000:localhost:8000

"""
Goal: Take user feedback based on the input chosen in dropdown menu
    1 dropdown menu per row. 
