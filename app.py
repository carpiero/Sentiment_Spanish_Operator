# Import required libraries
from plotly.subplots import make_subplots
import json
import dash
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.express as px
import re
import locale
import plotly.graph_objects as go
import warnings
import datetime
from datetime import datetime as dt
from wrangling import word_cloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64



today = datetime.date.today()
yest = today - datetime.timedelta(days=1)
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

warnings.filterwarnings('ignore')

#####   controls
from controls import df, GRUPO_dict, USER_dict


############# RUN APP
app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}],title='Sentimiento Móvil',update_title='Cargando...')
server = app.server

################### google analytics

app.index_string = '''<!DOCTYPE html>
<html>
<head>
  <!-- Global site tag (gtag.js) - Google Analytics -->
    <script>(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-180754723-1', 'auto');
    ga('send', 'pageview');
    </script>
  <!-- End Global Google Analytics -->
{%metas%}
<title>{%title%}</title>
{%favicon%}
{%css%}
    <meta name="description" content="DataTown | CESEL Interactive Dashboard" />
    <meta name="title" property="og:title" content="DataTown | CESEL Interactive Dashboard" />
    <meta property="og:type" content="DataTown | CESEL Interactive Dashboard" />
    <meta name="image" property="og:image" content="https://i.ibb.co/vQkQkYL/jorge-fernandez-salas-Ch-SZETOal-I-unsplash-asdasdasdasda.jpg" />
    <meta name="description" property="og:description" content="DataTown | CESEL Interactive Dashboard" />
    <meta name="author" content="DataTown | CESEL Interactive Dashboard" />
</head>
<body>
{%app_entry%}
<footer>
{%config%}
{%scripts%}
{%renderer%}
</footer>
</body>
</html>
'''



##################    Create controls

GRUPO_options = [ {"label": GRUPO_dict[x], "value": x}for x in GRUPO_dict]

USER_options = [ {"label": USER_dict[x], "value": x}for x in USER_dict]




locale.setlocale(locale.LC_ALL, '')

