import requests
import json
import telepot
import argparse
import time
import PIL
from PIL import Image, ImageDraw, ImageFont
import sys
from datetime import datetime

# Create bot (see https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e):
# - On Telegram, search @ BotFather, send him a “/start” message
# - Send another “/newbot” message, then follow the instructions to setup a name and a username
# - Copy API token
# - Go to bot in Telegram, and press /start
# - Bot can be accessed by others as well.
# - Once activated, user_id will be added to getUpdates response

def send_bulletin(token,chat_id,bulletin,method):

	file = bulletin

	bot = telepot.Bot(token)

	# Check chat ID's
	# url = 'https://api.telegram.org/bot' + token + '/getUpdates'
	# resp = requests.get(url)
	# r_json = json.loads(resp.text)
	# print('r_json:')
	# print(r_json)

	# Method options are file and url
	if method == 'file':
		print(chat_id)
		bot.sendPhoto(chat_id, photo=open(file, 'rb'))
	else:
		with open('bulletin.png', 'wb') as f:
			f.write(requests.get(file).content)
			f.close()
			time.sleep(3)

		print(chat_id)
		bot.sendPhoto(chat_id, photo=open('bulletin.png', 'rb'))



#Assign outcome images to variable
botsalt = Image.open("/usr/src/app/Bulletin/A3_botsalt.png")
bottemp = Image.open("/usr/src/app/Bulletin/A3_bottemp.png")
chl = Image.open("/usr/src/app/Bulletin/A3_chl.png")
oxy = Image.open("/usr/src/app/Bulletin/A3_oxy.png")
ssi = Image.open("/usr/src/app/Bulletin/A3_ssi.png")

logo = Image.open("/usr/src/app/Bulletin/FORCOAST_Logo_WhiteBack.png")
footer = Image.open("/usr/src/app/Bulletin/FORCOAST_Footer_Blue.png")


botsalt_width, botsalt_height = botsalt.size
bottemp_width, bottemp_height = bottemp.size
chl_width, chl_height = chl.size
oxy_width, oxy_height = oxy.size
ssi_width, ssi_height = ssi.size
logo_width, logo_height = logo.size
footer_width, footer_height= footer.size

#rescale
ssi_new_width = 2050
ssi_new_height = int((ssi_new_width/ssi_width)*ssi_height)
ssi_resize = ssi.resize((ssi_new_width, ssi_new_height), PIL.Image.NEAREST)

footer_new_width = 4250
footer_new_height = int((footer_new_width/footer_width)*footer_height)
footer_resize = footer.resize((footer_new_width, footer_new_height), PIL.Image.NEAREST)

logo_new_width = 600
logo_new_height = int((logo_new_width/logo_width)*logo_height)
logo_resize = logo.resize((logo_new_width, logo_new_height), PIL.Image.NEAREST)

botsalt_new_width = 1100
botsalt_new_height = int((botsalt_new_width/botsalt_width)*botsalt_height)
botsalt_resize = botsalt.resize((botsalt_new_width, botsalt_new_height), PIL.Image.NEAREST)

bottemp_new_width = 1100
bottemp_new_height = int((bottemp_new_width/bottemp_width)*bottemp_height)
bottemp_resize = bottemp.resize((bottemp_new_width, bottemp_new_height), PIL.Image.NEAREST)

chl_new_width = 1100
chl_new_height = int((chl_new_width/chl_width)*chl_height)
chl_resize = chl.resize((chl_new_width, chl_new_height), PIL.Image.NEAREST)

oxy_new_width = 1100
oxy_new_height = int((oxy_new_width/oxy_width)*oxy_height)
oxy_resize = oxy.resize((oxy_new_width, oxy_new_height), PIL.Image.NEAREST)

newBulletin = Image.new("RGBA", (4250, 2100), (255, 255, 255))
newBulletin.paste(botsalt_resize, (50, 366))
newBulletin.paste(bottemp_resize, (50, 1166))
newBulletin.paste(chl_resize, (3200, 366))
newBulletin.paste(oxy_resize, (3200, 1166))
newBulletin.paste(ssi_resize, (1150, 366))
newBulletin.paste(logo_resize, (180, 0))
newBulletin.paste(footer_resize, (0, 1967))
draw = PIL.ImageDraw.Draw(newBulletin)

