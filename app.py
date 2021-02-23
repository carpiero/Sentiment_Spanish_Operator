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
from controls import df, GRUPO_dict, USER_dict, df_f, df_g_stars, df_word, df_g_sunburst, df_g_source, df_g_time, df_g_menciones


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
    <meta name="description" content="Sentimiento Móvil | Sentiment Analysis (NLP) of Mobile Operators" />
    <meta name="title" property="og:title" content="Sentimiento Móvil | Sentiment Analysis (NLP) of Mobile Operators" />
    <meta property="og:type" content="Sentimiento Móvil | Sentiment Analysis (NLP) of Mobile Operators" />
    <meta name="image" property="og:image" content="https://i.ibb.co/ZNr9vr7/brett-jordan-ul-Rl-Am1-ITMU-unsplash.jpg" />
    <meta name="description" property="og:description" content="Sentimiento Móvil | Sentiment Analysis (NLP) of Mobile Operators" />
    <meta name="author" content="Sentimiento Móvil | Sentiment Analysis (NLP) of Mobile Operators" />
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
                                "height": "55px",
                                "width": "auto",
                                'float': 'right','margin-top':'35px'
                            },
                        ),html.H3(
                                    "Análisis de Sentimiento Twitter",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Operadoras Móviles", style={"margin-top": "0px"}
                                ),
                                html.H4(
                                    "El modelo usado para analizar las menciones (bert-base-multilingual-uncased), esta diseñado para predecir el sentimiento como un número de Stars (entre 1 y 5). ", style={"margin-top": "0px"}
                                ),html.Br(),
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
                        ) ,html.Br(),
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
                        ) ,html.Br(),html.Br(),html.Br(),html.Br(),
                            html.Div(html.A(html.Button("Learn More", id="learn-more-button"),
                            href="https://github.com/carpiero/Sentiment_Spanish_Operator",
                        ),className="dcc_control" )
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
                        #         html.Div(html.A(html.Button("Learn More", id="learn-more-button"),
                        #     href="https://github.com/carpiero/Sentiment_Spanish_Operator",
                        # ),className="mini_container" ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="stars_graph",config = {'displayModeBar': False})],
                            id="countGraphContainer",
                            className="pretty_container",style={'min-width': '500px','min-height': '350px'},
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
                    [dcc.Graph(id="sunburst_tweet",config = {'displayModeBar': False})],
                    className="pretty_container four columns",style={'min-width': '250px','min-height': '250px'},
                ),
                html.Div(
                    [dcc.Graph(id="source_tweet",config = {'displayModeBar': False})],
                    className="pretty_container four columns",style={'min-width': '150px','min-height': '150px'},
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="time_tweet",config = {'displayModeBar': False})],
                    className="pretty_container twelve columns",style={'min-width': '500px','min-height': '350px'},
                ),
        #         html.Div(
        #             [dcc.Graph(id="box_graph",config = {'displayModeBar': False})],
        #             className="pretty_container four columns",style={'min-height': '680px'},
        #         )
             ],
            className="row flex-display",
        ),
                html.Div(
            [
                html.Div(
                    [dcc.Graph(id="menciones_tweet",config = {'displayModeBar': False})],
                    className="pretty_container twelve columns",style={'min-width': '500px','min-height': '350px'},
                ),
        #         html.Div(
        #             [dcc.Graph(id="box_graph",config = {'displayModeBar': False})],
        #             className="pretty_container four columns",style={'min-height': '680px'},
        #         )
             ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

####################################################
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("stars_graph", "figure")],
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
         Input("USER_types" , "value") , Input("date_picker_select" , 'start_date'),Input("date_picker_select" , 'end_date')

    ],
)
def update_text(USER_types,start_date , end_date ):

    # value=df.loc[df['username'].isin(USER_types),'username'].count()

    value= df.loc[(df['username'].isin(USER_types))&(df['created_at'] >= start_date) & (df['created_at'] < end_date),'username'].count()

    value=locale.format_string('%.0f', value, True)

    return f'{value} tweets'


@app.callback (Output("sentimiento_medio", "children"),
    [
        Input("USER_types" , "value") , Input("date_picker_select" , 'start_date'),Input("date_picker_select" , 'end_date')

    ],
)

def update_text(USER_types,start_date , end_date ):

    value = df.loc[(df['username'].isin(USER_types)) & (df['created_at'] >= start_date) & (
                df['created_at'] < end_date) , 'stars'].mean()

    value=locale.format_string('%.2f', round(value,2), True)

    return f'{value} Stars de media'

