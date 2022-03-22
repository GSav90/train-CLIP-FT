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


# misclassification_content = html.Div([
#     html.Button("Add Filter", id="dynamic-add-filter", n_clicks=0),
#     html.Div(id='dynamic-dropdown-container', children=[]),
#     dbc.Table.from_dataframe(df_out, striped=True, bordered=True, hover=True, responsive="lg",size="lg",style = {'margin-right':'2px','margin-left':'2px'}),
# ])

misclassification_content = html.Div([
    html.Br(),
    html.Div(id='dropdown-container-output'),
    html.Br(),
    dbc.Button("Add batch",
                id="add_batch_id",
                color="success",
                className="me-1"),
    dbc.Button("Submit",
                id="submit_button_id",
                color="success",
                className="me-1"),
    html.Div(id='dropdown-container', children=[]),
    html.Div(id='dbc-table-output'),
])
start=0
# misclassification_content = html.Div(
#     [
#         html.Div(id="dynamic-output"),
#         dbc.Table.from_dataframe(df_out, striped=True, bordered=True, hover=True, responsive="lg",size="lg",style = {'margin-right':'2px','margin-left':'2px'}),
#         html.Div(id='dropdown-container', children=[]),
#         # dcc.Store(id='intermediate-value'),
        
#     ]
# )
# @app.callback(
#     Output('dropdown-container', 'children'),
#     Input('add-filter', 'n_clicks'),
#     State('dropdown-container', 'children'))
# def display_dropdowns(n_clicks, children):
#     elem=gap.add_dropdown_dcc(n_clicks)
#     children.append(elem)
#     return children


@app.callback(
    Output('dropdown-container', 'children'),
    Input('submit_button_id', 'n_clicks'),
    Input('add_batch_id', 'n_clicks'),
    State('dropdown-container', 'children'))
def display_dropdowns(submit_click,add_batch, children):
    if add_batch:
        st=(add_batch*10)-10
    else:
        st=start
    end=st+10
    df_out=gap.get_table_data(filepath,st,end)
    new_children= df_out["Feedback"].tolist()
    children.append(new_children)
    return children

@app.callback(
    Output('dbc-table-output', 'children'),
    Input('add_batch_id', 'n_clicks'),
    State('dropdown-container', 'children'))
def display_dropdowns(add_batch, children):
    if add_batch:
        st=(add_batch*10)-10
    else:
        st=start
    end=st+10
    df_out=gap.get_table_data(filepath,st,end)
    new_children= df_out["Feedback"].tolist()
    children.append(new_children)
    # new_child=dcc.Dropdown(
    #         id={
    #             'type': 'feedback-dropdown',
    #             'index': idx
    #         },
    #         options=drop_lst,
    #         value="Other",
    #         clearable=False,
    #     )
    return dbc.Table.from_dataframe(df_out, striped=True, bordered=True, hover=True, responsive="lg",size="lg",style = {'margin-right':'2px','margin-left':'2px'})


@app.callback(
    Output('dropdown-container-output', 'children'),
    Input({'type': 'filter-dropdown', 'index': ALL}, 'value'),
)
def display_output(values):
    for (i, value) in enumerate(values):
        with open(feedback_file,"a") as f:
            f.write(f"{i},{value}")
    #return f"Printing text {values}"
    return html.Div([
        html.Div('Dropdown {} = {}'.format(i + 1, value))
        for (i, value) in enumerate(values)
    ])


# @app.callback(
#     Output({'type': 'dynamic-output', 'index': ALL}, 'children'),
#     Input({'type': 'feedback-dropdown', 'index': ALL}, 'value'),
#     State({'type': 'feedback-dropdown', 'index': MATCH}, 'id'),
#     # State({'type': 'dynamic-dropdown', 'index': ALL}, 'id'),
# )
# def which_feedback_clicked(values):
#     # return html.Div([
#     #     html.Div('Dropdown {} = {}'.format(i + 1, value))
#     #     for (i, value) in enumerate(values)
#     # ])
#     ctx = dash.callback_context

#     if not ctx.triggered:
#         button_id = "No clicks yet"
#     else:
#         button_id = ctx.triggered[0]["prop_id"].split(".")[0]

#     ctx_msg = json.dumps(
#         {"states": ctx.states, "triggered": ctx.triggered, "inputs": ctx.inputs},
#         indent=4,
#     )
#     return ctx_msg
    # return html.Div('Dropdown {} = {} and dash context is ={}'.format(id['index'], value, ctx_msg))
    # if button_id == "plot_submit_button_id":
    #     return [ctx_msg, f"Symbol : {symbol_drop} , Strategy: {strat_drop}"]
    # else:
    #     return "waiting for submit button to be clicked"









# def add_radioitems(self,idx,drop_lst=None):
#         return dbc.Col(
#                             [
#                                 dcc.RadioItems(
#                                                 id=radio_id,
#                                                 options = [
#                                                     {'label':'{}'.format(i), 'value':'{}'.format(i) } for i in drop_lst
#                                                 ]
#                                                 ),
#                                 html.Div(id='radio_button_id_out')
#                             ])

# @app.callback(Output('intermediate-value', 'data'), Input('dropdown', 'value'))
# def intermediate_data(value):
#     df_out=gap.get_table_data(filepath,10)
#     return json.dumps(df_out)
    
    
    
    
# @app.callback(Output("radio_button_id_out","children"),[Input('intermediate-value', 'data'),])
# def listen_radio_buttons(dataset):
#     """
#     This callback takes in page2-buttons selected value and returns content to display
#     in selected-button
#     """
    
#     row_id, feedback= dataset["fid"].split('_')

#     row=df_out.iloc[row_id]
#     row["feedback"]=feedback
#     row.to_csv(feedback_file, mode="a", index=False, header=os.path.exists(feedback_file))
#     return 




### 