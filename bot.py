import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from binance.client import Client
import talib as ta
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import sys
import math
import json


liste = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT','NEOUSDT', 'LTCUSDT', 'QTUMUSDT', 'ADAUSDT', 'XRPUSDT', 'EOSUSDT', 'IOTAUSDT', 'XLMUSDT', 'ONTUSDT', 'TRXUSDT', 'ETCUSDT', 'ICXUSDT', 'NULSUSDT', 'VETUSDT', 'PAXUSDT', 'LINKUSDT', 'WAVESUSDT', 'BTTUSDT', 'ONGUSDT', 'HOTUSDT', 'ZILUSDT', 'ZRXUSDT', 'FETUSDT', 'BATUSDT', 'XMRUSDT', 'ZECUSDT', 'IOSTUSDT', 'CELRUSDT', 'DASHUSDT', 'NANOUSDT', 'OMGUSDT', 'THETAUSDT', 'ENJUSDT', 'MITHUSDT', 'MATICUSDT', 'ATOMUSDT', 'TFUELUSDT', 'ONEUSDT', 'FTMUSDT', 'ALGOUSDT', 'GTOUSDT', 'DOGEUSDT', 'DUSKUSDT', 'ANKRUSDT', 'WINUSDT', 'COSUSDT', 'COCOSUSDT', 'MTLUSDT', 'TOMOUSDT', 'PERLUSDT', 'DENTUSDT', 'MFTUSDT', 'KEYUSDT', 'DOCKUSDT', 'WANUSDT', 'FUNUSDT', 'CVCUSDT', 'CHZUSDT', 'BANDUSDT', 'BEAMUSDT', 'XTZUSDT', 'RENUSDT', 'RVNUSDT', 'HBARUSDT', 'NKNUSDT', 'STXUSDT', 'KAVAUSDT', 'ARPAUSDT', 'IOTXUSDT', 'RLCUSDT', 'CTXCUSDT', 'BCHUSDT', 'TROYUSDT', 'VITEUSDT', 'FTTUSDT','OGNUSDT', 'DREPUSDT', 'TCTUSDT', 'WRXUSDT', 'BTSUSDT', 'LSKUSDT', 'BNTUSDT', 'LTOUSDT', 'AIONUSDT', 'MBLUSDT', 'COTIUSDT','STPTUSDT', 'WTCUSDT', 'DATAUSDT','SOLUSDT', 'CTSIUSDT', 'HIVEUSDT', 'CHRUSDT', 'GXSUSDT', 'ARDRUSDT', 'MDTUSDT', 'STMXUSDT', 'KNCUSDT', 'REPUSDT', 'LRCUSDT', 'PNTUSDT', 'COMPUSDT', 'SCUSDT', 'ZENUSDT', 'SNXUSDT', 'VTHOUSDT', 'DGBUSDT', 'GBPUSDT', 'SXPUSDT', 'MKRUSDT','DCRUSDT', 'STORJUSDT', 'MANAUSDT', 'AUDUSDT', 'YFIUSDT', 'BALUSDT', 'BLZUSDT', 'IRISUSDT', 'KMDUSDT', 'JSTUSDT', 'SRMUSDT', 'ANTUSDT', 'CRVUSDT', 'SANDUSDT', 'OCEANUSDT', 'NMRUSDT', 'DOTUSDT', 'LUNAUSDT', 'RSRUSDT', 'PAXGUSDT', 'WNXMUSDT', 'TRBUSDT', 'BZRXUSDT', 'SUSHIUSDT', 'YFIIUSDT', 'KSMUSDT', 'EGLDUSDT', 'DIAUSDT', 'RUNEUSDT', 'FIOUSDT', 'UMAUSDT','BELUSDT', 'WINGUSDT', 'UNIUSDT', 'NBSUSDT', 'OXTUSDT', 'SUNUSDT', 'AVAXUSDT', 'HNTUSDT', 'FLMUSDT', 'ORNUSDT', 'UTKUSDT', 'XVSUSDT', 'ALPHAUSDT', 'AAVEUSDT', 'NEARUSDT', 'FILUSDT', 'INJUSDT', 'AUDIOUSDT', 'CTKUSDT', 'AKROUSDT', 'AXSUSDT', 'HARDUSDT', 'DNTUSDT', 'STRAXUSDT', 'UNFIUSDT', 'ROSEUSDT', 'AVAUSDT', 'XEMUSDT', 'SKLUSDT', 'SUSDUSDT', 'GRTUSDT', 'JUVUSDT', 'PSGUSDT', '1INCHUSDT', 'REEFUSDT', 'OGUSDT', 'ATMUSDT', 'ASRUSDT', 'CELOUSDT', 'RIFUSDT', 'BTCSTUSDT', 'TRUUSDT', 'CKBUSDT', 'TWTUSDT', 'FIROUSDT', 'LITUSDT', 'SFPUSDT', 'DODOUSDT', 'CAKEUSDT', 'ACMUSDT', 'BADGERUSDT', 'FISUSDT', 'OMUSDT', 'PONDUSDT', 'DEGOUSDT', 'ALICEUSDT', 'LINAUSDT', 'PERPUSDT', 'RAMPUSDT', 'SUPERUSDT', 'CFXUSDT']
liste_json=[]



