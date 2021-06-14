# -*- coding: utf-8 -*-

import pygame, requests
import pygame.image
import json
import os
import io
import math
from time import sleep
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
import datetime 

# function to map a range value to another range
def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

# function to shorten a number with a word
millnames = ['',' K',' M',' B',' T']
def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.3f}{}'.format(n / 10**(3 * millidx), millnames[millidx])    

class Crypto_coin:
        
    def __init__(self, symbol='SAFEMOON', coins_held=0, purchase_value=0, api_currency_type='GBP'):
        self.symbol = symbol
        self.coins_held = coins_held
        self.purchase_value = purchase_value
        self.api_currency_type = api_currency_type
        #self.api_currency_type_symbol = CurrencySymbols.get_symbol(api_currency_type)
        self.name = None # name of the coin
        self.logo_url = None # stores the logo url
        self.logo_img = None # stores the download logo image
        self.api_data = None # stores the response of api about current price data
        self.api_info_data = None # place to store the infor api - dtails about the coin, updated on a less frequent basis than the price detail
        self.market_cap = None # market cap of the coin
        self.percent_change_1h = None
        self.percent_change_24h = None
        self.percent_change_7d = None
        self.percent_change_30d = None
        self.percent_change_60d = None
        self.percent_change_90d = None
        self.circulating_supply = None
        self.cmc_rank = None
        self.old_price_value = None
        self.current_value = None 
        self.current_value_str = None # string version of the current value
        self.current_total_value = 0.0 
        self.current_total_value_str = None # string version of the current total value
        self.volume_24h = None 
        self.volume_24h_str = None # string version of the current volume
        
    def api_updated(self, new_api_data):
        self.api_data = new_api_data
        print("Api quote dump:")
        print(json.dumps(self.api_data.data))
        self.market_cap = json.dumps(self.api_data.data[self.symbol]["quote"][self.api_currency_type]["market_cap"])
        self.percent_change_1h = float(json.dumps(self.api_data.data[self.symbol]["quote"][self.api_currency_type]["percent_change_1h"]))
        self.percent_change_24h = float(json.dumps(self.api_data.data[self.symbol]["quote"][self.api_currency_type]["percent_change_24h"]))
        self.percent_change_7d = float(json.dumps(self.api_data.data[self.symbol]["quote"][self.api_currency_type]["percent_change_7d"]))
        self.percent_change_30d = float(json.dumps(self.api_data.data[self.symbol]["quote"][self.api_currency_type]["percent_change_30d"]))
        self.percent_change_60d = float(json.dumps(self.api_data.data[self.symbol]["quote"][self.api_currency_type]["percent_change_60d"]))
        self.percent_change_90d = float(json.dumps(self.api_data.data[self.symbol]["quote"][self.api_currency_type]["percent_change_90d"]))
        self.circulating_supply = json.dumps(self.api_data.data[self.symbol]["circulating_supply"])
        #self.icon = None
        self.name = json.dumps(self.api_data.data[self.symbol]["name"])
        self.cmc_rank = json.dumps(self.api_data.data[self.symbol]["cmc_rank"])
        self.old_price_value = self.current_value
        self.current_value = ("{:.12f}".format(float(json.dumps(self.api_data.data[self.symbol]["quote"][self.api_currency_type]["price"]))))
        self.current_value_str = str(self.current_value)
        self.current_total_value = ("{:.2f}".format(my_safe_moon * float(json.dumps(self.api_data.data[self.symbol]["quote"][self.api_currency_type]["price"]))))
        self.current_total_value_str = str(self.current_total_value)
        self.volume_24h = float(json.dumps(self.api_data.data[self.symbol]["quote"][self.api_currency_type]["volume_24h"]))
        self.volume_24h_str = "24h vol: " + str(millify(self.volume_24h))   

    def info_updated(self, new_info_api_data):
        self.api_info_data = new_info_api_data
        print("Api info dump:")
        print(json.dumps(self.api_info_data.data))
        self.logo_url = json.dumps(self.api_info_data.data[self.symbol]["logo"])
        self.logo_url = self.logo_url.strip('\"')
        r = requests.get(str(self.logo_url))
        self.logo_img = pygame.image.load(io.BytesIO(r.content))
        

