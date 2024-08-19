def distance_location(x_start, y_start, x_end, y_end):
    """
    Estimate distance from (x_start, y_start) to (x_end, y_end)
    """
    return abs(x_end - x_start) + abs(y_end - y_start)