class BinanceConnection:
    def __init__(self, file):
        self.connect(file)

    """ Creates Binance client """

    def connect(self, file):
        lines = [line.rstrip('\n') for line in open(file)]
        key = lines[0]
        secret = lines[1]
        self.client = Client(key, secret)


def generateStochasticRSI(close_array, timeperiod):
    # 1) ilk aşama rsi değerini hesaplıyoruz.
    rsi = ta.RSI(close_array, timeperiod=timeperiod)

    # 2) ikinci aşamada rsi arrayinden sıfırları kaldırıyoruz.
    rsi = rsi[~np.isnan(rsi)]

    # 3) üçüncü aşamada ise ta-lib stoch metodunu uyguluyoruz.
    stochrsif, stochrsis = ta.STOCH(rsi, rsi, rsi, fastk_period=13, slowk_period=6, slowd_period=3)

    return stochrsif, stochrsis

#Grafik oluşturmak için
def generateStochRSITable(pair,new_time,stochasticRsiF,stochasticRsiS):
    plt.figure(figsize=(11, 6))
    plt.plot(new_time[116:], stochasticRsiF[100:], label='StochRSI fast')
    plt.plot(new_time[116:], stochasticRsiS[100:], label='StochRSI slow')
    plt.xticks(rotation=90, fontsize=5)
    plt.title(f"Stochastic RSI - {pair} - (4h)")
    plt.xlabel("Open Time")
    plt.ylabel("Value")
    plt.legend()
    plt.show()

def generateSupertrend(close_array, high_array, low_array, atr_period, atr_multiplier):

    try:
        atr = ta.ATR(high_array, low_array, close_array, atr_period)
    except:
        print('exception in atr:', sys.exc_info()[0], 'pair', pair, flush=True)
        print('filename', filename, flush=True)
        return False, False

    previous_final_upperband = 0
    previous_final_lowerband = 0
    final_upperband = 0
    final_lowerband = 0
    previous_close = 0
    previous_supertrend = 0
    supertrend = []
    supertrendc = 0

    for i in range(0, len(close_array)):
        if np.isnan(close_array[i]):
            pass
        else:
            highc = high_array[i]
            lowc = low_array[i]
            atrc = atr[i]
            closec = close_array[i]

            if math.isnan(atrc):
                atrc = 0

            basic_upperband = (highc + lowc) / 2 + atr_multiplier * atrc
            basic_lowerband = (highc + lowc) / 2 - atr_multiplier * atrc

            if basic_upperband < previous_final_upperband or previous_close > previous_final_upperband:
                final_upperband = basic_upperband
            else:
                final_upperband = previous_final_upperband

            if basic_lowerband > previous_final_lowerband or previous_close < previous_final_lowerband:
                final_lowerband = basic_lowerband
            else:
                final_lowerband = previous_final_lowerband

            if previous_supertrend == previous_final_upperband and closec <= final_upperband:
                supertrendc = final_upperband
            else:
                if previous_supertrend == previous_final_upperband and closec >= final_upperband:
                    supertrendc = final_lowerband
                else:
                    if previous_supertrend == previous_final_lowerband and closec >= final_lowerband:
                        supertrendc = final_lowerband
                    elif previous_supertrend == previous_final_lowerband and closec <= final_lowerband:
                        supertrendc = final_upperband

            supertrend.append(supertrendc)

            previous_close = closec

            previous_final_upperband = final_upperband

            previous_final_lowerband = final_lowerband

            previous_supertrend = supertrendc

    return supertrend

