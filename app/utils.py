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

def get_n_thumbnail_from_folder(folder_path,n=5):
    images = []
    for path in os.listdir(folder_path):
        full_path = os.path.join(folder_path, path)
        if os.path.isfile(full_path):
            images.append(full_path)
    images_div = []
    samples=random.sample(images, n)
    for i in samples:
        encoded_image = base64.b64encode(open(i, "rb").read())
        images_div.append(generate_thumbnail(encoded_image))
    return images_div


        
def get_misclassifications(df):
    
    true_gtin_name=row["name"]
    predicted_gtin_name=row["name_predictions"]

    true_img_path=row["img_path"]
    encoded_image = base64.b64encode(open(true_img_path, "rb").read())
    true_img_thumbnail=generate_thumbnail(encoded_image)

    predicted_img_folder_path=row["predicted_gtin_enroll_folder"]
    prediction_thumnails=get_n_thumbnail_from_folder(predicted_img_folder_path,5)
        
    return true_gtin_name, predicted_gtin_name, true_img_thumbnail, prediction_thumnails


def add_dropdown(idx):
    return dbc.DropdownMenu(label=str(idx),id=f"id_{str(idx)}",children=[
                dbc.DropdownMenuItem("GTIN Incorrectly labeled"),
                dbc.DropdownMenuItem("Cleanup Enrollment Images"),
                dbc.DropdownMenuItem("Model Error"),
                dbc.DropdownMenuItem("Multiple Items in Test Image with true class"),
                dbc.DropdownMenuItem("Other"),
            ],color="success", className="m-1"
            )


def add_radioitems(idx,drop_lst):
    return dbc.Col(
                            [
                                dcc.RadioItems(
                                                id='feedback_radio_id',
                                                options = [
                                                    {'label':'{}'.format(i), 'value': f"{str(idx)}_{i}"} for i in drop_list
                                                ]
                                                ),
                                html.Div(id='radio_button_id_out')
                            ],
    )

