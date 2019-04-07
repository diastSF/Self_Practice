import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from plotly import tools
import plotly.graph_objs as go
import pandas as pd
import requests

app = dash.Dash(__name__)

api = requests.get('http://api-pokemon-baron.herokuapp.com/pokemon')

dfPokemon = pd.DataFrame(api.json(), columns = api.json()[0].keys())

app.title = 'Dashboard Pokemon'

app.layout = html.Div([
    html.H1('Dashboard Pokemon'),
    html.H3('Created by : Diast S. Fiddin'),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Tabs(id='Tabs', value='tab-1', children=[
        dcc.Tab(label='Data Pokemon', value='tab-1', children=[
            html.Div([
                html.Div([
                    html.P('Name : '),
                    dcc.Input(
                        id='filtername',
                        type='text',
                        value='',
                        style=dict(width='100%')
                    )
                ], className = 'col-4'),
                html.Div([
                    html.P('Generation : '),
                    dcc.Dropdown(
                        id='filtergeneration',
                        options=[i for i in [{'label':'All Generation', 'value':''},
                                            {'label':'1st Generation', 'value':'1'},
                                            {'label':'2nd Generation', 'value':'2'},
                                            {'label':'3rd Generation', 'value':'3'},
                                            {'label':'4th Generation', 'value':'4'},
                                            {'label':'5th Generation', 'value':'5'},
                                            {'label':'6th Generation', 'value':'6'},]],
                        value=''
                    )
                ], className = 'col-4'),
                html.Div([
                    html.P('Category : '),
                    dcc.Dropdown(
                        id='filterlegendary',
                        options=[i for i in [{'label':'All Pokemon', 'value':''},
                                            {'label':'Legendary', 'value':'True'},
                                            {'label':'Non-Legendary', 'value':'False'}]],
                        value=''
                    )
                ], className = 'col-4'),
            ], className='row'),
            html.Br(),
            html.Div([
                html.Div([
                    html.P('Total Stats : '),
                    dcc.RangeSlider(
                        id='filtertotal',
                        min=dfPokemon['Total'].min(),
                        max=dfPokemon['Total'].max(),
                        step=10,
                        value=[dfPokemon['Total'].min(),dfPokemon['Total'].max()],
                        marks={i : '{}'.format(i) for i in range(dfPokemon['Total'].min(),dfPokemon['Total'].max()+1,100)},
                        className='rangeslider'
                    )
                ], className = 'col-9'),
                html.Div([
                ], className = 'col-1'),
                html.Div([
                    html.Br(),
                    html.Button(
                        'Search',
                        id = 'buttonsearch',
                        style=dict(width='100%')
                    )
                ], className = 'col-2')
            ], className='row'),
            html.Br(),
            html.Br(),
            html.Div([
                html.Div([
                    html.P('Max Rows : '),
                    dcc.Input(
                        id='filterrow',
                        type='number',
                        value='50',
                        style=dict(width='50%')
                    )
                ], className = 'col-3')
            ], className = 'row'),
            html.Div([
                html.Center([
                    html.H2('Data Pokemon', className='title'),
                    html.Div(
                        id='tablepokemon',
                    )
                ])
            ])
        ]),
        dcc.Tab(label='Categorical Plot', value='tab-2', children=[
            html.Div([
                html.Div([
                    html.P('Jenis Plot :'),
                    dcc.Dropdown(
                        id='jeniscatplot',
                        options=[{'label':i,'value':i} for i in ['Bar','Box','Violin']],
                        value='Bar'
                    )
                ], className = 'col-3'),
                html.Div([
                    html.P('X :'),
                    dcc.Dropdown(
                        id='xcatplot',
                        options=[{'label':i,'value':i} for i in ['Generation','Type 1','Type 2']],
                        value='Generation'
                    )
                ], className = 'col-3'),
                html.Div([
                    html.P('Y :'),
                    dcc.Dropdown(
                        id='ycatplot',
                        options=[{'label':i,'value':i} for i in dfPokemon.columns[4:11]],
                        value='Total'
                    )
                ], className = 'col-3'),
                html.Div([
                    html.P('Stats :'),
                    dcc.Dropdown(
                        id='statscatplot',
                        options=[i for i in [{'label':'Mean','value':'mean'},
                                            {'label':'Standart Deviation','value':'std'},
                                            {'label':'Count','value':'count'},
                                            {'label':'Min','value':'min'},
                                            {'label':'Max','value':'max'},
                                            {'label':'25th Precentiles','value':'25%'},
                                            {'label':'Median','value':'50%'},
                                            {'label':'75th Precentiles','value':'75%'}]],
                        value='mean'
                    )
                ], className = 'col-3'),
            ], className = 'row'),
            html.Br(),
            html.Br(),
            html.Br(),
            dcc.Graph(
                        id = 'catplotgraph',
                    )
        ]),
        dcc.Tab(label='Scatter Plot', value='tab-3'),
        dcc.Tab(label='Pie Chart', value='tab-4'),
        dcc.Tab(label='Histogram', value='tab-5'),
    ], style={
        'fontFamily':'system-ui'
    }, content_style={
        'fontFamily':'Helvetica',
        'borderBottom':'1px solid #d6d6d6',
        'borderLeft':'1px solid #d6d6d6',
        'borderRight':'1px solid #d6d6d6',
        'padding':'44px'
    }),
], style={
    'maxWidth':'1200px',
    'margin':'0 auto'
})

