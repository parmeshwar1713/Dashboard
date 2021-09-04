# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 09:31:06 2021

@author: keerthi
"""
from os import name
import dash_table 
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
import dash
import pandas as pd
import numpy as np
from millify import millify
import dash
import dash_html_components as html
from plotly.offline import plot
from plotly.graph_objs import Scatter
from plotly.subplots import make_subplots
import imageio

# from dash_slicer import VolumeSlicer

from django_plotly_dash import DjangoDash
config = {'modeBarButtonsToRemove': ['toggleSpikelines','hoverCompareCartesian','zoom2d','zoomIn2d',
                                     'zoomOut2d','resetScale2d','autoScale2d','select2d','pan2d','lasso2d'],
          'displaylogo': False
}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# d = pd.read('qfq.xlsx')
# df = pd.read_excel("C:/Users/Administrator/Downloads/QAFAC Spend Analysis Rev1.xlsx",'Data')
# df['Quarters'] = df['Document Date'].dt.quarter
app = DjangoDash('SimpleExample1',suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP]) 

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 09:31:06 2021

@author: keerthi
"""
config = {'modeBarButtonsToRemove': ['toggleSpikelines','hoverCompareCartesian','zoom2d','zoomIn2d',
                                     'zoomOut2d','resetScale2d','autoScale2d','select2d','pan2d','lasso2d'],
          'displaylogo': False
}

# d = pd.ExcelFile('C:/Users/Administrator/Downloads/QAFAC Spend Analysis Rev1.xlsx')
df = pd.read_excel("/home/dev/PiLOg/MYDASH/mydash1/QAFAC Spend Analysis Rev1.xlsx",'Data')
# df=pd.read_csv("test12.csv")
df['Quarters'] = df['Document Date'].dt.quarter

# vendor_cont = {'Contract':list(df[df['Contract']=='Contract']['Vendor'].unique()),
#                'Non Contract':list(df[df['Contract']=='Non Contract']['Vendor'].unique())}

def spend_trends(df):
    dt_ = pd.pivot_table(df, values='Value in USD', index=['Year','Quarters'], aggfunc=np.sum)
    d_t = dt_.reset_index()
    # l1=["Q1-2015","Q2-2015","Q3-2015","Q4-2015","Q1-2016","Q2-2016","Q3-2016","Q4-2016","Q1-2017","Q2-2017","Q3-2017","Q4-2017","Q1-2018","Q2-2018","Q3-2018","Q4-2018","Q1-2019","Q2-2019","Q3-2019","Q4-2019","Q1-2020","Q2-2020","Q3-2020","Q4-2020","Q1-2021"]
    l1=[]
    l2=[]
    # my_array1 = np.asarray(l1)
    for i in range(len(d_t["Year"])):
        l1.append("Q"+str(d_t["Quarters"][i])+"-"+str(d_t["Year"][i]))
        l2.append(d_t['Value in USD'][i])
    print(l1)
    arr=np.array(l1)
    d1={"Year":l1}
    fd1=pd.DataFrame(d1)
    fig = go.Figure(data=[go.Scatter(x=fd1['Year'], y=l2,
                    mode='lines+markers',
                    name='Predicted Values',marker_color='#0B4a99')])
    # fig = go.Figure(data=[px.Scatter(y=l2,x=fd1["Year"], marker_color='#0B4a99')])
    return html.Div([
                dbc.Card(
            dbc.CardBody([
                dcc.Graph(config=config,
                          figure=fig.update_layout(barmode='group',
                         xaxis={'showgrid':True,'title':'Year'}, 
                         yaxis={'showgrid':True,'title':'Value in USD','color':'black'},
                         title = 'Spend Trends', 
                         paper_bgcolor= 'rgba(0, 0, 0, 0)',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        height = 300, hovermode = 'closest')
                    )
                ])
            )
        ])
                                       
def spend_contract(df):
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(config=config,
                          figure={'data':[{'names':df['Contract'].values,'values':df['Value in USD'],
                                           'labels':df['Contract'].values,'type':'pie','hole':.4}],
                        'layout':{"xaxis": {"title": 'Contract','showgrid':False,"color":"black"}, 
                  "yaxis": {"title": 'Value in USD','showgrid':False,"color":"black"},'plot_bgcolor':'rgba(0, 0, 0, 0)',
                  'paper_bgcolor':'rgba(0, 0, 0, 0)','template':'plotly_dark','font':{'color':'black'},
                  'title':'Spend by Contract','height':300, 'legend':{'yanchor':"bottom",
                                                                        'y':-0.5,
                                                                        'xanchor':"right",
                                                                        'x':1
                                                                      }
                  }})
                ])
            )
        ])

