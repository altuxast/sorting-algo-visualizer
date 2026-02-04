import pygame

from draw_info import DrawInformation
from draw import draw
from sorting import bubble_sort, insertion_sort, selection_sort, merge_sort
from utils import generate_starting_list
from ui.helpers import is_hovered
from sorting_registry import ALGORITHM_LIST, ALGORITHMS

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
        "algorithm": "Bubble Sort",
        "heat_map": False,
        "ascending": True,
        "paused": False,
        "button_hovered": {
            "algorithm": False,
            "heat_map": False,
            "start": False,
            "reset": False,
            "pause": False,
            "ascending": False,
            "descending": False,
        },
        "button_clicked": {
            "algorithm": False,
            "heat_map": False,
            "start": False,
            "reset": False,
            "pause": False,
            "ascending": False,
            "descending": False,
        },
        "tooltips": {
            "algorithm": "Select sorting algorithm",
            "start": "Start sorting (Space)",
            "reset": "Reset list (R)",
            "pause": "Pause / Resume (P)",
            "heat_map": "Toggle heat map",
            "ascending": "Sort ascending (A)",
            "descending": "Sort descending (D)",
        },
    }

    # Attach UI state to draw_info so draw_list() can read heat_map
    draw_info.ui_state = ui_state

    ascending_button_rect = None
    descending_button_rect = None

    def handle_algorithm_dropdown_click(ui_state, mouse_pos, draw_info):
        if not ui_state["button_clicked"]["algorithm"]:
            return None  # dropdown is closed

        x = 20
        y = draw_info.TITLE_HEIGHT + 20
        width = 200
        height = 30

        # Each item appears below the main dropdown

        for index, name in enumerate(ALGORITHM_LIST):
            item_rect = pygame.Rect(x, y + (index + 1) * height, width, height)

            if item_rect.collidepoint(mouse_pos):
                return name

        return None

    # ------------
    #  Event Loop
    # ------------
    while run:
        clock.tick(120)
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # ---------------------
        #  Update hover states
        # ---------------------
        ui_state["button_hovered"]["algorithm"] = is_hovered(
            mouse_pos, 20, draw_info.TITLE_HEIGHT + 30, 200, 30
        )
        ui_state["button_hovered"]["heat_map"] = is_hovered(
            mouse_pos, 380, draw_info.TITLE_HEIGHT + 30, 20, 20
        )
        ui_state["button_hovered"]["start"] = is_hovered(
            mouse_pos, 20, draw_info.TITLE_HEIGHT + 80, 100, 30
        )
        ui_state["button_hovered"]["reset"] = is_hovered(
            mouse_pos, 140, draw_info.TITLE_HEIGHT + 80, 100, 30
        )
        ui_state["button_hovered"]["pause"] = is_hovered(
            mouse_pos, 260, draw_info.TITLE_HEIGHT + 80, 100, 30
        )
        ui_state["button_hovered"]["ascending"] = is_hovered(
            mouse_pos, 380, draw_info.TITLE_HEIGHT + 70, 120, 30
        )
        ui_state["button_hovered"]["descending"] = is_hovered(
            mouse_pos, 520, draw_info.TITLE_HEIGHT + 70, 120, 30
        )
        
        # Hover detection for dropdown items
        ui_state["algorithm_hover_index"] = None
        
        if ui_state["button_clicked"]["algorithm"]:
            for i, name in enumerate(ALGORITHM_LIST):
                item_y = draw_info.TITLE_HEIGHT + 20 + (i + 1) * 30
                if is_hovered(mouse_pos, 20, item_y, 200, 30):
                    ui_state["algorithm_hover_index"] = i
                    break

        selected = handle_algorithm_dropdown_click(ui_state, mouse_pos, draw_info)

        if selected:
            ui_state["algorithm"] = selected
            sorting_algorithm = ALGORITHMS[selected]
            ui_state["button_clicked"]["algorithm"] = False

        # -----------------------------------
        #  Momentary buttons (Start / Reset)
        # -----------------------------------
        ui_state["button_clicked"]["start"] = (
            mouse_pressed[0] and ui_state["button_hovered"]["start"]
        )
        ui_state["button_clicked"]["reset"] = (
            mouse_pressed[0] and ui_state["button_hovered"]["reset"]
        )
        ui_state["button_clicked"]["pause"] = (
            mouse_pressed[0] and ui_state["button_hovered"]["pause"]
        )

        # Start / Reset actions
        if mouse_pressed[0] and ui_state["button_hovered"]["start"]:
            ui_state["button_clicked"]["start"] = True
            ascending_button_rect, descending_button_rect = draw(
                draw_info, ui_state, mouse_pos
            )
            pygame.display.update()
            pygame.time.delay(100)
            if not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(
                    draw_info, ui_state["ascending"]
                )
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
            ascending_button_rect, descending_button_rect = draw(
                draw_info, ui_state, mouse_pos
            )

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
                    sorting_algorithm_generator = sorting_algorithm(
                        draw_info, ui_state["ascending"]
                    )
                # Pause
                elif event.key == pygame.K_p and sorting:
                    ui_state["paused"] = not ui_state["paused"]
                # elif event.key == pygame.K_a and not sorting:
                #     ui_state["ascending"] = True
                # elif event.key == pygame.K_d and not sorting:
                #     ui_state["ascending"] = False
                elif event.key == pygame.K_b and not sorting:
                    ui_state["algorithm"] = "Bubble Sort"
                    sorting_algorithm = bubble_sort

                elif event.key == pygame.K_i and not sorting:
                    ui_state["algorithm"] = "Insertion Sort"
                    sorting_algorithm = insertion_sort

                elif event.key == pygame.K_s and not sorting:
                    ui_state["algorithm"] = "Selection Sort"
                    sorting_algorithm = selection_sort

                elif event.key == pygame.K_m and not sorting:
                    ui_state["algorithm"] = "Merge Sort"
                    sorting_algorithm = merge_sort

            # -------------------------
            # Mouse clicks (sticky buttons)
            # -------------------------
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Ascending / Descending
                if ascending_button_rect and ascending_button_rect.collidepoint(
                    mouse_pos
                ):
                    ui_state["ascending"] = True
                    ui_state["button_clicked"]["ascending"] = True
                    ui_state["button_clicked"]["descending"] = False

                if descending_button_rect and descending_button_rect.collidepoint(
                    mouse_pos
                ):
                    ui_state["ascending"] = False
                    ui_state["button_clicked"]["ascending"] = False
                    ui_state["button_clicked"]["descending"] = True

                # Pause toggle
                if ui_state["button_hovered"]["pause"] and sorting:
                    ui_state["paused"] = not ui_state["paused"]

                # Algorithm dropdown
                if ui_state["button_hovered"]["algorithm"]:
                    ui_state["button_clicked"]["algorithm"] = not ui_state[
                        "button_clicked"
                    ]["algorithm"]

                # Heat map toggle
                elif ui_state["button_hovered"]["heat_map"]:
                    ui_state["heat_map"] = not ui_state["heat_map"]

    pygame.quit()


if __name__ == "__main__":
    main()
