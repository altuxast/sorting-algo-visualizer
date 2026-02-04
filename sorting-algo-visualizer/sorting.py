from utils_draw import draw_list
from draw_info import DrawInformation


def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            # Mark activity for comparison
            draw_info.activity[j] += 1
            draw_info.activity[j + 1] += 1

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]

                # Mark activity for swap
                draw_info.activity[j] += 2
                draw_info.activity[j + 1] += 2

                draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
                yield True

    return lst


def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        # Mark initial touch
        draw_info.activity[i] += 1

        j = i
        while True:
            ascending_sort = j > 0 and lst[j - 1] > current and ascending
            descending_sort = j > 0 and lst[j - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            # Mark activity for comparison
            draw_info.activity[j] += 1
            draw_info.activity[j - 1] += 1

            lst[j] = lst[j - 1]
            j -= 1
            lst[j] = current

            # Mark activity for shift
            draw_info.activity[j] += 2
            if j + 1 < len(lst):
                draw_info.activity[j + 1] += 2

            draw_list(draw_info, {j - 1: draw_info.GREEN, j: draw_info.RED}, True)
            yield True

    return lst


def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    n = len(lst)

    for i in range(n):
        min_or_max_idx = i

        for j in range(i + 1, n):
            # Mark comparison activity
            draw_info.activity[j] += 1
            draw_info.activity[min_or_max_idx] += 1

            if (lst[j] < lst[min_or_max_idx] and ascending) or (
                lst[j] > lst[min_or_max_idx] and not ascending
            ):
                min_or_max_idx = j

            # Highlight comparison
            draw_list(
                draw_info, {j: draw_info.BLUE, min_or_max_idx: draw_info.RED}, True
            )
            yield True

        # Swap
        lst[i], lst[min_or_max_idx] = lst[min_or_max_idx], lst[i]

        # Mark swap activity
        draw_info.activity[i] += 2
        draw_info.activity[min_or_max_idx] += 2

        draw_list(draw_info, {i: draw_info.GREEN, min_or_max_idx: draw_info.RED}, True)
        yield True

    return lst


def merge_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def merge_sort_recursive(start, end):
        if end - start <= 1:
            return

        mid = (start + end) // 2
        yield from merge_sort_recursive(start, mid)
        yield from merge_sort_recursive(mid, end)

        # Merge step
        left = lst[start:mid]
        right = lst[mid:end]

        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            draw_info.activity[k] += 1
        
            if (left[i] <= right[j] and ascending) or (
                left[i] >= right[j] and not ascending
            ):
                lst[k] = left[i]
                i += 1
            else:
                lst[k] = right[j]
                j += 1
        
            draw_list(draw_info, {k: draw_info.RED}, True)
            yield True          # ← you were missing this
            k += 1              # ← and this

        # Remaining left
        while i < len(left):
            lst[k] = left[i]
            draw_info.activity[k] += 1
            draw_list(draw_info, {k: draw_info.GREEN}, True)
            yield True
            i += 1
            k += 1
            
        # Remaining right
        while j < len(right):
            lst[k] = right[j]
            draw_info.activity[k] += 1
            draw_list(draw_info, {k: draw_info.GREEN}, True)
            yield True
            j += 1
            k += 1
    
    # Kick off recursion
    yield from merge_sort_recursive(0, len(lst))
    return lst