def spend_material(df):
    dm_ = pd.pivot_table(df, values='Value in USD', index=['Material Group'], aggfunc=np.sum)
    dm = dm_.sort_values('Value in USD',ascending=False).head(15).reset_index()
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(config=config,
                          figure={'data':[{'x':dm['Material Group'],
                                           'y':dm['Value in USD'], 'text': dm['Value in USD'],
                                           'type':'line','marker':{'color':'#40875e'},
                                          'texttemplate':'%{text:.2s}', 'textposition':'outside'}],
                                 'layout':{"xaxis": {'showgrid':False,"color":"black",'categoryorder':'total descending'}, 
                  "yaxis": {"title": 'Value in USD','showgrid':True,"color":"black"},'plot_bgcolor':'rgba(0, 0, 0, 0)',
                  'paper_bgcolor':'rgba(0, 0, 0, 0)','template':'plotly_dark','font':{'color':'black'},
                  'title':'Spend by Material Group','hovermode':'closest','height':405,
                  }})
               ])
            )
        ])
#88**************************************************************************************************************************
def spend_vendor(df):
    dv_ = pd.pivot_table(df, values='Value in USD', index=['Vendor'], aggfunc=np.sum)
    dv = dv_.sort_values('Value in USD',ascending=False).head(20).reset_index()  
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                 dcc.Graph(config=config,
                          figure={'data':[{'x':dv['Vendor'],'y':dv['Value in USD'], 'text': dv['Value in USD'],
                                           'type':'bar','marker':{'color':'#40875e'},
                                           'texttemplate':'%{text:.2s}', 'textposition':'outside'}],
                                 'layout':{"xaxis": {'showgrid':False,"color":"black",'categoryorder':'total descending'}, 
                  "yaxis": {"title": 'Value in USD','showgrid':True,"color":"black"},'plot_bgcolor':'rgba(0, 0, 0, 0)',
                  'paper_bgcolor':'rgba(0, 0, 0, 0)','template':'plotly_dark','font':{'color':'black'},
                  'title':'Spend by Vendor','hovermode':'closest','height':400}})
               ])
            )
        ])
#*****************************************************************************************************************************
# def spend_vendor(df):
#     dv_ = pd.pivot_table(df, values='Value in USD', index=['Vendor'], aggfunc=np.sum)
#     dv = dv_.sort_values('Value in USD',ascending=False).head(20).reset_index() 
#     fig = px.bar(dv, x=dv['Vendor'], y=dv['Value in USD'],
#              color='Value in USD') 
#     return html.Div([
#                 dbc.Card(
#             dbc.CardBody([
#                 dcc.Graph(config=config,
#                           figure=fig.update_layout(showlegend=False,
#                          xaxis= {'showgrid':False,'categoryorder':'total descending','tickmode':'array','tickangle':-45, 'tickvals':[],
#                                 'ticktext':[]}, 
#                          yaxis={'showgrid':True,'title':'Value in USD'},
#                          title = 'Spend by Vendor', 
#                          paper_bgcolor= 'rgba(0, 0, 0, 0)',
#                         plot_bgcolor= 'rgba(0, 0, 0, 0)',
#                         height = 405, hovermode = 'closest')
#                     )
#                 ])
#             )
#         ])       
################################################################################################################################
def spend_unspsc(df):
    du_ = pd.pivot_table(df, values='Value in USD', index=['UNSPSC Description'], aggfunc=np.sum)
    du = du_.sort_values('Value in USD',ascending=False).head(20).reset_index()
    du.loc[4,'UNSPSC Description']='Services'
    du.loc[0,'UNSPSC Description']='Miscellaneous'
    fig = px.treemap(du, path=["UNSPSC Description"], values="Value in USD",names=du['Value in USD'])
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(config=config,
                          figure=fig.update_layout(margin = dict(t=50, l=25, r=25, b=25),
                         title = 'Spend by UNSPSC', 
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        height = 852, hovermode = 'closest'))
               ])
            )
        ])


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "1rem 1rem",
    "background-color":"#002060",
    "height": "100%",
    #"overflowY": "scroll"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-top": 0,
    "margin-left": "18rem",
    "background-color": "#3D09DA",
    "height": "100%",
}

