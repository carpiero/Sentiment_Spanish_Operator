import pandas as pd



df=pd.read_parquet('./data/df_total.parquet')
#df= pd.read_parquet('./data/df.parquet')
df= df.loc[df['username']!='@vodafoneyu']


########### controls

GRUPO=sorted(df['GRUPO'].unique().to_list())
GRUPO_dict = dict(zip(GRUPO, GRUPO))

USER=sorted(df['username'].unique().to_list())
USER_dict = dict(zip(USER, USER))

################# wordcloud
df_word=df[['username','created_at','Tweet_Content_Token']]


############## stars graph

df_f=df[['stars','username','created_at','GRUPO','source']]

df_f['orden'] = ''

df_f.loc[df_f['username'] == '@vodafone_es' , 'orden'] = 11
df_f.loc[df_f['username'] == '@Lowi_es' , 'orden'] = 13
df_f.loc[df_f['username'] == '@vodafoneyu' , 'orden'] = 12
df_f.loc[df_f['username'] == '@movistar_es' , 'orden'] = 4
df_f.loc[df_f['username'] == '@TuentiES' , 'orden'] = 6
df_f.loc[df_f['username'] == '@o2es' , 'orden'] = 5
df_f.loc[df_f['username'] == '@orange_es' , 'orden'] = 7
df_f.loc[df_f['username'] == '@jazztel_es' , 'orden'] = 10
df_f.loc[df_f['username'] == '@Amena' , 'orden'] = 9
df_f.loc[df_f['username'] == '@simyo_es' , 'orden'] = 8
df_f.loc[df_f['username'] == '@masmovil' , 'orden'] = 1
df_f.loc[df_f['username'] == '@pepephone' , 'orden'] = 2
df_f.loc[df_f['username'] == '@yoigo' , 'orden'] = 3

df_f['color'] = ''

df_f.loc[df_f['username'] == '@vodafone_es' , 'color'] = '#E64A19'
df_f.loc[df_f['username'] == '@Lowi_es' , 'color'] =   '#FF7043'   #'#FFAB91'
df_f.loc[df_f['username'] == '@vodafoneyu' , 'color'] = '#FF7043'
df_f.loc[df_f['username'] == '@movistar_es' , 'color'] = '#2962FF'
df_f.loc[df_f['username'] == '@TuentiES' , 'color'] = '#82B1FF'
df_f.loc[df_f['username'] == '@o2es' , 'color'] = '#0D47A1'
df_f.loc[df_f['username'] == '@orange_es' , 'color'] = '#F57C00'
df_f.loc[df_f['username'] == '@jazztel_es' , 'color'] = '#FFE0B2'
df_f.loc[df_f['username'] == '@Amena' , 'color'] = '#FF9800'
df_f.loc[df_f['username'] == '@simyo_es' , 'color'] = '#FFB74D'
df_f.loc[df_f['username'] == '@masmovil' , 'color'] = '#FFFF00'
df_f.loc[df_f['username'] == '@pepephone' , 'color'] = '#FFFF8D'
df_f.loc[df_f['username'] == '@yoigo' , 'color'] = '#FFF9C4'


df_g_stars=df_f[['stars','username','created_at','orden','color']]

df_g_sunburst=df_f[['stars','username','created_at','GRUPO']]

df_g_source=df_f[['username','created_at','source']]

df_g_time=df_f[['stars','username','created_at']]

df_g_menciones=df_f[['username','created_at']]









