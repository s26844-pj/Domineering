```markdown
# Domineering

Projekt wykonany w ramach przedmiotu  
**NAI – Narzędzia Sztucznej Inteligencji**

## Autorzy

- Łukasz Dahm
- Michał Kujawa

## Opis projektu

Domineering to dwuosobowa, turowa gra planszowa o sumie zerowej.

Gracze wykonują ruchy na planszy 4×4:

- gracz **V** układa domino pionowo,
- gracz **H** układa domino poziomo.

Każde domino zajmuje dwa sąsiednie, wolne pola.

Gracz, który w swojej turze nie może wykonać legalnego ruchu, przegrywa.

## Zasady gry

https://en.wikipedia.org/wiki/Domineering

## Sztuczna inteligencja

Komputer gra jako gracz **H**.

Do wyboru ruchu wykorzystuje algorytm **Minimax**.

Algorytm analizuje możliwe przyszłe ruchy komputera oraz przeciwnika. Zakłada przy tym, że przeciwnik również będzie wybierał najlepsze możliwe ruchy.

W algorytmie:

- **H** jest graczem MAX i maksymalizuje wynik,
- **V** jest graczem MIN i minimalizuje wynik.

Ocena stanów końcowych:

- `1` – wygrana komputera H,
- `-1` – przegrana komputera H.

## Wymagania

- Python 3

Projekt nie wymaga instalowania dodatkowych bibliotek.

## Uruchomienie

W terminalu należy przejść do katalogu projektu:

```bash
cd Domineering
```

Następnie uruchomić program:

```bash
python3 main.py
```

## Sterowanie

Gracz wykonuje ruch poprzez podanie:

1. numeru wiersza,
2. numeru kolumny.

Program wyświetla listę aktualnie dostępnych ruchów.

Przykład:

```text
Dostępne ruchy: [(0, 0), (0, 1), (0, 2)]
Podaj wiersz: 0
Podaj kolumnę: 1
```

## Struktura projektu

```text
Domineering/
├── main.py
├── README.md
└── screenshot.png
```

## Przykładowa rozgrywka

Zrzut ekranu z przykładowej rozgrywki znajduje się w pliku:

`screenshot.png`
```