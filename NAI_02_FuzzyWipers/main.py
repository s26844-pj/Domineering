"""
NAI - Narzędzia Sztucznej Inteligencji
Zadanie 1 - System wykorzystujący logikę rozmytą

Temat:
Inteligentne sterowanie wycieraczkami samochodowymi.

Autorzy:
- Łukasz Dahm
- Michał Kujawa

Opis:
Program wykorzystuje logikę rozmytą do określenia prędkości
pracy wycieraczek samochodowych.

System posiada trzy wejścia:
1. Natężenie deszczu: 0-100 %
2. Prędkość samochodu: 0-140 km/h
3. Widoczność: 0-100 %

System posiada jedno wyjście:
- Prędkość wycieraczek: 0-100 %

Program wykonuje:
1. Fuzzification - rozmywanie wartości wejściowych.
2. Zastosowanie reguł IF-THEN.
3. Operacje rozmyte AND i OR.
4. Defuzzification - obliczenie jednej konkretnej wartości wyjściowej.

Środowisko:
- Python 3
- Tkinter

Uruchomienie:
python3 main.py
"""


# Importujemy bibliotekę tkinter.
# Dzięki niej możemy stworzyć okno programu oraz suwaki.
import tkinter as tk


# ---------------------------------------------------------
# FUNKCJE PRZYNALEŻNOŚCI - MEMBERSHIP FUNCTIONS
# ---------------------------------------------------------


def low_membership(value, maximum):
    """
    Oblicza stopień przynależności wartości do zbioru LOW.

    Args:
        value: Aktualna wartość wejściowa.
        maximum: Maksymalna wartość dla danej zmiennej.

    Returns:
        Liczbę od 0 do 1 określającą,
        jak bardzo dana wartość jest niska.
    """

    # Wyliczamy połowę całego zakresu.
    half = maximum / 2

    # Jeżeli wartość jest na początku skali,
    # uznajemy ją całkowicie za niską.
    if value <= 0:
        return 1.0

    # Jeżeli wartość przekroczyła połowę skali,
    # nie uznajemy jej już za niską.
    if value >= half:
        return 0.0

    # Pomiędzy 0 a połową skali
    # stopień przynależności stopniowo maleje.
    return 1 - (value / half)


def medium_membership(value, maximum):
    """
    Oblicza stopień przynależności wartości do zbioru MEDIUM.

    Args:
        value: Aktualna wartość wejściowa.
        maximum: Maksymalna wartość dla danej zmiennej.

    Returns:
        Liczbę od 0 do 1 określającą,
        jak bardzo dana wartość jest średnia.
    """

    # Wyliczamy środek zakresu.
    half = maximum / 2

    # Jeżeli jesteśmy przed środkiem skali...
    if value <= half:

        # ...przynależność do MEDIUM stopniowo rośnie.
        return value / half

    # Jeżeli jesteśmy za środkiem skali...
    else:

        # ...przynależność do MEDIUM stopniowo maleje.
        return (maximum - value) / half


def high_membership(value, maximum):
    """
    Oblicza stopień przynależności wartości do zbioru HIGH.

    Args:
        value: Aktualna wartość wejściowa.
        maximum: Maksymalna wartość dla danej zmiennej.

    Returns:
        Liczbę od 0 do 1 określającą,
        jak bardzo dana wartość jest wysoka.
    """

    # Wyliczamy środek zakresu.
    half = maximum / 2

    # Wartości poniżej połowy
    # nie traktujemy jako wysokich.
    if value <= half:
        return 0.0

    # Maksymalna wartość jest całkowicie HIGH.
    if value >= maximum:
        return 1.0

    # Pomiędzy połową i maksimum
    # przynależność do HIGH stopniowo rośnie.
    return (value - half) / half


# ---------------------------------------------------------
# GŁÓWNY SYSTEM LOGIKI ROZMYTEJ
# ---------------------------------------------------------


