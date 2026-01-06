import pygame

from draw_info import DrawInformation
from draw import draw
from sorting import bubble_sort, insertion_sort
from utils import generate_starting_list
from ui.helpers import is_hovered

def main():
    pygame.init()
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    
    sorting = False
    sorting_algorithm = bubble_sort
    sorting_algorithm_generator = None

    # UI state
    ui_state = {
        "algo_left": "Bubble Sort",
        "algo_right": "Insertion Sort",
        "heat_map": False,
        "ascending": True,
        "paused": False,
        "button_hovered": {
            "algo_left": False,
            "algo_right": False,
            "heat_map": False,
            "start": False,
            "reset": False,
            "pause": False,
            "ascending": False,
            "descending": False
        },
        "button_clicked": {
            "algo_left": True,   # start with Bubble Sort selected
            "algo_right": False,
            "heat_map": False,
            "start": False,
            "reset": False,
            "pause": False,
            "ascending": False,
            "descending": False
        },
        "tooltips": {
            "algo_left": "Select Bubble Sort (B)",
            "algo_right": "Select Insertion Sort (I)",
            "start": "Start sorting (Space)",
            "reset": "Reset list (R)",
            "pause": "Pause / Resume (P)",
            "heat_map": "Toggle heat map",
            "ascending": "Sort ascending (A)",
            "descending": "Sort descending (D)"            
        }
    }
    
    # Attach UI state to draw_info so draw_list() can read heat_map
    draw_info.ui_state = ui_state

    ascending_button_rect = None
    descending_button_rect = None
    
    while run:
        clock.tick(120)
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # -------------------------
        # Update hover states
        # -------------------------
        ui_state["button_hovered"]["algo_left"] = is_hovered(mouse_pos, 20, draw_info.TITLE_HEIGHT + 30, 160, 30)
        ui_state["button_hovered"]["algo_right"] = is_hovered(mouse_pos, 200, draw_info.TITLE_HEIGHT + 30, 160, 30)
        ui_state["button_hovered"]["heat_map"] = is_hovered(mouse_pos, 380, draw_info.TITLE_HEIGHT + 30, 20, 20)
        ui_state["button_hovered"]["start"] = is_hovered(mouse_pos, 20, draw_info.TITLE_HEIGHT + 80, 100, 30)
        ui_state["button_hovered"]["reset"] = is_hovered(mouse_pos, 140, draw_info.TITLE_HEIGHT + 80, 100, 30)
        ui_state["button_hovered"]["pause"] = is_hovered(mouse_pos, 260, draw_info.TITLE_HEIGHT + 80, 100, 30)
        ui_state["button_hovered"]["ascending"] = is_hovered(mouse_pos, 380, draw_info.TITLE_HEIGHT + 70, 120, 30)
        ui_state["button_hovered"]["descending"] = is_hovered(mouse_pos, 520, draw_info.TITLE_HEIGHT + 70, 120, 30)

        # -------------------------
        # Momentary buttons (Start / Reset)
        # -------------------------
        ui_state["button_clicked"]["start"] = mouse_pressed[0] and ui_state["button_hovered"]["start"]
        ui_state["button_clicked"]["reset"] = mouse_pressed[0] and ui_state["button_hovered"]["reset"]
        ui_state["button_clicked"]["pause"] = mouse_pressed[0] and ui_state["button_hovered"]["pause"]
        
        # Start / Reset actions
        if mouse_pressed[0] and ui_state["button_hovered"]["start"]:
            ui_state["button_clicked"]["start"] = True
            ascending_button_rect, descending_button_rect = draw(draw_info, ui_state, mouse_pos)
            pygame.display.update()
            pygame.time.delay(100)
            if not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ui_state["ascending"])
        else:
            ui_state["button_clicked"]["start"] = False
        if ui_state["button_clicked"]["reset"]:
            lst = generate_starting_list(n, min_val, max_val)
            draw_info.set_list(lst)
            sorting = False

        # -------------------------
        # Sorting step
        # -------------------------
        if sorting and not ui_state["paused"]:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            ascending_button_rect, descending_button_rect = draw(draw_info, ui_state, mouse_pos)

        # -------------------------
        # Event handling
        # -------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # -------------------------
            # Keyboard shortcuts
            # -------------------------
            if event.type == pygame.KEYDOWN:
                # Reset
                if event.key == pygame.K_r:
                    lst = generate_starting_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False
                # Start
                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    sorting_algorithm_generator = sorting_algorithm(draw_info, ui_state["ascending"])
                # Pause
                elif event.key == pygame.K_p and sorting:
                    ui_state["paused"] = not ui_state["paused"]
                # elif event.key == pygame.K_a and not sorting:
                #     ui_state["ascending"] = True
                # elif event.key == pygame.K_d and not sorting:
                #     ui_state["ascending"] = False
                elif event.key == pygame.K_b and not sorting:
                    sorting_algorithm = bubble_sort
                    ui_state["button_clicked"]["algo_left"] = True
                    ui_state["button_clicked"]["algo_right"] = False
                    ui_state["algo_left"] = "Bubble Sort"
                elif event.key == pygame.K_i and not sorting:
                    sorting_algorithm = insertion_sort
                    ui_state["button_clicked"]["algo_left"] = False
                    ui_state["button_clicked"]["algo_right"] = True
                    ui_state["algo_right"] = "Insertion Sort"

            # -------------------------
            # Mouse clicks (sticky buttons)
            # -------------------------
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if ascending_button_rect and ascending_button_rect.collidepoint(mouse_pos):
                    ui_state["ascending"] = True
                    ui_state["button_clicked"]["ascending"] = True
                    ui_state["button_clicked"]["descending"] = False
                if descending_button_rect and descending_button_rect.collidepoint(mouse_pos):
                    ui_state["ascending"] = False
                    ui_state["button_clicked"]["ascending"] = False
                    ui_state["button_clicked"]["descending"] = True
                # Pause toggle
                if ui_state["button_hovered"]["pause"] and sorting:
                    ui_state["paused"] = not ui_state["paused"]
                # Bubble Sort
                if ui_state["button_hovered"]["algo_left"]:
                    ui_state["button_clicked"]["algo_left"] = True
                    ui_state["button_clicked"]["algo_right"] = False
                    sorting_algorithm = bubble_sort
                    ui_state["algo_left"] = "Bubble Sort"
                # Insertion Sort
                elif ui_state["button_hovered"]["algo_right"]:
                    ui_state["button_clicked"]["algo_left"] = False
                    ui_state["button_clicked"]["algo_right"] = True
                    sorting_algorithm = insertion_sort
                    ui_state["algo_right"] = "Insertion Sort"
                # Heat map toggle
                elif ui_state["button_hovered"]["heat_map"]:
                    ui_state["heat_map"] = not ui_state["heat_map"]

    pygame.quit()


if __name__ == "__main__":
    main()
