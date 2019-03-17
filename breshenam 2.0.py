#MARCHE POUR TOUTE MATRICE
#ON PEUT DEPLACER LE PERSONNAGE
#IL Y A JUSTE UN PROBLEME AU NIVEAUX DES VITRES JE NE SAIS PAS SI C'EST QUAND ON LES PLACE OU QUAND ON ENLEVE LE POINT
#DE LA DROITE QUI SE TROUVE SUR LA VITRE MAIS IL Y EN A CERTAINES TRANSFORMENT EN POINTS VUS
#AUSSI J'AI ESSAYER DE METTRE UNE LIMITE DE VUE MAIS PAREIL ENCORE UN PROBLEME AVEC LES VITRES, LA VUE VAS TROP LOIN
#DITES MOI VOUS PENSEZ IL VAUT MIEUX TOUT METTRE EN ANGLAIS MEME LES DOCSTRING OU TOUT METTRE EN FRANCAIS

from PIL import Image
from math import sqrt


def line_first_octant(start, end):
    """calcul les pixels par lesquel la droite reliant start: (x1, x2) et end: (y1, y2) passe
    On considère que le coefficient directeur de la droite est compris entre 0 et 1, que x1 < x2 et y1 < y2
    Retourne une liste de coordonnées de pixels"""
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    points = list()
    y = y1
    e = dx
    for x in range(x1, x2 + 1):
        points.append((x, y))
        e -= 2 * dy
        if e < 0:
            e += 2 * dx
            y += 1
    return points


def line_of_sight(start, end, board, limit):
    """calcul les pixels par lesquel la droite reliant start: (x1, x2) et end: (y1, y2) passe,
    Pour toute valeur de coefficient directeur et pour tous points start et end
    Retourne une liste de coordonnées de pixels"""
    #Dans ce programme, on parle d'octants, on prendra pour octant1 les droites de coefficient directeur compris entre
    #O et 1 et on tournera ensuite dans le sens trigonométrique pour les numéro des autres octants.
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    points = list()

    # Conditions initiales
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Permet de traiter les droites dans les octants 2, 3, 6 et 7
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Pour traiter les droites dans les octants 3, 4, 5 et 6
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # On recalcule les variations des coordonnées
    dx = x2 - x1
    dy = y2 - y1

    # On calcule l'erreur commise
    error = dx
    ystep = 1 if y1 < y2 else -1

    # On trace la ligne de vue sur le modèle de la fonction line_first_octant
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= 2 * abs(dy)
        if error < 0:
            y += ystep
            error += 2 * dx

    # On met les coordonnées dans l'ordre (en partant de start) si on se trouvait dans les octants 3, 4, 5 ou 6
    if swapped:
        points.reverse()

    points2 = points[:]

    for k, p in enumerate(points):
        i, j = p
        # On arrête la vue si on rencontre un mur
        if board[j][i] == "m":
            return points2[:k]
        # On retire simplement le points de la ligne de vue si on se trouve sur une vitre
        elif board[j][i] == "g":
            points2.remove(p)
    return points2


def create_matrix(column, line):
    lst = [[0] * line for i in range(column)]
    return lst


img = Image.open("/home/maxime/Documents/S2/INFO/ProjetS2/sprites_proj.png")  # Modifier l'adresse pour pouvoir accéder
# au fichier
print(img)
finish = Image.open("/home/maxime/Documents/S2/INFO/ProjetS2/Imagevide.png")  # Pareil


def display_image(lst):
    '''Permet d'afficher une image avec le module PIL'''
    glass = img.crop((31, 36, 45, 50))
    invisible = img.crop((45, 36, 59, 50))
    wall = img.crop((31, 22, 45, 36))
    visible = img.crop((31, 50, 45, 64))
    character = img.crop((33, 2, 47, 16))
    for i, val in enumerate(lst):
        for j, val2 in enumerate(val):
            if val2 == "m":
                finish.paste(wall, (14 * j, 14 * i, 14 * j + 14, 14 * i + 14))
            elif val2 == "g":
                finish.paste(glass, (14 * j, 14 * i, 14 * j + 14, 14 * i + 14))
            elif val2 == "@":
                finish.paste(character, (14 * j, 14 * i, 14 * j + 14, 14 * i + 14))
            elif val2 == 0:
                finish.paste(invisible, (14 * j, 14 * i, 14 * j + 14, 14 * i + 14))
            else:
                finish.paste(visible, (14 * j, 14 * i, 14 * j + 14, 14 * i + 14))
    finish.show()


