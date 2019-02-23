from math import *
from random import *
from PIL import Image


def matrice(colonne, ligne):
    lst = [[0] * ligne for i in range(colonne)]
    return lst


img = Image.open(
    "/home/raphael/Documents/MPCI L1/Ligne de vue/sprites_proj.png")  # Modifier l'adresse pour pouvoir accéder au fichier
print(img)
rendu = Image.open("/home/raphael/Documents/MPCI L1/Ligne de vue/Imagevide.png")  # Pareil

mur_vitre = img.crop((31, 36, 45, 50))

non_visible = img.crop((45, 36, 59, 50))

mur_opaque = img.crop((31, 22, 45, 36))

visible = img.crop((31, 50, 45, 64))

personnage = img.crop((33, 2, 47, 16))


def affiche_image(lst):
    for i, val in enumerate(lst):
        for j, val2 in enumerate(val):
            if val2 == 1:
                rendu.paste(visible, (14 * j, 14 * i, 14 * j + 14, 14 * i + 14))
            elif val2 == 2:
                rendu.paste(mur_opaque, (14 * j, 14 * i, 14 * j + 14, 14 * i + 14))
            elif val2 == 4:
                rendu.paste(mur_vitre, (14 * j, 14 * i, 14 * j + 14, 14 * i + 14))
            elif val2 == "@":
                rendu.paste(personnage, (14 * j, 14 * i, 14 * j + 14, 14 * i + 14))
            else:
                rendu.paste(non_visible, (14 * j, 14 * i, 14 * j + 14, 14 * i + 14))
    rendu.show()


def affiche_tableau(lst):
    for i in lst:
        for j in i:
            if j == 1:
                print("\033[31m*\033[0m", "", end="")
            elif j == 2:
                print("\033[37m#\033[0m", "", end="")
            elif j == 4:
                print("\033[37m/\033[0m", "", end="")
            elif j == '@':
                print("\033[32m@\033[0m", "", end="")
            else:
                print("\033[30m0\033[0m", "", end="")
        print()


def placer_mur_ancien(direction, longueur, position_x_départ, position_y_départ, type_de_mur, matrice):
    """g pour direction gauche, d pour direction droite, h pour haut et b pour bas, opaque pour mur opaque, vitre pour vitre"""
    if type_de_mur == "vitre":
        if direction == "d":
            for i in range(longueur):
                [position_y_départ][position_x_départ + i] = 4
        elif direction == "g":
            for i in range(longueur):
                matrice[position_y_départ][position_x_départ - i] = 4
        elif direction == "h":
            for i in range(longueur):
                matrice[position_y_départ - i][position_x_départ] = 4
        elif direction == "b":
            for i in range(longueur):
                matrice[position_y_départ + i][position_x_départ] = 4
    if type_de_mur == "opaque":
        if direction == "d":
            for i in range(longueur):
                matrice[position_y_départ][position_x_départ + i] = 2
        elif direction == "g":
            for i in range(longueur):
                matrice[position_y_départ][position_x_départ - i] = 2
        elif direction == "h":
            for i in range(longueur):
                matrice[position_y_départ - i][position_x_départ] = 2
        elif direction == "b":
            for i in range(longueur):
                matrice[position_y_départ + i][position_x_départ] = 2

def placer_mur_seul(position_x, position_y, type_de_mur, matrice):
    if type_de_mur == "vitre":
        matrice[position_y][position_x] = 4
    if type_de_mur == "opaque":
        matrice[position_y][position_x] = 2

