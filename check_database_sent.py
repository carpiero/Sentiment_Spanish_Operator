if __name__ == "__main__":
    import pandas as pd
    from sqlalchemy import create_engine
    import configparser
    import datetime

    cfg = configparser.RawConfigParser()
    cfg.read('/home/carpiero/ir/pass_projects/pass.ini')

    user = cfg['ssh']['username']
    passw = cfg['ssh']['password']
    engine = create_engine(f'postgresql://{user}:{passw}@localhost/carpiero' , echo=True)
    sqlite_connection = engine.connect()

    df_postgresql = pd.read_sql_query("SELECT * FROM twitter_operators_sent_02", engine, coerce_float=True, parse_dates=['created_at'])

    print(df_postgresql)

    value = pd.DataFrame(df_postgresql['username'].value_counts())
    value['Percentage'] = value['username'] / value['username'].sum()
    value.style.format({'Percentage': '{:,.0%}'.format})
    print(f'\n\n{value}')

    value_group = pd.DataFrame(df_postgresql['GRUPO'].value_counts())
    value_group['Percentage'] = value_group['GRUPO'] / value_group['GRUPO'].sum()
    value_group.style.format({'Percentage': '{:,.0%}'.format})
    print(f'\n\n{value_group}\n\n')


    print(df_postgresql.info(memory_usage='deep'))

    yest = datetime.date.today() - datetime.timedelta(days=1)
    print(f'\n\nFinish Update Day: {yest}\n\n')

    print(df_postgresql[['created_at']].resample('D' , on='created_at').count())

    stars=df_postgresql.pivot_table(index=['username'], values=['stars']).sort_values(by='stars', ascending=False)
    print(f'\n\n{stars}')

    df_postgresql['Year'] = pd.DatetimeIndex(df_postgresql['created_at']).year
    df_postgresql['Month'] = pd.DatetimeIndex(df_postgresql['created_at']).month
    df_postgresql['Day'] = pd.DatetimeIndex(df_postgresql['created_at']).day

    stars2=df_postgresql.pivot_table(index=['username'] , columns=['Year','Month' , 'Day'] , values=['stars']).iloc[: , -1:]

    print(f'\n\n{stars2}\n\n')

    today = datetime.date.today()
    yest = today - datetime.timedelta(days=1)

    today2 = pd.to_datetime(today)
    yest2 = pd.to_datetime(yest)

    start_date = yest2
    end_date = today2

    df = df_postgresql.loc[(df_postgresql['created_at'] >= start_date) & (df_postgresql['created_at'] < end_date)]

    print(df['username'].value_counts())


