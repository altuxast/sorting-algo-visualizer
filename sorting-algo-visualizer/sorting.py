from draw import draw_list
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
