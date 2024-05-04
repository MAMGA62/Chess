
import pygame


# Classe qui regroupe toutes les pieces du jeu
class Piece(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0, type="pawn", team=0):
        super().__init__()

        self.types = ["king", "queen", "bishop", "horse", "castle", "pawn"]

        self.type = type
        # Team 0 : Blanc | Team 1 : Noir
        self.team = team

        self.sprite_sheet = pygame.image.load("assets/img/sprites_modif.png")
        self.image = self.get_image(self.types.index(self.type), self.team)
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.position = [x, y]

        self.place(x, y)

    def get_image(self, x, y):
        image = pygame.Surface([200, 200])
        image.blit(self.sprite_sheet, (0, 0), (x * 200, y * 200, 200, 200))
        image.set_colorkey([0, 0, 0])
        return image

    def get_type(self):
        return self.type

    def get_team(self):
        return self.team

    def get_position(self):
        return self.position

    def place(self, x, y):
        self.rect.x = 133 + x * 90
        self.position[0] = x
        self.rect.y = 125 + y * 90
        self.position[1] = y

    def death(self, game):
        """Supprime et replace la pièce dans le 'cimetière'["""
        game.pieces.remove(self)
        game.deaths[self.team].append(self)

        self.rect.x = 900 - len(game.deaths[self.team]) * 25
        self.rect.y = 0 + abs(self.team - 1) * 900

        if self.type == "king":
            print("\nFin de la partie!")

            if self.team == 0:
                print("L'équipe Noire a gagné!")
            else:
                print("L'équipe Blanche a gagné!")

            game.stop()

    def is_square(self, x, y):
        """Renvoie True si la case existe"""
        return 0 <= x <= 7 and 0 <= y <= 7

    def get_min(self, x, y):
        """Renvoie la coordonnée la plus petite"""
        if x >= y:
            return y
        else:
            return x

    def check_top(self, possibilities, i=0):
        """Check les cases du dessus"""
        for y in range(0, self.position[1]):
            possibilities[i].append((self.position[0], (self.position[1] - 1) - y))

        return possibilities

    def check_bottom(self, possibilities, i=1):
        """Check les cases du dessous"""
        for y in range(self.position[1] + 1, 8):
            possibilities[i].append((self.position[0], y))

        return possibilities

    def check_left(self, possibilities, i=2):
        """Check les cases à gauche"""
        for x in range(0, self.position[0]):
            possibilities[i].append(((self.position[0] - 1) - x, self.position[1]))

        return possibilities

    def check_right(self, possibilities, i=3):
        """Check les cases à droite"""
        for x in range(self.position[0] + 1, 8):
            possibilities[i].append((x, self.position[1]))

        return possibilities

    def check_top_left(self, possibilities, i=4):
        """Check les cases dans la diagonale haut-gauche"""
        for x_y in range(1, self.get_min(self.position[0], self.position[1]) + 1):
            possibilities[i].append((self.position[0] - x_y, self.position[1] - x_y))

        return possibilities

    def check_top_right(self, possibilities, i=5):
        """Check les cases dans la diagonale haut-droite"""
        for v in range(1,  self.get_min(7 - self.position[0], self.position[1]) + 1):
            possibilities[i].append((self.position[0] + v, self.position[1] - v))

        return possibilities

    def check_bottom_left(self, possibilities, i=6):
        """Check les cases dans la diagonale bas-gauche"""
        for v in range(1, self.get_min(self.position[0], 7 - self.position[1]) + 1):
            possibilities[i].append((self.position[0] - v, self.position[1] + v))

        return possibilities

    def check_bottom_right(self, possibilities, i=7):
        """Check les cases dans la diagonale bas-droite"""
        for x_y in range(1, self.get_min(7 - self.position[0], 7 - self.position[1]) + 1):
            possibilities[i].append((self.position[0] + x_y, self.position[1] + x_y))

        return possibilities


# Classe pour le roi
class King(Piece):
    def __init__(self, x=0, y=0, team=0):
        super().__init__(x=x, y=y, type="king", team=team)

    def possibilities(self):
        """Revoie une liste de coordonnées possibles pour le roi (non-vérifiée)"""
        # Possibilités pour chacune des cases autour
        unchecked_possibilities = [[(self.position[0], self.position[1] - 1)], [(self.position[0], self.position[1] + 1)], [(self.position[0] - 1, self.position[1])], [(self.position[0] + 1, self.position[1])], [(self.position[0] - 1, self.position[1] - 1)], [(self.position[0] + 1, self.position[1] - 1)], [(self.position[0] - 1, self.position[1] + 1)], [(self.position[0] + 1, self.position[1])]]
        possibilities = []
        for possibility in unchecked_possibilities:
            if self.is_square(possibility[0][0], possibility[0][1]):
                possibilities.append(possibility)

            else:
                possibilities.append([])


        return possibilities


