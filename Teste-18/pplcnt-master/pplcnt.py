#! /usr/bin/python3
import sys
from gpiozero import MotionSensor
from gpiozero import Button
from signal import pause
from pathlib import Path
from time import sleep
#import keyboard
import pygame

count_path = "./count.txt"
start_date = "01.11.2019"
logo_path = "logo_example.png"
font_path = "Roboto-Regular.ttf"

pir = MotionSensor(4)
button = Button(3)

peoplecount = 0
count = 0

text_col = (0,0,0)
text_bg_col = (255,255,255)
circle_col = (255,255,255)
bg_col = (0,0,0)

def updateText():
	global count
	global text
	newtext = "%04d" % count
	text = font.render(newtext, True, text_col, text_bg_col)

def load_count():
	global peoplecount
	global count
	try:
		with open(count_path, "r") as f:
			peoplecount = int(f.read())
			count = peoplecount // 2
	except Exception as error:
		print("Could not open file \"%s\"" % count_path)

def save_count():
	global peoplecount
	with open(count_path, "w") as f:
		f.write("%d" % peoplecount)

def onMotion():
	global peoplecount
	global count
	global text

	print("Motion!")
	peoplecount += 1
	count = peoplecount // 2
	print("count: ", count)
	save_count()
	updateText()

def onButton():
	global peoplecount
	global count

	print("reset count")
	peoplecount = 0
	count = 0

def quitting():
	print("Bye!")
	pygame.quit()
	sys.exit()

pir.when_motion = onMotion
#button.when_pressed = onButton

#keyboard.add_hotkey('q', lambda: quitting())

load_count()

pygame.init()

display = pygame.display.set_mode(flags=pygame.FULLSCREEN)
pygame.mouse.set_visible(False)
surface = pygame.display.get_surface()
width = surface.get_width()
height = surface.get_height()
print("%d %d" % (width, height))

font = pygame.font.Font(font_path, 350)
text = font.render("text", True, text_col, text_bg_col)

font2 = pygame.font.Font(font_path, 75)
text_visitors = font2.render("Visitors", True, text_col, text_bg_col)
text_since = font2.render("since", True, text_col, text_bg_col)
text_date = font2.render(start_date, True, text_col, text_bg_col)

logo = pygame.image.load(logo_path)
logo_s = pygame.transform.smoothscale(logo, (300,300))

updateText()

running = True

while running:
	while True:
		e = pygame.event.poll()
		#print(e.type)
		if e.type == pygame.NOEVENT:
			break
		if e.type == pygame.QUIT:
			quitting()
	pressed = pygame.key.get_pressed()
	display.fill(bg_col)
	pygame.draw.circle(surface, circle_col, (width//2, height//2), 600)
	display.blit(text,          ((width//2)-(text.get_width()//2), 	        (height//2)-(text.get_height()//2)))
	display.blit(text_visitors, ((width//2)-(text_visitors.get_width()//2), (400)-(text_visitors.get_height()//2)))
	display.blit(text_since,    ((width//2)-(text_since.get_width()//2),    (475)-(text_since.get_height()//2)))
	display.blit(text_date,     ((width//2)-(text_date.get_width()//2),     (550)-(text_date.get_height()//2)))
	display.blit(logo_s,        ((width//2)-(logo_s.get_width()//2),        (1200)-(logo_s.get_height()//2)))
	pygame.display.update()
	pygame.time.wait(1)
