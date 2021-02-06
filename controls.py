import pandas as pd



df=pd.read_parquet('./data/df.parquet')


########### controls

GRUPO=sorted(df['GRUPO'].unique().to_list())
GRUPO_dict = dict(zip(GRUPO, GRUPO))

USER=sorted(df['username'].unique().to_list())
USER_dict = dict(zip(USER, USER))