#####################################################3

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        # html.Div(
        #     [
        #         # html.Div(
        #         #     [
        #         #         html.Img(
        #         #             src=app.get_asset_url("25231.svg"),
        #         #             id="plotly-image",
        #         #             style={
        #         #                 "height": "60px",
        #         #                 "width": "auto",
        #         #                 "margin-bottom": "25px",
        #         #             },
        #         #         )
        #         #     ],
        #         #     className="one-third column",
        #         # ),
        #         html.Div(
        #             [
        #                 html.Div(
        #                     [
        #                         html.H3(
        #                             "Análisis de sentimiento Twitter",
        #                             style={"margin-bottom": "0px"},
        #                         ),
        #                         html.H5(
        #                             "Operadoras Móviles", style={"margin-top": "0px"}
        #                         ),
        #                     ]
        #                 )
        #             ],
        #             className="one-half column",
        #             id="title",
        #         ),
        #
        #         html.Div(
        #             [
        #                 html.Img(
        #                     src=app.get_asset_url("github.svg"),
        #                     id="plotly-image",
        #                     style={
        #                         "height": "25px",
        #                         "width": "auto",
        #                         'float': 'right','margin-top':'35px'
        #                     },
        #                 ),
        #                 html.A(
        #                     html.Button("Learn More", id="learn-more-button"),
        #                     href="https://github.com/carpiero/Sentiment_Spanish_Operator",
        #                 ),
        #
        #             ],
        #             className="one-third column",
        #             id="button",
        #         ),
        #     ],
        #     id="header",
        #     className="row flex-display",
        #     style={"margin-bottom": "0px"},
        # ),
        html.Div(
            [
                html.Div(
                    [html.Img(
                            src=app.get_asset_url("twitterlogo.png"),
                            id="plotly-image",
                            style={
                                "height": "35px",
                                "width": "auto",
                                'float': 'right','margin-top':'35px'
                            },
                        ),html.H3(
                                    "Análisis de sentimiento Twitter",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Operadoras Móviles", style={"margin-top": "0px"}
                                ),
                        html.P(
                            "Grupo Móvil",
                            className="control_label",
                        ),dcc.Checklist(
                            id="GRUPO_types" ,
                            options=GRUPO_options,
                            value=list(GRUPO_dict.keys())[:],labelStyle={'display': 'inline-block'},#multi=True,
                            className="dcc_control" ,
                        ) ,
                        html.P("Operador", className="control_label"),
                        dcc.Dropdown(
                            id="USER_types" ,
                            # options=well_type_options,
                            # value=list(WELL_TYPES.keys()),
                            className="dcc_control" ,multi=True,
                        ) ,
                        html.P("Fecha de análisis") ,
                        dcc.DatePickerRange(display_format='DD / MM / YYYY',
                            id="date_picker_select" ,
                            start_date=yest ,
                            end_date=today,
                            min_date_allowed=dt(2020 , 11 , 25) ,
                            max_date_allowed=tomorrow ,
                            initial_visible_month=lastMonth,
                            clearable=True,
                            first_day_of_week=1,
                            day_size=35,
                            number_of_months_shown=2,
                            show_outside_days=True,
                            #with_full_screen_portal=True,
                            with_portal=True,
                        ) ,

                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.P('Número de Tweets'),html.H6(id="Tweets_Totales_text")  ] ,
                                    id="Población" ,
                                    className="mini_container" ,
                                ) ,
                                html.Div(
                                    [ html.P("Análisis de Sentimiento 1-5 Stars"), html.H6(id="sentimiento_medio") ] ,
                                    id="sentimiento_medio_id" ,
                                    className="mini_container" ,
                                ) ,
                                html.Div(
                                    [html.P("Tweet con más Likes"),html.H6(id='twitt_best_likes') ,
                                     ] ,
                                    id="twitt_best_likes_text" ,
                                    className="mini_container" ,
                                ) ,
                                html.Div(
                                    # [html.P("URL"),dcc.Link("h",id="url") ,
                                    #  ] ,
                                     id="url_text" ,
                                    className="mini_container" ,
                                ),
                                html.Div(html.A(html.Button("Learn More", id="learn-more-button"),
                            href="https://github.com/carpiero/Sentiment_Spanish_Operator",
                        ),className="mini_container" ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="percentil_graph",config = {'displayModeBar': False})],
                            id="countGraphContainer",
                            className="pretty_container",style={'min-height': '280px'},
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div([html.P("WordCloud"),html.Img(id="wordcloud",style={
                                "height": "auto",
                                "width": "auto",
                                'float': 'left',
                            })],
                   className="pretty_container four columns",style={'min-width': '500px','min-height': '350px'},
                ),
                html.Div(
                    [dcc.Graph(id="coste_bars_graph",config = {'displayModeBar': False})],
                    className="pretty_container eight columns",
                ),
            ],
            className="row flex-display",
        ),
        # html.Div(
        #     [
        #         html.Div(
        #             [dcc.Graph(id="map_graph",config={'modeBarButtonsToRemove': ['lasso2d','pan2d'],'displaylogo': False})],
        #             className="pretty_container eight columns",style={'min-height': '680px'},
        #         ),
        #         html.Div(
        #             [dcc.Graph(id="box_graph",config = {'displayModeBar': False})],
        #             className="pretty_container four columns",style={'min-height': '680px'},
        #         )
        #     ],
        #     className="row flex-display",
        # ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

####################################################
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("percentil_graph", "figure")],
)


############# dropdown

@app.callback(
    [Output("USER_types", "value"),Output("USER_types", "options")], [Input("GRUPO_types", "value")]
)
def display_status(GRUPO_types):
    if len(GRUPO_types) == 4:
        value = list(USER_dict.keys())[:]
        options = USER_options

    else:
        user_def = sorted(df.loc[df['GRUPO'].isin(GRUPO_types) , 'username'].unique().to_list())
        USER_def = dict(zip(user_def, user_def))
        options = [ {"label": USER_def[x], "value":x}for x in USER_def ]
        value=list(USER_def.keys())[:]

    return (value,options)


############# minicontainer

@app.callback(Output("Tweets_Totales_text", "children"),
    [
        Input("GRUPO_types" , "value") , Input("USER_types" , "value") , Input("date_picker_select" , 'start_date'),Input("date_picker_select" , 'end_date')

    ],
)
def update_text(GRUPO_types, USER_types,start_date , end_date ):

    # value=df.loc[df['username'].isin(USER_types),'username'].count()

    value= df.loc[(df['username'].isin(USER_types))&(df['created_at'] >= start_date) & (df['created_at'] < end_date),'username'].count()

    value=locale.format_string('%.0f', value, True)

    return f'{value} tweets'


