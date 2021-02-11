import pandas as pd



df=pd.read_parquet('./data/df.parquet')


########### controls

GRUPO=sorted(df['GRUPO'].unique().to_list())
GRUPO_dict = dict(zip(GRUPO, GRUPO))

USER=sorted(df['username'].unique().to_list())
USER_dict = dict(zip(USER, USER))


############## stars graph

df_f=df[['stars','username','created_at']]

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















