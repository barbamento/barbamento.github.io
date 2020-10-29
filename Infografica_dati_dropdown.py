import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from flask_frozen import Freezer

import pandas as pd
import csv
import os
from collections import defaultdict
import requests

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
#########################################################################################################################
#########################################################################################################################
############         ########     #####          #####     ##############################################################
############    ###    ####    #     #####    ######    #    ############################################################
############    ###    ###    ###    #####    ######   ###   ############################################################
############    ###    ###    ###    #####    ######   ###   ############################################################
############    ###    ###           #####    ######         ############################################################
############    ###    ###    ###    #####    ######   ###   ############################################################
############         #####    ###    #####    ######   ###   ############################################################
#########################################################################################################################
#########################################################################################################################

columns = defaultdict(list)
os_link="https://github.com/pcm-dpc/COVID-19/raw/master/"

def date_extraction(os_link):
    path=os_link+"/dati-regioni/dpc-covid19-ita-regioni-latest.csv"
    dict1=requests.get(path).text.strip().split("\n")
    dict2=csv.DictReader(dict1)
    for row in dict2: 
        data=(int((row["data"])[5:7]),int((row["data"])[8:10]))
    return data

def estrazione_dati_nazionali(os_link,label):
    result=[]
    path=os_link+"/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv"
    if label=="data":
        dati=dict1=requests.get(path).text.strip().split("\n")
        dati=csv.DictReader(dati)
        for row in dati:
            result.append(row["data"][0:10])
        return(result)
    else:
        dati=dict1=requests.get(path).text.strip().split("\n")
        dati=csv.DictReader(dati)
        for row in dati:
            result.append(int(row[label]))
        return(result)

columns["terapia_intensiva"]=estrazione_dati_nazionali(os_link,"terapia_intensiva")
columns["nuovi_positivi"]=estrazione_dati_nazionali(os_link,"nuovi_positivi")


app.layout = html.Div([
    dcc.Dropdown(
        id='graph_label',
        options=[
            {'label': "terapie", 'value': "terapia_intensiva"},
            {'label': "casi giornalieri", 'value': "nuovi_positivi"} 
        ],
        value='terapia_intensiva'
    ),
    dcc.Graph(id='graphic')
])

@app.callback(
    Output('graphic', 'figure'),
    [Input('graph_label', 'value')])

def update_graph(graph_label):
    fig1 = px.bar(columns[graph_label])
    return fig1
    
#freezer=Freezer(app)

if __name__ == '__main__':
    #freezer.freeze()
    app.run_server(debug=True)
