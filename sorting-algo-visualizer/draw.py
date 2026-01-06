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
        y=draw_info.TITLE_HEIGHT + 20,
        width=160,
        height=30,
        text=ui_state["algo_left"],
        hovered=ui_state["button_hovered"]["algo_left"],
        clicked=ui_state["button_clicked"]["algo_left"]
    )

    draw_dropdown(
        draw_info,
        x=200,
        y=draw_info.TITLE_HEIGHT + 20,
        width=160,
        height=30,
        text=ui_state["algo_right"],
        hovered=ui_state["button_hovered"]["algo_right"],
        clicked=ui_state["button_clicked"]["algo_right"]
    )

    draw_dropdown(
        draw_info,
        x=20,
        y=draw_info.TITLE_HEIGHT + 70,
        width=100,
        height=30,
        text="Start",
        hovered=ui_state["button_hovered"]["start"],
        clicked=ui_state["button_clicked"]["start"]
    )

    draw_dropdown(
        draw_info,
        x=140,
        y=draw_info.TITLE_HEIGHT + 70,
        width=100,
        height=30,
        text="Reset",
        hovered=ui_state["button_hovered"]["reset"],
        clicked=ui_state["button_clicked"]["reset"]
    )

    draw_dropdown(
        draw_info,
        x=260,
        y=draw_info.TITLE_HEIGHT + 70,
        width=100,
        height=30,
        text="Pause",
        hovered=ui_state["button_hovered"]["pause"],
        clicked=ui_state["button_clicked"]["pause"]
    )

    ascending_button_rect = draw_dropdown(
        draw_info,
        x=380,
        y=draw_info.TITLE_HEIGHT + 70,
        width=120,
        height=30,
        text="Ascending",
        hovered=ui_state["button_hovered"]["ascending"],
        clicked=ui_state["button_clicked"]["ascending"]
    )

    descending_button_rect = draw_dropdown(
        draw_info,
        x=520,
        y=draw_info.TITLE_HEIGHT + 70,
        width=120,
        height=30,
        text="Descending",
        hovered=ui_state["button_hovered"]["descending"],
        clicked=ui_state["button_clicked"]["descending"]
    )

    # Heat Map
    draw_checkbox(
        draw_info,
        x=380,
        y=draw_info.TITLE_HEIGHT + 30,
        label="Heat Map",
        checked=ui_state["heat_map"],
        hovered=ui_state["button_hovered"]["heat_map"]
    )

    draw_list(draw_info)
    
    pygame.display.update()
    return ascending_button_rect, descending_button_rect

def heat_color(t):
    # t is normalized activity in [0, 1]
    
    if t < 0.33:
        # Blue -> Red gradient
        
        return(
            0,
            int(255 * (t / 0.33)),
            255 - int(255 * (t / 0.33))
        )
    elif t < 0.66:
        # Green -> Yellow
        
        t2 = (t - 0.33) / 0.33
        return (
            int(255 * t2),
            255,
            0
        )
    else:
        # Yellow -> Red
        
        t3 = (t - 0.66) / 0.34
        return (
            255,
            255 - int(255 * t3),
            0
        )

def draw_list(draw_info, color_positions={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
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

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()
