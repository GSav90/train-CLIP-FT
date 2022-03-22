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

from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from maindash import app
    
# external_stylesheets =[dbc.themes.LUX] # ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
# # app = dash.Dash(__name__)
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


    


########################################
############Summary metrics ############
########################################

# def get_summary_metrics(summary_df,drop_lst):
#     if summary_df.shape[0]==0:
#         summary_df=pd.DataFrame({"feedback": drop_list, "count":[0]*len(drop_lst)})
#     fig=px.bar(summary_df, x='feedback', y='count',orientation='h')
#     return fig



def display_summary(id,desc, color="primary"):
    return html.Div(
        [
            # dcc.Graph(figure=figr)
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            dbc.Col(
                                html.H5(
                                    [
                                        "",
                                        dbc.Badge(
                                            desc,
                                            color=color,
                                            # text_color="primary",
                                            className="border me-1",
                                        ),
                                    ],
                                ),
                                width={"offset": 4},
                            )
                        ),
                        dcc.Graph(id=id),
                    ]
                )
            ),
        ]
    )
summary_content = dbc.Container(
    [
        html.H1(children="Summary Metrics"),
        html.Br(),
        ##html.Div([dcc.Graph(figure=get_summary_metrics())]),
        dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div([dcc.Graph(figure="summary_id_graph")]),
                            html.Button("Refresh", id="refresh_plot_id", n_clicks=0),
                            # dcc.Location(id="url_new", refresh=True),
                            
                            # display_summary(
                            #     "summary_id_graph",
                            #     "Stats",
                            #     "success",
                            # ),
                        ]
                    )
                ),
                width=12)
                # ,align="center"
    ]
)



@app.callback(
    Output("summary_id_graph", "children"),
    Input('refresh_plot_id', 'n_clicks'),
)
def summary_tab_cont(nclick):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if nclick:
        feedback_file=os.path.join("/Users/g0s00lq/Documents/Github_new/NextGen/train-CLIP-FT/app","Feedback.csv")
        if not os.path.exists(feedback_file):
            return {}
        df = pd.read_csv(feedback_file)
        grouped=df.groupby(["feedback"])["row_id"].count().reset_index()
        fig = px.bar(grouped, x="feedback", y="row_id",color='feedback')#,color_discrete_sequence =['green']*len(grouped))
        # fig.update_traces(marker_color='green')
        fig.update_layout(
            title="Feedback Statistics",
            barmode="group",
            paper_bgcolor="rgb(255, 255, 255)",
            plot_bgcolor="rgb(255, 255, 255)",
        )
        return fig
    
    return "Click on refresh"

# if __name__ == "__main__":
#     feedback_file=os.path.join("/Users/g0s00lq/Documents/Github_new/NextGen/train-CLIP-FT/app","Feedback.csv")
#     df = pd.read_csv(feedback_file)
#     grouped=df.groupby(["feedback"])["row_id"].count().reset_index()
#     fig = px.bar(grouped, x="feedback", y="row_id",color='feedback')#,color_discrete_sequence =['green']*len(grouped))
#     # fig.update_traces(marker_color='green')
#     fig.update_layout(
#         title="Feedback Statistics",
#         barmode="group",
#         paper_bgcolor="rgb(255, 255, 255)",
#         plot_bgcolor="rgb(255, 255, 255)",
#     )
#     fig.show()

# if __name__ == "__main__":
#     # app.run_server(debug=True)
#     app.server.run(port=8000, host="127.0.0.1", debug=True)