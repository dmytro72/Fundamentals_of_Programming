def flood_fill(image, location, new_color):
    original_color = get_pixel(image, *location)

    def get_neighbors(cell):
        x, y = cell
        return [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]

    to_color = []

    while to_color:
        this_cell = to_color.pop(0)
        set_pixel(image, *this_cell, new_color)
        for neighbor in get_neighbors(this_cell):
            to_color.append(neighor)


##### IMAGE REPRESENTATION WITH SIMILAR ABSTRACTIONS TO LAB 1 AND 2


def get_width(image):
    return image.get_width() // SCALE


def get_height(image):
    return image.get_height() // SCALE


def get_pixel(image, x, y):
    color = image.get_at((x * SCALE, y * SCALE))
    return (color.r, color.g, color.b)


def set_pixel(image, x, y, color):
    loc = x * SCALE, y * SCALE
    c = pygame.Color(*color[::-1])
    for i in range(SCALE):
        for j in range(SCALE):
            image.set_at((loc[0] + i, loc[1] + j), c)
    # comment out the two lines below to avoid redrawing the image every time
    # we set a pixel
    # screen.blit(image, (0, 0))
    # pygame.display.flip()


import os
import sys

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from pygame.locals import *

COLORS = {
    pygame.K_r: (255, 0, 0),
    pygame.K_w: (255, 255, 255),
    pygame.K_k: (0, 0, 0),
    pygame.K_g: (0, 255, 0),
    pygame.K_b: (0, 0, 255),
    pygame.K_c: (0, 255, 255),
    pygame.K_y: (255, 230, 0),
    pygame.K_p: (179, 0, 199),
    pygame.K_o: (255, 77, 0),
    pygame.K_n: (66, 52, 0),
    pygame.K_e: (152, 152, 152),
}

COLOR_NAMES = {
    pygame.K_r: "red",
    pygame.K_w: "white",
    pygame.K_k: "black",
    pygame.K_g: "green",
    pygame.K_b: "blue",
    pygame.K_c: "cyan",
    pygame.K_y: "yellow",
    pygame.K_p: "purple",
    pygame.K_o: "orange",
    pygame.K_n: "brown",
    pygame.K_e: "grey",
}

SCALE = 7
IMAGE = "flood_input.png"

pygame.init()
image = pygame.image.load(IMAGE)
dims = (image.get_width() * SCALE, image.get_height() * SCALE)
screen = pygame.display.set_mode(dims)
image = pygame.transform.scale(image, dims)
screen.blit(image, (0, 0))
pygame.display.flip()
initial_color = pygame.K_p
cur_color = COLORS[initial_color]
print("current color:", COLOR_NAMES[initial_color])
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key in COLORS:
                cur_color = COLORS[event.key]
                print("current color:", COLOR_NAMES[event.key])
            elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            flood_fill(image, (event.pos[0] // SCALE, event.pos[1] // SCALE), cur_color)
            screen.blit(image, (0, 0))
            pygame.display.flip()
