import pygame

from ui.helpers import draw_title, is_hovered
from ui.ribbon import draw_ribbon
from ui.controls import draw_dropdown, draw_checkbox, draw_tooltip
from sorting_registry import ALGORITHM_LIST
from utils_draw import draw_list

# from draw_list import draw_list


# def draw(draw_info, algo_name, ascending):
def draw(draw_info, ui_state, mouse_pos=None):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    draw_title(draw_info)

    draw_ribbon(draw_info)

    # Algorithms
    dropdown_rect, item_rects = draw_dropdown(
        draw_info,
        x=20,
        y=draw_info.TITLE_HEIGHT + 20,
        width=200,
        height=30,
        text=ui_state["algorithm"],
        hovered=ui_state["button_hovered"]["algorithm"],
        clicked=ui_state["button_clicked"]["algorithm"],
        items=ALGORITHM_LIST,
        hovered_index=ui_state.get("algorithm_hover_index")
    )

    draw_dropdown(
        draw_info,
        x=20,
        y=draw_info.TITLE_HEIGHT + 70,
        width=100,
        height=30,
        text="Start",
        hovered=ui_state["button_hovered"]["start"],
        clicked=ui_state["button_clicked"]["start"],
    )

    draw_dropdown(
        draw_info,
        x=140,
        y=draw_info.TITLE_HEIGHT + 70,
        width=100,
        height=30,
        text="Reset",
        hovered=ui_state["button_hovered"]["reset"],
        clicked=ui_state["button_clicked"]["reset"],
    )

    draw_dropdown(
        draw_info,
        x=260,
        y=draw_info.TITLE_HEIGHT + 70,
        width=100,
        height=30,
        text="Pause",
        hovered=ui_state["button_hovered"]["pause"],
        clicked=ui_state["button_clicked"]["pause"],
    )

    ascending_button_rect, _ = draw_dropdown(
        draw_info,
        x=380,
        y=draw_info.TITLE_HEIGHT + 70,
        width=120,
        height=30,
        text="Ascending",
        hovered=ui_state["button_hovered"]["ascending"],
        clicked=ui_state["button_clicked"]["ascending"],
    )

    descending_button_rect, _ = draw_dropdown(
        draw_info,
        x=520,
        y=draw_info.TITLE_HEIGHT + 70,
        width=120,
        height=30,
        text="Descending",
        hovered=ui_state["button_hovered"]["descending"],
        clicked=ui_state["button_clicked"]["descending"],
    )

    # Heat Map
    draw_checkbox(
        draw_info,
        x=380,
        y=draw_info.TITLE_HEIGHT + 30,
        label="Heat Map",
        checked=ui_state["heat_map"],
        hovered=ui_state["button_hovered"]["heat_map"],
    )

    draw_list(draw_info)

    # Tooltips
    if mouse_pos is not None:
        hovered_key = None
        for key, hovered in ui_state["button_hovered"].items():
            if hovered:
                hovered_key = key
                break
        if hovered_key:
            text = ui_state.get("tooltips", {}).get(hovered_key)
            if text:
                draw_tooltip(draw_info, text, mouse_pos)

    pygame.display.update()
    return ascending_button_rect, descending_button_rect, item_rects

