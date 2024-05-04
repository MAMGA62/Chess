
import pygame
from models.pieces import *
from math import sqrt, ceil


class Game:
    def __init__(self):
        super().__init__()

        pygame.display.set_caption("ChessGame")
        pygame.display.set_icon(pygame.image.load("assets/img/chess_icon.png"))
        self.screen = pygame.display.set_mode((1000, 1000))
        self.bg = pygame.image.load("assets/img/bg.jpg")

        self.turn = 0

        self.piece_selected = None
        self.pieces = pygame.sprite.Group()
        self.deaths = [[], []]

        self.circles_positions = []
        self.circles_rects = []

        self.plateau = [[0] * 8 for _ in range(8)]

        self.running = True

    def get_plateau(self):
        return self.plateau

    def get_pieces(self):
        return self.pieces

    def get_death_pieces(self):
        return self.deaths

    def start(self):
        self.running = True

        self.prepare()

        while self.running:

            self.screen.blit(self.bg, (0, 0))

            # On affiche tous les cercles
            for x, y in self.circles_rects:
                pygame.draw.circle(self.screen, (168, 135, 255), (x, y), 45)

            # On affiche toutes les pièces
            for piece in self.get_pieces():
                self.screen.blit(piece.image, piece.rect)

            # On affiche toutes les pièces "mortes" (On commence par les derniers pour qu'ils soient + en arrière plan)
            for death_piece_team in self.get_death_pieces():
                for death_piece in death_piece_team:
                    self.screen.blit(death_piece.image, death_piece.rect)

            pygame.display.flip()

            for event in pygame.event.get():
                # Quand on fait un clique gauche
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # si une pièce est sélectionnée
                    if self.piece_selected is not None:
                        # pour chaque cercles disponibles
                        for i in range(len(self.circles_rects)):
                            # Si on clique sur le cercle (Calcul de la distance entre 2 points dans un repère orthonormé mmhhhh)
                            if ceil(sqrt((event.pos[0] - self.circles_rects[i][0]) ** 2 + (event.pos[1] - self.circles_rects[i][1]) ** 2)) <= 45:
                                # print("yes")

                                # On vérifie si la case est occupé par un ennemi
                                if isinstance(self.get_plateau()[self.circles_positions[i][1]][self.circles_positions[i][0]], Piece):
                                    # (On sait déjà que c'est une ennemi)
                                    # On supprime la pièce visée
                                    self.get_plateau()[self.circles_positions[i][1]][self.circles_positions[i][0]].death(self)

                                # On déplace la pièce
                                self.move_piece(self.piece_selected, self.circles_positions[i][0], self.circles_positions[i][1])

                                # On passe le tour à l'autre joueur
                                self.change_turn()

                                break

                        self.piece_selected = None
                        self.circles_positions.clear()
                        self.circles_rects.clear()
                    else:
                        for piece in self.pieces:
                            if piece.get_team() == self.turn:
                                # Si on clique sur cette piece
                                if piece.rect.collidepoint(event.pos):
                                    # print("ok")
                                    self.circles_positions.clear()
                                    self.circles_rects.clear()

                                    self.piece_selected = piece

                                    for position in self.check_squares(piece):
                                        self.circles_positions.append(position)
                                        self.circles_rects.append((183 + position[0] * 90, 179 + position[1] * 90))

                                    break

                elif event.type == pygame.QUIT:
                    self.stop()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop()

    def stop(self):
        """Arrête la partie et ferme la fenêtre"""
        pygame.quit()
        self.running = False

    def create_piece(self, x=0, y=0, type="pawn", team=0):
        """Crée une pièce """
        if type == "king":
            self.plateau[y][x] = King(x=x, y=y, team=team)
        elif type == "queen":
            self.plateau[y][x] = Queen(x=x, y=y, team=team)
        elif type == "bishop":
            self.plateau[y][x] = Bishop(x=x, y=y, team=team)
        elif type == "horse":
            self.plateau[y][x] = Horse(x=x, y=y, team=team)
        elif type == "castle":
            self.plateau[y][x] = Castle(x=x, y=y, team=team)
        elif type == "pawn":
            self.plateau[y][x] = Pawn(x=x, y=y, team=team)

        self.pieces.add(self.get_plateau()[y][x])
        return self.plateau[y][x]

    def move_piece(self, piece, x, y):
        """Place la pièce aux coordonnées x/y et actualise le tableau"""
        stop = False
        for i in range(8):
            for j in range(8):
                if self.get_plateau()[i][j] == piece:
                    self.plateau[i][j] = 0
                    stop = True
                    break
            if stop:
                break

        piece.place(x, y)
        self.plateau[y][x] = piece

    def change_turn(self):
        self.turn = abs(self.turn - 1)

    def check_squares(self, piece):
        """Fonction qui vérifie si les cases du plateau sont déjà prises par des pièces ou non"""
        possibilities = []
        piece_possibilities = piece.possibilities()

        for t_possibility in range(len(piece_possibilities)):
            for possibility in piece_possibilities[t_possibility]:
                if self.get_plateau()[possibility[1]][possibility[0]] == 0:
                    possibilities.append(possibility)

                elif isinstance(self.get_plateau()[possibility[1]][possibility[0]], Piece):
                    if self.get_plateau()[possibility[1]][possibility[0]].get_team() != piece.get_team() and piece.type != "pawn":
                        possibilities.append(possibility)

                    if piece.type != "horse":
                        break

        # On rajoute les possibilités pour que les pions puissent prendre les pieces en diagonale
        if piece.type == "pawn":
            # Team blanche
            if piece.get_team() == 0:
                # 1ère position
                if piece.is_square(piece.position[0] - 1, piece.position[1] - 1):
                    position1 = (piece.position[0] - 1, piece.position[1] - 1)

                    if isinstance(self.get_plateau()[position1[1]][position1[0]], Piece):
                        if self.get_plateau()[position1[1]][position1[0]].get_team() != piece.get_team():
                            possibilities.append(position1)

                # 2ème position
                if piece.is_square(piece.position[0] + 1, piece.position[1] - 1):
                    position2 = (piece.position[0] + 1, piece.position[1] - 1)

                    if isinstance(self.get_plateau()[position2[1]][position2[0]], Piece):
                        if self.get_plateau()[position2[1]][position2[0]].get_team() != piece.get_team():
                            possibilities.append(position2)
            # Team noire
            else:
                # 1ère position
                if piece.is_square(piece.position[0] - 1, piece.position[1] + 1):
                    position1 = (piece.position[0] - 1, piece.position[1] + 1)

                    if isinstance(self.get_plateau()[position1[1]][position1[0]], Piece):
                        if self.get_plateau()[position1[1]][position1[0]].get_team() != piece.get_team():
                            possibilities.append(position1)

                # 2ème position
                if piece.is_square(piece.position[0] + 1, piece.position[1] + 1):
                    position2 = (piece.position[0] + 1, piece.position[1] + 1)

                    if isinstance(self.get_plateau()[position2[1]][position2[0]], Piece):
                        if self.get_plateau()[position2[1]][position2[0]].get_team() != piece.get_team():
                            possibilities.append(position2)

        return possibilities

    def prepare(self):
        """Permet de placer les pièces au début de la partie sur le plateau"""

        # Pièces du haut
        self.b_c1 = self.create_piece(x=0, y=0, type="castle", team=1)
        self.b_h1 = self.create_piece(x=1, y=0, type="horse", team=1)
        self.b_b1 = self.create_piece(x=2, y=0, type="bishop", team=1)
        self.b_q = self.create_piece(x=3, y=0, type="queen", team=1)
        self.b_k = self.create_piece(x=4, y=0, type="king", team=1)
        self.b_b2 = self.create_piece(x=5, y=0, type="bishop", team=1)
        self.b_h2 = self.create_piece(x=6, y=0, type="horse", team=1)
        self.b_c2 = self.create_piece(x=7, y=0, type="castle", team=1)
        self.b_p1 = self.create_piece(x=0, y=1, type="pawn", team=1)
        self.b_p2 = self.create_piece(x=1, y=1, type="pawn", team=1)
        self.b_p3 = self.create_piece(x=2, y=1, type="pawn", team=1)
        self.b_p4 = self.create_piece(x=3, y=1, type="pawn", team=1)
        self.b_p5 = self.create_piece(x=4, y=1, type="pawn", team=1)
        self.b_p6 = self.create_piece(x=5, y=1, type="pawn", team=1)
        self.b_p7 = self.create_piece(x=6, y=1, type="pawn", team=1)
        self.b_p8 = self.create_piece(x=7, y=1, type="pawn", team=1)

        # Pièces du bas
        self.w_c1 = self.create_piece(x=0, y=7, type="castle", team=0)
        self.w_h1 = self.create_piece(x=1, y=7, type="horse", team=0)
        self.w_b1 = self.create_piece(x=2, y=7, type="bishop", team=0)
        self.w_q = self.create_piece(x=3, y=7, type="queen", team=0)
        self.w_k = self.create_piece(x=4, y=7, type="king", team=0)
        self.w_b2 = self.create_piece(x=5, y=7, type="bishop", team=0)
        self.w_h2 = self.create_piece(x=6, y=7, type="horse", team=0)
        self.w_c2 = self.create_piece(x=7, y=7, type="castle", team=0)
        self.w_p1 = self.create_piece(x=0, y=6, type="pawn", team=0)
        self.w_p2 = self.create_piece(x=1, y=6, type="pawn", team=0)
        self.w_p3 = self.create_piece(x=2, y=6, type="pawn", team=0)
        self.w_p4 = self.create_piece(x=3, y=6, type="pawn", team=0)
        self.w_p5 = self.create_piece(x=4, y=6, type="pawn", team=0)
        self.w_p6 = self.create_piece(x=5, y=6, type="pawn", team=0)
        self.w_p7 = self.create_piece(x=6, y=6, type="pawn", team=0)
        self.w_p8 = self.create_piece(x=7, y=6, type="pawn", team=0)