cmc = CoinMarketCapAPI('enter-your-cmc-api-here')
coin_symbol = 'SAFEMOON'
my_safe_moon = 10000000 # how much safemoon do I own
my_money_spent = 10.00 # how much money i've spent
real_currency = 'GBP'

crypto = Crypto_coin(symbol=coin_symbol, coins_held=my_safe_moon, purchase_value=my_money_spent, api_currency_type=real_currency)

sleep_time = 1
api_info_next_check = datetime.datetime.now()
api_info_next_check_query_time = 28800 # time in seconds between coin api info queries
api_data_next_check = datetime.datetime.now()
api_data_query_time = 360 # time in seconds between api queries

os.putenv('SDL_FBDEV', '/dev/fb1')

#Colours
LCD_WHITE = (255,255,255)
LCD_RED = (255,0,0)
LCD_GREEN = (0,255,0)
LCD_BLUE = (0,0,255)
LCD_BLACK = (0,0,0)
LCD_LIGHT_YELLOW = (255,255,51)



pygame.init()
pygame.mouse.set_visible(False)
lcd = pygame.display.set_mode((320, 240))
# fill the screen black
lcd.fill((0,0,0))
pygame.display.update()

# set up font sizes
lcd_font = None # name of the font to use - use None if you want to use the system font
font_big = pygame.font.Font(lcd_font, 80)
font_medium = pygame.font.Font(lcd_font, 50)
font_small = pygame.font.Font(lcd_font, 25)

