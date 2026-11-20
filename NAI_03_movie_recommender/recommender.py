"""Silnik rekomendacji filmow i seriali oparty na K-Means i miarach podobienstwa."""

import math
import numpy as np
from sklearn.cluster import KMeans


def euclidean_similarity(dataset, user1, user2):
    """Oblicza podobienstwo dwoch uzytkownikow na podstawie odleglosci euklidesowej.

    Zwraca wartosc z przedzialu (0, 1], gdzie 1 oznacza identyczne oceny.
    Gdy uzytkownicy nie maja wspolnych filmow, zwraca 0.0.
    """
    common_movies = []
    for movie in dataset[user1]:
        if movie in dataset[user2]:
            common_movies.append(movie)

    if len(common_movies) == 0:
        return 0.0

    sum_of_squares = 0.0
    for movie in common_movies:
        diff = dataset[user1][movie] - dataset[user2][movie]
        sum_of_squares = sum_of_squares + (diff * diff)

    distance = math.sqrt(sum_of_squares)
    return 1.0 / (1.0 + distance)


def pearson_similarity(dataset, user1, user2):
    """Oblicza korelacje Pearsona miedzy ocenami dwoch uzytkownikow.

    Zwraca wartosc z przedzialu [-1, 1]. Wymaga co najmniej dwoch wspolnych filmow.
    """
    common_movies = []
    for movie in dataset[user1]:
        if movie in dataset[user2]:
            common_movies.append(movie)

    n = len(common_movies)
    if n < 2:
        return 0.0

    sum1 = 0.0
    sum2 = 0.0
    for movie in common_movies:
        sum1 = sum1 + dataset[user1][movie]
        sum2 = sum2 + dataset[user2][movie]

    avg1 = sum1 / n
    avg2 = sum2 / n

    numerator = 0.0
    denom1 = 0.0
    denom2 = 0.0

    for movie in common_movies:
        d1 = dataset[user1][movie] - avg1
        d2 = dataset[user2][movie] - avg2
        numerator = numerator + (d1 * d2)
        denom1 = denom1 + (d1 * d1)
        denom2 = denom2 + (d2 * d2)

    if denom1 == 0 or denom2 == 0:
        return 0.0

    return numerator / math.sqrt(denom1 * denom2)


def cluster_users(dataset, num_clusters=3):
    """Grupuje uzytkownikow w klastry za pomoca algorytmu K-Means.

    Tworzy macierz ocen (uzytkownicy x filmy), gdzie brak oceny to 0,
    a nastepnie przypisuje kazdego uzytkownika do numeru klastra.
    """
    users = list(dataset.keys())

    all_movies_set = set()
    for user in users:
        for movie in dataset[user]:
            all_movies_set.add(movie)
    all_movies = sorted(list(all_movies_set))

    matrix = np.zeros((len(users), len(all_movies)))

    for i in range(len(users)):
        user = users[i]
        for j in range(len(all_movies)):
            movie = all_movies[j]
            if movie in dataset[user]:
                matrix[i][j] = dataset[user][movie]

    if num_clusters > len(users):
        num_clusters = len(users)

    model = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    labels = model.fit_predict(matrix)

    clusters = {}
    for i in range(len(users)):
        clusters[users[i]] = int(labels[i])

    return clusters


def _calculate_predictions(dataset, target_user, candidate_users, metric):
    """Wylicza przewidywane oceny nieobejrzanych filmow na podstawie grupy uzytkownikow."""
    weighted_sums = {}
    similarity_sums = {}

    for other_user in candidate_users:
        if other_user == target_user:
            continue

        if metric == "pearson":
            sim = pearson_similarity(dataset, target_user, other_user)
        else:
            sim = euclidean_similarity(dataset, target_user, other_user)

        if sim <= 0:
            continue

        for movie in dataset[other_user]:
            if movie not in dataset[target_user]:
                if movie not in weighted_sums:
                    weighted_sums[movie] = 0.0
                    similarity_sums[movie] = 0.0

                weighted_sums[movie] = weighted_sums[movie] + (dataset[other_user][movie] * sim)
                similarity_sums[movie] = similarity_sums[movie] + sim

    predictions = {}
    for movie in weighted_sums:
        predictions[movie] = weighted_sums[movie] / similarity_sums[movie]

    return predictions


def _fallback_average_ratings(dataset, target_user, candidate_users):
    """Wylicza zwykla srednia ocen filmow, gdy brak wspolnych pozycji do porownania."""
    totals = {}
    counts = {}

    for other_user in candidate_users:
        if other_user == target_user:
            continue

        for movie in dataset[other_user]:
            if movie not in dataset[target_user]:
                if movie not in totals:
                    totals[movie] = 0.0
                    counts[movie] = 0

                totals[movie] = totals[movie] + dataset[other_user][movie]
                counts[movie] = counts[movie] + 1

    averages = {}
    for movie in totals:
        averages[movie] = totals[movie] / counts[movie]

    return averages


def _get_rating_from_pair(pair):
    """Funkcja pomocnicza do sortowania listy par (tytul, ocena) po ocenie."""
    return pair[1]


def recommend_movies(dataset, target_user, metric="euclidean", num_clusters=3, count=5):
    """Wyznacza rekomendacje oraz antyrekomendacje dla wybranego uzytkownika.

    Najpierw szuka podobnych osob w tym samym klastrze K-Means. Jesli filmow
    jest za malo, uzupelnia wyniki o pozostalych uzytkownikow ze zbioru.

    Zwraca krotke: (lista_rekomendacji, lista_antyrekomendacji, numer_klastra).
    """
    if target_user not in dataset:
        raise ValueError("Nie znaleziono uzytkownika: " + target_user)

    clusters = cluster_users(dataset, num_clusters)
    target_cluster = clusters[target_user]

    same_cluster_users = []
    all_other_users = []

    for user in dataset:
        if user != target_user:
            all_other_users.append(user)
            if clusters[user] == target_cluster:
                same_cluster_users.append(user)

    predictions = _calculate_predictions(dataset, target_user, same_cluster_users, metric)

    if len(predictions) < count * 2:
        extra_predictions = _calculate_predictions(dataset, target_user, all_other_users, metric)
        for movie in extra_predictions:
            if movie not in predictions:
                predictions[movie] = extra_predictions[movie]

    if len(predictions) < count * 2:
        fallback = _fallback_average_ratings(dataset, target_user, all_other_users)
        for movie in fallback:
            if movie not in predictions:
                predictions[movie] = fallback[movie]

    ranked = []
    for movie in predictions:
        ranked.append((movie, round(predictions[movie], 2)))

    ranked.sort(key=_get_rating_from_pair, reverse=True)

    recommendations = ranked[:count]

    anti_recommendations = ranked[-count:]
    anti_recommendations.reverse()

    return recommendations, anti_recommendations, target_cluster