@app.callback (Output("twitt_best_likes", "children"),
    [
        Input("USER_types" , "value") , Input("date_picker_select" , 'start_date'),Input("date_picker_select" , 'end_date')

    ],
)
def update_text(USER_types,start_date , end_date ):

    value = df.loc[(df['username'].isin(USER_types)) & (df['created_at'] >= start_date) & (
            df['created_at'] < end_date) & (df['urls'] != 'no url')]

    value = value.loc[value['Tweet_Number_of_Likes'].idxmax() , 'Tweet_Content']

    return value


@app.callback (Output("url_text", "children"),
    [
        Input("USER_types" , "value") , Input("date_picker_select" , 'start_date') ,
        Input("date_picker_select" , 'end_date')

    ],
)
def update_text(USER_types,start_date , end_date ):
    value = df.loc[(df['username'].isin(USER_types)) & (df['created_at'] >= start_date) & (
            df['created_at'] < end_date) & (df['urls'] != 'no url')]

    value = value.loc[value['Tweet_Number_of_Likes'].idxmax() , 'urls']

    return [html.P("URL"),dcc.Link(href=value,target="_blank")]




################   stars_graph graph

@app.callback(
    Output("stars_graph", "figure"),
    [
        Input("USER_types" , "value") , Input("date_picker_select" , 'start_date') ,
        Input("date_picker_select" , 'end_date'),
            ],[State("wordcloud", "relayoutData")]
    # [State("lock_selector", "value"), State("wordcloud", "relayoutData")],
)
def make_stars_graph_figure(USER_types,start_date , end_date, wordcloud):
    df_stars= df_g_stars
    df_stars = df_stars.loc[(df['username'].isin(USER_types)) &(df_stars['created_at'] >= start_date) & ( df_stars['created_at'] < end_date) ,]
    df_stars =  df_stars.pivot_table(index=['username','orden','color'],values=['stars']).sort_values(by='orden' ,ascending=True).reset_index()
    df_stars['stars'] = round(df_stars['stars'] ,2 )

    colors = df_stars['color'].to_list()

    fig = go.Figure()

    fig.add_trace(go.Bar(x=df_stars['username'] , y=df_stars['stars'] , name='Masmovil' , marker_color=colors))


    # y = [line] * df2['Descripción'].shape[0]
    since = datetime.datetime.strptime(start_date , '%Y-%m-%d')
    until = datetime.datetime.strptime(end_date, '%Y-%m-%d')
    since=datetime.datetime.strftime(since , '%d-%m-%Y')
    until=datetime.datetime.strftime(until , '%d-%m-%Y')

    fig.update_layout(title=f'Análisis de Sentimiento, Stars de media desde {since} a {until}')

    fig.update_traces(texttemplate="%{y:.2f} Stars" , textposition='inside',textfont_size=13,
                      #marker_color=['#D62728', '#3366CC',  '#2CA02C', 'rgb(217, 95, 2)']
                      )
    # fig.update_traces(marker_line_color='#C8CDD0')

    line = df.loc[(df['username'].isin(USER_types)) & (df['created_at'] >= start_date) & (
            df['created_at'] < end_date) , 'stars'].mean()

    fig.add_shape(type='line' ,
                  x0=0 ,
                  y0=line ,
                  x1=1 ,
                  y1=line ,
                  line=dict(color='#EFF3F5' , width=1.2 , dash='dash'),
                  xref='paper' ,
                  yref='y'
                  )
    # fig.add_trace(go.Scatter(x=df_stars['username'] , y=[line] * df_stars['username'].shape[0] , showlegend=False ,
    #                          hoverinfo='skip' ,
    #                          line=dict(color='#000000' , width=0.8 , dash='solid')))


    fig.update_layout(margin=dict(l=10 , r=50 , t=50 , b=10),
                     yaxis=dict(
                          title='Stars 1 - 5' ,
                          titlefont_size=16 ,
                          tickfont_size=12 ,showticklabels=True,range=[0,5],
                          color='#C8CDD0',showline=True,gridcolor='#8D8D8D',linewidth=0.2,linecolor='#8D8D8D',zerolinecolor='#8D8D8D',
                         #zeroline=False,
                             ) ,
                      xaxis=dict( titlefont_size=16 ,
                          tickfont_size=14 , showticklabels=True , type="category",
                          #gridcolor='black',
                          color='#C8CDD0',
                            showgrid=False,gridcolor='#8D8D8D',showline=False ,linecolor='#8D8D8D' ,linewidth=10.2,zerolinecolor='#8D8D8D',
                             ) ,

                      # legend=dict(
                      #     x=1 ,
                      #     y=1 ,font_color='rgb(50, 50, 50)',
                      #     # bgcolor='rgba(255, 255, 255, 0)' ,
                      #     bgcolor='#eeeeee',
                      #     font_size=14, #bgcolor="#e5ecf6",bordercolor="Black",
                      # ) ,
                      barmode='relative' ,
                      bargap=0.20 ,  # gap between bars of adjacent location coordinates.
                      # bargroupgap=0.1,  # gap between bars of the same location coordinate.
                      autosize=True,showlegend=False,paper_bgcolor="#212E36",title_font_color='#EFF3F5', plot_bgcolor="#212E36")



    return fig




