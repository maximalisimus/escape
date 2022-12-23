#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pathlib
from typing import Tuple

pygame.mixer.pre_init(44100, -16, 2, 512) # важно прописать до pygame.init()
pygame.init()

W, H = 596, 385
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Esc")
pygame.display.set_icon(pygame.image.load(str(pathlib.Path('./config/').joinpath('logo.png').resolve())))

clock = pygame.time.Clock()
FPS = 60

Score = Old_Score = 0
Level = Old_Level = 1
Live = Old_Live = 4

is_Start = True

size_surf_score = (92,22)
size_surf_level = (26, 22)
size_surf_lives = (128,32)

# 16 x 18 (24x24)
size_table = (434, 385)
surf_table = pygame.Surface((size_table[0], size_table[1]))

coord_score = (475,40)
coord_level = (510, 110.5)
coord_live = (460, 160)
coord_score_bg = (450, 0)

surf_score = pygame.Surface((size_surf_score[0], size_surf_score[1]))
surf_level = pygame.Surface((size_surf_level[0], size_surf_level[1]))
surf_lives = pygame.Surface((size_surf_lives[0], size_surf_lives[1]))

pos_live_x = {
				0: 0,
				1: 0,
				2: 32,
				3: 64,
				4: 96,
			}
pos_live_y = 0

pos_score_x = {
				0: 1,
				1: 14,
				2: 27,
				3: 40,
				4: 53,
				5: 66,
				6: 79,
			}
pos_score_y = 1

