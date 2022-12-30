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