def fuzzy_wipers(rain, speed, visibility):
    """
    Oblicza prędkość wycieraczek za pomocą logiki rozmytej.

    Args:
        rain: Natężenie deszczu w zakresie 0-100 %.
        speed: Prędkość samochodu w zakresie 0-140 km/h.
        visibility: Widoczność w zakresie 0-100 %.

    Returns:
        Prędkość pracy wycieraczek w zakresie 0-100 %.
    """

    # -----------------------------------------------------
    # KROK 1 - FUZZIFICATION
    # -----------------------------------------------------
    #
    # Zamieniamy konkretne liczby na stopnie
    # przynależności do zbiorów rozmytych.


    # Sprawdzamy, jak bardzo deszcz jest mały.
    rain_low = low_membership(rain, 100)

    # Sprawdzamy, jak bardzo deszcz jest średni.
    rain_medium = medium_membership(rain, 100)

    # Sprawdzamy, jak bardzo deszcz jest duży.
    rain_high = high_membership(rain, 100)


    # Sprawdzamy, jak bardzo prędkość jest mała.
    speed_low = low_membership(speed, 140)

    # Sprawdzamy, jak bardzo prędkość jest średnia.
    speed_medium = medium_membership(speed, 140)

    # Sprawdzamy, jak bardzo prędkość jest duża.
    speed_high = high_membership(speed, 140)


    # Mała wartość widoczności oznacza słabą widoczność.
    visibility_poor = low_membership(visibility, 100)

    # Środkowa wartość oznacza średnią widoczność.
    visibility_medium = medium_membership(visibility, 100)

    # Duża wartość oznacza dobrą widoczność.
    visibility_good = high_membership(visibility, 100)


    # -----------------------------------------------------
    # KROK 2 - REGUŁY IF-THEN
    # -----------------------------------------------------


    # REGUŁA 1:
    # IF rain is LOW
    # THEN wiper speed is VERY LOW.
    rule1 = rain_low
    output1 = 10


    # REGUŁA 2:
    # IF rain is MEDIUM
    # THEN wiper speed is MEDIUM.
    rule2 = rain_medium
    output2 = 50


    # REGUŁA 3:
    # IF rain is HIGH
    # THEN wiper speed is HIGH.
    rule3 = rain_high
    output3 = 85


    # REGUŁA 4:
    # IF visibility is POOR
    # THEN wiper speed is HIGH.
    rule4 = visibility_poor
    output4 = 70


    # Łączymy średni i duży deszcz.
    #
    # max() reprezentuje tutaj operator OR.
    rain_not_low = max(rain_medium, rain_high)


    # REGUŁA 5:
    # IF speed is HIGH
    # AND rain is MEDIUM OR HIGH
    # THEN wiper speed is VERY HIGH.
    #
    # min() reprezentuje operator AND.
    rule5 = min(speed_high, rain_not_low)
    output5 = 95


    # REGUŁA 6:
    # IF rain is LOW
    # AND visibility is GOOD
    # THEN wiper speed is VERY LOW.
    rule6 = min(rain_low, visibility_good)
    output6 = 5


    # REGUŁA 7:
    # IF visibility is MEDIUM
    # THEN wiper speed is MEDIUM.
    rule7 = visibility_medium
    output7 = 40


    # REGUŁA 8:
    # IF speed is MEDIUM
    # AND rain is HIGH
    # THEN wiper speed is HIGH.
    rule8 = min(speed_medium, rain_high)
    output8 = 80


    # -----------------------------------------------------
    # KROK 3 - DEFUZZIFICATION
    # -----------------------------------------------------
    #
    # Każda reguła proponuje inną prędkość.
    # Łączymy je w jeden konkretny wynik.
    #
    # Używamy średniej ważonej.


    # Liczymy sumę:
    # siła reguły * wynik reguły.
    numerator = (
        rule1 * output1
        + rule2 * output2
        + rule3 * output3
        + rule4 * output4
        + rule5 * output5
        + rule6 * output6
        + rule7 * output7
        + rule8 * output8
    )


    # Liczymy sumę siły wszystkich aktywnych reguł.
    denominator = (
        rule1
        + rule2
        + rule3
        + rule4
        + rule5
        + rule6
        + rule7
        + rule8
    )


    # Zabezpieczenie przed dzieleniem przez zero.
    if denominator == 0:
        return 0


    # Obliczamy końcową wartość wyjściową.
    result = numerator / denominator


    # Zwracamy końcową prędkość wycieraczek.
    return result


