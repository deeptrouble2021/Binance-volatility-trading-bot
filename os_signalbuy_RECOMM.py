# Based off Firewatch custsignalmod.py

from tradingview_ta import TA_Handler, Interval, Exchange
# use for environment variables
import os
# use if needed to pass args to external modules
import sys
# used for directory handling
import glob

import time

MY_EXCHANGE = 'BINANCE'
MY_SCREENER = 'CRYPTO'
MY_FIRST_INTERVAL = Interval.INTERVAL_1_MINUTE
MY_SECOND_INTERVAL = Interval.INTERVAL_5_MINUTES
MY_THIRD_INTERVAL = Interval.INTERVAL_15_MINUTES
PAIR_WITH = 'USDT'

TIME_TO_WAIT = 1 # Minutes to wait between analysis
FULL_LOG = True # List anylysis result to console
SIGNAL_NAME = 'os_signalbuy_RECOMM'
SIGNAL_FILE = 'signals/' + SIGNAL_NAME + '.buy'
TICKERS = 'tickers.txt'

def analyze(pairs):
    taMax = 0
    taMaxCoin = 'none'
    signal_coins = {}
    first_analysis = {}
    second_analysis = {}
    third_analysis = {}
    first_handler = {}
    second_handler = {}
    third_handler = {}
    
    if os.path.exists(SIGNAL_FILE):
        os.remove(SIGNAL_FILE)

    for pair in pairs:
        first_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_FIRST_INTERVAL,
            timeout= 10
        )
        second_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_SECOND_INTERVAL,
            timeout= 10
        )
        third_handler[pair] = TA_Handler(
            symbol=pair,
            exchange=MY_EXCHANGE,
            screener=MY_SCREENER,
            interval=MY_THIRD_INTERVAL,
            timeout= 10
        )

    for pair in pairs:
       
        try:
            first_analysis = first_handler[pair].get_analysis()
            second_analysis = second_handler[pair].get_analysis()
            third_analysis = third_handler[pair].get_analysis()
        except Exception as e:
            print(f'{SIGNAL_NAME}')
            print("Exception:")
            print(e)
            print (f'Coin: {pair}')
            print (f'First handler: {first_handler[pair]}')
            print (f'Second handler: {second_handler[pair]}')
            print (f'Second handler: {third_handler[pair]}')
            return
               
        first_recommendation = first_analysis.summary['RECOMMENDATION']
        second_recommendation = second_analysis.summary['RECOMMENDATION']
        third_recommendation = third_analysis.summary['RECOMMENDATION']
        
        if FULL_LOG:
            print(f'{SIGNAL_NAME}: {pair} First {first_recommendation} Second {second_recommendation} Third {third_recommendation}')
                
        if  (first_recommendation == "BUY" or first_recommendation == "STRONG_BUY") and \
            (second_recommendation == "BUY" or second_recommendation == "STRONG_BUY") and \
            (third_recommendation == "BUY" or third_recommendation == "STRONG_BUY"):
            print(f'{SIGNAL_NAME}: buy signal detected on {pair}')

            signal_coins[pair] = pair
            
            with open(SIGNAL_FILE,'a+') as f:
                f.write(pair + '\n')

    return signal_coins

def do_work():
    try:
        signal_coins = {}
        pairs = {}

        pairs=[line.strip() for line in open(TICKERS)]
        for line in open(TICKERS):
            pairs=[line.strip() + PAIR_WITH for line in open(TICKERS)] 
        
        while True:
            print(f'{SIGNAL_NAME}: Analyzing {len(pairs)} coins')
            signal_coins = analyze(pairs)
            if len(signal_coins) == 0:
                print(f'{SIGNAL_NAME}: No coins above buy threshold on three timeframes. Waiting {TIME_TO_WAIT} minutes for next analysis')
            else:
                print(f'{SIGNAL_NAME}: {len(signal_coins)} coins above buy treshold on three timeframes. Waiting {TIME_TO_WAIT} minutes for next analysis')

            time.sleep((TIME_TO_WAIT*60))
    except Exception as e:
            print(f'{SIGNAL_NAME}: Exception: {e}')