while True:
    now = datetime.datetime.now()
    
    #check is the coin info api should be updated
    if now > api_info_next_check:
        crypto.info_updated(cmc.cryptocurrency_info(symbol=crypto.symbol))
        api_info_next_check = now + datetime.timedelta(seconds = api_info_next_check_query_time) # update when the next info api query should happen
    
    # check if the price data api should be refreshed
    if now > api_data_next_check:
        crypto.api_updated(cmc.cryptocurrency_quotes_latest(symbol=crypto.symbol, convert=crypto.api_currency_type)) # load the latest api data into the crypto coin
        print ("Coin: " + str(crypto.name) + "  current total value is: " + str(crypto.current_total_value_str) + "  coin price is : " + str(crypto.current_value_str) + "  CMC rank = " + str(crypto.cmc_rank) + ".")
        api_data_next_check = now + datetime.timedelta(seconds = api_data_query_time) # update when the next api data query should happen
        print ("Next API query is at: " + str(api_data_next_check))
    
        # coin name at the top
        text_coin_name = font_small.render('%s'%crypto.name.strip('\"'), True, LCD_WHITE)
        rect_coin_name = text_coin_name.get_rect(center=(160+32,16))
        # coin symbol
        text_coin_symbol = font_small.render('(%s)'%crypto.symbol, True, LCD_WHITE)
        rect_coin_symbol = text_coin_symbol.get_rect(center=(160+32,48))

        #work out which is longer, the name or symbol
        image_name_length = text_coin_name.get_width() if text_coin_name.get_width() > text_coin_symbol.get_width() else text_coin_symbol.get_width()
        #print (image_name_length)
        rect_coin_image = crypto.logo_img.get_rect(topleft=(160 - image_name_length,2))

        #owned total value top middle
        text_total_value = font_big.render('%s'%crypto.current_total_value_str, True, LCD_GREEN if float(crypto.current_total_value) > float(crypto.purchase_value) else LCD_RED)
        rect_total_value = text_total_value.get_rect(center=(160,100))
        
        #coin current value second middle
        text_coin_value = font_medium.render('%s'%crypto.current_value_str, True, LCD_GREEN if crypto.current_value > crypto.old_price_value else LCD_RED)
        rect_coin_value = text_coin_value.get_rect(center=(160,140))
        
        # currency type bottom right
        text_api_currency_type = font_small.render('Currency: %s'%(crypto.api_currency_type), True, LCD_WHITE)
        rect_api_currency_type = text_api_currency_type.get_rect(midright=(318,170))
        # market cap 
        text_market_cap = font_small.render('Market cap: %s'%(millify(crypto.market_cap)), True, LCD_WHITE)
        rect_market_cap = text_market_cap.get_rect(midright=(318,190))
        # 24 hour volume bottom right
        text_volume_24h = font_small.render('%s'%crypto.volume_24h_str, True, LCD_WHITE)
        rect_volume_24h = text_volume_24h.get_rect(midright=(318,210))
        # cmc rank bottom right
        text_cmc_rank = font_small.render('CMC rank: %s'%crypto.cmc_rank, True, LCD_WHITE)
        rect_cmc_rank = text_cmc_rank.get_rect(midright=(318,230))
        
        # past 24 hours performance bottom left
        text_24h_change_text = font_small.render('%24h: ', True, LCD_WHITE)
        rect_24h_change_text = text_24h_change_text.get_rect(midleft=(2,170))
        text_24h_change = font_small.render('%f'%crypto.percent_change_24h, True, LCD_GREEN if crypto.percent_change_24h > 0 else LCD_RED)
        rect_24h_change = text_24h_change.get_rect(midleft=(54,170))
        # past 7 days performance bottom left
        text_7d_change_text = font_small.render('%7d: ', True, LCD_WHITE)
        rect_7d_change_text = text_7d_change_text.get_rect(midleft=(2,190))
        text_7d_change = font_small.render('%f'%crypto.percent_change_7d, True, LCD_GREEN if crypto.percent_change_7d > 0 else LCD_RED)
        rect_7d_change = text_7d_change.get_rect(midleft=(54,190))
        # past 30 days performance bottom left
        text_30d_change_text = font_small.render('%30d: ', True, LCD_WHITE)
        rect_30d_change_text = text_30d_change_text.get_rect(midleft=(2,210))
        text_30d_change = font_small.render('%f'%crypto.percent_change_30d, True, LCD_GREEN if crypto.percent_change_30d > 0 else LCD_RED)
        rect_30d_change = text_30d_change.get_rect(midleft=(54,210))
        # past 60 days performance bottom left
        text_60d_change_text = font_small.render('%60d: ', True, LCD_WHITE)
        rect_60d_change_text = text_60d_change_text.get_rect(midleft=(2,230))
        text_60d_change = font_small.render('%f'%crypto.percent_change_60d, True, LCD_GREEN if crypto.percent_change_60d > 0 else LCD_RED)
        rect_60d_change = text_60d_change.get_rect(midleft=(54,230))

    bar_length = int(translate(int((api_data_next_check-now).total_seconds()), api_data_query_time, 0, 0, 320)) # calculate how long the bar should be for showing the time left until an API refresh
    
    lcd.fill((0,0,0)) # clear the screen
    
    lcd.blit(crypto.logo_img, rect_coin_image) # coin logo
    lcd.blit(text_coin_name, rect_coin_name) # coin name
    lcd.blit(text_coin_symbol, rect_coin_symbol) # coin symbol
    lcd.blit(text_coin_value, rect_coin_value) # write coin value
    lcd.blit(text_total_value, rect_total_value) # write total value of owned coins
    lcd.blit(text_api_currency_type, rect_api_currency_type) # write currency type
    lcd.blit(text_market_cap, rect_market_cap) # write market cap
    lcd.blit(text_volume_24h, rect_volume_24h) # write last 24h volume of traded coins
    lcd.blit(text_cmc_rank, rect_cmc_rank) # write cmc rank
    lcd.blit(text_24h_change_text, rect_24h_change_text) # 24h change text
    lcd.blit(text_24h_change, rect_24h_change) # 24h change
    lcd.blit(text_7d_change_text, rect_7d_change_text) # 7d change text
    lcd.blit(text_7d_change, rect_7d_change) # 7d change
    lcd.blit(text_30d_change_text, rect_30d_change_text) # 30d change test
    lcd.blit(text_30d_change, rect_30d_change) # 30d change
    lcd.blit(text_60d_change_text, rect_60d_change_text) # 60d change test
    lcd.blit(text_60d_change, rect_60d_change) # 60d change
    pygame.draw.lines(lcd, LCD_LIGHT_YELLOW, True, [(0,239), (bar_length,239)], 1) # draw API query time bar along the bottom
    
    pygame.display.update() # update the screen
    
    sleep(sleep_time)