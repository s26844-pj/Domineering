"""Glowny plik uruchomieniowy silnika rekomendacji filmow i seriali."""

from data_loader import load_ratings
from recommender import recommend_movies


def choose_user(dataset):
    """Wyswietla liste uzytkownikow i pozwala wybrac jednego z nich po numerze."""
    users = list(dataset.keys())
    print("\nDostepni uzytkownicy:")
    for i in range(len(users)):
        print(str(i + 1) + ". " + users[i])

    while True:
        choice = input("\nWybierz numer uzytkownika: ").strip()
        if choice.isdigit():
            index = int(choice) - 1
            if index >= 0 and index < len(users):
                return users[index]
        print("Niepoprawny numer. Sprobuj ponownie.")


def choose_metric():
    """Pozwala uzytkownikowi wybrac miare podobienstwa w konsoli."""
    print("\nWybierz miare podobienstwa:")
    print("1. Odleglosc euklidesowa (Euclidean)")
    print("2. Korelacja Pearsona (Pearson)")

    while True:
        choice = input("Twoj wybor (1 lub 2): ").strip()
        if choice == "1":
            return "euclidean"
        if choice == "2":
            return "pearson"
        print("Wpisz 1 albo 2.")


def print_results(user, cluster_id, metric, recommendations, anti_recommendations):
    """Wypisuje w konsoli 5 rekomendacji oraz 5 antyrekomendacji."""
    print("\n==========================================")
    print("Uzytkownik:", user)
    print("Przypisany klaster K-Means:", cluster_id)
    print("Miara podobienstwa:", metric)
    print("==========================================")

    print("\n5 polecanych filmow/seriali (rekomendacje):")
    for i in range(len(recommendations)):
        title = recommendations[i][0]
        score = recommendations[i][1]
        print(str(i + 1) + ". " + title + " (przewidywana ocena: " + str(score) + ")")

    print("\n5 odradzanych filmow/seriali (antyrekomendacje):")
    for i in range(len(anti_recommendations)):
        title = anti_recommendations[i][0]
        score = anti_recommendations[i][1]
        print(str(i + 1) + ". " + title + " (przewidywana ocena: " + str(score) + ")")


def main():
    """Uruchamia silnik rekomendacji w trybie interaktywnym."""
    dataset = load_ratings("Dane.txt")

    if len(dataset) == 0:
        print("Brak danych w pliku.")
        return

    selected_user = choose_user(dataset)
    metric = choose_metric()

    recommendations, anti_recommendations, cluster_id = recommend_movies(
        dataset,
        selected_user,
        metric=metric,
        num_clusters=3,
        count=5,
    )

    print_results(
        selected_user,
        cluster_id,
        metric,
        recommendations,
        anti_recommendations,
    )


if __name__ == "__main__":
    main()