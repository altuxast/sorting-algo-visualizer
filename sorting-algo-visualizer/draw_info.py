import pygame
import math

pygame.init()

class DrawInformation:
    TITLE_HEIGHT = 50
    RIBBON_HEIGHT = 100
    BLACK = 0, 0, 0
    BLUE = 0, 0, 255
    CYAN = 0, 255, 255
    GREEN = 0, 63, 0
    RED = 255, 0, 0
    WHITE = 255, 255, 255
    BACKGROUND_COLOR = CYAN

    GRADIENTS = [
        (127, 95, 255),
        (159, 143, 255),
        (191, 159, 255)
    ]

    FONT = pygame.font.SysFont("courier new", 16)
    LARGE_FONT = pygame.font.SysFont("courier new", 21)

    SIDE_PAD = 100
    TOP_PAD = TITLE_HEIGHT + RIBBON_HEIGHT

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2
