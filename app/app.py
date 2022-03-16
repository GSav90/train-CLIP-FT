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
from layouts import misclassification_content,summary_content
# from dash_colorgrading import discrete_background_color_bins

# external_stylesheets =[dbc.themes.BOOTSTRAP] # ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(external_stylesheets=[dbc.themes.PULSE])
# (color_grading_styles, legend) = discrete_background_color_bins(df, columns=cols)
# image_filename = "/Users/g0s00lq/Documents/Github_new/self_experiments/code_samples/catalog_data/00011115871324/0a439101-7fc7-4e38-a983-2656e92cafa8_1.f69ff07a5afdb36c60b81a40a3e98442.jpeg"  # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, "rb").read())

# app.layout = html.Div([html.Img(src=f"data:image/png;base64,{encoded_image.decode()}")])



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

    