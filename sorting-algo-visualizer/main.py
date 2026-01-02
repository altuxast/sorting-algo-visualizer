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
        "button_hovered": {
            "algo_left": False,
            "algo_right": False,
            "heat_map": False,
            "start": False,
            "reset": False
        },
        "button_clicked": {
            "algo_left": True,   # start with Bubble Sort selected
            "algo_right": False,
            "heat_map": False,
            "start": False,
            "reset": False
        }
    }

    while run:
        clock.tick(120)
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # -------------------------
        # Update hover states
        # -------------------------
        ui_state["button_hovered"]["algo_left"] = is_hovered(mouse_pos, 20, draw_info.TITLE_HEIGHT + 30, 160, 30)
        ui_state["button_hovered"]["algo_right"] = is_hovered(mouse_pos, 200, draw_info.TITLE_HEIGHT + 30, 160, 30)
        ui_state["button_hovered"]["heat_map"] = is_hovered(mouse_pos, 400, draw_info.TITLE_HEIGHT + 35, 20, 20)
        ui_state["button_hovered"]["start"] = is_hovered(mouse_pos, 20, draw_info.TITLE_HEIGHT + 80, 100, 30)
        ui_state["button_hovered"]["reset"] = is_hovered(mouse_pos, 140, draw_info.TITLE_HEIGHT + 80, 100, 30)

        # -------------------------
        # Momentary buttons (Start / Reset)
        # -------------------------
        ui_state["button_clicked"]["start"] = mouse_pressed[0] and ui_state["button_hovered"]["start"]
        ui_state["button_clicked"]["reset"] = mouse_pressed[0] and ui_state["button_hovered"]["reset"]

        # Start / Reset actions
        if mouse_pressed[0] and ui_state["button_hovered"]["start"]:
            ui_state["button_clicked"]["start"] = True
            draw(draw_info, ui_state, mouse_pos)
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
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, ui_state, mouse_pos)

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
                if event.key == pygame.K_r:
                    lst = generate_starting_list(n, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False
                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    sorting_algorithm_generator = sorting_algorithm(draw_info, ui_state["ascending"])
                elif event.key == pygame.K_a and not sorting:
                    ui_state["ascending"] = True
                elif event.key == pygame.K_d and not sorting:
                    ui_state["ascending"] = False
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
