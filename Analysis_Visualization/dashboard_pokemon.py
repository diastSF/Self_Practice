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
        dcc.Tab(label='Scatter Plot', value='tab-3', children = [
            html.Div([
                html.Div([
                    html.P('Hue :'),
                    dcc.Dropdown(
                        id='huescatplot',
                        options=[{'label':i,'value':i} for i in ['Legendary','Generation','Type 1','Type 2']],
                        value='Legendary'
                    )
                ], className = 'col-4'),
                html.Div([
                    html.P('X :'),
                    dcc.Dropdown(
                        id='xscatplot',
                        options=[{'label':i,'value':i} for i in dfPokemon.columns[4:11]],
                        value='Total'
                    )
                ], className = 'col-4'),
                html.Div([
                    html.P('Y :'),
                    dcc.Dropdown(
                        id='yscatplot',
                        options=[{'label':i,'value':i} for i in dfPokemon.columns[4:11]],
                        value='Attack'
                    )
                ], className = 'col-4'),
            ], className = 'row'),
            html.Br(),
            html.Br(),
            html.Br(),
            dcc.Graph(
                id = 'scatplotgraph',
            )
        ]),
        dcc.Tab(label='Pie Chart', value='tab-4', children = [
            html.Div([
                html.Div([
                    html.P('Group :'),
                    dcc.Dropdown(
                        id='grouppieplot',
                        options=[{'label':i,'value':i} for i in ['Legendary','Generation','Type 1','Type 2']],
                        value='Legendary'
                    )
                ], className = 'col-4')
            ], className = 'row'),
            html.Br(),
            html.Br(),
            html.Br(),
            dcc.Graph(
                id = 'pieplotgraph',
            )
        ]),
        dcc.Tab(label='Histogram', value='tab-5', children = [
            html.Div([
                html.Div([
                    html.P('X :'),
                    dcc.Dropdown(
                        id='xhistplot',
                        options=[{'label':i,'value':i} for i in dfPokemon.columns[4:11]],
                        value='Total'
                    )
                ], className = 'col-4'),
                html.Div([
                    html.P('Hue :'),
                    dcc.Dropdown(
                        id='huehistplot',
                        options=[{'label':i,'value':i} for i in ['All','Legendary','Generation']],
                        value='All'
                    )
                ], className = 'col-4'),
                html.Div([
                    html.P('Std :'),
                    dcc.Dropdown(
                        id='stdhistplot',
                        options=[{'label':'{} Standart Deviation'.format(i),'value':i} for i in ['1','2','3']],
                        value='2'
                    )
                ], className = 'col-4')
            ], className = 'row'),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            dcc.Graph(
                id = 'histplotgraph',
            )
        ]),
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

#_____________________________CALLBACK SCATTER PLOT______________________________

legendDict = {
    'Legendary' : {'True' : 'Legendary',
                    'False' : 'Non-Legendary'},
    'Generation' : {1 : '1st Generation',
                    2 : '2nd Generation',
                    3 : '3rd Generation',
                    4 : '4th Generation',
                    5 : '5th Generation',
                    6 : '6th Generation'},
    'Type 1' : {i : i for i in dfPokemon['Type 1'].unique()},
    'Type 2' : {i : i for i in dfPokemon['Type 2'].unique()}
}

@app.callback(Output('scatplotgraph','figure'),
                [Input('huescatplot','value'),
                Input('xscatplot','value'),
                Input('yscatplot','value')]
)

def update_scatplot(hue,x,y):
    return dict(
        data = [
            go.Scatter(
                x = dfPokemon[dfPokemon[hue] == var][x],
                y = dfPokemon[dfPokemon[hue] == var][y],
                name = legendDict[hue][var],
                mode = 'markers'
            ) for var in dfPokemon[hue].unique()
        ],
        layout = dict(
            title = 'Scatter Plot Pokemon',
            xaxis = dict(title = x),
            yaxis = dict(title = y),
            margin = {'l':40,'b':40,'t':40,'r':10},
            hovermode = 'closest'
        )
    )

#_____________________________CALLBACK PIE PLOT______________________________