font_param = ImageFont.truetype("/usr/src/app/Bulletin/ariali.ttf", 30)
font_title = ImageFont.truetype("/usr/src/app/Bulletin/arial.ttf", 150)
now = datetime.now()
dt_string = now.strftime("%a %b %d %H:%M:%S %Y")



draw.text((1550, 100), 'Site prospection', font = font_title, fill=(23,111,176,255))

if __name__ == '__main__':

    # Get input from command line arguments
    parser = argparse.ArgumentParser(description = "Description for my parser")
    parser.add_argument("-A", "--year_begin", help = "Year begin parameter", required = True, default = "")
    parser.add_argument("-B", "--year_end", help = "Year end parameter", required = True, default = "")
    parser.add_argument("-C", "--month_begin", help = "Month begin parameter", required = True, default = "")
    parser.add_argument("-D", "--month_end", help = "Month end parameter", required = True, default = "")
    parser.add_argument("-E", "--salinity_low", help = "Salinity low parameter", required = True, default = "")
    parser.add_argument("-F", "--salinity_high", help = "Salinity high parameter", required = True, default = "")
    parser.add_argument("-G", "--temperature_low", help = "Temperature low parameter", required = True, default = "")
    parser.add_argument("-H", "--temperature_high", help = "Temperature high parameter", required = True, default = "")
    parser.add_argument("-I", "--food", help = "Food parameter", required = True, default = "")
    parser.add_argument("-J", "--oxygen_low", help = "Oxygen low parameter", required = True, default = "")
    parser.add_argument("-K", "--resuspension", help = "Resuspension treshold parameter", required = True, default = "")
    parser.add_argument("-L", "--decay", help = "Expected decay parameter", required = True, default = "")
    parser.add_argument("-M", "--token", help = "Telegram bot token", required = True, default = "")
    parser.add_argument("-N", "--chat_id", help = "Telegram chat ID", required = True, default = "")
    parser.add_argument("-O", "--bulletin", help = "Bulletin to be send", required = True, default = "")
    parser.add_argument("-P", "--method", help = "Specify file or URL as input", required = False, default = "url")

    argument = parser.parse_args()
    
    #draw input parameters on bulletin
    
    #Month to string
    mydateB = argument.month_begin
    mydateB_datetime = datetime.strptime(mydateB, "%m")
    mydateB_string = mydateB_datetime.strftime("%b")
    
    mydateE = argument.month_end
    mydateE_datetime = datetime.strptime(mydateE, "%m")
    mydateE_string = mydateE_datetime.strftime("%b")
    
    draw.text((3200, 0), 'Bulletin generated on: {12}\n\n'\
                      'Parameters:\n'\
                      'Site: Limfjord\n'\
                      'Period: {0} {1} - {2} {3} \n'\
                      'Salinity thresholds: {4} - {5}\n'\
                      'Temperature thresholds: {6} - {7}\n'\
                      'Half saturation constant for food: {8}\n'\
                      'Oxygen lower treshold: {9}\n'\
                      'Resuspension treshold: {10}\n'\
                      'Expected dacay: {11}'
                      .format(mydateB_string, argument.year_begin, mydateE_string, argument.year_end, \
                              argument.salinity_low, argument.salinity_high, argument.temperature_low,\
                              argument.temperature_high, argument.food, argument.oxygen_low,\
                              argument.resuspension, argument.decay, dt_string), \
                       font = font_param, fill=(0,0,0,255))

    #save bulletin
    newBulletin.save(r"/usr/src/app/output/bulletin.png", quality = 100)
    
    #take arguments and send bulletin
    if argument.token:
        token = argument.token
        print('Bot token = ' + token)
    if argument.chat_id:
        chat_id = argument.chat_id
        print('Chat ID = ' + chat_id)
    if argument.bulletin:
        bulletin = argument.bulletin
        print('Bulletin filename = ' + bulletin)
    if argument.method:
        method = argument.method
        print('Method = ' + method)

    send_bulletin(token,chat_id,bulletin,method)