# ---------------------------------------------------------
# FUNKCJA OBSŁUGUJĄCA GUI
# ---------------------------------------------------------


def update_result(value=None):
    """
    Aktualizuje wynik po przesunięciu dowolnego suwaka.

    Args:
        value: Wartość przekazywana automatycznie przez Tkinter.
               Nie jest bezpośrednio używana.

    Returns:
        None
    """

    # Pobieramy natężenie deszczu.
    rain = rain_slider.get()

    # Pobieramy prędkość samochodu.
    speed = speed_slider.get()

    # Pobieramy widoczność.
    visibility = visibility_slider.get()


    # Uruchamiamy nasz system logiki rozmytej.
    result = fuzzy_wipers(
        rain,
        speed,
        visibility
    )


    # Pokazujemy wynik w oknie.
    result_label.config(
        text=f"Prędkość wycieraczek: {result:.1f}%"
    )


# ---------------------------------------------------------
# TWORZENIE OKNA PROGRAMU
# ---------------------------------------------------------


# Tworzymy główne okno.
window = tk.Tk()


# Nadajemy nazwę oknu.
window.title(
    "Inteligentne wycieraczki - Fuzzy Logic"
)


# Ustawiamy rozmiar okna.
window.geometry("600x550")


# ---------------------------------------------------------
# TYTUŁ PROGRAMU
# ---------------------------------------------------------


# Tworzymy tytuł.
title_label = tk.Label(
    window,
    text="Sterowanie wycieraczkami",
    font=("Arial", 20)
)


# Wyświetlamy tytuł.
title_label.pack(pady=20)


# ---------------------------------------------------------
# SUWAK - DESZCZ
# ---------------------------------------------------------


# Tworzymy opis suwaka.
rain_label = tk.Label(
    window,
    text="Natężenie deszczu [%]"
)


# Wyświetlamy opis.
rain_label.pack()


# Tworzymy suwak.
rain_slider = tk.Scale(
    window,
    from_=0,
    to=100,
    orient=tk.HORIZONTAL,
    length=400,
    command=update_result
)


# Wyświetlamy suwak.
rain_slider.pack(pady=10)


# ---------------------------------------------------------
# SUWAK - PRĘDKOŚĆ SAMOCHODU
# ---------------------------------------------------------


# Tworzymy opis.
speed_label = tk.Label(
    window,
    text="Prędkość samochodu [km/h]"
)


# Wyświetlamy opis.
speed_label.pack()


# Tworzymy suwak.
speed_slider = tk.Scale(
    window,
    from_=0,
    to=140,
    orient=tk.HORIZONTAL,
    length=400,
    command=update_result
)


# Wyświetlamy suwak.
speed_slider.pack(pady=10)


# ---------------------------------------------------------
# SUWAK - WIDOCZNOŚĆ
# ---------------------------------------------------------


# Tworzymy opis.
visibility_label = tk.Label(
    window,
    text="Widoczność [%]"
)


# Wyświetlamy opis.
visibility_label.pack()


# Tworzymy suwak.
visibility_slider = tk.Scale(
    window,
    from_=0,
    to=100,
    orient=tk.HORIZONTAL,
    length=400,
    command=update_result
)


# Wyświetlamy suwak.
visibility_slider.pack(pady=10)


# ---------------------------------------------------------
# WYNIK
# ---------------------------------------------------------


# Tworzymy pole wyświetlające wynik.
result_label = tk.Label(
    window,
    text="Prędkość wycieraczek: 0%",
    font=("Arial", 18)
)


# Wyświetlamy wynik.
result_label.pack(pady=30)


# ---------------------------------------------------------
# WARTOŚCI POCZĄTKOWE
# ---------------------------------------------------------


# Początkowy deszcz = 30%.
rain_slider.set(30)


# Początkowa prędkość auta = 50 km/h.
speed_slider.set(50)


# Początkowa widoczność = 70%.
visibility_slider.set(70)


# Obliczamy pierwszy wynik.
update_result()


# ---------------------------------------------------------
# START PROGRAMU
# ---------------------------------------------------------


# Uruchamiamy główną pętlę programu.
#
# Program od tej chwili czeka na ruchy użytkownika
# i reaguje na przesuwanie suwaków.
window.mainloop()