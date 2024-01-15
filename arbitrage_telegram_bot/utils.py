name2url = {
    'bybit': 'https://www.bybit.com/ru-RU/trade/spot',
    'mexc':  'https://www.mexc.com/ru-RU/exchange',
    'bitget': 'https://www.bitget.com/ru/spot',
    'bingx': 'https://bingx.com/ru-ru/spot',
    "binance": "https://www.binance.com/en/trade",
    'lbank': "https://www.lbank.com/trade"
}

name2symbol = {
    'bybit': lambda t1, t2: f'{t1}/{t2}',       
    'mexc':  lambda t1, t2: f'{t1}_{t2}',
    'bitget': lambda t1, t2: f'{t1}{t2}',
    'bingx': lambda t1, t2: f'{t1}{t2}',
    "binance": lambda t1, t2: f'{t1}_{t2}',
    "lbank": lambda t1, t2: f'{t1}_{t2}'
}

def get_url(cex_name, t1, t2):
    return f'{name2url[cex_name.lower()]}/{name2symbol[cex_name.lower()](t1, t2)}'


def format_opportunity(opportunity) -> str:
    currency = opportunity.symbols.split('/')[1]
    link1 = get_url(opportunity.cex_ask, opportunity.symbols.split('/')[0], currency)
    link2 = get_url(opportunity.cex_bid, opportunity.symbols.split('/')[0], currency)
    main_coin = opportunity.symbols.split('/')[0]

    min_liquidity = min(float(opportunity.bid_liquidity), float(opportunity.ask_liquidity))

    withdraw_fee = float(opportunity.withdraw_fee) * float(opportunity.ask_price)

    trading_fee = float(opportunity.ask_trade_fee) + float(opportunity.bid_trade_fee)
    ask_price = round(float(opportunity.ask_price), 10)
    bid_price = round(float(opportunity.bid_price), 10)
    ask_price_2 = round(float(opportunity.ask_price_2), 10)
    bid_price_2 = round(float(opportunity.bid_price_2), 10)

    ask_price_row = f"""<b>Цена:</b> {ask_price} - {ask_price_2} {currency}""" if ask_price != ask_price_2 else f"""<b>Цена:</b> {ask_price} {currency}"""
    bid_price_row = f"""<b>Цена:</b> {bid_price} - {bid_price_2} {currency}""" if bid_price != bid_price_2 else f"""<b>Цена:</b> {bid_price} {currency}"""
    spread_row = f"""💫 <b>Спред:</b> {round(min(float(opportunity.spread), float(opportunity.spread_2))*100, 2)}%""" 
    withdraw_fee_row = f"""<b>Минимальная комиссия за вывод:</b> {opportunity.withdraw_fee} {main_coin} ~ {round(withdraw_fee, 6)} {currency}""" if opportunity.withdraw_fee != 'inf' else "Данные о коммиссии за вывод отсутсвуют\n"

    res = f"""
<i>{opportunity.symbols}</i>
<a href='{link1}'>{opportunity.cex_ask}</a> -> <a href='{link2}'>{opportunity.cex_bid}</a>

📈 {opportunity.cex_ask}
{ask_price_row}
<b>Объём:</b> {round(float(opportunity.ask_liquidity), 2)} {currency}

📉 {opportunity.cex_bid}
{bid_price_row}
<b>Объём:</b> {round(float(opportunity.bid_liquidity), 2)} {currency}

{spread_row}

<b>Доступные сети:</b> {', '.join(opportunity.chains)}
{withdraw_fee_row}
<b>Комиссия за торговлю:</b> {trading_fee}%
"""
    
    if opportunity.cex_bid.lower() == 'lbank':
        res = res + "\n<i>Осторожно: </i>отсутсвуют данные о возможности депозита в LBank"
    return res 