@app.callback (Output("sentimiento_medio", "children"),
    [
        Input("GRUPO_types" , "value") , Input("USER_types" , "value") , Input("date_picker_select" , 'start_date'),Input("date_picker_select" , 'end_date')

    ],
)

def update_text(GRUPO_types, USER_types,start_date , end_date ):

    value = df.loc[(df['username'].isin(USER_types)) & (df['created_at'] >= start_date) & (
                df['created_at'] < end_date) , 'stars'].mean()

    value=locale.format_string('%.2f', round(value,2), True)

    return f'{value} Stars de media'

@app.callback (Output("twitt_best_likes", "children"),
    [
        Input("GRUPO_types" , "value") , Input("USER_types" , "value") , Input("date_picker_select" , 'start_date'),Input("date_picker_select" , 'end_date')

    ],
)
def update_text(GRUPO_types, USER_types,start_date , end_date ):

    value = df.loc[(df['username'].isin(USER_types)) & (df['created_at'] >= start_date) & (
            df['created_at'] < end_date) & (df['urls'] != 'no url')]

    value = value.loc[value['Tweet_Number_of_Likes'].idxmax() , 'Tweet_Content']

    return value


@app.callback (Output("url_text", "children"),
    [
        Input("GRUPO_types" , "value") , Input("USER_types" , "value") , Input("date_picker_select" , 'start_date') ,
        Input("date_picker_select" , 'end_date')

    ],
)
def update_text(GRUPO_types, USER_types,start_date , end_date ):
    value = df.loc[(df['username'].isin(USER_types)) & (df['created_at'] >= start_date) & (
            df['created_at'] < end_date) & (df['urls'] != 'no url')]

    value = value.loc[value['Tweet_Number_of_Likes'].idxmax() , 'urls']

    return [html.P("URL"),dcc.Link(href=value,target="_blank")]




################   percentil_graph graph

