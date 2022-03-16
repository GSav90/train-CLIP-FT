import dash
import dash_bootstrap_components as dbc



# from dash_colorgrading import discrete_background_color_bins

external_stylesheets =[dbc.themes.BOOTSTRAP] # ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(external_stylesheets=[dbc.themes.PULSE])
# (color_grading_styles, legend) = discrete_background_color_bins(df, columns=cols)
# image_filename = "/Users/g0s00lq/Documents/Github_new/self_experiments/code_samples/catalog_data/00011115871324/0a439101-7fc7-4e38-a983-2656e92cafa8_1.f69ff07a5afdb36c60b81a40a3e98442.jpeg"  # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, "rb").read())

# app.layout = html.Div([html.Img(src=f"data:image/png;base64,{encoded_image.decode()}")])