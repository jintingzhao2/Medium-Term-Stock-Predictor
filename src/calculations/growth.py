import pandas as pd
import numpy as np


def calculate_absolute_increase(df: pd.DataFrame, y_col: str) -> float:
    series = df[y_col].dropna()
    if series.empty:
        return 0.0
    return series.iloc[-1] - series.iloc[0]


def calculate_percent_increase(df: pd.DataFrame, y_col: str) -> float:
    series = df[y_col].dropna()
    if series.empty or series.iloc[0] == 0:
        return 0.0
    return ((series.iloc[-1] - series.iloc[0]) / np.abs(series.iloc[0])) * 100
