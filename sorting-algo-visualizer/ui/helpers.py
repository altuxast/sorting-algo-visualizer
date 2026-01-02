import pygame

def draw_title(draw_info):
    pygame.draw.rect(
        draw_info.window,
        draw_info.BLUE,
        (0, 0, draw_info.width, draw_info.TITLE_HEIGHT)
    )

    title = draw_info.LARGE_FONT.render(
        "Sorting Algorithm Visualizer",
        True,
        draw_info.WHITE
    )

    draw_info.window.blit(
        title,
        (
            draw_info.width // 2 - title.get_width() // 2,
            (draw_info.TITLE_HEIGHT - title.get_height()) // 2
        )
    )

def is_hovered(mouse_pos, x, y, width, height):
    mx, my = mouse_pos
    return x <= mx <= x + width and y <= my <= y + height

def is_clicked(mouse_pos, mouse_pressed, x, y, width, height):
    if is_hovered(mouse_pos, x, y, width, height) and mouse_pressed[0]:
        return True
    return False


