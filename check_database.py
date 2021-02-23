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

    df_sqlite = pd.read_sql_query("SELECT * FROM twitter_operators", engine, coerce_float=True, parse_dates=['created_at'])

    print(df_sqlite)

    value = pd.DataFrame(df_sqlite['username'].value_counts())
    value['Percentage'] = value['username'] / value['username'].sum()
    value.style.format({'Percentage': '{:,.0%}'.format})
    print(f'\n\n{value}')

    value_group = pd.DataFrame(df_sqlite['GRUPO'].value_counts())
    value_group['Percentage'] = value_group['GRUPO'] / value_group['GRUPO'].sum()
    value_group.style.format({'Percentage': '{:,.0%}'.format})
    print(f'\n\n{value_group}\n\n')


    print(df_sqlite.info(memory_usage='deep'))

    yest = datetime.date.today() - datetime.timedelta(days=1)
    print(f'\n\nFinish Update Day: {yest}\n\n')

    print(df_sqlite[['created_at']].resample('D' , on='created_at').count())

