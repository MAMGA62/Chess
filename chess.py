
import pygame
from models.pieces import *
from game import Game

if __name__ == '__main__':
    pygame.init()

    game = Game()
    game.start()

    print("\nPartie Terminée !")
