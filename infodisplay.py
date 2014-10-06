import sys, pygame 
from pygame.locals import * 
import time 
import subprocess 
import os 
import glob 
import pywapi 
import pprint


os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"
pygame.init()

installPath = "/home/pi/infodisplay/"
forcastIcons = {}
timer = 0
def getWeather(item):

	if item == "curr_cond":
		curr_cond = weather_com_result['current_conditions']['text'].lower()
		return(curr_cond)
	if item == "curr_temp":
		celsiusTemp = int(weather_com_result['current_conditions']['temperature'])
		fTemp = 9.0/5.0 * int(celsiusTemp) + 32
		return int(fTemp)
	if item == "curr_hum":
		curr_humidity = int(weather_com_result['current_conditions']['humidity'])
		return(curr_humidity)
	if item == "curr_wind_speed":
		curr_wind_speed = int(weather_com_result['current_conditions']['wind']['speed'])
		mph_wind =  0.6214 * float(curr_wind_speed)
		return(int(mph_wind))
	if item == "curr_gust":
		curr_gust = str(weather_com_result['current_conditions']['wind']['gust'])
		if curr_gust == "N/A":
                	return("0")
		else:
			mph_gust =  0.6214 * float(curr_gust)
			return(int(mph_gust))

#define function that checks for mouse location
def on_click():
	click_pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
	#check to see if exit has been pressed
	if 270 <= click_pos[0] <= 320 and 10 <= click_pos[1] <=50:
		print "You pressed exit" 
		button(0)
	#now check to see if play was pressed
	if 70 <= click_pos[0] <= 100 and 100 <= click_pos[1] <=130:
                print "You pressed button play"
                button(1)	
	#now check to see if stop  was pressed
        if 80 <= click_pos[0] <= 135 and 80 <= click_pos[1] <=130:
                print "You pressed button stop"
                button(2)
	#now check to see if refreshed  was pressed
        if 270 <= click_pos[0] <= 320 and 70 <= click_pos[1] <=120:
                print "You pressed button refresh"
                button(3)
	#now check to see if previous  was pressed
        if 10 <= click_pos[0] <= 60 and 180 <= click_pos[1] <=230:
                print "You pressed button previous"
                button(4)

	 #now check to see if next  was pressed
        if 70 <= click_pos[0] <= 120 and 180 <= click_pos[1] <=230:
                print "You pressed button next"
                button(5)

	 #now check to see if volume down was pressed
        if 130 <= click_pos[0] <= 180 and 180 <= click_pos[1] <=230:
                print "You pressed volume down"
                button(6)

	 #now check to see if button 7 was pressed
        if 190 <= click_pos[0] <= 240 and 180 <= click_pos[1] <=230:
                print "You pressed volume up"
                button(7)

	 #now check to see if button 8 was pressed
        if 250 <= click_pos[0] <= 300 and 180 <= click_pos[1] <=230:
                print "You pressed mute"
                button(8)

	 #now check to see if button 9 was pressed
        if 15 <= click_pos[0] <= 125 and 165 <= click_pos[1] <=200:
                print "You pressed button 9"
                button(9)


#define action on pressing buttons
def button(number):
	print "You pressed button ",number
	if number == 0:    #specific script when exiting
		screen.fill(black)
		font=pygame.font.Font(None,24)
        	label=font.render("Radioplayer will continue in background", 1, (white))
        	#screen.blit(label,(0,90))
		pygame.display.flip()
		time.sleep(5)
		sys.exit()

	if number == 1:	
		subprocess.call("mpc play ", shell=True)
		refresh_menu_screen()

	if number == 2:
		subprocess.call("mpc stop ", shell=True)
		refresh_menu_screen()

	if number == 3:
		subprocess.call("mpc stop ", shell=True)
		subprocess.call("mpc play ", shell=True)
		refresh_menu_screen() 
		
	if number == 4:
		subprocess.call("mpc prev ", shell=True)
		refresh_menu_screen()

	if number == 5:
		subprocess.call("mpc next ", shell=True)
		refresh_menu_screen()

	if number == 6:
		subprocess.call("mpc volume -10 ", shell=True)
		refresh_menu_screen()

	if number == 7:
		subprocess.call("mpc volume +10 ", shell=True)
		refresh_menu_screen()

	if number == 8:
		subprocess.call("mpc volume 0 ", shell=True)
		refresh_menu_screen()	

def refresh_menu_screen():
	curr_cond_icon=""
