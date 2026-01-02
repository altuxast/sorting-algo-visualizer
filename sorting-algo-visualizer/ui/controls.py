import pygame

def draw_dropdown(draw_info, x, y, width, height, text, hovered=False, clicked=False):
    if clicked:
        color_bg = (255, 0, 0)
    elif hovered:
        color_bg = (200, 200, 200)
    else:
        color_bg = draw_info.WHITE

    pygame.draw.rect(draw_info.window, color_bg, (x, y, width, height))
    pygame.draw.rect(draw_info.window, draw_info.BLACK, (x, y, width, height), 2)

    label = draw_info.FONT.render(text, True, draw_info.BLACK)
    draw_info.window.blit(label, (x + 10, y + 8))


def draw_checkbox(draw_info, x, y, label, checked, hovered=False):
    box_size = 20

    bg_color = (220, 220, 220) if hovered else draw_info.WHITE
    pygame.draw.rect(draw_info.window, bg_color, (x, y, box_size, box_size))

    pygame.draw.rect(draw_info.window, draw_info.BLACK, (x, y, box_size, box_size), 2)

    if checked:
        pygame.draw.line(draw_info.window, draw_info.GREEN, (x, y), (x + box_size, y + box_size), 3)
        pygame.draw.line(draw_info.window, draw_info.GREEN, (x + box_size, y), (x, y + box_size), 3)

    text = draw_info.FONT.render(label, True, draw_info.BLACK)
    draw_info.window.blit(text, (x + box_size + 5, y))

