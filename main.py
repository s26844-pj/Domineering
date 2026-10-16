# Tworzymy dwuwymiarową listę (4 wiersze na 4 kolumny), która reprezentuje planszę
board = [
    [".", ".", ".", "."],  # Wiersz 0 - kropki oznaczają puste pola
    [".", ".", ".", "."],  # Wiersz 1
    [".", ".", ".", "."],  # Wiersz 2
    [".", ".", ".", "."]   # Wiersz 3
]


def display_board(board):  # Definicja funkcji wyświetlającej aktualny stan planszy
    print("  0 1 2 3")  # Wypisujemy na górze numery kolumn dla ułatwienia orientacji
    for i in range(len(board)):  # Pętla przechodzi przez indeksy wierszy: 0, 1, 2, 3
        print(i, " ".join(board[i]))  # Wypisuje numer wiersza (i) oraz elementy tego wiersza połączone spacją


def get_vertical_moves(board):  # Funkcja szukająca wszystkich dostępnych ruchów dla gracza V (pionowego)
    moves = []  # Tworzymy pustą listę, do której będziemy zapisywać znalezione ruchy
    for row in range(len(board) - 1):  # Pętla po wierszach od 0 do 2 (bez ostatniego, bo domino zajmuje też row + 1)
        for col in range(len(board[0])):  # Pętla po wszystkich kolumnach: od 0 do 3
            if board[row][col] == "." and board[row + 1][col] == ".":  # Sprawdzamy, czy pole obecne ORAZ pole pod nim są puste
                moves.append((row, col))  # Dodajemy współrzędne górnego pola klocka jako krotkę (wiersz, kolumna) do listy

    return moves  # Zwracamy gotową listę wszystkich legalnych ruchów pionowych


def get_horizontal_moves(board):  # Funkcja szukająca wszystkich dostępnych ruchów dla komputera H (poziomego)
    moves = []  # Pusta lista na legalne ruchy poziome
    for row in range(len(board)):  # Pętla po wszystkich wierszach: od 0 do 3
        for col in range(len(board[0]) - 1):  # Pętla po kolumnach od 0 do 2 (bez ostatniej, bo domino zajmuje też col + 1)
            if board[row][col] == "." and board[row][col + 1] == ".":  # Sprawdzamy, czy pole obecne ORAZ pole po prawej są puste
                moves.append((row, col))  # Dodajemy współrzędne lewego pola klocka do listy ruchów

    return moves  # Zwracamy listę legalnych ruchów poziomych


def make_vertical_move(board, row, col):  # Funkcja stawiająca pionowy klocek gracza V na planszy
    board[row][col] = "V"  # Wpisujemy literę "V" na wybranym polu (górna część klocka)
    board[row + 1][col] = "V"  # Wpisujemy literę "V" na polu bezpośrednio poniżej (dolna część klocka)


def undo_vertical_move(board, row, col):  # Funkcja cofająca ruch pionowy (potrzebna do symulacji w Minimaxie)
    board[row][col] = "."  # Przywracamy kropkę (puste pole) na górnym polu klocka
    board[row + 1][col] = "."  # Przywracamy kropkę na dolnym polu klocka


def make_horizontal_move(board, row, col):  # Funkcja stawiająca poziomy klocek komputera H na planszy
    board[row][col] = "H"  # Wpisujemy literę "H" na wybranym polu (lewa część klocka)
    board[row][col + 1] = "H"  # Wpisujemy literę "H" na polu bezpośrednio po prawej (prawa część klocka)


def undo_horizontal_move(board, row, col):  # Funkcja cofająca ruch poziomy (do symulacji w Minimaxie)
    board[row][col] = "."  # Przywracamy kropkę na lewym polu klocka
    board[row][col + 1] = "."  # Przywracamy kropkę na prawym polu klocka


