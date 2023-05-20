import string
import math
import random
import numpy as np
import pandas as pd
from datetime import datetime
import Levenshtein
import os
import sys

from data_utils.modify_df import apply_change


# alfa (>0)moze dosc istotnie namieszac i niestety jest ustalana troche na oko (ze wzgledu na to, jak istotne jest dokladne rozroznienie wartosci w_I od w_R). Dodatkowo dochodzi kwestia interpretacji wyniku, bo np jezeli zmienne sa roznych znakow, to metryka wychodzi ujemna, co nie powinno miec miejsca.
def correctness(
    df_og: pd.DataFrame, df_test: pd.DataFrame, alpha: float = 1
) -> pd.DataFrame:
    results = []

    for column in df_og.columns:
        w_I = df_test[column]
        w_R = df_og[column]

        # dla slow liczona jest odleglosc Levenshteina
        if isinstance(w_I[0], str) and isinstance(w_R[0], str):
            correctness = [
                1 - Levenshtein.distance(wi, wr) / max(len(wi), len(wr))
                for wi, wr in zip(w_I, w_R)
            ]
        else:
            # metryka z literatury
            correctness = [
                1 - math.pow(abs(wi - wr) / max(abs(wi), abs(wr)), alpha)
                for wi, wr in zip(w_I, w_R)
            ]

        results.append(correctness)

    results = pd.DataFrame(results).transpose()
    results.columns = df_og.columns

    return results


# ma to odzwierciedlac metryke z literatury. Problemem jest ustalenie wartosci decline (robi sie to na oko, nie liczac pewniakow, kiedy decline=0 lub 1) oraz ustalenie wieku zmiennej (musimy miec np. podana date danego odczytu lub wiedziec z kiedy pochodza dane).
def timeliness(w: datetime, decline=1) -> float:
    current_date = datetime.now()
    # obecnie zakladamy, ze mierzona zmienna jest data
    last_update = datetime.strptime(w, "%Y-%m-%d")
    age = (current_date - last_update).days

    return math.exp(-decline * age)


# liczy kompletnosc danych dla kazdej kolumny
def completeness(data: pd.DataFrame, attribute: str) -> list:
    data = data.replace("", np.nan)

    return 1 - data[attribute].isna().sum().sum() / len(data)


# zlicza wspolczynnik unikalnych wierszy
def uniqueness(data: pd.DataFrame) -> float:
    total_rows = len(data)
    unique_rows = len(data.drop_duplicates())
    # uniqueness_ratio = 1 - (unique_rows/total_rows)
    uniqueness_ratio = unique_rows / total_rows

    return uniqueness_ratio


# spojnosc
# def consistency(): # 'Number of inconsistent units / Total number of consistency checks performed'
# bez konkretnego zbioru danych implementacja tej metryki jest niemozliwa/bezsensowna, bo na spojnosc skladaja sie rozne reguly zadane dla konkretnych danych (np sprawdzenie, czy numer telefonu ma 9 cyfr).


# poprawnosc
# def validity(): # 'kappa coefficient'
# cecha ta moze byc przydatna przy ocenie zgodnosci wartosci przewidywanych z wartosciami rzeczywistymi.


# stosownosc
# def relevance(): # 'ISO/IEC 25024'
# ponownie bez konkretnego zbioru danych zdefiniowanie tej metryki jest bezcelowe.


if __name__ == "__main__":
    df = pd.read_csv("data.csv")

    # # 1.aktualnosc
    print(timeliness("2023-05-18"))

    # 2.kompletnosc
    for col in df.columns:
        print(completeness(df, col))

    # 3.dokladnosc
    # pobieramy ramke ze zmienionymi wartosciami o +-10%
    df_modified = apply_change(df, 10)
    df_modified.to_csv("data_modified.csv", index=False)

    correctness(df, df_modified).to_csv("correct_data.csv", index=False)

    # 4.unikalnosc
    unique = uniqueness(df)
    print(unique)
