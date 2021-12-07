import numpy as np
import pandas as pd

POSITIVE_DIRECTIONS = ["forward", "down"]
NEGATIVE_DIRECTIONS = ["up"]
DEPTH_DIRECTIONS = ["down", "up"]


def direction_translation(row: pd.Series) -> int:
    """
    Translates the 'direction', 'steps' pair into an integer counting the
    directional steps taken
    """
    direction_flag = 0
    if row["direction"] in POSITIVE_DIRECTIONS:
        direction_flag += 1
    elif row["direction"] in NEGATIVE_DIRECTIONS:
        direction_flag -= 1
    else:
        raise ValueError("Invalid direction")
    return direction_flag * row["steps"]


def multiply_ending_coordinates(
    raw_data_file: str = "./moves_rd.txt", is_aim: bool = False
) -> int:
    """
    Multiplies ending coordinates of submarine based on path provided in
    `raw_data_file`
    """
    df = pd.read_csv(raw_data_file, delim_whitespace=True, names=["direction", "steps"])

    if not is_aim:
        df["direction_type"] = np.where(
            df["direction"].isin(DEPTH_DIRECTIONS), "depth", "horizontal"
        )
        df["directional_steps"] = df.apply(direction_translation, axis=1)
        ending_coordinates = df.groupby("direction_type")["directional_steps"].sum()

    else:
        df["aim_change"] = df["steps"] * (
            (df["direction"] == "up") * -1 + (df["direction"] == "down") * 1
        )
        df["cumul_aim"] = df["aim_change"].cumsum()
        df["horizontal"] = (
            (df["direction"] == "forward") * df["steps"]
        ).cumsum()
        df["depth"] = (
            (df["direction"] == "forward") * df["cumul_aim"] * df['steps']
        ).cumsum()
        ending_coordinates = df.tail(1)[['depth', 'horizontal']]

    return (ending_coordinates["depth"] * ending_coordinates["horizontal"]).item()


if __name__ == "__main__":
    print(multiply_ending_coordinates())  # Part 1 Solution: 2036120
    print(multiply_ending_coordinates(is_aim=True))  # Part 2 Solution: 2015547716