def has_moves(board, player):  # Funkcja sprawdzająca, czy dany gracz ma jeszcze jakikolwiek ruch (czy nie przegrał)
    if player == "V":  # Jeśli sprawdzamy gracza V...
        return len(get_vertical_moves(board)) > 0  # Zwraca True, jeśli lista jego możliwych ruchów nie jest pusta (długość > 0)
    if player == "H":  # Jeśli sprawdzamy komputer H...
        return len(get_horizontal_moves(board)) > 0  # Zwraca True, jeśli lista ruchów komputera nie jest pusta (długość > 0)


def player_move(board):  # Funkcja obsługująca turę człowieka
    valid_moves = get_vertical_moves(board)  # Pobieramy aktualną listę dostępnych ruchów dla gracza V
    print("Dostępne ruchy:", valid_moves)  # Wyświetlamy graczowi podpowiedź z listą możliwych ruchów

    while True:  # Nieskończona pętla – będzie pytać o ruch, dopóki gracz nie poda poprawnego
        try:  # Rozpoczynamy blok wyłapywania błędów (gdyby gracz wpisał np. literę lub sam Enter zamiast liczby)
            row = int(input("Podaj wiersz: "))  # Pobieramy tekst z klawiatury i zamieniamy go na liczbę całkowitą (int)
            col = int(input("Podaj kolumnę: "))  # Pobieramy kolumnę i zamieniamy na liczbę całkowitą (int)
        except ValueError:  # Jeśli zamiana na liczbę (int) się nie udała i wystąpił błąd ValueError...
            print("Podaj poprawne liczby!")  # Wyświetlamy komunikat o błędzie
            continue  # Przeskakujemy na sam początek pętli `while`, pytając o współrzędne jeszcze raz

        if (row, col) in valid_moves:  # Sprawdzamy, czy podana para (wiersz, kolumna) znajduje się na liście legalnych ruchów
            make_vertical_move(board, row, col)  # Jeśli tak, wykonujemy ten ruch na planszy
            break  # Przerywamy pętlę `while`, kończąc turę gracza
        else:  # Jeśli podane współrzędne są zajęte lub poza zakresem...
            print("Nieprawidłowy ruch. Spróbuj ponownie.")  # Informujemy gracza i pętla wraca na początek


def minimax(board, player):  # Główna funkcja sztucznej inteligencji – rekurencyjnie przeszukuje drzewo gry
    if player == "H" and not has_moves(board, "H"):  # Warunek końca: jeśli jest tura H i nie ma on żadnego ruchu...
        return -1  # Zwracamy -1 (oznacza to porażkę komputera H w tej gałęzi symulacji)

    if player == "V" and not has_moves(board, "V"):  # Warunek końca: jeśli jest tura V i nie ma on żadnego ruchu...
        return 1  # Zwracamy 1 (oznacza to zwycięstwo komputera H w tej gałęzi symulacji)

    if player == "H":  # Gałąź dla gracza MAX (komputer H szuka jak najwyższego wyniku, czyli dąży do 1)
        best_score = -999  # Ustawiamy początkowy najlepszy wynik na bardzo niską wartość

        for row, col in get_horizontal_moves(board):  # Pobieramy każdy możliwy ruch (krotkę) i od razu rozbijamy go na zmienne row i col
            make_horizontal_move(board, row, col)  # Wykonujemy próbny ruch komputera na planszy
            score = minimax(board, "V")  # Wywołujemy minimax rekurencyjnie – sprawdzamy, jak odpowie na to gracz V
            undo_horizontal_move(board, row, col)  # Cofamy próbny ruch, aby przywrócić planszę do stanu sprzed symulacji

            if score > best_score:  # Jeśli wynik z tej ścieżki jest większy niż dotychczasowy najlepszy...
                best_score = score  # Zapisujemy go jako nowy najlepszy wynik

        return best_score  # Zwracamy najlepszy wynik, jaki komputer H może osiągnąć z tego stanu planszy

    if player == "V":  # Gałąź dla gracza MIN (zakładamy, że człowiek V gra optymalnie i chce zaszkodzić komputerowi, dążąc do -1)
        best_score = 999  # Ustawiamy początkowy wynik na bardzo wysoką wartość

        for row, col in get_vertical_moves(board):  # Przechodzimy przez każdy możliwy ruch gracza V
            make_vertical_move(board, row, col)  # Wykonujemy próbny ruch gracza V na planszy
            score = minimax(board, "H")  # Sprawdzamy rekurencyjnie, jak w kolejnym kroku odpowie komputer H
            undo_vertical_move(board, row, col)  # Cofamy próbny ruch gracza V, przywracając stan planszy

            if score < best_score:  # Gracz V wybiera wynik najmniejszy (najmniej korzystny dla komputera H)...
                best_score = score  # Nadpisujemy najlepszy wynik z punktu widzenia gracza V

        return best_score  # Zwracamy wynik wybrany przez gracza V


