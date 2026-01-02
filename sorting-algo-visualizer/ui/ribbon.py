import pygame

def draw_ribbon(draw_info):
    y = draw_info.TITLE_HEIGHT
    
    pygame.draw.rect(
        draw_info.window,
        draw_info.WHITE,
        (0, draw_info.TITLE_HEIGHT, draw_info.width, draw_info.RIBBON_HEIGHT)
    )
