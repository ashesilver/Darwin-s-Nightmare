import platform
import threading
# import zipfile
import pickle
import time
import os
import swapcore
from swapcore.constants import *
import pygame
from pygame.constants import *


pygame.init()

PROGRAM_DIMENSIONS = (DEFAULT_PROGRAM_WIDTH, DEFAULT_PROGRAM_HEIGHT)

platform_system = platform.system()
if platform_system == 'Windows':
    import win32api  # win32gui, win32con
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()  # solves dpi scaling problems on Windows

    work_area = win32api.GetMonitorInfo(win32api.EnumDisplayMonitors()[0][0])['Work']
    # work_area: (x, y, z, t), the screen area minus the area of the taskbar

    # SM_CXPADDEDBORDER = 92
    # SM_CYCAPTION = 4
    caption_height = win32api.GetSystemMetrics(92) + \
                     win32api.GetSystemMetrics(4)

    min_screen_width, min_screen_height, max_screen_width, max_screen_height = work_area
    PROGRAM_DIMENSIONS = (max_screen_width - min_screen_width,
                          max_screen_height - min_screen_height - caption_height)

    program_x, program_y = min_screen_width, min_screen_height + caption_height

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (program_x, program_y)

# constants
FPS = 60
RUNNING = True
PROGRAM_DIMENSIONS = (DEFAULT_PROGRAM_WIDTH, DEFAULT_PROGRAM_HEIGHT)
PROGRAM_WIDTH, PROGRAM_HEIGHT = PROGRAM_DIMENSIONS
RUNDIR_PATH = os.path.dirname(os.path.abspath(__file__))
RUNDIR = os.path.basename(RUNDIR_PATH)  # rundir: run directory

# create the window
screen = pygame.display.set_mode(PROGRAM_DIMENSIONS)
pygame.display.set_caption("*map.swptm - %s - %s" % (RUNDIR_PATH, RUNDIR))
clock = pygame.time.Clock()