def best_computer_move(board):  # Funkcja decydująca, który konkretnie ruch (wiersz, kolumna) komputer ma wykonać w swojej turze
    best_score = -999  # Początkowa najniższa ocena ruchu
    best_move = None  # Zmienna na przechowanie współrzędnych najlepszego ruchu (na początku pusta)

    for row, col in get_horizontal_moves(board):  # Sprawdzamy po kolei każdy dostępny w tym momencie ruch komputera
        make_horizontal_move(board, row, col)  # Wykonujemy próbny ruch na planszy
        score = minimax(board, "V")  # Uruchamiamy algorytm minimax (zaczynając od odpowiedzi gracza V), aby ocenił ten ruch
        undo_horizontal_move(board, row, col)  # Cofamy próbny ruch na planszy

        if score > best_score:  # Jeśli sprawdzany ruch daje lepszy wynik niż wszystkie poprzednie...
            best_score = score  # Zapamiętujemy ten nowy najlepszy wynik
            best_move = (row, col)  # Zapamiętujemy współrzędne (wiersz, kolumna), które dały ten wynik

    return best_move  # Zwracamy współrzędne najlepszego znalezionego ruchu


def computer_move(board):  # Funkcja wykonująca właściwy ruch komputera w grze
    move = best_computer_move(board)  # Pobieramy najlepsze współrzędne wyliczone przez funkcję wyżej

    if move is not None:  # Upewniamy się, że ruch został znaleziony (że nie jest pusty)
        row, col = move  # Rozpakowujemy krotkę `move` na dwie osobne zmienne: `row` i `col`
        make_horizontal_move(board, row, col)  # Stawiamy klocek "H" na planszy już na stałe
        print("Komputer wykonał ruch:", move)  # Wypisujemy w terminalu informację, gdzie komputer postawił klocek


def game():  # Główna funkcja sterująca przebiegiem rozgrywki
    while True:  # Pętla główna gry – działa w kółko aż do wygranej jednej ze stron
        print()  # Wypisuje pustą linię dla odstępu
        display_board(board)  # Wyświetla aktualny stan planszy przed ruchem człowieka

        if not has_moves(board, "V"):  # Sprawdza, czy gracz V ma jeszcze jakikolwiek legalny ruch
            print("Nie masz już możliwego ruchu. Komputer wygrywa!")  # Jeśli nie ma, informuje o wygranej komputera
            break  # Przerywa pętlę `while` i kończy grę

        print("\nTwój ruch:")  # Wypisuje nagłówek tury gracza (`\n` robi dodatkową pustą linię przed tekstem)
        player_move(board)  # Wywołuje funkcję pobierającą i wykonującą ruch człowieka

        print()  # Wypisuje pustą linię
        display_board(board)  # Wyświetla planszę po ruchu człowieka

        if not has_moves(board, "H"):  # Sprawdza, czy komputer H ma jeszcze jakikolwiek legalny ruch
            print("Komputer nie ma już możliwego ruchu. Wygrywasz!")  # Jeśli nie ma, informuje o wygranej gracza
            break  # Przerywa pętlę `while` i kończy grę

        print("\nRuch komputera:")  # Wypisuje nagłówek przed ruchem AI
        computer_move(board)  # Wywołuje funkcję, w której komputer oblicza i wykonuje swój ruch


game()  # Wywołanie funkcji `game()` – ta linijka faktycznie uruchamia cały program po włączeniu skryptu