images = {
		'bonus': {
					1: {
						'name': 'alarm',
						'surf': pygame.image.load(str(pathlib.Path('./images/alarm.png').resolve())).convert_alpha(),
						'score': 100,
						'type': 'bonus',
						},
					2: {
						'name': 'burger',
						'surf': pygame.image.load(str(pathlib.Path('./images/burger.png').resolve())).convert_alpha(),
						'score': 50,
						'type': 'bonus',
						},
					3: {
						'name': 'clock',
						'surf': pygame.image.load(str(pathlib.Path('./images/clock.png').resolve())).convert_alpha(),
						'score': 30,
						'type': 'bonus',
						},
					4: {
						'name': 'coffee',
						'surf': pygame.image.load(str(pathlib.Path('./images/coffee.png').resolve())).convert_alpha(),
						'score': 20,
						'type': 'bonus',
						},
					5: {
						'name': 'cola',
						'surf': pygame.image.load(str(pathlib.Path('./images/cola.png').resolve())).convert_alpha(),
						'score': 10,
						'type': 'bonus',
						},
					6: {
						'name': 'medicine_chest',
						'surf': pygame.image.load(str(pathlib.Path('./images/medicine-chest.png').resolve())).convert_alpha(),
						'score': 1,
						'type': 'bonus',
						},
					7: {
						'name': 'stop',
						'surf': pygame.image.load(str(pathlib.Path('./images/stop.png').resolve())).convert_alpha(),
						'score': 1,
						'type': 'bonus',
						},
					8: {
						'name': 'thermos',
						'surf': pygame.image.load(str(pathlib.Path('./images/thermos.png').resolve())).convert_alpha(),
						'score': 1,
						'type': 'bonus',
						},
					9: {
						'name': 'heart',
						'surf': pygame.image.load(str(pathlib.Path('./images/heart.png').resolve())).convert_alpha(),
						'score': 1,
						'type': 'bonus',
						},
				},
		'wall': {
				1: pygame.image.load(str(pathlib.Path('./images/tile-1.png').resolve())).convert_alpha(),
				2: pygame.image.load(str(pathlib.Path('./images/tile-2.png').resolve())).convert_alpha(),
				3: pygame.image.load(str(pathlib.Path('./images/tile-3.png').resolve())).convert_alpha(),
				4: pygame.image.load(str(pathlib.Path('./images/tile-4.png').resolve())).convert_alpha(),
				5: pygame.image.load(str(pathlib.Path('./images/tile-5.png').resolve())).convert_alpha(),
				6: pygame.image.load(str(pathlib.Path('./images/tile-6.png').resolve())).convert_alpha(),
				},
		'bg': {
				1: pygame.image.load(str(pathlib.Path('./images/esc_1.png').resolve())).convert_alpha(),
				2: pygame.image.load(str(pathlib.Path('./images/esc_2.png').resolve())).convert_alpha(),
				3: pygame.image.load(str(pathlib.Path('./images/esc_3.png').resolve())).convert_alpha(),
				4: pygame.image.load(str(pathlib.Path('./images/esc_4.png').resolve())).convert_alpha(),
				5: pygame.image.load(str(pathlib.Path('./images/esc_5.png').resolve())).convert_alpha(),
				6: pygame.image.load(str(pathlib.Path('./images/esc_6.png').resolve())).convert_alpha(),
				7: pygame.image.load(str(pathlib.Path('./images/esc_t.png').resolve())).convert_alpha(),
				8: pygame.image.load(str(pathlib.Path('./images/esc-bg.png').resolve())).convert_alpha(),
				9: pygame.image.load(str(pathlib.Path('./images/score-bg.png').resolve())).convert_alpha(),
			},
		'weapon': {
					1: { 
							'name': 'bomb',
							'surf': pygame.image.load(str(pathlib.Path('./images/bomb.png').resolve())).convert_alpha(),
							'type': 'weapon',
						},
					2: { 
							'name': 'shot',
							'surf': pygame.image.load(str(pathlib.Path('./images/bullet.png').resolve())).convert_alpha(),
							'type': 'weapon',
						},
				},
		'else': {
					1: pygame.image.load(str(pathlib.Path('./images/hatch-bombs.png').resolve())).convert_alpha(),
					2: pygame.image.load(str(pathlib.Path('./images/hatch-bombs-2.png').resolve())).convert_alpha(),
					3: pygame.image.load(str(pathlib.Path('./images/Helicopter_1.png').resolve())).convert_alpha(),
					4: pygame.image.load(str(pathlib.Path('./images/Helicopter_2.png').resolve())).convert_alpha(),
					5: pygame.image.load(str(pathlib.Path('./images/Helicopter_3.png').resolve())).convert_alpha(),
					6: pygame.image.load(str(pathlib.Path('./images/Helicopter_4.png').resolve())).convert_alpha(),
					7: pygame.image.load(str(pathlib.Path('./images/ladder.png').resolve())).convert_alpha(),
					8: pygame.image.load(str(pathlib.Path('./images/ladder-2.png').resolve())).convert_alpha(),
					9: pygame.image.load(str(pathlib.Path('./images/left-pistol.png').resolve())).convert_alpha(),
					10: pygame.image.load(str(pathlib.Path('./images/right-pistol.png').resolve())).convert_alpha(),
					11: pygame.image.load(str(pathlib.Path('./images/live-bg.png').resolve())).convert_alpha(),
					12: pygame.image.load(str(pathlib.Path('./images/died-bg.png').resolve())).convert_alpha(),
					13: pygame.image.load(str(pathlib.Path('./images/door.png').resolve())).convert_alpha(),
					14: pygame.image.load(str(pathlib.Path('./images/blade-rear.png').resolve())).convert_alpha(),
					15: pygame.image.load(str(pathlib.Path('./images/blade-up.png').resolve())).convert_alpha(),
				},
		'LCD': {
					'0': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-0.png').resolve())).convert_alpha(),
					'1': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-1.png').resolve())).convert_alpha(),
					'2': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-2.png').resolve())).convert_alpha(),
					'3': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-3.png').resolve())).convert_alpha(),
					'4': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-4.png').resolve())).convert_alpha(),
					'5': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-5.png').resolve())).convert_alpha(),
					'6': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-6.png').resolve())).convert_alpha(),
					'7': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-7.png').resolve())).convert_alpha(),
					'8': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-8.png').resolve())).convert_alpha(),
					'9': pygame.image.load(str(pathlib.Path('./images/LCD/lcd-9.png').resolve())).convert_alpha(),
				},
		}

levels = tuple(map(lambda x: str(pathlib.Path('./levels/').joinpath(f"ESC_{x}.DAT").resolve()), range(1,31)))

pygame.mixer.music.load(str(pathlib.Path('./sounds/music.mp3').resolve()))

sounds = {
			'alarm': pygame.mixer.Sound(str(pathlib.Path('./sounds/alarm.WAV').resolve())),
			'applause': pygame.mixer.Sound(str(pathlib.Path('./sounds/applause.WAV').resolve())),
			'bomb': pygame.mixer.Sound(str(pathlib.Path('./sounds/bomb.WAV').resolve())),
			'burger': pygame.mixer.Sound(str(pathlib.Path('./sounds/burger.WAV').resolve())),
			'clock': pygame.mixer.Sound(str(pathlib.Path('./sounds/clock.WAV').resolve())),
			'coffee': pygame.mixer.Sound(str(pathlib.Path('./sounds/coffee.WAV').resolve())),
			'cola': pygame.mixer.Sound(str(pathlib.Path('./sounds/cola.WAV').resolve())),
			'heart': pygame.mixer.Sound(str(pathlib.Path('./sounds/heart.WAV').resolve())),
			'jump': pygame.mixer.Sound(str(pathlib.Path('./sounds/jump.WAV').resolve())),
			'live': pygame.mixer.Sound(str(pathlib.Path('./sounds/live.WAV').resolve())),
			'final': pygame.mixer.Sound(str(pathlib.Path('./sounds/final.WAV').resolve())),
			'shot': pygame.mixer.Sound(str(pathlib.Path('./sounds/shot.WAV').resolve())),
			'start': pygame.mixer.Sound(str(pathlib.Path('./sounds/start.WAV').resolve())),
			'stop': pygame.mixer.Sound(str(pathlib.Path('./sounds/stop.WAV').resolve())),
			'thermos': pygame.mixer.Sound(str(pathlib.Path('./sounds/thermos.WAV').resolve())),
		}

