import swapeng.swapeng016.swapcore as swapcore
import pygame
from pygame.constants import *
import pickle
import random
import time
import os
import sys
from os import path


RUNNING = True
PROGRAM_WIDTH, PROGRAM_HEIGHT = 1280, 720
WIDTH, HEIGHT = 1280, 720
PROGRAM_DIMENSIONS = (PROGRAM_WIDTH, PROGRAM_HEIGHT)


pygame.init()
pygame.mixer.init(22050, -16, 2, 4096)
screen = pygame.display.set_mode(PROGRAM_DIMENSIONS)
pygame.display.set_caption("Darwin's Nightmare")
