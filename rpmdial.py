# this class displays a dial that measures RPM

import math
import pygame


class RpmDial:
    def __init__(self, multiplier_rpm, max_rpm, width, height, font):
        self.multiplier_rpm = multiplier_rpm
        self.max_rpm = max_rpm
        self.width = width
        self.height = height
        self.font = font
        self.min_rpm = 0  # should always be zero
        max_rotation = 180  # sets the max rotation of the RPM needle to 180 degrees
        self.angle_increment = max_rotation / max_rpm
        self.dial_radius = height - 50

    def get_pos(self, rpm_magnitude, radius):
        needle_angle = ((rpm_magnitude / self.multiplier_rpm) * self.angle_increment)
        x = self.width + radius * math.cos(math.radians(needle_angle) - math.pi)
        y = self.height + radius * math.sin(math.radians(needle_angle) - math.pi)
        return x, y

    def draw(self, rpm_magnitude, surface):
        if rpm_magnitude > (self.max_rpm * self.multiplier_rpm):
            rpm_magnitude = self.max_rpm * self.multiplier_rpm

        # draw dial
        outside_line_thickness = 20
        pygame.draw.circle(surface, pygame.Color('gray'), (self.width, self.height), self.dial_radius,
                           outside_line_thickness, True, True)
        multiplier_text = self.font.render("x1000 RPM", True, pygame.Color('white'))
        multiplier_text_rect = multiplier_text.get_rect()
        multiplier_text_rect.midbottom = (512, 150)
        surface.blit(multiplier_text, multiplier_text_rect)
        pygame.draw.line(surface, pygame.Color('green'), (self.width, self.dial_radius),
                         self.get_pos(rpm_magnitude, self.dial_radius), 4)
        pygame.draw.circle(surface, pygame.Color('gray'), (self.width, self.dial_radius), self.dial_radius * 0.05)

        # draw numbers on dial
        number_of_loops = 0
        while number_of_loops <= self.max_rpm:
            label = self.font.render(str(number_of_loops), True, pygame.Color('white'))
            label_rect = label.get_rect()
            if number_of_loops > 4:
                label_rect.bottomleft = self.get_pos((number_of_loops * self.multiplier_rpm), self.dial_radius)
                surface.blit(label, label_rect)
            elif number_of_loops == 4:
                label_rect.midbottom = self.get_pos((number_of_loops * self.multiplier_rpm), self.dial_radius)
                surface.blit(label, label_rect)
            else:
                label_rect.bottomright = self.get_pos((number_of_loops * self.multiplier_rpm), self.dial_radius)
                surface.blit(label, label_rect)
            number_of_loops += 1
