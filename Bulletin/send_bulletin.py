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
botsalt = Image.open("/usr/src/app/output/botsalt.png")
bottemp = Image.open("/usr/src/app/output/bottemp.png")
chl = Image.open("/usr/src/app/output/chl.png")
oxy = Image.open("/usr/src/app/output/oxy.png")
ssi = Image.open("/usr/src/app/output/ssi.png")

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

logo_new_width = 700
logo_new_height = int((logo_new_width/logo_width)*logo_height)
logo_resize = logo.resize((logo_new_width, logo_new_height), PIL.Image.NEAREST)

newBulletin = Image.new("RGBA", (4250, 1899), (255, 255, 255))
newBulletin.paste(botsalt, (50, 466))
newBulletin.paste(bottemp, (50, 1016))
newBulletin.paste(chl, (3200, 466))
newBulletin.paste(oxy, (3200, 1016))
newBulletin.paste(ssi_resize, (1100, 466))
newBulletin.paste(logo_resize, (180, 50))
newBulletin.paste(footer_resize, (0, 1766))
draw = PIL.ImageDraw.Draw(newBulletin)

font_param = ImageFont.truetype("/usr/src/app/Bulletin/ariali.ttf", 30)
font_title = ImageFont.truetype("/usr/src/app/Bulletin/arial.ttf", 150)
now = datetime.now()
dt_string = now.strftime("%a %b %d %H:%M:%S %Y")



draw.text((1550, 150), 'Site prospection', font = font_title, fill=(23,111,176,255))

if __name__ == '__main__':

    # Get input from command line arguments
    parser = argparse.ArgumentParser(description = "Description for my parser")
    parser.add_argument("-A", "--year", help = "Year parameter", required = True, default = "")
    parser.add_argument("-B", "--month_begin", help = "Month begin parameter", required = True, default = "")
    parser.add_argument("-C", "--month_end", help = "Month end parameter", required = True, default = "")
    parser.add_argument("-D", "--salinity_low", help = "Salinity low parameter", required = True, default = "")
    parser.add_argument("-E", "--salinity_high", help = "Salinity high parameter", required = True, default = "")
    parser.add_argument("-F", "--temperature_low", help = "Temperature low parameter", required = True, default = "")
    parser.add_argument("-G", "--temperature_high", help = "Temperature high parameter", required = True, default = "")
    parser.add_argument("-H", "--food", help = "Food parameter", required = True, default = "")
    parser.add_argument("-I", "--oxygen_low", help = "Oxygen low parameter", required = True, default = "")
    parser.add_argument("-J", "--resuspension", help = "Resuspension treshold parameter", required = True, default = "")
    parser.add_argument("-K", "--decay", help = "Expected decay parameter", required = True, default = "")
    parser.add_argument("-L", "--token", help = "Telegram bot token", required = True, default = "")
    parser.add_argument("-M", "--chat_id", help = "Telegram chat ID", required = True, default = "")
    parser.add_argument("-N", "--bulletin", help = "Bulletin to be send", required = True, default = "")
    parser.add_argument("-O", "--method", help = "Specify file or URL as input", required = False, default = "url")

    argument = parser.parse_args()
    
    #draw input parameters on bulletin
    
    #Month to string
    mydateB = argument.month_begin
    mydateB_datetime = datetime.strptime(mydateB, "%m")
    mydateB_string = mydateB_datetime.strftime("%b")
    
    mydateE = argument.month_end
    mydateE_datetime = datetime.strptime(mydateE, "%m")
    mydateE_string = mydateE_datetime.strftime("%b")
    
    draw.text((3200, 50), 'Bulletin generated on: {11}\n\n'\
                      'Parameters:\n\n'\
                      'Site: Limfjord\n'\
                      'Period: {0} {1} - {2} {1} \n'\
                      'Salinity thresholds: {3} - {4}\n'\
                      'Temperature thresholds: {5} - {6}\n'\
                      'Half saturation constant for food: {7}\n'\
                      'Oxygen lower treshold: {8}\n'\
                      'Resuspension treshold: {9}\n'\
                      'Expected dacay: {10}'
                      .format(mydateB_string, argument.year, mydateE_string, \
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