################    wordcloud graph
@app.callback(
    Output("wordcloud", "src"),
    [
         Input("USER_types" , "value") , Input("date_picker_select" , 'start_date') ,
        Input("date_picker_select" , 'end_date') ,
    ] , [State("wordcloud" , "relayoutData")]
    # [State("lock_selector", "value"), State("wordcloud", "relayoutData")],
)
def make_wordcloud_figure(USER_types,start_date , end_date, wordcloud):
    df_wor = df_word
    df_filter = df_wor.loc[(df_wor['username'].isin(USER_types)) & (df_wor['created_at'] >= start_date) & (df_wor['created_at'] < end_date)]
    all_words = ' '.join([text for i in df_filter[ 'Tweet_Content_Token'] for text in i])

    img= BytesIO()
    word_cloud.generate_wordcloud(all_words).save(img, format='PNG')
    return f'data:image/png;base64,{base64.b64encode(img.getvalue()).decode()}'


################    sunburst_tweet graph

@app.callback(Output("sunburst_tweet", "figure"),
    [
        Input("USER_types" , "value") , Input("date_picker_select" , 'start_date') ,
        Input("date_picker_select" , 'end_date') ,
    ] , [State("wordcloud" , "relayoutData")]
    # [State("lock_selector", "value"), State("wordcloud", "relayoutData")],
)
def make_sunburts_tweet_figure(USER_types,start_date , end_date, wordcloud):
    df_stars = df_g_sunburst
    df_stars = df_stars.loc[(df['username'].isin(USER_types)) & (df_stars['created_at'] >= start_date) & (
                df_stars['created_at'] < end_date) ,]

    df_stars['count'] = 1

    sum= df_stars['count'].sum()
    sum = locale.format_string('%.0f' , sum , True)
    fig = px.sunburst(df_stars, path=['GRUPO' , 'username'] , values='count' , color='GRUPO',
                      color_discrete_map = {'Vodafone': '#E64A19' , 'Movistar': '#2962FF' , 'Masmovil': '#8E8E00' , 'Orange': '#A56B00'},
                      labels={'parent': 'Grupo Móvil','count': 'Nº de Menciones','labels': 'Operadora'},#hover_name='username',
                        hover_data = {'count': ':,' , 'GRUPO': False ,
                                                          }


                      )
    fig.update_traces(textinfo="label+percent root")


    fig.update_layout(margin=dict(l=15 , r=15 , t=30 , b=5) ,title=f'Distribución Nº de Menciones {sum}' ,
                      yaxis=dict(
                          title='Stars 0 - 5' ,
                          titlefont_size=16 ,
                          tickfont_size=12 , showticklabels=True , range=[0 , 5] ,
                          color='#C8CDD0' , showline=True , gridcolor='#8D8D8D' , linewidth=0.2 , linecolor='#8D8D8D' ,
                          zerolinecolor='#8D8D8D' ,
                          # zeroline=False,
                      ) ,
                      xaxis=dict(
                          titlefont_size=16 ,
                          tickfont_size=14 , showticklabels=True , type="category" ,
                          # gridcolor='black',
                          color='#C8CDD0' ,
                          showgrid=False , gridcolor='#8D8D8D' , showline=False , linecolor='#8D8D8D' , linewidth=10.2 ,
                          zerolinecolor='#8D8D8D' ,
                      ) ,

                      # legend=dict(
                      #     x=1 ,
                      #     y=1 ,font_color='rgb(50, 50, 50)',
                      #     # bgcolor='rgba(255, 255, 255, 0)' ,
                      #     bgcolor='#eeeeee',
                      #     font_size=14, #bgcolor="#e5ecf6",bordercolor="Black",
                      # ) ,
                      barmode='relative' ,
                      bargap=0.20 ,  # gap between bars of adjacent location coordinates.
                      # bargroupgap=0.1,  # gap between bars of the same location coordinate.
                      autosize=True , showlegend=False , paper_bgcolor="#212E36" , title_font_color='#EFF3F5' ,
                      plot_bgcolor="#212E36",
                      hoverlabel=dict(

                          font_size=14,
                                 ),
                      )

    return fig