@app.callback(
    Output("percentil_graph", "figure"),
    [
        Input("GRUPO_types" , "value") , Input("USER_types" , "value") , Input("municipio_types" , "value") ,
        Input("partida_de_coste_types" , "value")
    ],[State("wordcloud", "relayoutData")]
    # [State("lock_selector", "value"), State("wordcloud", "relayoutData")],
)
def make_percentil_graph_figure(GRUPO_types, USER_types,municipio_types,partida_de_coste_types, wordcloud):
    if partida_de_coste_types == 'TODOS':
        if GRUPO_types == 'TODAS' and USER_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_count_cn
            df1=df.iloc[[0]]
            df2=df.iloc[[1]]
            df3=df.iloc[[2]]
            df4=df.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['CCAA'] , y=df1['PC_TOTAL'],name='Percentil 90',marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['CCAA'] , y=df2['PC_TOTAL'],name='Percentil 75',marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['CCAA'] , y=df3['PC_TOTAL'],name='Percentil 25',marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['CCAA'] , y=df4['PC_TOTAL'],name='Mediana',marker_color='rgb(217, 95, 2)'))


            fig.update_layout(title=f'Coste por habitante Total, Comunidades Autónomas')

        elif GRUPO_types != 'TODAS' and USER_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_count_c_new_n
            df = df.append(df_count_c.loc[df_count_c['CCAA']==GRUPO_types])
            df.iloc[3,0]=f'{GRUPO_types}.'

            df1 = df.iloc[[0]]
            df2 = df.iloc[[1]]
            df3 = df.iloc[[2]]
            df4 = df.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['CCAA'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['CCAA'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['CCAA'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['CCAA'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por habitante Total, Comunidades Autónomas')

        elif GRUPO_types != 'TODAS' and USER_types != 'TODAS' and municipio_types == 'TODOS':
            df = df_count_p_new_n
            df = df.append(df_count_p.loc[df_count_p['Provincia'] == USER_types])

            df.iloc[3 , 0] = f'{USER_types}.'

            df1 = df.iloc[[0]]
            df2 = df.iloc[[1]]
            df3 = df.iloc[[2]]
            df4 = df.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['Provincia'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['Provincia'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['Provincia'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['Provincia'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por habitante Total, Provincias')

        elif GRUPO_types == 'TODAS' and USER_types != 'TODAS' and municipio_types == 'TODOS':
            df = df_count_p_new_n
            df = df.append(df_count_p.loc[df_count_p['Provincia'] == USER_types])

            df.iloc[3 , 0] = f'{USER_types}.'

            df1 = df.iloc[[0]]
            df2 = df.iloc[[1]]
            df3 = df.iloc[[2]]
            df4 = df.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['Provincia'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['Provincia'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['Provincia'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['Provincia'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por habitante Total, Provincias')

        else:
            cohorte = df_cohorte.loc[df_cohorte['Nombre Ente Principal'] == municipio_types , 'cohorte_pob'].unique().to_list()[0]

            df = df_final_pob[['Nombre Ente Principal' , 'cohorte_pob' , 'PC_TOTAL']].loc[
                (df_final_pob['cohorte_pob'] == cohorte) & (df_final_pob['PC_TOTAL'] > 0)].sort_values(by='PC_TOTAL' ,ascending=False)
            df['Nombre Ente Principal'] = df['Nombre Ente Principal'].astype('object')
            df2 = df.loc[(df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.77 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.51 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.25 , interpolation='nearest'))]

            df2.drop_duplicates(subset='PC_TOTAL' , keep='last' , inplace=True)
            df2 = df2.append(df.loc[df['Nombre Ente Principal'] == municipio_types])
            df = df2
            df['PC_TOTAL'] = round(df['PC_TOTAL'] , )
            df.iloc[3 , 0] = f'{municipio_types}.'

            df1 = df.iloc[[0]]
            df2 = df.iloc[[1]]
            df3 = df.iloc[[2]]
            df4 = df.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['Nombre Ente Principal'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['Nombre Ente Principal'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['Nombre Ente Principal'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['Nombre Ente Principal'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(xaxis=dict(title=f' Municipios con {cohorte} hab.'))
            fig.update_layout(title=f'Coste Mediano por habitante Total')



    else:
        if GRUPO_types == 'TODAS' and USER_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_count_c_pc

            df = df.loc[df['Descripción'] == partida_de_coste_types].sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df.loc[(df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.90 , interpolation='nearest')) | \
                        (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.75 , interpolation='nearest')) | \
                        (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.25 , interpolation='nearest'))]
            df8=df8.sort_values(by='PC_TOTAL' , ascending=False)

            df8=df8.append(df.loc[df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.50 , interpolation='nearest')])
            df8['PC_TOTAL'] = round(df8['PC_TOTAL'] , )
            df1 = df8.iloc[[0]]
            df2 = df8.iloc[[1]]
            df3 = df8.iloc[[2]]
            df4 = df8.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['CCAA'] , y=df1['PC_TOTAL'] , name='Percentil 90' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['CCAA'] , y=df2['PC_TOTAL'] , name='Percentil 75' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['CCAA'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['CCAA'] , y=df4['PC_TOTAL'] , name='Mediana' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por hab. Total, CCCAA, {partida_de_coste_types}')


        elif GRUPO_types != 'TODAS' and USER_types == 'TODAS' and municipio_types == 'TODOS':
            df = df_count_c_pc

            df = df.loc[df['Descripción'] == partida_de_coste_types].sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df.loc[(df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.75 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.50 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.25 , interpolation='nearest'))]
            df8 = df8.sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df8.append(df.loc[df['CCAA'] == GRUPO_types])
            df8['PC_TOTAL'] = round(df8['PC_TOTAL'] , )
            df8.iloc[3,0] = f'{GRUPO_types}.'

            df1 = df8.iloc[[0]]
            df2 = df8.iloc[[1]]
            df3 = df8.iloc[[2]]
            df4 = df8.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['CCAA'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['CCAA'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['CCAA'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['CCAA'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por hab. Total, CCCAA, {partida_de_coste_types}')

        elif GRUPO_types != 'TODAS' and USER_types != 'TODAS' and municipio_types == 'TODOS':
            df = df_count_p_pc

            df = df.loc[df['Descripción'] == partida_de_coste_types].sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df.loc[(df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.75 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.50 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.25 , interpolation='nearest'))]
            df8 = df8.sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df8.append(df.loc[df['Provincia'] == USER_types])
            df8['PC_TOTAL'] = round(df8['PC_TOTAL'] , )
            df8.iloc[3 , 0] = f'{USER_types}.'

            df1 = df8.iloc[[0]]
            df2 = df8.iloc[[1]]
            df3 = df8.iloc[[2]]
            df4 = df8.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['Provincia'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['Provincia'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['Provincia'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['Provincia'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por hab. Total, Provincias, {partida_de_coste_types}')



        elif GRUPO_types == 'TODAS' and USER_types != 'TODAS' and municipio_types == 'TODOS':
            df = df_count_p_pc

            df = df.loc[df['Descripción'] == partida_de_coste_types].sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df.loc[(df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.75 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.50 , interpolation='nearest')) | \
                         (df['PC_TOTAL'] == df['PC_TOTAL'].quantile(0.25 , interpolation='nearest'))]
            df8 = df8.sort_values(by='PC_TOTAL' , ascending=False)

            df8 = df8.append(df.loc[df['Provincia'] == USER_types])
            df8['PC_TOTAL'] = round(df8['PC_TOTAL'] , )
            df8.iloc[3 , 0] = f'{USER_types}.'

            df1 = df8.iloc[[0]]
            df2 = df8.iloc[[1]]
            df3 = df8.iloc[[2]]
            df4 = df8.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['Provincia'] , y=df1['PC_TOTAL'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['Provincia'] , y=df2['PC_TOTAL'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['Provincia'] , y=df3['PC_TOTAL'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(
                go.Bar(x=df4['Provincia'] , y=df4['PC_TOTAL'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(title=f'Coste por hab. Total, Provincias, {partida_de_coste_types}')

        else:
            cohorte = df_cohorte.loc[df_cohorte['Nombre Ente Principal'] == municipio_types , 'cohorte_pob'].unique().to_list()[0]

            df = df_count_m_pc.loc[(df_count_m_pc['cohorte_pob'] == cohorte)  & (df_count_m_pc['Descripción'] == partida_de_coste_types)].sort_values(by='coste_efectivo_PC' , ascending=False)
            # df['Nombre Ente Principal'] = df['Nombre Ente Principal'].astype('object')

            df2 = df.loc[(df['coste_efectivo_PC'] == df['coste_efectivo_PC'].quantile(0.76 , interpolation='nearest')) | \
                         (df['coste_efectivo_PC'] == df['coste_efectivo_PC'].quantile(0.53 , interpolation='nearest')) | \
                         (df['coste_efectivo_PC'] == df['coste_efectivo_PC'].quantile(0.22 , interpolation='nearest'))]

            df2 = df2.sort_values(by='coste_efectivo_PC' , ascending=False)
            df2.drop_duplicates(subset='coste_efectivo_PC' , keep='last' , inplace=True)
            df = df2.append(df.loc[df['Nombre Ente Principal'] == municipio_types])

            df.iloc[3 , 0] = f'{municipio_types}.'
            df['coste_efectivo_PC'] = round(df['coste_efectivo_PC'] , )

            df1 = df.iloc[[0]]
            df2 = df.iloc[[1]]
            df3 = df.iloc[[2]]
            df4 = df.iloc[[3]]

            fig = go.Figure()
            fig.add_trace(go.Bar(x=df1['Nombre Ente Principal'] , y=df1['coste_efectivo_PC'] , name='Percentil 75' , marker_color='#D62728'))
            fig.add_trace(go.Bar(x=df2['Nombre Ente Principal'] , y=df2['coste_efectivo_PC'] , name='Mediana' , marker_color='#3366CC'))
            fig.add_trace(go.Bar(x=df3['Nombre Ente Principal'] , y=df3['coste_efectivo_PC'] , name='Percentil 25' , marker_color='#2CA02C'))
            fig.add_trace(go.Bar(x=df4['Nombre Ente Principal'] , y=df4['coste_efectivo_PC'] , name='Elección' , marker_color='rgb(217, 95, 2)'))
            fig.update_layout(xaxis=dict(title=f'Municipios con {cohorte} hab.'))
            fig.update_layout(title=f'Coste Mediano por hab., {partida_de_coste_types}')

    fig.update_traces(texttemplate="%{y:,} €/h" , textposition='inside',textfont_size=13,
                      #marker_color=['#D62728', '#3366CC',  '#2CA02C', 'rgb(217, 95, 2)']
                      )
    fig.update_traces(marker_line_color='rgb(8,48,107)')




    fig.update_layout(margin=dict(l=10 , r=50 , t=50 , b=10),
                      xaxis_tickfont_size=12 ,
                      # xaxis_tickangle=90 ,
                      yaxis=dict(
                          title='Coste efectivo €/hab.' ,
                          titlefont_size=16 ,
                          tickfont_size=12 ,showticklabels=True,
                          color='rgb(50, 50, 50)',
                             ) ,
                      xaxis=dict(
                          titlefont_size=16 ,
                          tickfont_size=14 , showticklabels=True ,
                          gridcolor='black',
                          color='rgb(50, 50, 50)',
                            showgrid=False,showline=False,
                             ) ,

                      legend=dict(
                          x=1 ,
                          y=1 ,font_color='rgb(50, 50, 50)',
                          # bgcolor='rgba(255, 255, 255, 0)' ,
                          bgcolor='#eeeeee',
                          font_size=14, #bgcolor="#e5ecf6",bordercolor="Black",
                      ) ,
                      barmode='relative' ,
                      bargap=0.55 ,  # gap between bars of adjacent location coordinates.
                      # bargroupgap=0.1,  # gap between bars of the same location coordinate.
                      autosize=True,showlegend=True,paper_bgcolor="#F9F9F9",title_font_color='rgb(50, 50, 50)')

    fig.update_layout(yaxis=dict(gridcolor='#cacaca') ,
                      xaxis=dict(showline=True ,linecolor='#929292' ,linewidth=0.5),
                      plot_bgcolor="#F9F9F9")

    return fig




################    wordcloud graph
@app.callback(
    Output("wordcloud", "src"),
    [
        Input("GRUPO_types" , "value") , Input("USER_types" , "value") , Input("date_picker_select" , 'start_date') ,
        Input("date_picker_select" , 'end_date')
    ],[State("wordcloud", "relayoutData")]
    # [State("lock_selector", "value"), State("wordcloud", "relayoutData")],
)
def make_wordcloud_figure(GRUPO_types, USER_types,start_date , end_date, wordcloud):
    df_filter = df.loc[(df['username'].isin(USER_types)) & (df['created_at'] >= start_date) & (df['created_at'] < end_date)]
    all_words = ' '.join([text for i in df_filter[ 'Tweet_Content_Token'] for text in i])

    img= BytesIO()
    word_cloud.generate_wordcloud(all_words).save(img, format='PNG')
    return f'data:image/png;base64,{base64.b64encode(img.getvalue()).decode()}'











################    coste_bars graph

@app.callback(Output("coste_bars_graph", "figure"),
    [
        Input("GRUPO_types" , "value") , Input("USER_types" , "value") , Input("municipio_types" , "value"),Input("partida_de_coste_types" , "value")
    ],[State("wordcloud", "relayoutData")]
    # [State("lock_selector", "value"), State("wordcloud", "relayoutData")],
)
def make_coste_bars_figure(GRUPO_types, USER_types,municipio_types, partida_de_coste_types,wordcloud):

    if GRUPO_types == 'TODAS' and USER_types == 'TODAS' and municipio_types == 'TODOS':

        df = df_n

        fig = go.Figure()

        # fig.add_trace(go.Bar(x=df['Descripción'] ,y=df['coste_efectivo_new'] ,name='Total Nacional' ,marker_color='rgb(55, 83, 109)'))
        # fig.add_trace(go.Bar(x=df['Descripción'] ,y=df['coste_efectivo_new'] ,name='Total Nacional' ,marker_color='rgb(26, 118, 255)'))

        if partida_de_coste_types !='TODOS':
            colors = ['rgb(55, 83, 109)'] * df['Descripción'].shape[0]

            for pos , item in enumerate(df['Descripción'].to_list()):
                if item == partida_de_coste_types:
                    colors[pos] = 'rgb(217, 95, 2)'
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name='Total Nacional',
                                 marker_color=colors))

            line = int(df.loc[df['Descripción'] == partida_de_coste_types , 'coste_efectivo_new'])
            fig.add_trace(go.Scatter(x=df['Descripción'] , y=[line] * df['Descripción'].shape[0] , showlegend=False ,hoverinfo='skip',
                                     line=dict(color='rgb(217, 95, 2)' , width=0.8 , dash='solid')))


        else:
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name='Total Nacional',
                                 marker_color='rgb(55, 83, 109)'))

        fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name='Total Nacional' ,
                             marker_color='rgb(26, 118, 255)'))









    elif GRUPO_types != 'TODAS' and USER_types == 'TODAS' and municipio_types == 'TODOS':

        df = df_n

        df2 = df_c

        div = df_final_pob.loc[df_final_pob['CCAA'] == GRUPO_types , 'Población 2018'].sum()
        df2 = df2.loc[df2['CCAA'] == GRUPO_types]
        df2['coste_efectivo_new'] = round(df2['coste_efectivo'] / div,)


        fig = go.Figure()
        # fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'{GRUPO_types}' ,
        #                      marker_color='rgb(55, 83, 109)'))
        # fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name='Total Nacional' ,
        #                      marker_color='rgb(26, 118, 255)'))

        if partida_de_coste_types !='TODOS':
            colors = ['rgb(55, 83, 109)'] * df2['Descripción'].shape[0]

            for pos , item in enumerate(df2['Descripción'].to_list()):
                if item == partida_de_coste_types:
                    colors[pos] = 'rgb(217, 95, 2)'
            fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'{GRUPO_types}' ,
                                 marker_color=colors))

            line=int(df2.loc[df2['Descripción'] == partida_de_coste_types , 'coste_efectivo_new'])
            fig.add_trace(go.Scatter(x=df['Descripción'] , y=[line] * df['Descripción'].shape[0] , showlegend=False ,hoverinfo='skip',
                                     line=dict(color='rgb(217, 95, 2)' , width=0.8 , dash='solid')))

        else:
            fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'{GRUPO_types}' ,
                                 marker_color='rgb(55, 83, 109)'))

        fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name='Total Nacional' ,
                             marker_color='rgb(26, 118, 255)'))


    elif GRUPO_types != 'TODAS' and USER_types != 'TODAS' and municipio_types == 'TODOS':

        df = df_p
        div = df_final_pob.loc[df_final_pob['Provincia'] == USER_types , 'Población 2018'].sum()
        df = df.loc[df['Provincia'] == USER_types]
        df['coste_efectivo_new'] = round(df['coste_efectivo'] / div,)


        df2 = df_c
        div = df_final_pob.loc[df_final_pob['CCAA'] == GRUPO_types , 'Población 2018'].sum()
        df2 = df2.loc[df2['CCAA'] == GRUPO_types]
        df2['coste_efectivo_new'] = round(df2['coste_efectivo'] / div,)


        fig = go.Figure()
        # fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name=f'{USER_types}' ,
        #                      marker_color='rgb(55, 83, 109)'))
        # fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'{GRUPO_types}' ,
        #                      marker_color='rgb(26, 118, 255)'))


        if partida_de_coste_types !='TODOS':
            colors = ['rgb(55, 83, 109)'] * df['Descripción'].shape[0]

            for pos , item in enumerate(df['Descripción'].to_list()):
                if item == partida_de_coste_types:
                    colors[pos] = 'rgb(217, 95, 2)'
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name=f'{USER_types}',
                                 marker_color=colors))

            line = int(df.loc[df['Descripción'] == partida_de_coste_types , 'coste_efectivo_new'])
            fig.add_trace(go.Scatter(x=df2['Descripción'] , y=[line] * df2['Descripción'].shape[0], showlegend=False ,hoverinfo='skip',
                                     line=dict(color='rgb(217, 95, 2)' ,width=0.8 , dash='solid')))

        else:
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name=f'{USER_types}' ,
                                 marker_color='rgb(55, 83, 109)'))

        fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'{GRUPO_types}' ,
                             marker_color='rgb(26, 118, 255)'))






    elif GRUPO_types == 'TODAS' and USER_types != 'TODAS' and municipio_types == 'TODOS':

        df = df_p
        div = df_final_pob.loc[df_final_pob['Provincia'] == USER_types , 'Población 2018'].sum()
        df = df.loc[df['Provincia'] == USER_types]
        df['coste_efectivo_new'] = round(df['coste_efectivo'] / div,0)


        df2 = df_n

        fig = go.Figure()
        # fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name=f'{USER_types}' ,
        #                      marker_color='rgb(55, 83, 109)'))
        # fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'Total Nacional' ,
        #                      marker_color='rgb(26, 118, 255)'))

        if partida_de_coste_types !='TODOS':
            colors = ['rgb(55, 83, 109)'] * df['Descripción'].shape[0]

            for pos , item in enumerate(df['Descripción'].to_list()):
                if item == partida_de_coste_types:
                    colors[pos] = 'rgb(217, 95, 2)'
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name=f'{USER_types}',
                                 marker_color=colors))

            line = int(df.loc[df['Descripción'] == partida_de_coste_types , 'coste_efectivo_new'])
            fig.add_trace(go.Scatter(x=df2['Descripción'] , y=[line] * df2['Descripción'].shape[0] , showlegend=False ,hoverinfo='skip',
                                     line=dict(color='rgb(217, 95, 2)' , width=0.8 , dash='solid')))

        else:
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_new'] , name=f'{USER_types}' ,
                                 marker_color='rgb(55, 83, 109)'))

        fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_new'] , name=f'Total Nacional' ,
                             marker_color='rgb(26, 118, 255)'))


    else:
        df =df_m.loc[df_m['Nombre Ente Principal'] == municipio_types].sort_values(by='coste_efectivo_PC',ascending=False)
        # df['coste_efectivo_PC'] = round(df['coste_efectivo_PC'] , )



        cohorte = df_cohorte.loc[df_cohorte['Nombre Ente Principal'] == municipio_types , 'cohorte_pob'] \
            .unique().to_list()[0]

        # df2 = df_final_pob_melt_PC.loc[ df_final_pob_melt_PC['coste_efectivo_PC'] > 0]
        df2 = df_m.pivot_table(index=['cohorte_pob','Descripción'],values=['coste_efectivo_PC'],aggfunc=np.median).reset_index()
        df2= df2.loc[df2['cohorte_pob'] == cohorte]
        # df2['coste_efectivo_PC'] = round(df2['coste_efectivo_PC'] , )


        fig = go.Figure()
        # fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_PC'] , name=f'{municipio_types}' ,
        #                      marker_color='rgb(55, 83, 109)'))
        # fig.add_trace(go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_PC'] , name=f'Media Municipios con {cohorte} hab.' ,
        #                      marker_color='rgb(26, 118, 255)'))


        if partida_de_coste_types !='TODOS':
            colors = ['rgb(55, 83, 109)'] * df['Descripción'].shape[0]

            for pos , item in enumerate(df['Descripción'].to_list()):
                if item == partida_de_coste_types:
                    colors[pos] = 'rgb(217, 95, 2)'
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_PC'] , name=f'{municipio_types}',
                                 marker_color=colors))

            line = int(df.loc[df['Descripción'] == partida_de_coste_types , 'coste_efectivo_PC'])


            fig.add_trace(go.Scatter(x=df2['Descripción'] , y=[line] * df2['Descripción'].shape[0], showlegend=False ,hoverinfo='skip',
                                     line=dict(color='rgb(217, 95, 2)' , width=0.8 , dash='solid')))

        else:
            fig.add_trace(go.Bar(x=df['Descripción'] , y=df['coste_efectivo_PC'] , name=f'{municipio_types}' ,
                                 marker_color='rgb(55, 83, 109)'))

        fig.add_trace(
            go.Bar(x=df2['Descripción'] , y=df2['coste_efectivo_PC'] , name=f'Media Municipios con {cohorte} hab.' ,
                   marker_color='rgb(26, 118, 255)'))


    # fig.update_traces( marker_line_color='rgb(8,48,107)')
    fig.update_layout(margin=dict(l=20 , r=50 , t=50 , b=50) ,#plot_bgcolor="white",
                          title='Costes €/hab. por Partida de coste' ,
                          xaxis_tickfont_size=12 ,
                          xaxis_tickangle=-45 ,
                          yaxis=dict(
                              title='Coste €/hab.' ,
                              titlefont_size=16 ,
                              tickfont_size=12 ,showticklabels=True,color='rgb(50, 50, 50)',

                          ) ,
                          xaxis=dict(
                              title='Partidas de Costes' ,
                              titlefont_size=16 ,
                              tickfont_size=14 , showticklabels=False ,color='rgb(50, 50, 50)',
                            showline=False,
                            showgrid=False,

                          ) ,

                          legend=dict(
                              x=0.40 ,
                              y=0.9 ,font_color='rgb(50, 50, 50)',
                              # bgcolor='rgba(255, 255, 255, 0)' ,
                              # bordercolor='rgba(255, 255, 255, 0)',
                              font_size=14,bgcolor='#eeeeee',
        # bordercolor="Black",
        # borderwidth=0.8
                          ) ,
                          barmode='group' ,
                          # bargap=0.30 ,
                          # bargroupgap=0.35  ,
                        bargap = 0.10 ,  # gap between bars of adjacent location coordinates.
                        bargroupgap = 0.25 , # gap between bars of the same location coordinate.

                          paper_bgcolor="#F9F9F9",title_font_color='rgb(50, 50, 50)')

    fig.update_layout(yaxis=dict(gridcolor='#cacaca') ,
                      xaxis=dict(showline=True ,linecolor='#929292' ,linewidth=0.5),
                      plot_bgcolor="#F9F9F9")

    return fig






# Main
if __name__ == "__main__":
    app.run_server(debug=True)

    ########### debug FALSE
