
def calcule_vecteur(point1, point2):
    """prend deux listes  avec les coordonnées des points et retourne les coordonnées du vecteur"""
    x_vecteur = point2[0] - point1[0]
    y_vecteur = point2[1] - point1[1]
    return [x_vecteur, y_vecteur]


def calcule_normale(liste):  # pour un vecteur orienté vers le haut la normale est orientée vers la gauche
    """prend une  liste des coordonnées d'un vecteur et retourne sa normale"""
    x_normale = -liste[1]
    y_normale = liste[0]
    return [x_normale, y_normale]

def calcule_vecteurs_triangle(liste_de_liste):
    vecteur1 = calcule_vecteur(liste_de_liste[0], liste_de_liste[1])
    vecteur2 = calcule_vecteur(liste_de_liste[1], liste_de_liste[2])
    vecteur3 = calcule_vecteur(liste_de_liste[2], liste_de_liste[0])
    return[vecteur1, vecteur2, vecteur3]

def calcule_normales_triangle(liste_de_liste):  # les triangles doivent être rentrés dans le sens horaire
    """prend un triangle et retourne les coordonnées de ses normales dans l'ordre des points"""
    normale_1 = calcule_normale(calcule_vecteur(liste_de_liste[0], liste_de_liste[1]))
    normale_2 = calcule_normale(calcule_vecteur(liste_de_liste[1], liste_de_liste[2]))
    normale_3 = calcule_normale(calcule_vecteur(liste_de_liste[2], liste_de_liste[0]))
    return [normale_1, normale_2, normale_3]


