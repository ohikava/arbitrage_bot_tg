name2url = {
    'bybit': 'https://www.bybit.com/ru-RU/trade/spot',
    'mexc':  'https://www.mexc.com/ru-RU/exchange',
    'bitget': 'https://www.bitget.com/ru/spot',
    'bingx': 'https://bingx.com/ru-ru/spot',
}

name2symbol = {
    'bybit': lambda t1, t2: f'{t1}/{t2}',       
    'mexc':  lambda t1, t2: f'{t1}_{t2}',
    'bitget': lambda t1, t2: f'{t1}{t2}',
    'bingx': lambda t1, t2: f'{t1}{t2}'
}

def get_url(cex_name, t1, t2):
    return f'{name2url[cex_name.lower()]}/{name2symbol[cex_name.lower()](t1, t2)}'


def format_opportunity(opportunity) -> str:
    currency = opportunity.symbol.split('/')[1]
    link1 = get_url(opportunity.cex_ask, opportunity.symbol.split('/')[0], currency)
    link2 = get_url(opportunity.cex_bid, opportunity.symbol.split('/')[0], currency)

    min_liquidity = min(float(opportunity.bid_liquidity), float(opportunity.ask_liquidity))

    res = f"""
<i>{opportunity.symbol}</i>
<a href='{link1}'>{opportunity.cex_ask}</a> -> <a href='{link2}'>{opportunity.cex_bid}</a>

📈 {opportunity.cex_ask}
<b>Цена:</b> {round(float(opportunity.ask_price), 7)} {currency}
<b>Объём:</b> {round(float(opportunity.ask_liquidity), 2)} ~ {round(float(opportunity.ask_price) * float(opportunity.ask_liquidity), 2)} {currency}

📉 {opportunity.cex_bid}
<b>Цена:</b> {round(float(opportunity.bid_price), 7)} {currency}
<b>Объём:</b> {round(float(opportunity.bid_liquidity), 2)} ~ {round(float(opportunity.bid_price) * float(opportunity.bid_liquidity), 2)} {currency}

<b>Спред:</b> {round(float(opportunity.spread)*100, 2)}% ~ {round(min_liquidity * (float(opportunity.bid_price) - float(opportunity.ask_price)), 2)} {currency}
"""
    return res 