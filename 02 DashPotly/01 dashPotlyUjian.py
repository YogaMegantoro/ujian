import pandas as pd
import seaborn as sns
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from sqlalchemy import create_engine
import plotly.graph_objs as go

app = dash.Dash()

def setting_connect(MYSQL_USER,MYSQL_PASSWORD,MYSQL_HOST_IP,MYSQL_PORT,MYSQL_DATABASE):
    engine=create_engine('mysql+mysqlconnector://'+MYSQL_USER+':'+MYSQL_PASSWORD+'/'+MYSQL_DATABASE+'?host='+MYSQL_HOST_IP+'?port='+MYSQL_PORT)
    return engine.connect()

conn = setting_connect('root','mavacaga@localhost','localhost','3306','latihanujian')

results = conn.execute("SELECT * FROM ujiantitanic1.titanic; ").fetchall()
mydata= pd.DataFrame(results)
mydata.columns = results[0].keys()
mydata.head()

app.title = 'Purwadhika Dash Plotly';

color_set = {
    'survive': ['#ff3fd8','#4290ff'],
    'sex': ['#32fc7c','#ed2828'],
    'embark': ['#0059a3','#f2e200','#00c9ed'],
    'who': ['#ff8800','#ddff00','#3de800']
}


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col,className='table_dataset') for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col],className='table_dataset') for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
        ,className='table_dataset'
    )

app.layout = html.Div(children=[
    dcc.Tabs(id="tabs", value='tab-1',
        style={
            'fontFamily': 'system-ui'
        },
        content_style={
            'fontFamily': 'Arial',
            'borderLeft': '1px solid #d6d6d6',
            'borderRight': '1px solid #d6d6d6',
            'borderBottom': '1px solid #d6d6d6',
            'padding': '44px'
        },
        children=[
            dcc.Tab(label='Ujian Titanic', value='tab-1', children=[
                html.Div([
                    html.Center(html.H1('Table Titanic')),
                    #generate_table(dfTips)
                    dcc.Graph(
                        id = "tableData",
                        figure = {
                            "data" : [
                                go.Table(

                                    header = dict(
                                        values = [ "<b>" + col + " </b>" for col in mydata.columns ] ,
                                        font = dict(size=18),
                                        height = 30,
                                        #fill = dict(color="a1c13d1")
                                    ),
                                    cells=dict(
                                        values = [mydata[col] for col in mydata.columns ],
                                        # font = dict(size = 16),
                                        # height = 30,
                                        # #fill = dict(color="#EDFAFF")

                                    )
                                )
                            ]
                            #"layout" dict(height=500)
                        }
                    )
                ])
            ]),

            dcc.Tab(label='Categorical Plot', value='tab-2', children=[
            html.Div([
                html.H1('Categorical Tips Data Set'),
                html.Table([
                    html.Tr([
                        html.Td([
                            html.P("Jenis : "),
                            dcc.Dropdown(
                                id = 'ddl-jenis-plot-category',
                                options = [ {"label" : "Bar", "value" : "bar" },
                                            {"label" : "Violin", "value" : "violin"},
                                            {"label" : "Box" , "value" : "box"},

                                ],

                                value = "violin"


                            )
                        ]),

                        html.Td([
                            html.P("X Axis :"),
                            dcc.Dropdown(
                                id = "ddl-x-plot-category",
                                options = [
                                    {"label" : "Survived" , "value" : "survive"},
                                    {"label" : "Sex" , "value" : "sex"},
                                    {"label" : "Embark Town" , "value" : "embark"},
                                    {"label" : "Who" , "value" : "who"},

                                ],

                                value = "sex"
                            )
                        ])
                    ])
                ], style={ 'width' : '700px', 'margin': '0 auto'}),
                dcc.Graph(
                    id = "categoricalPlot",
                    figure = {
                        "data" : []
                    }
                )
            ])
        ]),
        ])
    ]) #layout


############################################

listGOFunc = {
    "bar": go.Bar,
    "violin": go.Violin,
    "box": go.Box
             }

def getPlot(jenis, xCategory) :
    return [listGOFunc[jenis](
                x=mydata[xCategory],
                y=mydata['fare'],
                text=mydata['sex'],
                opacity=0.7,
                name='Fare',
                marker=dict(color='blue'), #apa itu dict
                legendgroup='Fare'
            ),
            listGOFunc[jenis](
                x=dfTips[xCategory],
                y=dfTips['age'],
                text=dfTips['sex'],
                opacity=0.7,
                name='Age',
                marker=dict(color='orange'),
                legendgroup='Age'
            )]

@app.callback(
    Output('categoricalPlot', 'figure'),
    [Input('ddl-jenis-plot-category', 'value'),
    Input('ddl-x-plot-category', 'value')])
def update_category_graph(ddljeniscategory, ddlxcategory):
    return {
            'data': getPlot(ddljeniscategory,ddlxcategory),
            'layout': go.Layout(
                xaxis={'title': ddlxcategory.capitalize()}, yaxis={'title': 'US$'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1.2}, hovermode='closest',
                boxmode='group',violinmode='group'
                # plot_bgcolor= 'black', paper_bgcolor= 'black',
            )
    };

if __name__ == '__main__':
    # run server on port 1997
    # debug=True for auto restart if code edited
    app.run_server(debug=True,port=8053)
