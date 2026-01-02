import pygame

from ui.helpers import draw_title, is_hovered
from ui.ribbon import draw_ribbon
from ui.controls import draw_dropdown, draw_checkbox
# from draw_list import draw_list

# def draw(draw_info, algo_name, ascending):
def draw(draw_info, ui_state, mouse_pos=None):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    draw_title(draw_info)
    
    draw_ribbon(draw_info)
    
    # Algorithms
    draw_dropdown(
        draw_info,
        x=20,
        y=draw_info.TITLE_HEIGHT + 30,
        width=160,
        height=30,
        text=ui_state["algo_left"],
        hovered=ui_state["button_hovered"]["algo_left"],
        clicked=ui_state["button_clicked"]["algo_left"]
    )

    draw_dropdown(
        draw_info,
        x=200,
        y=draw_info.TITLE_HEIGHT + 30,
        width=160,
        height=30,
        text=ui_state["algo_right"],
        hovered=ui_state["button_hovered"]["algo_right"],
        clicked=ui_state["button_clicked"]["algo_right"]
    )

    draw_dropdown(
        draw_info,
        x=20,
        y=draw_info.TITLE_HEIGHT + 80,
        width=100,
        height=30,
        text="Start",
        hovered=ui_state["button_hovered"]["start"],
        clicked=ui_state["button_clicked"]["start"]
    )

    draw_dropdown(
        draw_info,
        x=140,
        y=draw_info.TITLE_HEIGHT + 80,
        width=100,
        height=30,
        text="Reset",
        hovered=ui_state["button_hovered"]["reset"],
        clicked=ui_state["button_clicked"]["reset"]
    )


    # Heat Map
    draw_checkbox(
        draw_info,
        x=400,
        y=draw_info.TITLE_HEIGHT + 35,
        label="Heat Map",
        checked=ui_state["heat_map"],
        hovered=ui_state["button_hovered"]["heat_map"]
    )

    draw_list(draw_info)
    
    pygame.display.update()

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()