################    source_tweet graph

@app.callback(Output("source_tweet", "figure"),
    [
        Input("USER_types" , "value") , Input("date_picker_select" , 'start_date') ,
        Input("date_picker_select" , 'end_date') ,
    ] , [State("wordcloud" , "relayoutData")]
    # [State("lock_selector", "value"), State("wordcloud", "relayoutData")],
)
def make_source_tweet_figure(USER_types,start_date , end_date, wordcloud):
    df_stars = df_g_source
    df_stars = df_stars.loc[(df_stars['username'].isin(USER_types)) & (df_stars['created_at'] >= start_date) & (
                df_stars['created_at'] < end_date) ,]

    df_stars = df_stars['source'].value_counts().rename_axis('unique_values').reset_index(name='counts').head(6).sort_values(by='counts' ,ascending=True)
    df_stars['percent'] = round(df_stars['counts'] / df_stars['counts'].sum()*100,1)
    # df_stars = df_stars.style.format({'percent': '{:,.1%}'.format})
    colors=['#BBDEFB','#90CAF9','#64B5F6','#2196F3','#1976D2','#0D47A1']

    fig = go.Figure()

    fig.add_trace(go.Bar(y=df_stars['unique_values'] , x=df_stars['percent'] , name='Masmovil' ,orientation='h',marker_color=colors,
                         ))

    fig.update_traces(texttemplate="%{x:.1f} %" , textposition='auto' , textfont_size=13 ,
                      # marker_color=['#D62728', '#3366CC',  '#2CA02C', 'rgb(217, 95, 2)']
                      )

    fig.update_layout(margin=dict(l=10 , r=20 , t=30 , b=10) ,title='Origen tweets' ,
                      xaxis=dict(
                          title='Porcentaje' ,#range=[0,100],
                          titlefont_size=16 ,
                          tickfont_size=12 , showticklabels=True ,
                          color='#C8CDD0' , showline=True , gridcolor='#8D8D8D' , linewidth=0.2 , linecolor='#8D8D8D' ,
                          zerolinecolor='#8D8D8D' ,
                          # zeroline=False,
                      ) ,
                      yaxis=dict(
                          titlefont_size=16 ,
                          tickfont_size=14 , showticklabels=True , type="category" ,
                          # gridcolor='black',
                          color='#C8CDD0' ,
                          showgrid=False , gridcolor='#8D8D8D' , showline=False , linecolor='#8D8D8D' , linewidth=10.2 ,
                          zerolinecolor='#8D8D8D' ,
                      ) ,

                      # legend=dict(
                      #     x=1 ,
                      #     y=1 ,font_color='rgb(50, 50, 50)',
                      #     # bgcolor='rgba(255, 255, 255, 0)' ,
                      #     bgcolor='#eeeeee',
                      #     font_size=14, #bgcolor="#e5ecf6",bordercolor="Black",
                      # ) ,
                      barmode='relative' ,
                      bargap=0.20 ,  # gap between bars of adjacent location coordinates.
                      # bargroupgap=0.1,  # gap between bars of the same location coordinate.
                      autosize=True , showlegend=False , paper_bgcolor="#212E36" , title_font_color='#EFF3F5' ,
                      plot_bgcolor="#212E36",
                      hoverlabel=dict(

                          font_size=16 ,
                                 ),
                      )

    return fig


################    time_tweet graph

