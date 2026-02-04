import pygame

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (
            draw_info.SIDE_PAD // 2,
            draw_info.TOP_PAD,
            draw_info.width - draw_info.SIDE_PAD,
            draw_info.height - draw_info.TOP_PAD,
        )
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        # Heat Map Coloring
        if draw_info.ui_state.get("heat_map", False):
            max_act = max(draw_info.activity) or 1
            t = draw_info.activity[i] / max_act
            color = heat_color(t)

        else:
            color = draw_info.GRADIENTS[i % 3]

        # Sorting algorithm highlight overrides heat map
        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(
            draw_info.window, color, (x, y, draw_info.block_width, draw_info.height)
        )

    if clear_bg:
        pygame.display.update()

def heat_color(t):
    # t is normalized activity in [0, 1]

    if t < 0.33:
        # Blue -> Red gradient

        return (0, int(255 * (t / 0.33)), 255 - int(255 * (t / 0.33)))
    elif t < 0.66:
        # Green -> Yellow

        t2 = (t - 0.33) / 0.33
        return (int(255 * t2), 255, 0)
    else:
        # Yellow -> Red

        t3 = (t - 0.66) / 0.34
        return (255, 255 - int(255 * t3), 0)