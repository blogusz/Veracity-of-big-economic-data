import math
import numpy as np
import pandas as pd
from datetime import datetime
import Levenshtein


# dokladnosc
def correctness(w_I, w_R, alpha=0.5):  # alfa (>0)moze dosc istotnie namieszac i niestety jest ustalana troche na oko (ze wzgledu na to, jak istotne jest dokladne rozroznienie wartosci w_I od w_R). Dodatkowo dochodzi kwestia interpretacji wyniku, bo np jezeli zmienne sa roznych znakow, to metryka wychodzi ujemna, co nie powinno miec miejsca
    if isinstance(w_I, str) and isinstance(w_R, str):
        # dla slow liczona jest odleglosc Levenshteina
        return 1 - Levenshtein.distance(w_I, w_R) / max(len(w_I), len(w_R))
    else:
        # metryka z literatury
        return 1-math.pow(abs(w_I - w_R) / max(abs(w_I), abs(w_R)), alpha)

# aktualnosc


def timeliness(w: datetime, decline=1):  # ma to odzwierciedlac metryke z literatury. Problemem jest ustalenie wartosci decline (robi sie to na oko, nie liczac pewniakow, kiedy decline=0 lub 1) oraz ustalenie wieku zmiennej (musimy miec np. podana date danego odczytu lub wiedziec z kiedy pochodza dane)
    current_date = datetime.now()
    # obecnie zakladamy, ze mierzona zmienna jest data
    last_update = datetime.strptime(w, "%Y-%m-%d")
    age = (current_date - last_update).days

    return math.exp(-decline * age)

# kompletnosc


# zlicza brakujace wartosci.
def completeness(data: pd.DataFrame, attribute: str):
    data = data.replace('', np.nan)

    return 1-data[attribute].isna().sum().sum()/len(data)

# unikalnosc


def uniqueness(data: pd.DataFrame):
    total_rows = len(data)
    unique_rows = len(data.drop_duplicates())
    # uniqueness_ratio = 1 - (unique_rows/total_rows)
    uniqueness_ratio = unique_rows/total_rows

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
    # 1.aktualnosc
    print(timeliness("2023-05-18"))

    # 2.kompletnosc
    data = pd.DataFrame({
        'name': ['John', 'Emily', 'Michael', 'Sarah'],
        'age': ['a', np.nan, 'b', '']
    })
    print(completeness(data, 'age'))

    # 3.dokladnosc
    w_I = 'Eissonhour'
    w_R = 'Eisenhower'
    print(correctness(w_I, w_R))

    w_I = 80000
    w_R = 79200
    print(correctness(w_I, w_R))

    # 4.unikalnosc
    data = pd.DataFrame({
        'name': ['John', 'Emily', 'John', 'Michael', 'Sarah'],
        'age': [25, 30, 25, 35, 30]
    })
    print(uniqueness(data))
