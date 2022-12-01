import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash
from dash import Dash,html,dcc
from dash.dependencies import Input,Output

# external CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

patients = pd.read_csv("IndividualDetails.csv")
total = patients.shape[0]
active=patients[patients['current_status']=='Hospitalized'].shape[0]
Recovered=patients[patients['current_status']=='Recovered'].shape[0]
deaths=patients[patients['current_status']=='Deceased'].shape[0]

cases = pd.read_csv('covid_19_india.csv')
cases['total']=cases['ConfirmedIndianNational']+cases['ConfirmedForeignNational']
cases['total'] = np.cumsum(cases['total'].values)

ages = pd.read_csv('AgeGroupDetails.csv')
options = [
    {'label':'All','value':'All'},
    {'label':'Hospitalized','value':'Hospitalized'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deceased','value':'Deceased'}
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Corona Virus Pandemic-India's Perspective"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total cases",className='text-light'),
                    html.H4(total,className='text-light')
                ],className='card-body')
            ],className='card bg-danger')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active cases",className='text-light'),
                    html.H4(active,className='text-light')
                ],className='card-body')
            ],className='card bg-warning')
        ],className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered cases",className='text-light'),
                    html.H4(Recovered,className='text-light')
                ],className='card-body')
            ],className='card bg-success')
        ],className='col-md-3'),
        html.Div([html.Div([
                html.Div([
                    html.H3("death cases",className='text-light'),
                    html.H4(deaths,className='text-light')
                ],className='card-body')
            ],className='card bg-info')
        ],className='col-md-3')
    ],className='row'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='line',figure={'data':[go.Scatter(x=cases['Date'],y=cases['total'])],
                                                'layout':go.Layout(title="Day-to-Day Analysis")})
                ],className='card-body')
            ],className='card')
        ],className='col-md-6'),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='pie',figure={'data':[go.Pie(labels=ages['AgeGroup'],values=ages['TotalCases'])],
                                                'layout' : go.Layout(title="Age Distribution") })
                ],className='card-body')
            ],className='card')
        ],className='col-md-6'),
    ],className='row'),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options=options,value='All'),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='card bg-secondary')
        ],className='col-md-12')
    ],className='row')
], className = "container")

@app.callback(Output('bar','figure'),[Input('picker','value')])
def update_graph(type):
    if type=='All':
        pbar = patients['detected_state'].value_counts().reset_index()
        return {'data':[go.Bar(x=pbar['index'],y=pbar['detected_state'])],
                'layout': go.Layout(title="State total count")}
    else:
        npat = patients[patients['current_status']==type]
        pbar = npat['detected_state'].value_counts().reset_index()
        return {'data':[go.Bar(x=pbar['index'],y=pbar['detected_state'])],
                'layout': go.Layout(title="State total count")}


if __name__ == "__main__":
    app.run_server(debug=True,port=5000)