#_____________________________CALLBACK TABLE POKEMON___________________________

@app.callback(Output('tablepokemon','children'),
                [Input('buttonsearch','n_clicks'),
                Input('filterrow','value')],
                [State('filtername','value'),
                State('filtergeneration','value'),
                State('filterlegendary','value'),
                State('filtertotal','value')])

def update_table(button,row,name,gen,leg,tot):
    dfNew = dfPokemon[(dfPokemon['Name'].str.contains(name,case=False))
                    & ((dfPokemon['Total'] >= tot[0]) & (dfPokemon['Total'] <= tot[1]))]
    if  gen != '' :
        dfNew = dfNew[dfNew['Generation'] == int(gen)]
    if leg != '' :
        dfNew = dfNew[dfNew['Legendary'] == leg]
    return html.Table(
        [html.Tr([
            html.Th(col) for col in dfNew.columns])] +
        [html.Tr([
            html.Td(str(dfNew[col].iloc[num])) for col in dfNew.columns
        ]) for num in range(min(int(row),len(dfNew)))]
    )

#_____________________________CALLBACK CATEGORICAL PLOT______________________________

funcDict = {'Bar':go.Bar,
            'Box':go.Box,
            'Violin':go.Violin}

def generateValue(legend,x,y,stats='mean'):
    return {
        'x' : {
            'Bar' : dfPokemon[dfPokemon['Legendary'] == legend][x].unique(),
            'Box' : dfPokemon[dfPokemon['Legendary'] == legend][x],
            'Violin' : dfPokemon[dfPokemon['Legendary'] == legend][x]
        },
        'y' : {
            'Bar' : dfPokemon[dfPokemon['Legendary'] == legend].groupby(x)[y].describe()[stats],
            'Box' : dfPokemon[dfPokemon['Legendary'] == legend][y],
            'Violin' : dfPokemon[dfPokemon['Legendary'] == legend][y]
        }
    }

@app.callback(Output('catplotgraph','figure'),
                [Input('jeniscatplot','value'),
                Input('xcatplot','value'),
                Input('ycatplot','value'),
                Input('statscatplot','value'),]
)

def update_catplot(jenis,x,y,stat):
    return dict(
        layout = go.Layout(
            title = '{} Plot Pokemon'.format(jenis),
            xaxis = dict(title = x),
            yaxis = dict(title = y),
            boxmode = 'group',
            violinmode = 'group'
        ),
        data = [
            funcDict[jenis](
                x = generateValue('True',x,y)['x'][jenis],
                y = generateValue('True',x,y,stat)['y'][jenis],
                name = 'Legendary'
            ),
            funcDict[jenis](
                x = generateValue('False',x,y)['x'][jenis],
                y = generateValue('False',x,y,stat)['y'][jenis],
                name = 'Non-Legendary'
            )
        ]
    )

@app.callback(Output('statscatplot','disabled'),
                [Input('jeniscatplot','value')]
)

def disabled_stats(jenis):
    if jenis != 'Bar':
        return True
    return False

if __name__ == '__main__':
    app.run_server(debug=True)