def print_level(level: int) -> str:
	if level<10:
		return f"0{level}"
	else:
		return f"{level}"

def print_score(score: int) -> str:
	if score < 10:
		return f"000000{score}"
	elif score < 100:
		return f"00000{score}"
	elif score < 1000:
		return f"0000{score}"
	elif score < 10000:
		return f"000{score}"
	elif score < 100000:
		return f"00{score}"
	elif score < 1000000:
		return f"0{score}"
	else:
		return f"{score}"

def DrawScore(surf, on_score: int):
	global images
	global size_surf_score
	global pos_score_x
	global pos_score_y
	pygame.draw.rect(surf, (0,0,0), (0, 0, size_surf_score[0], size_surf_score[1]))
	OnScore = tuple(print_score(on_score))
	for i in range(len(OnScore)):
		surf.blit(images['LCD'][OnScore[i]], (pos_score_x[i], pos_score_y))

def DrawLevel(surf, on_level: int):
	global images
	global size_surf_level
	global pos_score_x
	global pos_score_y
	pygame.draw.rect(surf, (0,0,0), (0, 0, size_surf_level[0], size_surf_level[1]))
	OnLevel = tuple(print_level(on_level))
	for i in range(len(OnLevel)):
		surf.blit(images['LCD'][OnLevel[i]], (pos_score_x[i], pos_score_y))

def DrawLive(screen_surf, surf, coord: Tuple[int, int]):
	screen_surf.blit(surf, (coord[0], coord[1]))

def DrawTotal(surface, score: int, level: int, live: int):
	global images
	global Score
	global Level
	global Live
	global Old_Score
	global Old_Level
	global Old_Live
	global is_Start
	
	global surf_score
	global surf_level
	global surf_lives
	
	global pos_live_x
	global pos_live_y
	
	if is_Start:
		is_Start = False
		DrawScore(surf_score, 0)
		Score = Old_Score = 0
		DrawLevel(surf_level, 1)
		Level = Old_Level = 1
		Live = Old_Live = 4
		for i in range(1,5):
			DrawLive(surf_lives, images['else'][11], (pos_live_x[i], pos_live_y))
	
	if score != Old_Score:
		DrawScore(surf_score, score)
		Old_Score = score
		surface.blit(surf_score, (coord_score[0], coord_score[1]))
	else:
		surface.blit(surf_score, (coord_score[0], coord_score[1]))
	
	if level != Old_Level:
		DrawLevel(surf_level, level)
		Old_Level = level
		surface.blit(surf_level, (coord_level[0], coord_level[1]))
	else:
		surface.blit(surf_level, (coord_level[0], coord_level[1]))
		
	if live != Old_Live:
		if live > Old_Live:
			DrawLive(surf_lives, images['else'][11], (pos_live_x[live], 0))
		else:
			DrawLive(surf_lives, images['else'][12], (pos_live_x[Old_Live], 0))
		surface.blit(surf_lives, (coord_live[0], coord_live[1]))
		Old_Live = live
	else:
		surface.blit(surf_lives, (coord_live[0], coord_live[1]))

def main():
	global Score
	global Level
	global Live
	global sc
	global clock
	global FPS
	
	global is_Start	
	global surf_table
	
	# pygame.mixer.music.play(-1)
	# pygame.mixer.music.pause()
	# pygame.mixer.music.unpause()
	# pygame.mixer.music.stop()
	# pygame.mixer.music.rewind() # Заново
	
	# start_sound = pygame.mixer.Sound(sounds['start'])
	# start_sound.play()
	# start_sound.stop()
	# start_sound.pause()
	# start_sound.unpause()
	# sounds['start'].play()
	
	sc.blit(images['bg'][8], (0, 0))
	sc.blit(images['bg'][9], (coord_score_bg[0], coord_score_bg[1]))
	
	DrawTotal(sc, 0, 1, 4)
	
	pygame.display.update()
	
	RUN = True
	while RUN:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				RUN = False
				exit()
		
		keys = pygame.key.get_pressed()
		mouse_pressed = pygame.mouse.get_pressed()
		#if mouse_pressed[0]:
		#	mouse_pos = pygame.mouse.get_pos()
		#	print(mouse_pos)
		
		clock.tick(FPS)

if __name__ == '__main__':
	main()