sidebar = html.Div(
    [
        dbc.Nav(
            [
              html.Br(),
              html.Br(),
              html.H4('Contract',style={'color':'white'}),
              dcc.Dropdown(id='contract',
                           options=[
                               {'label':i, 'value':i} for i in ['Non Contract','Contract']
                               ],
                           value='Non Contract',
                           clearable=False),
              html.Br(),
              html.H4('Year',style={'color':'white'}),
              dcc.Dropdown(id='year',
                            options=[
                                {'label':i, 'value':i} for i in [2015,2016,2017,2018,2019,2020,2021]],
                            value=[2015,2016,2017,2018,2019,2020,2021],
                            multi=True,
                            clearable=False
                            ),
              html.Br(),
            #   html.H4('Vendor',style={'color':'white'}),
            #   dcc.Dropdown(id='vendor', 
            #                 options=[
            #                    {'label':i, 'value':i} for i in df['Vendor']
            #                    ],
            #                 optionHeight=55, clearable=False
            #                )
                ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

#OPTIONS = [{'label':i.title(), 'value':i.title()} for i in df['Vendor'].unique()]

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# @app.callback(
#     Output('vendor', 'options'),
#     Input('contract','value'))
# def set_vendor_options(selected_contract):
#     return [{'label':i.title(), 'value':i} for i in vendor_cont[selected_contract]]

# @app.callback(
#     Output('vendor','value'),
#     Input('vendor','options'))
# def set_vendor_values(available_options):
#     return available_options[0]['value']

@app.callback(
    Output('page-content', 'children'),
    [Input('year', 'value'),
     Input('contract', 'value'),
    ])
def graph_content(year,contract):
    if ((year==[]) or (contract is None)):
        return dbc.Card([
            dbc.CardBody([
                html.H3("Warning!!!", className="card-title"),
                html.P("Please select atleast one value to get the analysis.",className='card-text')
                ])
            ],color='warning',inverse=True,className='shadow p-3 mb-5 bg-danger rounded')    
    else:
        df1 = df[df['Year'].isin(year)]
        #df_c = df1[df1['Contract']==contract]
        # df_v = df1[df1['Vendor']==vendor]
        df_c = df1[df1['Contract'] == contract]
        #print(df_c)
        if df_c.empty:
            return dbc.Card([
                dbc.CardBody([
                    html.H3("Warning!!!", className="card-title"),
                    html.P("There is no spent to the particular Vendor in the selected Year. " 
                           "Please select other Year to get the analysis.",className='card-text')
                    ])
                ],color='danger',inverse=True,className='shadow p-3 mb-5 bg-danger rounded')
        else:
            #df1 = df[df['Year']==year] 
            #d = pd.pivot_table(df1, values='Value in USD', index=['Year','Quarters'], aggfunc=np.sum)
            po_count = df_c['PO'].nunique()
            po_line_count = df_c['PO Item'].nunique()
            vendor_count = df_c['Vendor'].nunique()
            spent_sum = df_c['Value in USD'].sum() 
            
            return html.Div([            
                dbc.Card(
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col(html.H3("Spend Overview", style={'color':'white'}),width=3, align='center'),
                            dbc.Col(dbc.Card(html.P([html.H6("Total Spend:"),
                                                                           "$ {} USD".format(millify(spent_sum, precision=2))]),
                                             ),width=2,className="text-center"),
                            dbc.Col(dbc.Card(html.P([html.H6("Vendor:"), "{:,}".format(vendor_count)]),
                                             ),width=2,className="text-center"),
                            dbc.Col(dbc.Card(html.P([html.H6("PO Count:"), "{:,}".format(po_count)]),
                                             ),width=2,className="text-center"),
                            dbc.Col(dbc.Card(html.P([html.H6("PO Line Count:"), "{:,}".format(po_line_count)]),
                                             ),width=2,className="text-center")
                            ]),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([
                                spend_trends(df_c)
                                ], width=8),
                            dbc.Col([
                                spend_contract(df1)
                                ], width=4),
                            ], align='center',no_gutters=True),
                        #html.Br(),
                        dbc.Row([
                            dbc.Col([
                                spend_unspsc(df_c) 
                            ], width={"size": 4, "order": 1}),  
                            dbc.Col([
                                spend_material(df_c),
                                #html.Br(),
                                spend_vendor(df_c)
                            ], width={"size": 8, "order": "last"}),   
                            ],align='center',no_gutters=True),
                        ]),color="#002060"
                    )
                ])
            
if __name__ == "__main__":
    app.run_server(debug=True, port=8081)