def placer_mur (coordonnees_depart, coordonnees_arrivee, type_de_mur, matrice):
    # coordonnees_depart et coordonnees_arrivee sont des listes (coordonnees du point)
    if coordonnees_depart[0] == coordonnees_arrivee[0]:
        if coordonnees_arrivee[1] == coordonnees_depart[1] :
            placer_mur_seul(coordonnees_depart[0], coordonnees_depart[1], type_de_mur, matrice)
        elif coordonnees_depart[1] > coordonnees_arrivee[1]:
            for i in range(coordonnees_depart[1] - coordonnees_arrivee[1] + 1):
                placer_mur_seul(coordonnees_depart[0], coordonnees_arrivee[1] + i, type_de_mur, matrice)
        else:
            for i in range(coordonnees_arrivee[1] - coordonnees_depart[1] + 1):
                placer_mur_seul(coordonnees_depart[0], coordonnees_depart[1] + i, type_de_mur, matrice)
    else:
        point_depart = [0, 0]
        point_arrivee = [0, 0]
        if coordonnees_depart[0] <= coordonnees_arrivee[0]:
            point_depart = coordonnees_depart
            point_arrivee = coordonnees_arrivee
        else:
            point_depart = coordonnees_arrivee
            point_arrivee = coordonnees_depart
        coefficient = (point_arrivee[1] - point_depart[1]) / (point_arrivee[0] - point_depart[0])
        position_y = 0
        position_x = 0
        coefficient_2 = 0
        j = 0
        if 0 <= coefficient < 1:
            for i in range(point_arrivee[0] - point_depart[0] + 1):
                position_y += coefficient
                if position_y >= 1:
                    j += 1
                    position_y -= 1
                placer_mur_seul(point_depart[0] + i, point_depart[1] + j, type_de_mur, matrice)
        elif coefficient == 1:
            for i in range(point_arrivee[0] - point_depart[0] + 1):
                placer_mur_seul(point_depart[0] + i, point_depart[1] + i, type_de_mur, matrice)
        elif coefficient > 1:
            coefficient_2 = (point_arrivee[0] - point_depart[0]) / (point_arrivee[1] - point_depart[1])
            for i in range(point_arrivee[1] - point_depart[1] + 1):
                position_x += coefficient_2
                if position_x >= 1:
                    j += 1
                    position_x -= 1
                placer_mur_seul(point_depart[0] + j, point_depart[1] + i, type_de_mur, matrice)
        elif 0 >= coefficient > -1:
            for i in range(point_arrivee[0] - point_depart[0] + 1):
                position_y += coefficient
                if position_y <= -1:
                    j -= 1
                    position_y += 1
                placer_mur_seul(point_depart[0] + i, point_depart[1] + j, type_de_mur, matrice)
        elif coefficient == -1:
            for i in range(point_arrivee[0] - point_depart[0] + 1):
                placer_mur_seul(point_depart[0] + i, point_depart[1] - i, type_de_mur, matrice)
        elif coefficient < -1:
            coefficient_2 = (point_arrivee[0] - point_depart[0]) / (point_arrivee[1] - point_depart[1])
            for i in range(point_depart[1] - point_arrivee[1] + 1):
                position_x += coefficient_2
                if position_x <= -1:
                    j -= 1
                    position_x += 1
                placer_mur_seul(point_depart[0] - j, point_depart[1] - i, type_de_mur, matrice)

def placer_triangle(A, B, C, type_de_mur, matrice):
    # A, B et C sont des listes de coordonnees d'un point
    placer_mur(A, B, type_de_mur, matrice)
    placer_mur(B, C, type_de_mur, matrice)
    placer_mur(C, A, type_de_mur, matrice)

def placer_rectangle(hauteur, largeur, position_x_départ, position_y_départ, matrice):
    placer_mur_ancien("b", hauteur, position_x_départ, position_y_départ, matrice)
    placer_mur_ancien("b", hauteur + 1, position_x_départ + largeur, position_y_départ, matrice)
    placer_mur_ancien("d", largeur, position_x_départ, position_y_départ, matrice)
    placer_mur_ancien("d", largeur, position_x_départ, position_y_départ + hauteur, matrice)


def nb_de_droite(lst):
    colonne = len(lst)
    ligne = len(lst[1])
    return floor(3 * min(colonne, ligne) / 2)