if __name__ == '__main__':
    filename = 'credentials.txt'

    connection = BinanceConnection(filename)
    f = open("test.json",)
    liste_json = json.load(f)
    print(len(liste_json))

    while 1:
        try:
            for i in range(len(liste)):

                pair = liste[i]
                klines = connection.client.get_historical_klines(pair, Client.KLINE_INTERVAL_2HOUR,"124 hours ago UTC","now UTC")

                open_time = []
                high = []
                low = []
                close = []

                for k in range(len(klines)):
                    open_time.append(float(klines[k][0]))
                    high.append(float(klines[k][2]))
                    low.append(float(klines[k][3]))
                    close.append(float(klines[k][4]))

                close_array = np.asarray(close) 
                high_array = np.asarray(high)   
                low_array = np.asarray(low) 
                new_time = [datetime.fromtimestamp(time / 1000) for time in open_time]  
                new_time_x = [date.strftime("%d-%m-%y") for date in new_time]

                stochasticRsiF, stochasticRsiS = generateStochasticRSI(close_array, timeperiod=16)  
                supertrend = generateSupertrend(close_array, high_array, low_array, atr_period=10, atr_multiplier=3)  
                

                if (liste_json[i]['signalSend'] == False):

                    print("4 saatlik deneme")
                    print(pair)
                    print("F: ",stochasticRsiF[-1], new_time[-1])
                    print("S: ",stochasticRsiS[-1], new_time[-1])

                    if(close_array[-1]>supertrend[-1]):
                        print("SuperTrend var")
                        if (stochasticRsiF[-2]<=stochasticRsiS[-2]) and (stochasticRsiF[-1]>stochasticRsiS[-1]) and min(stochasticRsiF[-1],stochasticRsiS[-1])<25:
                            print("Super Trend Var - StochasticRSI var  - Value: ", pair ,stochasticRsiS[-1],new_time[-1],datetime.now().strftime("%H:%M:%S")) 
                            msg = str("Super Trend var - StochasticRSI var  - Birim: {} {}USDT ".format(pair,close_array[-1]))
                            liste_json[i].update({"name":pair,"price":close_array[-1],"supertrend":True,"stochrsi":True,"signalSend":True})
                            bot = telegram.Bot(token='TelegramToken')
                            bot.send_message(chat_id="TelegramChatID",text=msg) 
                        else:
                            liste_json[i].update({"name":pair,"price":close_array[-1],"supertrend":True,"stochrsi":False,"signalSend":False})
                    else:
                        print("SuperTrend yok")
                        liste_json[i].update({"name":pair,"price":close_array[-1],"supertrend":False,"stochrsi":False,"signalSend":False})
                else:
                    print("4 saatlik deneme")
                    print(pair)
                    print("F: ",stochasticRsiF[-1], new_time[-1])
                    print("S: ",stochasticRsiS[-1], new_time[-1])

                    if stochasticRsiF[-1]>30 and stochasticRsiS[-1] > 30:
                        print("StochasticRSI 30 üstünde")
                        liste_json[i].update({"name":pair,"price":close_array[-1],"supertrend":False,"stochrsi":False,"signalSend":False})



                print("-----------------------------------------------\n")    

        except:
            continue
        
        json1 = json.dumps(liste_json,ensure_ascii=False)
        with open("test.json","w",encoding="utf8") as f:
            f.write(json1)
               
               
        
        #generateStochRSITable(new_time,stochasticRsiF,stochasticRsiS)
 
    



    





