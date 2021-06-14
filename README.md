# cryptopi-monitor
Monitor cryptocurrency stats and compare it to your own wallet, displaying the details on a LCD screen using a Raspberry Pi

![IMG_2913](https://user-images.githubusercontent.com/74387709/121956079-996ff700-cd58-11eb-8741-4781e74b5742.jpeg)

<b>Features:</b></br>
* Queries CoinMarketCap for API data about a currency.</br>
* Updates current price on a regular interval</br>
* Details are coloured, green for good red for bad (not very colour blind friendly but these are easy to edit)</br>
* Shows details about your holding via editing a variable</br>
* Shows a bar along the bottom to display how far through a refresh it is</br>

<b>What you'll need:</b></br>
* A Raspberry Pi, This setup has a RPI4 in mind but an older one should work</br>
* An LCD screen such as the Adafruit 320x240 TFT touchscreen module https://www.adafruit.com/product/1601</br>
* Some knowledge of Python - I am a novice with coding so you may well want to improve my code.</br>

<b>Getting setup:</b></br>
* First off, connect your LCD screen and set it up as a 'Raw Frame Buffer Device' so that you can interact with it using pygameas a separate display. Adafruit have a good script/guide for using one of their devices: https://learn.adafruit.com/adafruit-pitft-28-inch-resistive-touchscreen-display-raspberry-pi/easy-install-2</br>
* Make sure you have Python 3 installed on your Raspberry Pi</br>
* Install the following Python modules:</br>
	    Pygame https://www.pygame.org/wiki/GettingStarted : </br>
		Coin Market Cap API https://pypi.org/project/python-coinmarketcap/ : </br>
	    
		sudo pip install pygame
		
		sudo pip install python-coinmarketcap
    
    
Edit lcd.py to enter your API key as well as enter in your currency info/how much you have:</br>

1. cmc = CoinMarketCapAPI('enter-your-cmc-api-here')
2. coin_symbol = 'SAFEMOON'
3. my_safe_moon = 10000000 # how much safemoon do I own
4. my_money_spent = 10.00 # how much money i've spent
5. real_currency = 'GBP'

Save and run the python script using sudo python lcd.py - see if it all works!

Possible future improvements:
- [ ] Work out how to query coins/tokens in a wallet for automatic updating of your value
- [ ] Better positioning on the screen to support screen sizes other than 320x240
- [ ] Check multiple coins/tokens and cycle through them all
