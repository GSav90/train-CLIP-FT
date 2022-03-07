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
# from dash_colorgrading import discrete_background_color_bins

external_stylesheets =[dbc.themes.BOOTSTRAP] # ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# (color_grading_styles, legend) = discrete_background_color_bins(df, columns=cols)
# image_filename = "/Users/g0s00lq/Documents/Github_new/self_experiments/code_samples/catalog_data/00011115871324/0a439101-7fc7-4e38-a983-2656e92cafa8_1.f69ff07a5afdb36c60b81a40a3e98442.jpeg"  # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, "rb").read())

# app.layout = html.Div([html.Img(src=f"data:image/png;base64,{encoded_image.decode()}")])


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
        
    
filepath="/home/jupyter/train-CLIP-FT/app/misclassifications_ET90_SN1.csv"
df=pd.read_csv(filepath)
true_gtin_name, predicted_gtin_name, true_img_thumbnail, prediction_thumnails= "","",None,None

df_out=pd.DataFrame()
n_rows=20
for idx,row in df.iloc[0:n_rows].iterrows():
    true_gtin_name, predicted_gtin_name, true_img_thumbnail, prediction_thumnails= get_misclassifications(df)
    row= {"true_img_thumbnail": true_img_thumbnail,\
          "true_gtin_name": true_gtin_name, 
          "predicted_gtin_name": predicted_gtin_name,\
             "pred_sample_1": prediction_thumnails[0],
             "pred_sample_2": prediction_thumnails[1],
             "pred_sample_3": prediction_thumnails[2],
             "pred_sample_4": prediction_thumnails[3],
             "pred_sample_5": prediction_thumnails[4],
            }
    df_out=df_out.append(row,ignore_index=True)
    
print(df_out.shape)

app.layout = html.Div(
    [
        html.H1(children="Analyze Misclassifications"),
        html.Br(),
        html.A(html.Button('Refresh Data'),href='/'),
        dbc.Table.from_dataframe(df_out, striped=True, bordered=True, hover=True, responsive="sm",size="lg",style = {'margin-right':'10px','margin-left':'10px'})
        # dcc.Dropdown(
        #     id="date",
        #     options=[
        #         {"label": str(key), "value": str(val)}
        #         for key, val in df["date"].unique().tolist()
        #     ],
        #     multi=False,
        #     placeholder="Filter by Market Cap",
        # ),
        # html.Button(id="submit-button-state", n_clicks=0, children="Submit"),
        # dash_table.DataTable(
        #     id="live-update-table",
        #     columns=[
        #         {"name": i, "id": i, "deletable": True, "selectable": True}
        #         for i in df_out.columns
        #     ],
        #     data=df_out.to_dict("records"),
        #     editable=True,
        #     filter_action="native",
        #     sort_action="native",
        #     sort_mode="multi",
        #     column_selectable="single",
            # style_cell=dict(textAlign="left"),
            # style_header=dict(backgroundColor="paleturquoise"),
            # style_data=dict(backgroundColor="lavender"),
            # style_data_conditional=color_grading_styles,
        # ),
        # html.Div(id="datatable-interactivity-container"),
        # dcc.Interval(
        #     id="interval-component", interval=1 * 1000, n_intervals=0  # in milliseconds
        # ),
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
    