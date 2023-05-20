import random
import pandas as pd


def change_value(x, percentage):
    # dla stringow zmieniamy litery, dla liczb wartosci
    if isinstance(x, str):
        modified_x = ""
        for char in x:
            if random.random() <= percentage / 100:
                char = random.choice("abcdefghijklmnopqrstuvwxyz")
            modified_x += char
        return modified_x
    else:
        change = x * percentage / 100
        return x + random.choice([-1, 1]) * change


# zwraca wejsciowy dataframe z wartosciami zmienionymi o +-percentage procent
def apply_change(df: pd.DataFrame, percentage: float) -> pd.DataFrame:
    df_modified = df.copy()
    for column in df.columns:
        df_modified[column] = df_modified[column].apply(
            lambda x: change_value(x, percentage)
        )
    return df_modified
