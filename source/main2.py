#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pathlib
from typing import Tuple
from enum import Enum
import random
from variables import *
from myfunc import *

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
screen1 = pygame.display.set_mode((W, H))
pygame.display.set_caption("Esc")
pygame.display.set_icon(pygame.image.load(str(pathlib.Path('./config/').joinpath('logo.png').resolve())))

clock = pygame.time.Clock()

surf_table = pygame.Surface((size_table[0], size_table[1]), pygame.SRCALPHA, 32).convert_alpha()
rect_table = surf_table.get_rect(topleft=(0, 0))

surf_score = pygame.Surface((size_surf_score[0], size_surf_score[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_level = pygame.Surface((size_surf_level[0], size_surf_level[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_lives = pygame.Surface((size_surf_lives[0], size_surf_lives[1]), pygame.SRCALPHA, 32).convert_alpha()

def main():
	RUN = True
	while RUN:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				RUN = False
				exit()
		
		clock.tick(FPS)

if __name__ == '__main__':
	main()
