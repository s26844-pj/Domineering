"""Modul do wczytywania i czyszczenia danych o ocenach filmow z pliku tekstowego."""

import json


TITLE_ALIASES = {
    "the matrix": "Matrix",
    "la casa de papel": "Dom z papieru",
    "kapitan philips": "Kapitan Phillips",
    "openheimer": "Oppenheimer",
    "mrocny rycerz": "Mroczny Rycerz",
    "dr. house": "Dr House",
    "dune 1": "Diuna",
    "dune 2": "Diuna: część druga",
    "titatnic": "Titanic",
    "better call soul": "Better Call Saul",
    "gran tourismo": "Gran Turismo",
    "farma clarskona": "Farma Clarksona",
    "how i meet your mother": "How I Met Your Mother",
    "pibull (2005-2008)": "Pitbull (2005-2008)",
    "eksperymeny ss": "Eksperyment SS",
    "ocalenie szeregowca rayana": "Szeregowiec Ryan",
    "kevin sam w nowym yorku": "Kevin sam w Nowym Jorku",
    "maze runner": "Więzień labiryntu",
    "maze runner 1": "Więzień labiryntu",
}


def parse_rating(value):
    """Zamienia tekst na ocene liczbowa z zakresu od 0 do 10.

    Zwraca liczbe zmiennoprzecinkowa albo None, gdy tekst nie jest poprawna ocena.
    """
    text = value.replace(",", ".")
    try:
        rating = float(text)
    except ValueError:
        return None

    if rating >= 0.0 and rating <= 10.0:
        return rating
    return None


def normalize_title(raw_title, canonical_titles):
    """Ujednolica tytul filmu, usuwa zbedne spacje i poprawia znane literowki."""
    parts = raw_title.strip().split()
    cleaned = " ".join(parts)
    lowered = cleaned.lower()

    if lowered in TITLE_ALIASES:
        cleaned = TITLE_ALIASES[lowered]
        lowered = cleaned.lower()

    if lowered not in canonical_titles:
        canonical_titles[lowered] = cleaned

    return canonical_titles[lowered]


def load_ratings(filepath):
    """Wczytuje plik tekstowy z ocenami oddzielonymi tabulatorami.

    Pomija puste pola i niekompletne wpisy, a w przypadku wielokrotnej oceny
    tego samego filmu przez jedna osobe wylicza srednia arytmetyczna.
    Zwraca slownik w formacie {uzytkownik: {tytul: ocena}}.
    """
    dataset = {}
    canonical_titles = {}

    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            raw_cells = line.split("\t")
            tokens = []
            for cell in raw_cells:
                cleaned_cell = cell.strip()
                if cleaned_cell != "":
                    tokens.append(cleaned_cell)

            if len(tokens) < 2:
                continue

            user = tokens[0]
            user_ratings = {}

            idx = 1
            while idx < len(tokens) - 1:
                candidate_title = tokens[idx]
                candidate_rating = parse_rating(tokens[idx + 1])

                if candidate_rating is not None:
                    title = normalize_title(candidate_title, canonical_titles)
                    if title not in user_ratings:
                        user_ratings[title] = []
                    user_ratings[title].append(candidate_rating)
                    idx = idx + 2
                else:
                    idx = idx + 1

            if len(user_ratings) > 0:
                averaged_ratings = {}
                for title in user_ratings:
                    scores = user_ratings[title]
                    total = 0.0
                    for score in scores:
                        total = total + score
                    averaged_ratings[title] = round(total / len(scores), 2)

                dataset[user] = averaged_ratings

    return dataset


def save_ratings_to_json(dataset, output_path):
    """Zapisuje wczytane i oczyszczone oceny do pliku JSON."""
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(dataset, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    data = load_ratings("Dane.txt")
    print("Wczytano uzytkownikow:", len(data))
    for person in data:
        print("-", person, ":", len(data[person]), "tytulow")