@app.callback(Output("time_tweet", "figure"),
    [
        Input("USER_types" , "value") , Input("date_picker_select" , 'start_date') ,
        Input("date_picker_select" , 'end_date') ,
    ] , [State("wordcloud" , "relayoutData")]
    # [State("lock_selector", "value"), State("wordcloud", "relayoutData")],
)
def make_time_tweet_figure(USER_types,start_date , end_date, wordcloud):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date )

    dias = end_date - start_date

    if dias < datetime.timedelta(days=31):
        rest = datetime.timedelta(days=31) - dias
        start_date = start_date - rest

    df_stars = df_g_time
    # df_stars = df_stars.loc[df['username'].isin(USER_types)]
    df_stars = df_stars.loc[(df_stars['username'].isin(USER_types)) & (df_stars['created_at'] >= start_date) & (
            df_stars['created_at'] < end_date) ,]
    df_media_total = df_stars.groupby(pd.Grouper(key='created_at' , freq='W'))[['stars']].mean().reset_index()
    df_media_total['username'] = 'Media Operadoras'
    df_stars = df_stars.groupby(['username',pd.Grouper(key='created_at',freq='W')])[['stars']].mean().reset_index()
    df_stars =df_stars.append(df_media_total)

    df_stars['stars'] = round(df_stars['stars'] , 2)

    fig = go.Figure()

    # fig.add_trace(go.Scatter(x=df_stars['created_at'] , y=df_stars['stars'] ,
    #                          mode='lines+markers' ,
    #                          name='lines+markers'))
    fig = px.line(df_stars , x='created_at' , y='stars' , color='username' ,
                  labels={'created_at': 'Fecha'} ,
                  hover_name='username',
                  hover_data={'stars': ':,' , 'username': False ,'created_at': '|Semana %V del año %Y' ,
                              },
                  color_discrete_map={'@vodafone_es': '#E64A19',
                                      '@Lowi_es':   '#FF7043',   #'#FFAB91'
                                        '@vodafoneyu': '#212E36',
                                         '@movistar_es': '#2962FF',
                                         '@TuentiES' :'#82B1FF',
                                         '@o2es' : '#0D47A1',
                                         '@orange_es': '#F57C00',
                                         '@jazztel_es': '#FFE0B2',
                                         '@Amena' : '#FF9800',
                                         '@simyo_es': '#FFB74D',
                                         '@masmovil' : '#FFFF00',
                                         '@pepephone' : '#FFFF8D',
                                         '@yoigo' : '#FFF9C4',
                                        'Media Operadoras':'#EFF3F5'},
                  category_orders={'username': ['Media Operadoras','@vodafone_es' , '@Lowi_es','@movistar_es','@o2es',
                                                '@TuentiES' ,'@orange_es','@Amena','@simyo_es','@jazztel_es','@masmovil',
                                                '@pepephone','@yoigo',
                                                '@vodafoneyu']})

    fig.update_traces(mode='lines+markers',line=dict( width=2))

    fig.update_layout(margin=dict(l=10 , r=20 , t=30 , b=10) ,title='Evolución Sentimiento Medio Semanal',
                      xaxis=dict(title='',
                          #title='Porcentaje' ,#range=[0,100],
                          titlefont_size=16 ,
                          tickfont_size=12 , showticklabels=True ,
                          color='#C8CDD0' , showline=True , gridcolor='#8D8D8D' , linewidth=0.2 , linecolor='#8D8D8D' ,
                          zerolinecolor='#8D8D8D' ,showgrid=False ,
                          # zeroline=False,
                      ) ,
                      yaxis=dict(
                          titlefont_size=16 ,
                          tickfont_size=14 , showticklabels=True ,
                          # gridcolor='black',
                          color='#C8CDD0' ,
                          showgrid=False , gridcolor='#8D8D8D' , showline=True , linecolor='#8D8D8D' , linewidth=0.2 ,
                          zerolinecolor='#8D8D8D' ,title_text='Stars 1 - 5'
                      ) ,

                      legend=dict(
                          x=1 ,
                          y=1 ,font_color='#C8CDD0',
                          # bgcolor='rgba(255, 255, 255, 0)' ,
                          bgcolor='#212E36',
                          font_size=14, #bgcolor="#e5ecf6",
                          bordercolor="#192229",borderwidth=2, title_text='',
                      ) ,
                      barmode='relative' ,
                      bargap=0.20 ,  # gap between bars of adjacent location coordinates.
                      # bargroupgap=0.1,  # gap between bars of the same location coordinate.
                      autosize=True , showlegend=True , paper_bgcolor="#212E36" , title_font_color='#EFF3F5' ,
                      plot_bgcolor="#212E36",
                      hoverlabel=dict(

                          font_size=16 ,
                                 ),
                      )

    return fig

################    menciones_tweet graph