def display_board(matrix):
    '''Permet d'afficher la matrice avec le champ de vue'''
    for i in matrix:
        for j in i:
            if j == "m":
                print("\033[37m#\033[0m", "", end="")
            elif j == "g":
                print("\033[37m/\033[0m", "", end="")
            elif j == '@':
                print("\033[32m@\033[0m", "", end="")
            elif j == 0:
                print("\033[30m0\033[0m", "", end="")
            else:
                print("\033[31m*\033[0m", "", end="")
        print()


def put_wall(direction, length, begin_x, begin_y, wall_type, matrix):
    """Permet de placer un mur sur la matrice de terrain
        Retourne la matrice modifiée
    l for left, r for right, t for top, b for bottom, glass for a glass, wall for a wall"""
    if wall_type == "glass":
        if direction == "r":
            for i in range(length):
                matrix[begin_y][begin_x + i] = "g"
        elif direction == "l":
            for i in range(length):
                matrix[begin_y][begin_x - i] = "g"
        elif direction == "t":
            for i in range(length):
                matrix[begin_y - i][begin_x] = "g"
        elif direction == "b":
            for i in range(length):
                matrix[begin_y + i][begin_x] = "g"
    if wall_type == "wall":
        if direction == "r":
            for i in range(length):
                matrix[begin_y][begin_x + i] = "m"
        elif direction == "l":
            for i in range(length):
                matrix[begin_y][begin_x - i] = "m"
        elif direction == "t":
            for i in range(length):
                matrix[begin_y - i][begin_x] = "m"
        elif direction == "b":
            for i in range(length):
                matrix[begin_y + i][begin_x] = "m"
    return matrix


def plusieurs_droites(start, board, limit):
    '''Permet de tracer toutes les lignes de vue qui compose le champ de vision
    Retourne une liste de liste de toutes les droites avec les points vue'''
    res = list()
    for i in range(len(board[0])):
        res.append(line_of_sight(start, (i, 0), board, limit))
        res.append(line_of_sight(start, (i, len(board) - 1), board, limit))
    for j in range(len(board)):
        res.append(line_of_sight(start, (0, j), board, limit))
        res.append(line_of_sight(start, (len(board[0]) - 1, j), board, limit))
    return res


def superpose_plusieurs_droites(board, points):
    '''Permet de superposer sur une matrice tous les points vus d'un CHAMP DE VISION'''
    for x in points:
        for y in x:
            i, j = y
            board[j][i] = 1
    return board


def superpose(board, points):
    '''Permet de superposer sur une matrice tous les points vus d'UNE DROITE'''
    for x in points:
        i, j = x
        board[j][i] = 1
    return board


line = 30
column = 30
limite = int(2 * min(column, line) / 5)
start = (int(column / 2 + 4), int(line / 2) - 3)
h, p = start
M = create_matrix(line, column)
put_wall("r", 18, 0, 11, "wall", M)
put_wall("r", 23, 0, 18, "wall", M)
put_wall("t", 3, 23, 18, "wall", M)
put_wall("t", 3, 23, 15, "glass", M)
put_wall("t", 2, 23, 12, "wall", M)
put_wall("r", 7, 23, 10, "wall", M)
put_wall("t", 12, 17, 11, "wall", M)
put_wall("r", 3, 12, 18, "glass", M)
put_wall("r", 1, 12, 18, "wall", M)
put_wall("r", 3, 9, 11, "glass", M)
put_wall("r", 2, 8, 11, "wall", M)
# print(M)
# end = (10, 8)
# L = line_of_sight(start, end, M)
# superpose(M, L)
L = plusieurs_droites(start, M, limite)
# print(L)
superpose_plusieurs_droites(M, L)
M[p][h] = "@"
display_board(M)
display_image(M)