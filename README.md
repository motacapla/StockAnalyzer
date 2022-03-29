EDA, Backtest via kabu+ dataset

# How to download sample data
"サンプルファイル"
https://kabu.plus/membership

# How to run

## Place all files like the following directory structure
```
backtracer.ipynb
kabu_plus/
 |- japan-all-stock-data/                            # 07_投資指標データ
    |- daily/
       |- japan-all-stock-data_20210301.csv
       |- *.csv
       ...
 |- japan-all-stock-prices-2/                        # 02_株価一覧表（詳細フォーマット）
    |- daily/
       ...
 |- tosho-stock-ohlc/                                # 06_株価四本値データ（日通し・前場・後場）
    |- daily/
       ... 
 |- japan-all-stock-margin-transactions/             # 10_信用取引残高データ
    |- weekly/
       ... 
```

## Open .ipynb notebook
```
$ jupyter notebook 
```

