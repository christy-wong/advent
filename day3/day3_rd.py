from collections import Counter


def power_consumption(raw_data_file: str = "./rays_rd.txt") -> int:
    """
    Produces decimal representation of the product of two 5-bit binary integers
    where the first is the `gamma_rate` and the second is the `epsilon_rate`.
    """
    with open(raw_data_file, "r") as f:
        data = []
        while line := f.readline().rstrip():
            data.append(list(map(int, line)))

    if all(len(row) == len(data[0]) for row in data):
        bits = len(data[0])
    else:
        raise ValueError('Inconsistent bit lengths in input data')

    gamma_rate_lst = [Counter(col).most_common(1)[0][0] for col in list(zip(*data))]
    gamma_rate = sum(j << i for i, j in enumerate(reversed(gamma_rate_lst)))
    epsilon_rate = gamma_rate ^ int('1' * bits, 2)
    return gamma_rate * epsilon_rate


if __name__ == "__main__":
    print(power_consumption())  # Part 1 Solution: 3277364
