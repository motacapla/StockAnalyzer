import os

import pandas as pd
import config

side_dict = {
    '1': 'sell',
    '2': 'buy',
    'sell': '1',
    'buy': '2'    
}

front_order_type_dict = {
    'market': '10',
    'limit': '20',
    '10': 'market',
    '20': 'limit'    
}

"""
    板情報のdataframeを作る
    FIXME: 再実行すると元ファイルが何故か消える
"""
def get_data_or_empty_dataframe():
    # ディレクトリなければ作る
    try:
        os.makedirs(config.today_dir_path)
    except:
        pass
    
    # ファイルが存在してたら返す
    if os.path.exists(config.data_file_path):
        return pd.read_csv(config.data_file_path)
    else:
        return pd.DataFrame()

"""
    板情報のdataframeをcsvで保存する
"""

def save(df):
    # ディレクトリなければ作る
    try:
        os.makedirs(config.today_dir_path)
    except:
        pass
    
    # ファイル作成して書き込み
    df.drop_duplicates().to_csv(config.data_file_path, index=False)        

"""
    板情報取得APIのresponseからobjectに変換する
"""
def convert_to_df(res):
    columns = set(res)
    bs_1_columns = ['Buy1', 'Sell1']
    b_columns = ['Buy'+str(x) for x in range(2, 11)]
    s_columns = ['Sell'+str(x) for x in range(2, 11)]
    bs_larger_than_1_columns = b_columns + s_columns

    s = pd.Series([], dtype=pd.UInt64Dtype)
    for c in columns:
        if c in bs_1_columns:
            s[c+'Time']= res[c]['Time']
            s[c+'Sign']= res[c]['Sign']
            s[c+'Price']= res[c]['Price']
            s[c+'Qty']= res[c]['Qty']
        elif c in bs_larger_than_1_columns:
            s[c+'Price']= res[c]['Price']
            s[c+'Qty']= res[c]['Qty']
        else:
            s[c] = res[c]
    return pd.DataFrame(s).T

"""
    銘柄をqty株保有しているか確認する
"""
def has_positions(positions, securities_code, qty):
    for position in positions:
        if position['Symbol'] == securities_code and position['LeavesQty'] == qty:
            return True
    return False

"""
    約定価格を取得する
"""
def get_price_from_positions(positions, securities_code, qty):
    for position in positions:
        if position['Symbol'] == securities_code and position['LeavesQty'] == qty:
            return position['Price']
    return None