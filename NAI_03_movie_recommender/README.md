## Autorzy

- Łukasz Dahm
- Michał Kujawa

# Silnik rekomendacji filmów i seriali

System rekomendacji i antyrekomendacji filmów/seriali napisany w języku Python. Łączy grupowanie użytkowników algorytmem **K-Means** z wyznaczaniem podobieństwa za pomocą **odległości euklidesowej** lub **korelacji Pearsona**.

## Struktura repozytorium

- `Dane.txt` – plik źródłowy z ocenami użytkowników w skali 0–10.
- `data_loader.py` – wczytywanie danych z pliku tekstowego, usuwanie pustych pól, uśrednianie duplikatów i ujednolicanie tytułów.
- `recommender.py` – klasteryzacja użytkowników (K-Means), obliczanie podobieństwa i generowanie listy 5 rekomendacji oraz 5 antyrekomendacji.
- `main.py` – prosty interfejs konsolowy uruchamiający program.
- `requirements.txt` – wymagane biblioteki zewnętrzne.

## Instalacja i uruchomienie

```bash
pip install -r requirements.txt
python main.py
```

Po uruchomieniu program wyświetli listę użytkowników z pliku `Dane.txt`, poprosi o wybór numeru osoby oraz metryki podobieństwa, a następnie wypisze:

1. **5 filmów/seriali polecanych** (najwyższa przewidywana ocena spośród nieobejrzanych tytułów).
2. **5 filmów/seriali odradzanych** (najniższa przewidywana ocena spośród nieobejrzanych tytułów).