# Classe pour la reine
class Queen(Piece):
    def __init__(self, x=0, y=0, team=0):
        super().__init__(x=x, y=y, type="queen", team=team)

    def possibilities(self):
        """Revoie une liste de coordonnées possibles pour la reine (non-vérifiée)"""
        possibilities = [[] for _ in range(8)]

        # Possibilités pour le haut
        self.check_top(possibilities, 0)

        # Possibilités pour le bas
        self.check_bottom(possibilities, 1)

        # Possibilités pour la gauche
        self.check_left(possibilities, 2)

        # Possibilités pour la droite
        self.check_right(possibilities, 3)

        # Possibilités diagonale haut gauche
        self.check_top_left(possibilities, 4)

        # Possibilités diagonale haut droite
        self.check_top_right(possibilities, 5)

        # Possibilités diagonale bas gauche
        self.check_bottom_left(possibilities, 6)

        # Possibilités diagonale bas droite
        self.check_bottom_right(possibilities, 7)

        return possibilities


# Classe pour fou
class Bishop(Piece):
    def __init__(self, x=0, y=0, team=0):
        super().__init__(x=x, y=y, type="bishop", team=team)

    def possibilities(self):
        """Revoie une liste de coordonnées possibles pour le fou (non-vérifiée)"""
        possibilities = [[] for _ in range(8)]

        # Possibilités diagonale haut gauche
        self.check_top_left(possibilities, 4)

        # Possibilités diagonale haut droite
        self.check_top_right(possibilities, 5)

        # Possibilités diagonale bas gauche
        self.check_bottom_left(possibilities, 6)

        # Possibilités diagonale bas droite
        self.check_bottom_right(possibilities, 7)

        return possibilities


# Classe pour cheval
class Horse(Piece):
    def __init__(self, x=0, y=0, team=0):
        super().__init__(x=x, y=y, type="horse", team=team)

    def possibilities(self):
        """Revoie une liste de coordonnées possibles pour le cheval (non-vérifiée)"""
        unchecked_possibilities = [
            [(self.position[0] - 1, self.position[1] - 2),
            (self.position[0] + 1, self.position[1] - 2),

            (self.position[0] - 2, self.position[1] + 1),
            (self.position[0] - 2, self.position[1] - 1),

            (self.position[0] + 2, self.position[1] + 1),
            (self.position[0] + 2, self.position[1] - 1),

            (self.position[0] - 1, self.position[1] + 2),
            (self.position[0] + 1, self.position[1] + 2)]
        ]

        possibilities = [[]]

        for t_possibility in unchecked_possibilities:
            for possibility in t_possibility:
                if self.is_square(possibility[0], possibility[1]):
                    possibilities[0].append(possibility)

        return possibilities


# Classe pour la tour
class Castle(Piece):
    def __init__(self, x=0, y=0, team=0):
        super().__init__(x=x, y=y, type="castle", team=team)

    def possibilities(self):
        """Revoie une liste de coordonnées possibles pour la reine (non-vérifiée)"""
        possibilities = [[] for _ in range(8)]

        # Possibilités pour le haut
        self.check_top(possibilities, 0)

        # Possibilités pour le bas
        self.check_bottom(possibilities, 1)

        # Possibilités pour la gauche
        self.check_left(possibilities, 2)

        # Possibilités pour la droite
        self.check_right(possibilities, 3)

        return possibilities


# Classe Pions
class Pawn(Piece):
    def __init__(self, x=0, y=0, team=0):
        super().__init__(x=x, y=y, type="pawn", team=team)

    def possibilities(self):
        unchecked_possibilities = [[] for _ in range(8)]
        possibilities = [[] for _ in range(8)]
        if self.team == 0:
            unchecked_possibilities.append([])
            unchecked_possibilities[0].append((self.position[0], self.position[1] - 1))

            if self.position[1] == 6:
                unchecked_possibilities[0].append((self.position[0], self.position[1] - 2))

        else:
            unchecked_possibilities[1].append((self.position[0], self.position[1] + 1))

            if self.position[1] == 1:
                unchecked_possibilities[1].append((self.position[0], self.position[1] + 2))

        for t_possibility in range(len(unchecked_possibilities)):

            for possibility in unchecked_possibilities[t_possibility]:
                if self.is_square(possibility[0], possibility[1]):
                    possibilities[t_possibility].append(possibility)

        return possibilities

