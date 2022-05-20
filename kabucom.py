import urllib.request
import json
import pprint
import secret

def get_host_url(prod_mode, suffix):
    if prod_mode:
        ip = 18080
    else:
        ip = 18081
    return 'http://localhost:'+str(ip)+'/kabusapi' + suffix


def get_api_token(api_pass, verbose=False, prod_mode=True):
    obj = {'APIPassword': api_pass}
    json_data = json.dumps(obj).encode('utf8')

    url = get_host_url(prod_mode, '/token')
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req) as res:
            if verbose:
                print(res.status, res.reason)
                for header in res.getheaders():
                    print(header)
                print()
            content = json.loads(res.read())
            return content['Token']
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:   
        raise(e)

"""
    Product
     - 0:すべて、1:現物、2:信用、3:先物、4:OP
    Side
     - '1':売、'2':買
    AddInfo
     - true:追加情報を出力する、false:追加情報を出力しない　※追加情報は、「現在値」、「評価金額」、「評価損益額」、「評価損益率」を意味します
"""
def get_positions(product:int, securities_code:str, side:str, addinfo='false', prod_mode=True):
    if prod_mode:
        api_pass = secret.API_PASS_PROD
    else:
        api_pass = secret.API_PASS_STG
    api_token = get_api_token(api_pass, prod_mode=prod_mode)

    url = get_host_url(prod_mode, '/positions')
    params = {'product': product }
    params['symbol'] = securities_code 
    params['side'] = str(side)
    params['addinfo'] = addinfo
    req = urllib.request.Request('{}?{}'.format(url, urllib.parse.urlencode(params)), method='GET')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', api_token)

    try:
        with urllib.request.urlopen(req) as res:
            content = json.loads(res.read())
            pprint.pprint(content)
            return content
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

"""
    Side
     - '1':売、'2':買
    CashMargin
     - 1:現物, 2:新規, 3:返済
    MarginTradeType
     - 1:制度信用, 2:一般信用（長期）, 3:一般信用（デイトレ）
    FrontOrderType
     - 10 成行 0
     - 13 寄成（前場）
     - 14 寄成（後場）0
     - 15 引成（前場）0
     - 16 引成（後場）0
     - 17 IOC成行 0
     - 20 指値 発注したい金額
     - 25 不成（前場）発注したい金額
     - 26 不成（後場）発注したい金額
     - 27 IOC指値 発注したい金額
     - 30 逆指値
    ExpireDay
     - yyyyMMdd形式。
     「0」を指定すると、kabuステーション上の発注画面の「本日」に対応する日付として扱います。
     「本日」は直近の注文可能日となり、以下のように設定されます。
      引けまでの間 : 当日
      引け後 : 翌取引所営業日
      休前日 : 休日明けの取引所営業日

    ReverseLimitOrder
    {
            'TriggerSec': 2, #1.発注銘柄 2.NK225指数 3.TOPIX指数
            'TriggerPrice': 30000,
            'UnderOver': 2, #1.以下 2.以上
            'AfterHitOrderType': 2, #1.成行 2.指値 3. 不成
            'AfterHitPrice': 8435
    }
"""
def post_order(securities_code, password, side:str, cash_margin:int, margin_trade_type:int, qty:int, front_order_type:int, price=0, expire_day=0, reverse_limit_order=None, prod_mode=True):
    if prod_mode:
        api_pass = secret.API_PASS_PROD
    else:
        api_pass = secret.API_PASS_STG
    api_token = get_api_token(api_pass, prod_mode=prod_mode)

    if cash_margin == 3:
        deliv_type = 2
        close_position_order = 0
    else:
        deliv_type = 0
        close_position_order = None

    obj = { 
        'Symbol': securities_code,
        'Password': password,
        'Exchange': 1, # 1:東証
        'SecurityType': 1,
        'Side': str(side),
        'CashMargin': cash_margin,
        'MarginTradeType': margin_trade_type,
        'DelivType': deliv_type,
        'AccountType': 4,
        'Qty': qty,
        'ClosePositionOrder': close_position_order,
        'FrontOrderType': front_order_type,
        'Price': price,
        'ExpireDay': expire_day,
        'ReverseLimitOrder': reverse_limit_order
    }
    json_data = json.dumps(obj).encode('utf-8')

    url = get_host_url(prod_mode, '/sendorder')
    req = urllib.request.Request(url, json_data, method='POST')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', api_token)

    print(req.headers, url, json_data)

    try:
        with urllib.request.urlopen(req) as res:
            content = json.loads(res.read())
            pprint.pprint(content)
            return content
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

"""

"""
def cancel_order(order_id, password, verbose=False, prod_mode=True):
    if prod_mode:
        api_pass = secret.API_PASS_PROD
    else:
        api_pass = secret.API_PASS_STG
    api_token = get_api_token(api_pass, prod_mode=prod_mode)
    
    obj = {'OrderID': order_id, 'Password': password}
    json_data = json.dumps(obj).encode('utf8')

    url = 'http://localhost:18080/kabusapi/cancelorder'
    req = urllib.request.Request(url, json_data, method='PUT')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', api_token)

    try:
        with urllib.request.urlopen(req) as res:
            if verbose:
                print(res.status, res.reason)
                for header in res.getheaders():
                    print(header)
                print()
        content = json.loads(res.read())
        return content
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)

def get_board(securities_code, verbose=False, prod_mode=True):
    if prod_mode:
        api_pass = secret.API_PASS_PROD
    else:
        api_pass = secret.API_PASS_STG
    api_token = get_api_token(api_pass, prod_mode=prod_mode)

    url = 'http://localhost:18080/kabusapi/board/'+str(securities_code)+'@1' # @1は東証
    req = urllib.request.Request(url, method='GET')
    req.add_header('Content-Type', 'application/json')
    req.add_header('X-API-KEY', api_token)

    try:
        with urllib.request.urlopen(req) as res:
            if verbose:
                print(res.status, res.reason)
                for header in res.getheaders():
                    print(header)
                print()
            content = json.loads(res.read())
            return content
    except urllib.error.HTTPError as e:
        print(e)
        content = json.loads(e.read())
        pprint.pprint(content)
    except Exception as e:
        print(e)