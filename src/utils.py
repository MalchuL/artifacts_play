MOVING_COOLDOWN = 5  # seconds


def estimate_moving_time(x_start, y_start, x_end, y_end):
    """Estimate the time it takes to move from (x_start, y_start) to (x_end, y_end) Calculated
    using the formula based on empirical data."""
    return abs(x_end - x_start) + abs(y_end - y_start)


def calculate_win_probability():
    """
    Example with chicken
    This is turn based fight simulation.
    Turn 1: The character used earth attack and dealt 4 damage.
    Turn 2: The monster used water attack and dealt 4 damage.
    Turn 3: The character used earth attack and dealt 4 damage.
    Turn 4: The monster used water attack and dealt 4 damage.

    If somebody has several attack in row attacks will be applied sequentially.
    Turn 1: The character used earth attack and dealt 4 damage.
    Turn 2: The monster used fire attack and dealt 28 damage.
    Turn 2: The monster used earth attack and dealt 28 damage.
    Turn 2: The monster used water attack and dealt 28 damage.
    Turn 2: The monster used air attack and dealt 28 damage.
    Turn 3: The character used earth attack and dealt 4 damage.
    Turn 4: The monster used fire attack and dealt 28 damage.
    Turn 4: The monster used earth attack and dealt 28 damage.
    :return:
    """
    pass
