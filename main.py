"""
Domineering - gra dwuosobowa z algorytmem Minimax.

Autorzy:
- Łukasz Dahm
- Michał Kujawa

Zasady gry:
Gracz V układa domino pionowo.
Gracz H układa domino poziomo.
Każde domino zajmuje dwa sąsiednie pola.
Gracz, który nie może wykonać legalnego ruchu w swojej turze, przegrywa.

Uruchomienie:
python3 main.py
"""

import copy


# Plansza 4x4.
# Kropka "." oznacza wolne pole.
board = [
    [".", ".", ".", "."],
    [".", ".", ".", "."],
    [".", ".", ".", "."],
    [".", ".", ".", "."]
]


def display_board(board):
    """Wyświetla aktualny stan planszy w terminalu."""
    for row in board:
        print(" ".join(row))


def get_vertical_moves(board):
    """
    Zwraca listę wszystkich legalnych ruchów gracza V.

    Gracz V układa domino pionowo, dlatego sprawdzane są
    dwa wolne pola znajdujące się jedno pod drugim.
    """
    moves = []

    # Sprawdzamy tylko pierwsze 3 wiersze,
    # ponieważ domino zajmuje również pole poniżej.
    for row in range(3):
        for col in range(4):
            if board[row][col] == "." and board[row + 1][col] == ".":
                moves.append((row, col))

    return moves


def make_vertical_move(board, row, col):
    """
    Wykonuje ruch gracza V.

    Zajmuje dwa pola ustawione pionowo.
    """
    board[row][col] = "V"
    board[row + 1][col] = "V"


def get_horizontal_moves(board):
    """
    Zwraca listę wszystkich legalnych ruchów gracza H.

    Gracz H układa domino poziomo, dlatego sprawdzane są
    dwa wolne pola znajdujące się obok siebie.
    """
    moves = []

    # Sprawdzamy tylko pierwsze 3 kolumny,
    # ponieważ domino zajmuje również pole po prawej stronie.
    for row in range(4):
        for col in range(3):
            if board[row][col] == "." and board[row][col + 1] == ".":
                moves.append((row, col))

    return moves


def make_horizontal_move(board, row, col):
    """
    Wykonuje ruch gracza H.

    Zajmuje dwa pola ustawione poziomo.
    """
    board[row][col] = "H"
    board[row][col + 1] = "H"


def player_move(board):
    """
    Pobiera ruch gracza V z terminala.

    Gracz podaje wiersz i kolumnę.
    Program sprawdza, czy wybrany ruch jest legalny.
    """
    while True:
        print("Dostępne ruchy:", get_vertical_moves(board))

        row = int(input("Podaj wiersz: "))
        col = int(input("Podaj kolumnę: "))

        # Sprawdzamy, czy ruch podany przez gracza
        # znajduje się na liście legalnych ruchów.
        if (row, col) in get_vertical_moves(board):
            make_vertical_move(board, row, col)
            break
        else:
            print("Nieprawidłowy ruch. Spróbuj ponownie.")


def has_moves(board, player):
    """
    Sprawdza, czy wskazany gracz posiada jeszcze legalny ruch.

    Zwraca True, jeśli ruch istnieje.
    Zwraca False, jeśli gracz nie może już wykonać ruchu.
    """
    if player == "V":
        return len(get_vertical_moves(board)) > 0

    if player == "H":
        return len(get_horizontal_moves(board)) > 0


def minimax(board, player):
    """
    Ocenia aktualny stan gry przy użyciu algorytmu Minimax.

    Komputer H jest graczem maksymalizującym.
    Człowiek V jest graczem minimalizującym.

    Wynik:
    1  - komputer H może doprowadzić do zwycięstwa,
    -1 - komputer H przegra przy optymalnej grze przeciwnika.
    """

    # Jeśli jest tura H i H nie ma ruchu,
    # komputer przegrywa.
    if player == "H" and not has_moves(board, "H"):
        return -1

    # Jeśli jest tura V i V nie ma ruchu,
    # komputer H wygrywa.
    if player == "V" and not has_moves(board, "V"):
        return 1

    # H jest graczem MAX.
    # Próbuje uzyskać jak najwyższy wynik.
    if player == "H":
        best_score = -999

        for row, col in get_horizontal_moves(board):
            # Tworzymy kopię planszy, żeby tylko zasymulować ruch.
            new_board = copy.deepcopy(board)

            # Symulujemy ruch H.
            make_horizontal_move(new_board, row, col)

            # Po ruchu H przychodzi kolej gracza V.
            score = minimax(new_board, "V")

            # H wybiera największy możliwy wynik.
            best_score = max(best_score, score)

        return best_score

    # V jest graczem MIN.
    # Próbuje uzyskać jak najgorszy wynik dla komputera H.
    if player == "V":
        best_score = 999

        for row, col in get_vertical_moves(board):
            # Tworzymy kopię planszy do symulacji.
            new_board = copy.deepcopy(board)

            # Symulujemy ruch V.
            make_vertical_move(new_board, row, col)

            # Po ruchu V przychodzi kolej H.
            score = minimax(new_board, "H")

            # V wybiera najmniejszy możliwy wynik dla H.
            best_score = min(best_score, score)

        return best_score


def best_computer_move(board):
    """
    Wybiera najlepszy ruch komputera H przy użyciu Minimaxu.

    Każdy legalny ruch komputera jest symulowany,
    a następnie oceniany przez funkcję minimax().
    """
    best_score = -999
    best_move = None

    for row, col in get_horizontal_moves(board):
        # Tworzymy kopię planszy dla testowanego ruchu.
        new_board = copy.deepcopy(board)

        # Symulujemy ruch komputera.
        make_horizontal_move(new_board, row, col)

        # Sprawdzamy wynik dalszej gry przy założeniu,
        # że przeciwnik również gra optymalnie.
        score = minimax(new_board, "V")

        # Zapamiętujemy ruch z najlepszym wynikiem.
        if score > best_score:
            best_score = score
            best_move = (row, col)

    return best_move


def computer_move(board):
    """
    Wykonuje najlepszy ruch komputera H.

    Ruch jest wybierany przez funkcję best_computer_move().
    """
    move = best_computer_move(board)

    if move is not None:
        row, col = move
        make_horizontal_move(board, row, col)
        print("Komputer wykonał ruch:", move)


def game():
    """
    Uruchamia główną pętlę gry.

    Gracz V i komputer H wykonują ruchy naprzemiennie,
    aż jeden z nich nie będzie miał legalnego ruchu.
    """
    while True:
        print()
        display_board(board)

        # Sprawdzamy, czy człowiek V może wykonać ruch.
        if not has_moves(board, "V"):
            print("Nie masz już możliwego ruchu. Komputer wygrywa!")
            break

        print("\nTwój ruch:")
        player_move(board)

        print()
        display_board(board)

        # Sprawdzamy, czy komputer H może wykonać ruch.
        if not has_moves(board, "H"):
            print("Komputer nie ma już możliwego ruchu. Wygrywasz!")
            break

        print("\nRuch komputera:")
        computer_move(board)


# Uruchomienie programu.
game()