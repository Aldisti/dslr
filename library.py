
from datetime import datetime
from functools import wraps
from math import sqrt
from re import match


def to_date(n: int, format: str="%d-%m-%Y") -> str:
    return datetime.fromtimestamp(n).strftime(format)

def to_unix(date: str, format: str="%Y-%m-%d") -> int:
    return datetime.strptime(date, format).timestamp()

def is_num(s: str) -> bool:
    return bool(match(r'^[-+]?\d*\.?\d+([eE][-+]?\d+)?$', s))



def ft_mean(values: list[int|float]) -> float:
    return sum(values) / len(values)

def ft_std(values: list[int|float]) -> float:
    mean = ft_mean(values)
    summation = 0
    for n in values:
        summation += (n - mean) ** 2
    return sqrt(summation / (len(values) - 1))

def ft_min(values: list[int|float]) -> int|float:
    minimum: int|float = values[0]
    for value in values:
        if value < minimum:
            minimum = value
    return minimum

def ft_q(values: list[int|float], perc: float) -> float:
    values = sorted(values)
    index = perc * (len(values) + 1)
    if index.is_integer():
        return values[int(index)]
    i_low = int(index)
    i_high = int(index) + 1
    return values[i_low] + (index - i_low) * (values[i_high] - values[i_low])

def ft_q1(values: list[int|float]) -> float:
    return ft_q(values, 0.25)

def ft_q2(values: list[int|float]) -> float:
    return ft_q(values, 0.5)

def ft_q3(values: list[int|float]) -> float:
    return ft_q(values, 0.75)

def ft_max(values: list[int|float]) -> int|float:
    maximum: int|float = values[0]
    for value in values:
        if value > maximum:
            maximum = value
    return maximum



def normalize_value(value: int|float, max: int|float, min: int|float) -> float:
    return ((value - min) / (max - min))

def normalize_values(values: list[int|float], max: int|float=None, min: int|float=None) -> list[float]:
    max = ft_max(values) if max is None else max
    min = ft_min(values) if min is None else min
    return [normalize_value(value, max, min) for value in values]



def ft_mse(pred_values: list[int|float], obs_values: list[int|float], sort: bool=False) -> float:
    if sort:
        pred_values = sorted(pred_values)
        obs_values = sorted(obs_values)
    count = 0
    summation = 0
    for pred, obs in zip(pred_values, obs_values):
        summation += (obs - pred) ** 2
        count += 1
    return summation / count



def catch(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            print("An error has occurred🤷")
    return wrapper