@app.callback(Output('pieplotgraph','figure'),
                [Input('grouppieplot','value')]
)

def update_pieplot(cat):
    return dict(
        data = [
            go.Pie(
                labels = [legendDict[cat][var] for var in dfPokemon[cat].unique()],
                values = [dfPokemon[dfPokemon[cat] == var]['Total'].count()
                            for var in dfPokemon[cat].unique()],
                hoverinfo = 'label+value',
                textinfo = 'percent'
            )
        ],
        layout = go.Layout(
            title = 'Pie Chart Pokemon',
            margin={'l': 160, 'b': 40, 't': 40, 'r': 10}
        )
    )

#_____________________________CALLBACK HISTOGRAM______________________________

rowcoldict = {
    'Legendary' : [1,2],
    'Generation' : [3,2]
}

@app.callback(Output('histplotgraph','figure'),
                [Input('xhistplot','value'),
                Input('huehistplot','value'),
                Input('stdhistplot','value')]
)

def update_histplot(x,hue,std):
    if hue == 'All':
        return dict(
            data = [
                go.Histogram(
                    x = dfPokemon[(dfPokemon['Total'] >= (
                        dfPokemon['Total'].mean() - (2 * dfPokemon['Total'].std())))
                            & (dfPokemon['Total'] <= (
                        dfPokemon['Total'].mean() + (2 * dfPokemon['Total'].std())))
                        ]['Total'],
                    name = 'Normal',
                    marker = dict(color = '#83BC74')
                ),
                go.Histogram(
                    x = dfPokemon[(dfPokemon['Total'] < (
                        dfPokemon['Total'].mean() - (2 * dfPokemon['Total'].std())))
                            | (dfPokemon['Total'] > (
                        dfPokemon['Total'].mean() + (2 * dfPokemon['Total'].std())))
                        ]['Total'],
                    name = 'Outlier',
                    marker = dict(color = '#E55261')
                )
            ],
            layout = go.Layout(
                title = 'Histogram {} Stats Pokemon'.format(x),
                xaxis = dict( title = 'Total'),
                yaxis = dict( title = 'Count'),
                height = 600,
                width = 1100
            )
        )



    fig = tools.make_subplots(
        rows = rowcoldict[hue][0], cols = rowcoldict[hue][1],
    )

    array = dfPokemon[hue].unique().reshape(rowcoldict[hue][0],rowcoldict[hue][1])

    for row in range(1, rowcoldict[hue][0]+1):
        for col in range(1,rowcoldict[hue][1]+1):
            dfFilter = dfPokemon[dfPokemon[hue] == array[row-1,col-1]]
            fig.append_trace(
                go.Histogram(
                    x = dfFilter[(dfFilter[x] >= (
                        dfFilter[x].mean() - (int(std) * dfFilter[x].std())))
                            & (dfFilter[x] <= (
                        dfFilter[x].mean() + (int(std) * dfFilter[x].std())))
                        ][x],
                    name = 'Normal {}'.format(legendDict[hue][array[row-1,col-1]]),
                    marker = dict(color = '#83BC74')
                ),
                row,col
            ),
            fig.append_trace(
                go.Histogram(
                    x = dfFilter[(dfFilter[x] < (
                        dfFilter[x].mean() - (int(std) * dfFilter[x].std())))
                            | (dfFilter[x] > (
                        dfFilter[x].mean() + (int(std) * dfFilter[x].std())))
                        ][x],
                    name = 'Outlier {}'.format(legendDict[hue][array[row-1,col-1]]),
                    marker = dict(color = '#E55261')
                ),
                row,col
            )

    for axis in range(1, len(dfPokemon[hue].unique())+1):
        fig['layout']['xaxis{}'.format(axis)].update(title = x)
        fig['layout']['yaxis{}'.format(axis)].update(title = 'Count')

    if hue == 'Generation':
        fig['layout'].update(height = 800, width = 1100, title = 'Histogram {} Stats Pokemon'.format(x))
    if hue == 'Legendary':
        fig['layout'].update(height = 500, width = 1100, title = 'Histogram {} Stats Pokemon'.format(x))
    
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)