#set up the fixed items on the menu
	weather_com_result = pywapi.get_weather_from_weather_com('61103', units='imperial')	

	current = time.strftime("%-I:%M")
	cur_date = time.strftime("%-m/%-d/%Y")
	cond = weather_com_result['current_conditions']['text'].lower()
	temp =int(weather_com_result['current_conditions']['temperature'])
	hum = int(weather_com_result['current_conditions']['humidity'])
	gust = str(weather_com_result['current_conditions']['wind']['gust'])
	#if gust <> "N/A":
	#	gust = int(0.6214 * gust)
	wind_speed = float(weather_com_result['current_conditions']['wind']['speed'])
	wind_speed = int(wind_speed)
	
	screen.fill(blue) #change the colours if needed
	# Set font sized
	font=pygame.font.Font(None,25)
	time_font=pygame.font.Font(None,85)
	temp_font = pygame.font.Font(None,30)
	heading_font = pygame.font.Font(None,20)
	
	clock=time_font.render(current, 1, (white))
	date=font.render(cur_date, 1, (white))
	screen.blit(clock,(1, -5))
	screen.blit(date,(148, 2))
	exit=pygame.image.load("quit.png")
	exit = pygame.transform.scale(exit,(40,40))
	screen.blit(exit,(270,5))
	# Display weather info
	#currCond = temp_font.render("Current: "+cond ,1,(white))
	curTemp = temp_font.render("Temp: "+str(temp)+ u'\N{DEGREE SIGN}'+"F",1,(white))
	screen.blit(curTemp,(5, 192))	
	curHum = temp_font.render("Humidity: "+str(hum)+"%",1,(white))
	screen.blit(curHum,(5,217))
	curWind = temp_font.render("Wind: "+str(wind_speed)+" mph",1,(white))
        screen.blit(curWind,(185,192))
	curGust = temp_font.render("Gust: "+str(gust)+" mph",1,(white))
        screen.blit(curGust,(185,217))
	pygame.draw.rect(screen, white, (1, 190, 319, 50),1)
	# Label days
	# current condition icon
	icon = (weather_com_result['current_conditions']['icon']) + ".png" 
        logo = pygame.image.load(icon)
	logo = pygame.transform.scale(logo,(50,50))
	todayHeading = heading_font.render("Today",1,(white))
	screen.blit(todayHeading, (10,70))
        screen.blit(logo, (5, 90))
	today_low = str(weather_com_result['forecasts'][0]['low'])
	today_high = str(weather_com_result['forecasts'][0]['high'])
	todayHighLow = heading_font.render(today_high + "/" + today_low, 1,(white))
	today_precip = str(weather_com_result['forecasts'][0]['day']['chance_precip'])
	tonight_precip = str(weather_com_result['forecasts'][0]['night']['chance_precip'])
	todayPrecip = heading_font.render("am: "+today_precip+"%", 1,(white))
	tonightPrecip = heading_font.render("pm: "+tonight_precip+"%", 1,(white))
	screen.blit(todayHighLow, (10, 140))
	screen.blit(todayPrecip, (10, 155))
	screen.blit(tonightPrecip, (10, 173))
	# Forcast icons
	start = 1
	for i in range(start, 5):
                
		if not(weather_com_result['forecasts'][i]):
                        break	
		forcastIcons[i] = installPath+ (weather_com_result['forecasts'][i]['day']['icon']) + ".png"
		logo = pygame.image.load(forcastIcons[i])	
		logo = pygame.transform.scale(logo,(50,50))
		day = str(weather_com_result['forecasts'][i]['day_of_week'])[:3]
		dayHeading = heading_font.render(day,1,(white))
		dayHigh = str(weather_com_result['forecasts'][i]['high'])
		dayLow = str(weather_com_result['forecasts'][i]['low'])
		dayHighLow = heading_font.render(dayHigh+"/"+dayLow,1,(white))
		precip_Day = str(weather_com_result['forecasts'][i]['day']['chance_precip'])
		precip_night = str(weather_com_result['forecasts'][i]['night']['chance_precip'])
		precipDayChance = heading_font.render("am: "+precip_Day+"%",1,(white))
		precipNightChance = heading_font.render("pm: "+precip_night+"%",1,(white))
		screen.blit(dayHeading,(i * 67, 70))
		screen.blit(logo, (i *  63, 90))
		screen.blit(dayHighLow,(i * 67,140))
		screen.blit(precipDayChance,(i * 67, 155))
		screen.blit(precipNightChance,(i * 67, 173))

	# rect = (left,top,width,heigth)
	# draw the main elements on the screen
	
	#pygame.draw.rect(screen, red, (8, 70, 304, 108),1)
	#pygame.draw.line(screen, red, (8,142),(310,142),1)

	
	pygame.display.flip()
	time.sleep(1)
	
def main():
	timer = 1
	backlightState = 1
        while 1:
		timer += 1
		refresh_menu_screen() 
                for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                print "screen pressed" #for debugging purposes
				if backlightState == 0:
					os.system(installPath+"backlighton.sh")
					backlightState = 1
					main()
                                pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1])
                                print pos #for checking
                                pygame.draw.circle(screen, white, pos, 2, 0) #for debugging purposes - adds a small dot where the screen is pressed
                                on_click()
		
#ensure there is always a safe way to end the program if the touch screen fails

                        if event.type == KEYDOWN:
                                if event.key == K_ESCAPE:
                                        sys.exit()
		if (timer >= 15):              		
		  	os.system(installPath+"backlightoff.sh")
                        timer = 1	
			backlightState = 0        

	time.sleep(0.2)        
	pygame.display.update()


#################### EVERTHING HAS NOW BEEN DEFINED ###########################

#set size of the screen
size = width, height = 320, 240
screen = pygame.display.set_mode(size)
pygame.mouse.set_visible(0)
#define colours
blue = 26, 0, 255
cream = 254, 255, 25
black = 0, 0, 0
white = 255, 255, 255
yellow = 255, 255, 0
red = 255, 0, 0
green = 0, 255, 0
os.system(installPath+"setupbacklight.sh")
os.system(installPath+"backlighton.sh")
refresh_menu_screen()  #refresh the menu interface 
main() #check for key presses and start emergency exit
station_name()

