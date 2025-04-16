def linear_spline(x, x_list, y_list):
    n = len(x_list) - 1
    for i in range(n):
        if x_list[i] >= x >= x_list[i + 1] or x_list[i] <= x <= x_list[i + 1]:
            return (
                y_list[i] + (y_list[i + 1] - y_list[i]) * 
                (x - x_list[i]) / (x_list[i + 1] - x_list[i])
            )
    # raise ValueError(f"Точка {x} находится вне диапазона интерполяции")