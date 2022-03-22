import dash
from dash import html
import base64
import os
from pprintpp import pprint
#from inference_clip import clip_inference
import pandas as pd
import random
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dataclasses import dataclass
from dash.dependencies import Input, Output, State

@dataclass
class getAppDataThreshold:
    batch_size= 10
    prediction_images=5
    rootdir="/Users/g0s00lq/Documents/Github_new/NextGen/dvc-manual/data/80gtin_allsubfolders"

class getAppData:

    def __init__(self,dropdown_labels=None):
        if not dropdown_labels:
            self.dropdown_labels=["GTIN Incorrectly labeled", "Cleanup Enrollment Images","Model Error","Multiple Items","Other",None]
        else:
            self.dropdown_labels= dropdown_labels
        

    def get_table_data(self,filepath,start_pos,end_pos,pred_img_count=getAppDataThreshold.prediction_images):
        df=pd.read_csv(filepath)
        true_gtin_name, predicted_gtin_name, true_img_thumbnail, prediction_thumnails= "","",None,None

        df_out=pd.DataFrame()
        #batch_size=batch_size
        for idx,prow in df.iloc[start_pos:end_pos+1].iterrows():
            true_gtin_name, predicted_gtin_name, true_img_thumbnail, prediction_thumnails= self.get_misclassifications(prow,pred_img_count)
            feedback=self.add_dropdown_dcc("id_"+str(idx))
            row= {"true_img_thumbnail": true_img_thumbnail,\
                "true_gtin_name": true_gtin_name, 
                "predicted_gtin_name": predicted_gtin_name,\
                    "pred_sample_1": prediction_thumnails[0],
                    "pred_sample_2": prediction_thumnails[1],
                    "pred_sample_3": prediction_thumnails[2],
                    "pred_sample_4": prediction_thumnails[3],
                    "pred_sample_5": prediction_thumnails[4],
                    "Refresh": html.A(html.Button('Refresh'),href='/'),
                    "Feedback": feedback,
                    }
            
            df_out=df_out.append(row,ignore_index=True)
            
        return df_out

    def add_dropdown_dcc(self,idx,drop_lst=None):
        if not drop_lst:
            drop_lst=self.dropdown_labels

        # new_elem=dcc.Dropdown(
        #                         id={
        #                             'type': 'dynamic-dropdown',
        #                             'index': idx
        #                         },
        #                         options=drop_lst,
        #                         value="Other",
        #                         #clearable=False,
        #                     ),
        new_elem= html.Div([
                            dcc.Dropdown(
                                id={
                                    'type': 'dynamic-dropdown',
                                    'index': idx
                                },
                                options=drop_lst,
                                value=None,
                                clearable=False,
                            ),
                            html.Div(
                                id={
                                    'type': 'dynamic-output',
                                    'index': idx
                                }
                            )
                        ])
        
        return new_elem
        
      
    def add_dropdown(self,idx):
        return dbc.DropdownMenu(label=str(idx),id=f"id_{str(idx)}",children=[
                    dbc.DropdownMenuItem("GTIN Incorrectly labeled"),
                    dbc.DropdownMenuItem("Cleanup Enrollment Images"),
                    dbc.DropdownMenuItem("Model Error"),
                    dbc.DropdownMenuItem("Multiple Items in Test Image with true class"),
                    dbc.DropdownMenuItem("Other"),
                ],color="success", className="m-1"
                )
    def add_radioitems(self,idx,drop_lst=None):
        if not drop_lst:
            drop_lst=self.dropdown_labels
        radio_id=f'fid_{str(idx)}'
        return dbc.Col(
                            [
                                dcc.RadioItems(
                                                id=radio_id,
                                                options = [
                                                    {'label':'{}'.format(i), 'value':'{}'.format(i) } for i in drop_lst
                                                ]
                                                ),
                                html.Div(id='radio_button_id_out')
                            ],radio_id
        )
    def get_misclassifications(self,row,pred_img_count):
    
        true_gtin_name=row["name"]
        predicted_gtin_name=row["name_predictions"]

        true_img_path=row["img_path"]
        
        true_img_path=true_img_path.split("80gtin_allsubfolders/")[1]
        
        true_img_path=os.path.join(getAppDataThreshold.rootdir,true_img_path)
        encoded_image = base64.b64encode(open(true_img_path, "rb").read())
        true_img_thumbnail=self.generate_thumbnail(encoded_image)
        
        predicted_img_folder_path=row["predicted_gtin_enroll_folder"].split("80gtin_allsubfolders/")[1]
        predicted_img_folder_path=os.path.join(getAppDataThreshold.rootdir,predicted_img_folder_path)
        prediction_thumnails=self.get_n_thumbnail_from_folder(predicted_img_folder_path,pred_img_count)
            
        return true_gtin_name, predicted_gtin_name, true_img_thumbnail, prediction_thumnails

    def generate_thumbnail(self,encoded_image):
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
    def get_n_thumbnail_from_folder(self,folder_path,n):
        images = []
        for path in os.listdir(folder_path):
            full_path = os.path.join(folder_path, path)
            if os.path.isfile(full_path):
                images.append(full_path)
        images_div = []
        samples=random.sample(images, n)
        for i in samples:
            encoded_image = base64.b64encode(open(i, "rb").read())
            images_div.append(self.generate_thumbnail(encoded_image))
        return images_div

    