# Author: Taylor C Hoyt
# Description: This program takes input from an OBDII ELM327 to USB adapter and displays
# information on a graphical interface, to be used as a heads-up display for a vehicle.

import button
import obd
import pygame
import rpmdial

from pygame.locals import *

# display resolution
screen_x = 1024
screen_y = 600

pygame.init()

pygame.display.set_caption('PyHUD')
flags = DOUBLEBUF
window_surface = pygame.display.set_mode((screen_x, screen_y), flags)
window_surface.set_alpha(None)

# fonts
main_font = pygame.font.Font("calibri-bold.ttf", 32)  # this font can be changed to whatever font
seven_segment_font = pygame.font.Font("Seven Segment.ttf", 32)

# connects OBD
connection = obd.OBD("\\.\\COM7")

# load button images
cel_image = pygame.image.load('cel_button.png').convert_alpha()
dtc_cmd = obd.commands.GET_DTC
dtc_response = connection.query(dtc_cmd)
if str(dtc_response) != "[]":  # if there is an active check engine code, then CEL button turns yellow
    cel_image = pygame.image.load('cel_active_button.png').convert_alpha()
# button instances
cel_button = button.Button(462, 525, cel_image, 0.5)

# rpm dial
n_width, n_height = screen_x // 2, screen_y // 2

dial = rpmdial.RpmDial(1000, 8, n_width, n_height, main_font)

# loop
is_running = True
while is_running:
    window_surface.fill((0, 0, 0))

    if cel_button.draw(window_surface):
        print('CEL')

    rpm_cmd = obd.commands.RPM
    rpm_response = connection.query(rpm_cmd)
    rpm_val = rpm_response.value
    rpm_mag = rpm_val.magnitude

    # draw rpm dial
    dial.draw(rpm_mag, window_surface)

    speed_cmd = obd.commands.SPEED
    speed_response = connection.query(speed_cmd)
    speed_mph = int(speed_response.value.to("mph").magnitude)
    speed_out = str(speed_mph) + " MPH"
    mph_text = seven_segment_font.render(speed_out, True, (255, 0, 0), (0, 0, 0))

    mph_text_rect = mph_text.get_rect()

    mph_text_rect.midtop = (n_width, n_height)

    window_surface.blit(mph_text, mph_text_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    pygame.display.update()
pygame.quit()
