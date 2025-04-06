from .serializers import *
from django.db.models import Q
import datetime

def update_stock_data(stock_id):
    global status, action, stock_exchange, target_gain_loss, gain_loss 
    target_price = 0.0
    time_left = 0.0
    gain_loss = 0.0
    stock = Stock.objects.get(id=stock_id)
    stock_targets = StockTarget.objects.filter(stock=stock).order_by('created')
    shares = stock.no_of_shares
    live_price = stock.live_price
    
    print('Stock : ', stock)
    # print('ALL Targets : ', stock_targets)

    if len(stock_targets) == 0:
        target_price = stock.target_price
        # print('target price', stock.target_price)
        if live_price is not None and stock.entry_price is not None:
            gain_loss = round((((live_price - stock.entry_price) / stock.entry_price) * 100), 2)
        time_left = (stock.end_date - datetime.date.today()).days
        
        
    if len(stock_targets) >= 1:
        for target in stock_targets:
            # print('Target : ', target, target.entry_price, target.gain_loss)
            target = stock_targets[0]
            target_price = target.target_price
            """ last hold price that is present in StockTarget instance """
            if live_price is not None and target.entry_price is not None:
                target_gain_loss = round((((live_price - target.entry_price) / target.entry_price) * 100), 2)
                time_left = (target.target_date - datetime.date.today()).days
                stock.end_date = target.target_date
                stock.save()
                target.gain_loss = target_gain_loss
                target.save()
                # print('Target Updated : ', target, target.entry_price, target.gain_loss)
                
    '''Calculating Upside Potential, Upside Left, Expected Returns, MCAP and Time Left'''
    
    # print('target_price', target_price, type(target_price))
    # print('live_price', live_price, type(live_price))
    if live_price is not None and target_price is not None:
        upside_left = round(abs(((target_price - live_price) / live_price) * 100), 2)
        expected_returns = round(abs(((target_price - target.entry_price) / target.entry_price) * 100), 2)
    else:
        upside_left = 0.0
        expected_returns = 0.0
    market_cap = round((shares * live_price) / 10000000, 2)
    print('Upside Left : ', upside_left)
    
    
    if time_left < 0:
        time_left = 0

    # print(time_left, upside_left, gain_loss, status, stock.action, market_cap)

    
    Stock.objects.filter(id=stock_id) \
        .update(upside_left=upside_left,
                expected_returns=expected_returns,
                # gain_loss=gain_loss,
                time_left=time_left,
                market_cap=market_cap
                )

