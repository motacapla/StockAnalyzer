import pandas as pd
from sqlalchemy import create_engine

""" 
mysql version 8

CREATE TABLE board (
    id BIGINT NOT NULL AUTO_INCREMENT, 
    Sell1Time DATETIME,
    Sell1Price FLOAT,
    Sell1Qty BIGINT,    
    Buy1Time DATETIME,
    Buy1Price FLOAT,
    Buy1Qty BIGINT,
    TotalMarketValue FLOAT,
    Symbol BIGINT,
    SymbolName CHAR(50),
    CalcPrice FLOAT,
    CurrentPriceChangeStatus CHAR(50),
    ChangePreviousClosePer FLOAT,
    ChangePreviousClose FLOAT,
    CurrentPriceStatus CHAR(50),
    TradingValue FLOAT,
    VWAP FLOAT,
    CurrentPrice FLOAT,
    CurrentPriceTime DATETIME,
    SecurityType CHAR(50),
    PRIMARY KEY (id)
);
"""

user = 'root'
passwd = 'meumeu'
host = 'localhost'
db = 'stock'

engine = create_engine('mysql://'+user+':'+passwd+'@'+host+'/'+db+'?charset=utf8')

columns = [
    'Sell1Time',
    'Sell1Price',
    'Sell1Qty',
    'Buy1Time',
    'Buy1Price',
    'Buy1Qty',
    'TotalMarketValue',
    'Symbol',
    'SymbolName',
    'CalcPrice',
    'CurrentPriceChangeStatus',
    'ChangePreviousClosePer',
    'ChangePreviousClose',
    'CurrentPriceStatus',
    'TradingValue',
    'VWAP',
    'CurrentPrice',
    'CurrentPriceTime',
    'SecurityType'
]

def insert(df):
    df[columns].to_sql('board', con=engine, if_exists='append', index=False)

def select():
    return pd.read_sql_query(sql="SELECT * from board", con=engine).set_index(keys='id')
