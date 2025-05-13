import pygame
import os

PATH_IMG = "img/"
def load_image(path):
    img = pygame.image.load(PATH_IMG + path).convert_alpha()

    return img


def load_images(path):
    imgs = []

    for i in os.listdir(PATH_IMG + path):
        imgs.append(load_image(path + '/' + i))

    return imgs