@app.callback(Output("menciones_tweet", "figure"),
    [
         Input("USER_types" , "value") , Input("date_picker_select" , 'start_date') ,
        Input("date_picker_select" , 'end_date') ,
    ] , [State("wordcloud" , "relayoutData")]
    # [State("lock_selector", "value"), State("wordcloud", "relayoutData")],
)
def make_menciones_tweet_figure(USER_types,start_date , end_date, wordcloud):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date )

    dias = end_date - start_date

    if dias < datetime.timedelta(days=31):
        rest = datetime.timedelta(days=31) - dias
        start_date = start_date - rest

    df_stars = df_g_menciones
    # df_stars = df_stars.loc[df['username'].isin(USER_types)]
    df_stars = df_stars.loc[(df_stars['username'].isin(USER_types)) & (df_stars['created_at'] >= start_date) & (
            df_stars['created_at'] < end_date) ,]

    df_stars['count'] = 1
    df_stars = df_stars.groupby(['username' , pd.Grouper(key='created_at' , freq='W')])[['count']].sum().reset_index()

    fig = go.Figure()


    fig = px.line(df_stars , x='created_at' , y='count' , color='username' ,
                  labels={'created_at': 'Fecha', 'count': 'Nº tweets'} ,
                  hover_name='username',
                  hover_data={'count': ':,' , 'username': False ,'created_at': '|Semana %V del año %Y' ,
                              },
                  color_discrete_map={'@vodafone_es': '#E64A19',
                                      '@Lowi_es':   '#FF7043',   #'#FFAB91'
                                        '@vodafoneyu': '#212E36',
                                         '@movistar_es': '#2962FF',
                                         '@TuentiES' :'#82B1FF',
                                         '@o2es' : '#0D47A1',
                                         '@orange_es': '#F57C00',
                                         '@jazztel_es': '#FFE0B2',
                                         '@Amena' : '#FF9800',
                                         '@simyo_es': '#FFB74D',
                                         '@masmovil' : '#FFFF00',
                                         '@pepephone' : '#FFFF8D',
                                         '@yoigo' : '#FFF9C4',
                                        'Media Operadoras':'#EFF3F5'},
                  category_orders={ 'username': ['@vodafone_es' , '@Lowi_es' , '@movistar_es' , '@o2es' ,
                                   '@TuentiES' , '@orange_es' , '@Amena' , '@simyo_es' , '@jazztel_es' , '@masmovil' ,
                                   '@pepephone' , '@yoigo' ,
                                   '@vodafoneyu']})

    fig.update_traces(mode='lines+markers',line=dict( width=2))

    fig.update_layout(margin=dict(l=10 , r=20 , t=30 , b=10) ,title='Evolución Número de menciones Semanal',
                      xaxis=dict(title='',
                          #title='Porcentaje' ,#range=[0,100],
                          titlefont_size=16 ,
                          tickfont_size=12 , showticklabels=True ,
                          color='#C8CDD0' , showline=True , gridcolor='#8D8D8D' , linewidth=0.2 , linecolor='#8D8D8D' ,
                          zerolinecolor='#8D8D8D' ,showgrid=False ,
                          # zeroline=False,
                      ) ,
                      yaxis=dict(
                          titlefont_size=16 ,
                          tickfont_size=14 , showticklabels=True ,
                          # gridcolor='black',
                          color='#C8CDD0' ,
                          showgrid=False , gridcolor='#8D8D8D' , showline=True , linecolor='#8D8D8D' , linewidth=0.2 ,
                          zerolinecolor='#8D8D8D' ,title_text='Número de Menciones'
                      ) ,

                      legend=dict(
                          x=1 ,
                          y=1 ,font_color='#C8CDD0',
                          # bgcolor='rgba(255, 255, 255, 0)' ,
                          bgcolor='#212E36',
                          font_size=14, #bgcolor="#e5ecf6",
                          bordercolor="#192229",borderwidth=2, title_text='',
                      ) ,
                      barmode='relative' ,
                      bargap=0.20 ,  # gap between bars of adjacent location coordinates.
                      # bargroupgap=0.1,  # gap between bars of the same location coordinate.
                      autosize=True , showlegend=True , paper_bgcolor="#212E36" , title_font_color='#EFF3F5' ,
                      plot_bgcolor="#212E36",
                      hoverlabel=dict(

                          font_size=16 ,
                                 ),
                      )

    return fig








# Main
if __name__ == "__main__":
    app.run_server(debug=True)

    ########### debug FALSE