def remplace(coeff, lst):
    colonne = len(lst)
    ligne = len(lst[1])
    positionx = floor(ligne / 2)
    positiony = floor(colonne / 2)
    compteur = 0
    compteur2 = 0
    distancey = 0
    distancey2 = 0
    distancex = 0
    distancex2 = 0
    limite = floor(2 * min(colonne, ligne) / 5)

    if coeff < 0 and coeff > (-1):

        n = positiony
        n2 = n
        y = 0
        y2 = y
        for j in range(ligne - positionx):
            y = y + coeff
            if lst[n][j + positionx - 1] != 2 and lst[n][j + positionx - 1] != 4:
                lst[n][j + positionx - 1] = 1
                distancex += 1
                if sqrt((distancex ** 2) + (distancey ** 2)) >= limite:
                    break
                if y <= (-1):
                    n = n + 1
                    if lst[n][j + positionx - 1] != 2 and lst[n][j + positionx - 1] != 4:
                        lst[n][j + positionx - 1] = 1
                        y = y + 1
                        distancey += 1
                        if sqrt((distancex ** 2) + (distancey ** 2)) >= limite:
                            break
                    else:
                        break
            else:
                break
        for j in range(ligne - positionx):
            y2 = y2 - coeff
            if lst[colonne - n2][ligne - (j + positionx - 1)] != 2 and lst[colonne - n2][
                ligne - (j + positionx - 1)] != 4:
                lst[colonne - n2][ligne - (j + positionx - 1)] = 1
                distancex2 += 1
                if sqrt((distancex2 ** 2) + (distancey2 ** 2)) >= limite:
                    break
                if y2 >= 1:
                    n2 = n2 + 1
                    if lst[colonne - n2][ligne - (j + positionx - 1)] != 2 and lst[colonne - n2][
                        ligne - (j + positionx - 1)] != 4:
                        lst[colonne - n2][ligne - (j + positionx - 1)] = 1
                        y2 = y2 - 1
                        distancey2 += 1
                        if sqrt((distancex2 ** 2) + (distancey2 ** 2)) >= limite:
                            break
                    else:
                        break
            else:
                break

    if coeff >= 0 and coeff < 1:

        n = colonne - positiony
        n2 = n
        y = 0
        y2 = y
        for j in range(ligne - positionx):
            y = y + coeff
            if lst[n][j + positionx - 1] != 2 and lst[n][j + positionx - 1] != 4:
                lst[n][j + positionx - 1] = 1
                distancex += 1
                if sqrt((distancex ** 2) + (distancey ** 2)) >= limite:
                    break
                if y >= (1):
                    n = n - 1
                    if lst[n][j + positionx - 1] != 2 and lst[n][j + positionx - 1] != 4:
                        lst[n][j + positionx - 1] = 1
                        y = y - 1
                        distancey += 1
                        if sqrt((distancex ** 2) + (distancey ** 2)) >= limite:
                            break
                    else:
                        break
            else:
                break
        for j in range(ligne - positionx):
            y2 = y2 - coeff
            if lst[colonne - n2][ligne - (j + positionx - 1)] != 2 and lst[colonne - n2][
                ligne - (j + positionx - 1)] != 4:
                lst[colonne - n2][ligne - (j + positionx - 1)] = 1
                distancex2 += 1
                if sqrt((distancex2 ** 2) + (distancey2 ** 2)) >= limite:
                    break
                if y2 <= (-1):
                    n2 = n2 - 1
                    if lst[colonne - n2][ligne - (j + positionx - 1)] != 2 and lst[colonne - n2][
                        ligne - (j + positionx - 1)] != 4:
                        lst[colonne - n2][ligne - (j + positionx - 1)] = 1
                        y2 = y2 + 1
                        distancey2 += 1
                        if sqrt((distancex2 ** 2) + (distancey2 ** 2)) >= limite:
                            break
                    else:
                        break
            else:
                break

    if coeff < (-1):
        n = positionx
        n2 = n
        y = 0
        y2 = y
        for j in range(ligne - positionx):
            y = y + (1 / coeff)
            if lst[j + positiony - 1][n] != 2 and lst[j + positiony - 1][n] != 4:
                lst[j + positiony - 1][n] = 1
                distancey += 1
                if sqrt((distancex ** 2) + (distancey ** 2)) >= limite:
                    break
                if y <= (-1):
                    n = n + 1
                    if lst[j + positiony - 1][n] != 2 and lst[j + positiony - 1][n] != 4:
                        lst[j + positiony - 1][n] = 1
                        y = y + 1
                        distancex += 1
                        if sqrt((distancex ** 2) + (distancey ** 2)) >= limite:
                            break
                    else:
                        break
            else:
                break

        for j in range(ligne - positionx):
            y2 = y2 - (1 / coeff)
            if lst[ligne - (j + positiony - 1)][colonne - n2] != 2 and lst[ligne - (j + positiony - 1)][
                colonne - n2] != 4:
                lst[ligne - (j + positiony - 1)][colonne - n2] = 1
                distancey2 += 1
                if sqrt((distancex2 ** 2) + (distancey2 ** 2)) >= limite:
                    break
                if y2 >= (1):
                    n2 = n2 + 1
                    if lst[ligne - (j + positiony - 1)][colonne - n2] != 2 and lst[ligne - (j + positiony - 1)][
                        colonne - n2] != 4:
                        lst[ligne - (j + positiony - 1)][colonne - n2] = 1
                        y2 = y2 - 1
                        distancex2 += 1
                        if sqrt((distancex2 ** 2) + (distancey2 ** 2)) >= limite:
                            break
                    else:
                        break
            else:
                break

    if coeff > 1:

        n = colonne - positionx
        n2 = n
        y = 0
        y2 = y
        for j in range(ligne - positionx):
            y = y + (1 / coeff)
            if lst[j + positiony - 1][n] != 2 and lst[j + positiony - 1][n] != 4:
                lst[j + positiony - 1][n] = 1
                distancey += 1
                if sqrt((distancex ** 2) + (distancey ** 2)) >= limite:
                    break
                if y >= 1:
                    n = n - 1
                    if lst[j + positiony - 1][n] != 2 and lst[j + positiony - 1][n] != 4:
                        lst[j + positiony - 1][n] = 1
                        y = y - 1
                        distancex += 1
                        if sqrt((distancex ** 2) + (distancey ** 2)) >= limite:
                            break
                    else:
                        break
            else:
                break
        for j in range(ligne - positionx):
            y2 = y2 - (1 / coeff)
            if lst[ligne - (j + positiony - 1)][colonne - n2] != 2 and lst[ligne - (j + positiony - 1)][
                colonne - n2] != 4:
                lst[ligne - (j + positiony - 1)][colonne - n2] = 1
                distancey2 += 1
                if sqrt((distancex2 ** 2) + (distancey2 ** 2)) >= limite:
                    break
                if y2 <= (-1):
                    n2 = n2 - 1
                    if lst[ligne - (j + positiony - 1)][colonne - n2] != 2 and lst[ligne - (j + positiony - 1)][
                        colonne - n2] != 4:
                        lst[ligne - (j + positiony - 1)][colonne - n2] = 1
                        y2 = y2 + 1
                        distancex2 += 1
                        if sqrt((distancex2 ** 2) + (distancey2 ** 2)) >= limite:
                            break
                    else:
                        break
            else:
                break

    if coeff == -1:
        y = positiony
        x = positionx
        for i in range(min(x, y)):
            if lst[y - i][x - i] != 2 and lst[y - i][x - i] != 4:
                lst[y - i][x - i] = 1
                compteur += 1
                if compteur >= limite:
                    break
            else:
                break
        for i in range(min(x, y)):
            if lst[y + i][x + i] != 2 and lst[y + i][x + i] != 4:
                lst[y + i][x + i] = 1
                compteur2 += 1
                if compteur2 >= limite:
                    break
            else:
                break

    if coeff == 1:
        y = positiony
        x = positionx
        for i in range(min(x, y)):
            if lst[y - i][x + i] != 2 and lst[y - i][x + i] != 4:
                lst[y - i][x + i] = 1
                compteur += 1
                if compteur >= limite:
                    break
            else:
                break
        for i in range(min(x, y)):
            if lst[y + i][x - i] != 2 and lst[y + i][x - i] != 4:
                lst[y + i][x - i] = 1
                compteur2 += 1
                if compteur2 >= limite:
                    break
            else:
                break

    lst[positiony][positionx] = '@'
    return lst


def ligne_de_vue(lst, nb_de_droite):
    for i in range(nb_de_droite):
        lst = remplace(tan(0.01745 * (90 - i * (180 / (nb_de_droite)))), lst)
    return lst


colonne = 30
ligne = 30
board = matrice(colonne, ligne)
x = [3, 27]
f = [7, 14]
a = [3, 8]
b = [5, 0]
c = [10, 3]
y = [15, 8]
d = [26, 5]
e = [13, 19]
z = [23, 23]
placer_mur(x, f, "opaque", board)
placer_mur(f, a, "opaque", board)
placer_mur(a, b, "opaque", board)
placer_mur(b, c, "opaque", board)
placer_mur(c, y, "opaque", board)
placer_mur(y, d, "opaque", board)
placer_mur(d, e, "opaque", board)
placer_mur(e, z, "opaque", board)
placer_mur(z, x, "opaque", board)
board1 = ligne_de_vue(board, 100)

affiche_tableau(board1)
affiche_image(board1)