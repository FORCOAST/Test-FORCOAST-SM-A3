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
botsalt = Image.open(r"/usr/src/app/output/botsalt.png")
bottemp = Image.open(r"/usr/src/app/output/bottemp.png")
chl = Image.open(r"/usr/src/app/output/chl.png")
fchl = Image.open(r"/usr/src/app/output/fchl.png")
foxy = Image.open(r"/usr/src/app/output/foxy.png")
fres = Image.open(r"/usr/src/app/output/fres.png")
fsal = Image.open(r"/usr/src/app/output/fsal.png")
ftem = Image.open(r"/usr/src/app/output/ftem.png")
oxy = Image.open(r"/usr/src/app/output/oxy.png")
resup = Image.open(r"/usr/src/app/output/resup.png")
ssi = Image.open(r"/usr/src/app/output/ssi.png")

logo = Image.open(r"/usr/src/app/Bulletin/FORCOAST_Logo_WhiteBack.png")
footer = Image.open(r"/usr/src/app/Bulletin/FORCOAST_Footer_Blue.png")

#get height and width for all images
#botsalt_width, botsalt_height = botsalt.size
#bottemp_width, bottemp_height = bottemp.size
#chl_width, chl_height = chl.size
#fchl_width, fchl_height = fchl.size
#foxy_width, foxy_height = foxy.size
#fres_width, fres_height = fres.size
#fsal_width, fsal_height = fsal.size
#ftem_width, ftem_height = ftem.size
#oxy_width, oxy_height = oxy.size
#resup_width, resup_height = resup.size
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

logo_new_width = 1000
logo_new_height = int((logo_new_width/logo_width)*logo_height)
logo_resize = logo.resize((logo_new_width, logo_new_height), PIL.Image.NEAREST)

#draw images on bulletin (non-parameter)
newBulletin = Image.new("RGBA", (4250, 2784), (255, 255, 255))
newBulletin.paste(botsalt, (1100, 50))
newBulletin.paste(bottemp, (2150, 50))
newBulletin.paste(chl, (3200, 50))
newBulletin.paste(fchl, (3200, 700))
newBulletin.paste(foxy, (50, 1350))
newBulletin.paste(fres, (3200, 1350))
newBulletin.paste(fsal, (50, 2000))
newBulletin.paste(ftem, (1100, 2000))
newBulletin.paste(oxy, (2150, 2000))
newBulletin.paste(resup, (3200, 2000))
newBulletin.paste(ssi_resize, (1100, 700))
newBulletin.paste(logo_resize, (50, 50))
newBulletin.paste(footer_resize, (0, 2650))
draw = PIL.ImageDraw.Draw(newBulletin)
font_title = ImageFont.truetype(r"/usr/src/app/Bulletin/arial.ttf", 100)
font_param = ImageFont.truetype(r"/usr/src/app/Bulletin/arial.ttf", 50)
draw.text((50, 660), 'A3: Site prospection', font = font_title, fill=(0,0,0,255))



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
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    draw.text((50, 780), 'Parameters:\n'\
                      'Site: Limfjord\n'\
                      'Year: {0}\n'\
                      'Months: {1}:{2}\n'\
                      'Salinity range: {3}:{4} (g/L)\n'\
                      'Temperature range: {5}:{6} (C)\n'\
                      'Half saturation constant for food: {7}\n'\
                      'Oxygen lower treshold: {8} (mg/L)\n'\
                      'Resuspension treshold: {9}\n'\
                      'Expected decay: {10}\n'\
                      'Bulletin generated on: {11}'
                      .format(argument.year, argument.month_begin, argument.month_end,\
                              argument.salinity_low, argument.salinity_high, argument.temperature_low,\
                              argument.temperature_high, argument.food, argument.oxygen_low,\
                              argument.resuspension, argument.decay, dt_string), \
                       font = font_param, fill=(23,111,176,255))
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
