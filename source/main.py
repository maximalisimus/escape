#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pathlib
from typing import Tuple
from enum import Enum
import random

class NoValue(Enum):
	''' Base Enum class elements '''

	def __repr__(self):
		return f"{self.__class__}: {self.name}"
	
	def __str__(self):
		return f"{self.name}"
	
	def __call__(self):
		return f"{self.value}"

class LevelCode(NoValue):
	Wall = 1
	Ladder = 2
	Door = 3
	HatchBombs = 4
	LeftPistol = 6
	RightPistol = 5
	Empty = 7
	
	@classmethod
	def GetCodeValue(cls, value):
		for x in cls:
			if value == x.value:
				return x
		return None
	
	@classmethod
	def GetCodeName(cls, OnName):
		for x in cls:
			if OnName == x:
				return x
		return None

class SelectHeroPos(NoValue):
	CENTER = 1
	LEFT = 2
	RIGHT = 3
	
	@classmethod
	def GetHeroPosValue(cls, value):
		for x in cls:
			if value == x.value:
				return x
		return None
	
	@classmethod
	def GetHeroPosName(cls, OnName):
		for x in cls:
			if OnName == x:
				return x
		return None

class TypeBlock(NoValue):
	Wall = 1
	Ladder = 2
	Bonus = 3
	Weapon = 4
	HatchBombs = 5
	LeftPistol = 6
	RightPistol = 7
	DoorOut = 8
	DoorIn = 9
	Door = 10
	Explotion = 11
	Clouds = 12
	Helicopter = 13
	Hero = 14
	Unknown = 15
	
	@classmethod
	def GetTypeBlocksValue(cls, value):
		for x in cls:
			if value == x.value:
				return x
		return None
	
	@classmethod
	def GetTypeBlocksName(cls, OnName):
		for x in cls:
			if OnName == x:
				return x
		return None

pygame.mixer.pre_init(44100, -16, 1, 512) # важно прописать до pygame.init()
pygame.init()

W, H = 596, 385
screen1 = pygame.display.set_mode((W, H))
pygame.display.set_caption("Esc")
pygame.display.set_icon(pygame.image.load(str(pathlib.Path('./config/').joinpath('logo.png').resolve())))

clock = pygame.time.Clock()
FPS = 60

Old_Score = 0
Old_Level = 1
Old_Live = 4

isStart = False
isGame = False

isUp = isLeft = isRight = isDown = isJump = False

size_surf_score = (92,22)
size_surf_level = (26, 22)
size_surf_lives = (128,32)
size_helicopter = (72, 48)

size_blocks = 24

# 16 row x 18 column (24 pixel x 24 pixel)
row_table = 16
col_table = 18
size_table = (432, 384)
surf_table = pygame.Surface((size_table[0], size_table[1]), pygame.SRCALPHA, 32).convert_alpha()
rect_table = surf_table.get_rect(topleft=(0, 0))

coord_score = (475,40)
coord_level = (510, 110.5)
coord_live = (460, 160)
coord_score_bg = (450, 0)
coord_helicopter = (216, 48)
coord_blade_side = (5, 15)
coord_blade_up = (22, 12)

surf_score = pygame.Surface((size_surf_score[0], size_surf_score[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_level = pygame.Surface((size_surf_level[0], size_surf_level[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_lives = pygame.Surface((size_surf_lives[0], size_surf_lives[1]), pygame.SRCALPHA, 32).convert_alpha()

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
					0: {
						'name': 'alarm',
						'surf': pygame.image.load(str(pathlib.Path('./images/alarm.png').resolve())).convert_alpha(),
						'score': 100,
						'type': TypeBlock.Bonus,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/alarm.WAV').resolve())),
						},
					1: {
						'name': 'burger',
						'surf': pygame.image.load(str(pathlib.Path('./images/burger.png').resolve())).convert_alpha(),
						'score': 50,
						'type': TypeBlock.Bonus,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/burger.WAV').resolve())),
						},
					2: {
						'name': 'clock',
						'surf': pygame.image.load(str(pathlib.Path('./images/clock.png').resolve())).convert_alpha(),
						'score': 30,
						'type': TypeBlock.Bonus,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/clock.WAV').resolve())),
						},
					3: {
						'name': 'coffee',
						'surf': pygame.image.load(str(pathlib.Path('./images/coffee.png').resolve())).convert_alpha(),
						'score': 20,
						'type': TypeBlock.Bonus,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/coffee.WAV').resolve())),
						},
					4: {
						'name': 'cola',
						'surf': pygame.image.load(str(pathlib.Path('./images/cola.png').resolve())).convert_alpha(),
						'score': 10,
						'type': TypeBlock.Bonus,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/cola.WAV').resolve())),
						},
					5: {
						'name': 'stop',
						'surf': pygame.image.load(str(pathlib.Path('./images/stop.png').resolve())).convert_alpha(),
						'score': 1,
						'type': TypeBlock.Bonus,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/stop.WAV').resolve())),
						},
					6: {
						'name': 'thermos',
						'surf': pygame.image.load(str(pathlib.Path('./images/thermos.png').resolve())).convert_alpha(),
						'score': 1,
						'type': TypeBlock.Bonus,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/thermos.WAV').resolve())),
						},
				},
		'sep_bonus': 
					{
						0: {
							'name': 'heart',
							'surf': pygame.image.load(str(pathlib.Path('./images/heart.png').resolve())).convert_alpha(),
							'score': 1,
							'type': TypeBlock.Bonus,
							'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/heart.WAV').resolve())),
							},
						1: {
						'name': 'medicine_chest',
						'surf': pygame.image.load(str(pathlib.Path('./images/medicine-chest.png').resolve())).convert_alpha(),
						'score': 1,
						'type': TypeBlock.Bonus,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/live.WAV').resolve())),
						},
					},
		'wall': {
				0: {
					'surf': pygame.image.load(str(pathlib.Path('./images/tile-1.png').resolve())).convert_alpha(),
					'name': 'tile',
					'type': TypeBlock.Wall,
					},
				1: {
					'surf': pygame.image.load(str(pathlib.Path('./images/tile-2.png').resolve())).convert_alpha(),
					'name': 'tile',
					'type': TypeBlock.Wall,
					},
				2: {
					'surf': pygame.image.load(str(pathlib.Path('./images/tile-3.png').resolve())).convert_alpha(),
					'name': 'tile',
					'type': TypeBlock.Wall,
					},
				3: {
					'surf': pygame.image.load(str(pathlib.Path('./images/tile-4.png').resolve())).convert_alpha(),
					'name': 'tile',
					'type': TypeBlock.Wall,
					},
				4: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/tile-5.png').resolve())).convert_alpha(),
					'name': 'tile',
					'type': TypeBlock.Wall,
					},
				5: {
					'surf': pygame.image.load(str(pathlib.Path('./images/tile-6.png').resolve())).convert_alpha(),
					'name': 'tile',
					'type': TypeBlock.Wall,
					},
				},
		'bg': {
				0: {
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_1.png').resolve())).convert_alpha(),
					'name': 'bg',
					'type': TypeBlock.Clouds,
					},
				1: {
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_2.png').resolve())).convert_alpha(),
					'name': 'bg',
					'type': TypeBlock.Clouds,
					},
				2: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_3.png').resolve())).convert_alpha(),
					'name': 'bg',
					'type': TypeBlock.Clouds,
					},
				3: {
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_4.png').resolve())).convert_alpha(),
					'name': 'bg',
					'type': TypeBlock.Clouds,
					},
				4: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_5.png').resolve())).convert_alpha(),
					'name': 'bg',
					'type': TypeBlock.Clouds,
					},
				5: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_6.png').resolve())).convert_alpha(),
					'name': 'bg',
					'type': TypeBlock.Clouds,
					},
				6: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_t.png').resolve())).convert_alpha(),
					'name': 'bg',
					'type': TypeBlock.Unknown,
					},
				7: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/esc-bg.png').resolve())).convert_alpha(),
					'name': 'bg',
					'type': TypeBlock.Unknown,
					},
				8: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/score-bg.png').resolve())).convert_alpha(),
					'name': 'bg',
					'type': TypeBlock.Unknown,
					},
			},
		'weapon': {
					1: { 
							'name': 'bomb',
							'surf': pygame.image.load(str(pathlib.Path('./images/bomb.png').resolve())).convert_alpha(),
							'type': TypeBlock.Weapon,
							'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/bomb.WAV').resolve())),
						},
					2: { 
							'name': 'shot',
							'surf': pygame.image.load(str(pathlib.Path('./images/bullet.png').resolve())).convert_alpha(),
							'type': TypeBlock.Weapon,
							'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/shot.WAV').resolve())),
						},
				},
		'else': {
					1: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/hatch-bombs.png').resolve())).convert_alpha(),
						'name': 'hatchbombs',
						'type': TypeBlock.HatchBombs,
						},
					2: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/hatch-bombs-2.png').resolve())).convert_alpha(),
						'name': 'hatchbombs',
						'type': TypeBlock.HatchBombs,
						},
					3: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/Helicopter_1.png').resolve())).convert_alpha(),
						'name': 'helicopter',
						'type': TypeBlock.Helicopter,
						},
					4: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/Helicopter_2.png').resolve())).convert_alpha(),
						'name': 'helicopter',
						'type': TypeBlock.Helicopter,
						},
					5: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/Helicopter_3.png').resolve())).convert_alpha(),
						'name': 'helicopter',
						'type': TypeBlock.Helicopter,
						},
					6: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/Helicopter_4.png').resolve())).convert_alpha(),
						'name': 'helicopter',
						'type': TypeBlock.Helicopter,
						},
					7: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/ladder.png').resolve())).convert_alpha(),
						'name': 'ladder',
						'type': TypeBlock.Ladder,
						},
					8: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/ladder-2.png').resolve())).convert_alpha(),
						'name': 'ladder',
						'type': TypeBlock.Ladder,
						},
					9: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/left-pistol.png').resolve())).convert_alpha(),
						'name': 'pistol',
						'type': TypeBlock.LeftPistol,
						},
					10: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/right-pistol.png').resolve())).convert_alpha(),
						'name': 'pistol',
						'type': TypeBlock.RightPistol,
						},
					11: {
						'surf': pygame.image.load(str(pathlib.Path('./images/live-bg.png').resolve())).convert_alpha(),
						'name': 'live-bg',
						'type': TypeBlock.Unknown,
						},
					12: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/died-bg.png').resolve())).convert_alpha(),
						'name': 'died-bg',
						'type': TypeBlock.Unknown,
						},
					13: {
						'surf': pygame.image.load(str(pathlib.Path('./images/door.png').resolve())).convert_alpha(),
						'name': 'door',
						'type': TypeBlock.Door,
						},
					14: {
						'surf': pygame.image.load(str(pathlib.Path('./images/blade-rear.png').resolve())).convert_alpha(),
						'name': 'blade-rear',
						'type': TypeBlock.Unknown,
						},
					15: {
						'surf': pygame.image.load(str(pathlib.Path('./images/blade-up.png').resolve())).convert_alpha(),
						'name': 'blade-up',
						'type': TypeBlock.Unknown,
						},
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
			'hero': {
						0: { 
							'surf': pygame.image.load(str(pathlib.Path('./images/hero.png').resolve())).convert_alpha(),
							'name': 'hero',
							'type': TypeBlock.Hero,
							},
						1: { 
							'surf': pygame.image.load(str(pathlib.Path('./images/hero-side-left.png').resolve())).convert_alpha(),
							'name': 'hero',
							'type': TypeBlock.Hero,
							},
					},
			'explotion': {
							0: {
								'surf': pygame.image.load(str(pathlib.Path('./images/exp-1.png').resolve())).convert_alpha(),
								'name': 'explotion',
								'type': TypeBlock.Explotion,
								},
							1: {
								'surf': pygame.image.load(str(pathlib.Path('./images/exp-2.png').resolve())).convert_alpha(),
								'name': 'explotion',
								'type': TypeBlock.Explotion,
								},
							2: {
								'surf': pygame.image.load(str(pathlib.Path('./images/exp-3.png').resolve())).convert_alpha(),
								'name': 'explotion',
								'type': TypeBlock.Explotion,
								},
							3: {
								'surf': pygame.image.load(str(pathlib.Path('./images/exp-4.png').resolve())).convert_alpha(),
								'name': 'explotion',
								'type': TypeBlock.Explotion,
								},
							4: {
								'surf': pygame.image.load(str(pathlib.Path('./images/exp-5.png').resolve())).convert_alpha(),
								'name': 'explotion',
								'type': TypeBlock.Explotion,
								},
							5: {
								'surf': pygame.image.load(str(pathlib.Path('./images/exp-6.png').resolve())).convert_alpha(),
								'name': 'hero',
								'type': TypeBlock.Explotion,
								},
						},
		}

pre_levels = map(lambda x: pathlib.Path('./levels/').joinpath(f"ESC_{x}.DAT").resolve(), range(1,31))
files_levels = tuple(map(lambda x: str(x), filter(lambda y: y.exists(), pre_levels)))
del pre_levels

pygame.mixer.music.load(str(pathlib.Path('./sounds/music.mp3').resolve()))

effects = {
			'applause': pygame.mixer.Sound(str(pathlib.Path('./sounds/applause.WAV').resolve())),
			'jump': pygame.mixer.Sound(str(pathlib.Path('./sounds/jump.WAV').resolve())),
			'final': pygame.mixer.Sound(str(pathlib.Path('./sounds/final.WAV').resolve())),
			'start': pygame.mixer.Sound(str(pathlib.Path('./sounds/start.WAV').resolve())),
			'helicopter': pygame.mixer.Sound(str(pathlib.Path('./sounds/helicopter.WAV').resolve()))
		}

pos_clicked = {
				1: {
						0: (516, 222),
						1: (538, 246),
					},
				2: {
						0: (492, 246),
						1: (516, 268),
					},
				3: {
						0: (516, 246),
						1: (538, 268),
					},
				4: {
						0: (538, 246),
						1: (562, 268),
					},
				5: {
						0: (516, 268),
						1: (538, 294),
					},
			}

bonus_line = (3, 6, 9, 12, 15)

LevelMap = pygame.sprite.Group()
DoorMap = pygame.sprite.Group()
PistolMap = pygame.sprite.Group()
HatchBombMap = pygame.sprite.Group()
BonusMap = pygame.sprite.Group()

PosCollision = {
				1: {
						12: (6, 8),
					},
				2: {
						6: (8, 13),
					},
				3: {
						6: (7, 12),
					},
				4: {
						12: (5, 10),
					},
				8: {
						9: (7, 13),
						12: (7, 15),
					},
				9: {
						6: (5, 11),
					},
				11: {
						12: (7, 9),
					},
				13: {
						6: (7, 18),
						9: (7, 18),
						12: (7, 18),
					},
				15: {
						3: (11, 13),
						6: (5, 7),
						9: (11, 13),
						12: (7, 9),
					},
				16: {
						3: (8, 10),
					},
				20: {
						9: (7, 13),
						12: (7, 15),
					},
				24: {
						9: (6, 10),
						12: (5, 11),
					},
				27: {
						3: (11, 13),
						6: (5, 7),
						9: (11, 13),
						12: (7, 9),
					},
				28: {
						6: (5, 11),
					},
				29: {
						9: (7, 13),
						12: (7, 15),
					},
				30: {
						3: (1, 17),
					},
				}

def SwitchShot(CasePos):
	return {
			LevelCode.LeftPistol: (images['weapon'][2]['surf'], images['weapon'][2]['name'], images['weapon'][2]['type'], images['weapon'][2]['sound']),
			LevelCode.RightPistol: (pygame.transform.flip(images['weapon'][2]['surf'], True, False), images['weapon'][2]['name'], images['weapon'][2]['type'], images['weapon'][2]['sound']),
	}.get(CasePos, (images['weapon'][2]['surf'], images['weapon'][2]['name'], images['weapon'][2]['type'], images['weapon'][2]['sound']))

def SwitchDoor(level_code):
	return {
			LevelCode.Door: (images['else'][13]['surf'], images['else'][13]['type']),
	}.get(level_code, (images['else'][13]['surf'], images['else'][13]['type']))

def SwitchPistol(CasePos):
	return {
			LevelCode.LeftPistol: (images['else'][9]['surf'],images['else'][9]['type']),
			LevelCode.RightPistol: (images['else'][10]['surf'], images['else'][10]['type']),
	}.get(CasePos, (images['else'][9]['surf'],images['else'][9]['type']))

def SwitchHatchBombs(CaseLevel):
	return {
			1: (images['else'][1]['surf'], images['else'][1]['type']),
			2: (images['else'][1]['surf'], images['else'][1]['type']),
			3: (images['else'][1]['surf'], images['else'][1]['type']),
			4: (images['else'][1]['surf'], images['else'][1]['type']),
			5: (images['else'][1]['surf'], images['else'][1]['type']),
			6: (images['else'][1]['surf'], images['else'][1]['type']),
			7: (images['else'][1]['surf'], images['else'][1]['type']),
			8: (images['else'][1]['surf'], images['else'][1]['type']),
			9: (images['else'][1]['surf'], images['else'][1]['type']),
			10: (images['else'][1]['surf'], images['else'][1]['type']),
			11: (images['else'][1]['surf'], images['else'][1]['type']),
			12: (images['else'][1]['surf'], images['else'][1]['type']),
			13: (images['else'][1]['surf'], images['else'][1]['type']),
			14: (images['else'][1]['surf'], images['else'][1]['type']),
			15: (images['else'][1]['surf'], images['else'][1]['type']),
			16: (images['else'][1]['surf'], images['else'][1]['type']),
			17: (images['else'][1]['surf'], images['else'][1]['type']),
			18: (images['else'][1]['surf'], images['else'][1]['type']),
			19: (images['else'][1]['surf'], images['else'][1]['type']),
			20: (images['else'][1]['surf'], images['else'][1]['type']),
			21: (images['else'][1]['surf'], images['else'][1]['type']),
			22: (images['else'][1]['surf'], images['else'][1]['type']),
			23: (images['else'][1]['surf'], images['else'][1]['type']),
			24: (images['else'][1]['surf'], images['else'][1]['type']),
			25: (images['else'][1]['surf'], images['else'][1]['type']),
			26: (images['else'][1]['surf'], images['else'][1]['type']),
			27: (images['else'][1]['surf'], images['else'][1]['type']),
			28: (images['else'][1]['surf'], images['else'][1]['type']),
			29: (images['else'][1]['surf'], images['else'][1]['type']),
			30: (images['else'][2]['surf'], images['else'][2]['type']),
	}.get(CaseLevel, (images['else'][1]['surf'], images['else'][1]['type']))

def SwitchLadder(CaseLevel):
	return {
			1: (images['else'][7]['surf'], images['else'][7]['type']),
			2: (images['else'][7]['surf'], images['else'][7]['type']),
			3: (images['else'][7]['surf'], images['else'][7]['type']),
			4: (images['else'][7]['surf'], images['else'][7]['type']),
			5: (images['else'][7]['surf'], images['else'][7]['type']),
			6: (images['else'][7]['surf'], images['else'][7]['type']),
			7: (images['else'][7]['surf'], images['else'][7]['type']),
			8: (images['else'][7]['surf'], images['else'][7]['type']),
			9: (images['else'][7]['surf'], images['else'][7]['type']),
			10: (images['else'][7]['surf'], images['else'][7]['type']),
			11: (images['else'][7]['surf'], images['else'][7]['type']),
			12: (images['else'][7]['surf'], images['else'][7]['type']),
			13: (images['else'][7]['surf'], images['else'][7]['type']),
			14: (images['else'][7]['surf'], images['else'][7]['type']),
			15: (images['else'][7]['surf'], images['else'][7]['type']),
			16: (images['else'][7]['surf'], images['else'][7]['type']),
			17: (images['else'][7]['surf'], images['else'][7]['type']),
			18: (images['else'][7]['surf'], images['else'][7]['type']),
			19: (images['else'][7]['surf'], images['else'][7]['type']),
			20: (images['else'][7]['surf'], images['else'][7]['type']),
			21: (images['else'][7]['surf'], images['else'][7]['type']),
			22: (images['else'][7]['surf'], images['else'][7]['type']),
			23: (images['else'][7]['surf'], images['else'][7]['type']),
			24: (images['else'][7]['surf'], images['else'][7]['type']),
			25: (images['else'][7]['surf'], images['else'][7]['type']),
			26: (images['else'][7]['surf'], images['else'][7]['type']),
			27: (images['else'][7]['surf'], images['else'][7]['type']),
			28: (images['else'][7]['surf'], images['else'][7]['type']),
			29: (images['else'][7]['surf'], images['else'][7]['type']),
			30: (images['else'][8]['surf'], images['else'][8]['type']),
	}.get(CaseLevel, (images['else'][7]['surf'], images['else'][7]['type']))

def SwitchWall(CaseLevel):
	return {
		1: (images['wall'][0]['surf'], images['wall'][0]['type']),
		2: (images['wall'][0]['surf'], images['wall'][0]['type']),
		3: (images['wall'][0]['surf'], images['wall'][0]['type']),
		4: (images['wall'][0]['surf'], images['wall'][0]['type']),
		5: (images['wall'][0]['surf'], images['wall'][0]['type']),
		6: (images['wall'][1]['surf'], images['wall'][1]['type']),
		7: (images['wall'][1]['surf'], images['wall'][1]['type']),
		8: (images['wall'][1]['surf'], images['wall'][1]['type']),
		9: (images['wall'][1]['surf'], images['wall'][1]['type']),
		10: (images['wall'][1]['surf'], images['wall'][1]['type']),
		11: (images['wall'][1]['surf'], images['wall'][1]['type']),
		12: (images['wall'][2]['surf'], images['wall'][2]['type']),
		13: (images['wall'][2]['surf'], images['wall'][2]['type']),
		14: (images['wall'][2]['surf'], images['wall'][2]['type']),
		15: (images['wall'][2]['surf'], images['wall'][2]['type']),
		16: (images['wall'][2]['surf'], images['wall'][2]['type']),
		17: (images['wall'][2]['surf'], images['wall'][2]['type']),
		18: (images['wall'][3]['surf'], images['wall'][3]['type']),
		19: (images['wall'][3]['surf'], images['wall'][3]['type']),
		20: (images['wall'][3]['surf'], images['wall'][3]['type']),
		21: (images['wall'][3]['surf'], images['wall'][3]['type']),
		22: (images['wall'][3]['surf'], images['wall'][3]['type']),
		23: (images['wall'][3]['surf'], images['wall'][3]['type']),
		24: (images['wall'][4]['surf'], images['wall'][4]['type']),
		25: (images['wall'][4]['surf'], images['wall'][4]['type']),
		26: (images['wall'][4]['surf'], images['wall'][4]['type']),
		27: (images['wall'][4]['surf'], images['wall'][4]['type']),
		28: (images['wall'][4]['surf'], images['wall'][4]['type']),
		29: (images['wall'][4]['surf'], images['wall'][4]['type']),
		30: (images['wall'][5]['surf'], images['wall'][5]['type']),
	}.get(CaseLevel, (images['wall'][0]['surf'], images['wall'][0]['type']))

def SwitchClouds(CaseLevel):
	return {
			1: images['bg'][0]['surf'],
			2: images['bg'][0]['surf'],
			3: images['bg'][0]['surf'],
			4: images['bg'][0]['surf'],
			5: images['bg'][0]['surf'],
			6: images['bg'][1]['surf'],
			7: images['bg'][1]['surf'],
			8: images['bg'][1]['surf'],
			9: images['bg'][1]['surf'],
			10: images['bg'][1]['surf'],
			11: images['bg'][1]['surf'],
			12: images['bg'][2]['surf'],
			13: images['bg'][2]['surf'],
			14: images['bg'][2]['surf'],
			15: images['bg'][2]['surf'],
			16: images['bg'][2]['surf'],
			17: images['bg'][2]['surf'],
			18: images['bg'][3]['surf'],
			19: images['bg'][3]['surf'],
			20: images['bg'][3]['surf'],
			21: images['bg'][3]['surf'],
			22: images['bg'][3]['surf'],
			23: images['bg'][3]['surf'],
			24: images['bg'][4]['surf'],
			25: images['bg'][4]['surf'],
			26: images['bg'][4]['surf'],
			27: images['bg'][4]['surf'],
			28: images['bg'][4]['surf'],
			29: images['bg'][4]['surf'],
			30: images['bg'][5]['surf'],
	}.get(CaseLevel, images['bg'][1]['surf'])

def SwitchHero(CasePos):
	return {
			SelectHeroPos.CENTER: images['hero'][0]['surf'],
			SelectHeroPos.LEFT: images['hero'][1]['surf'],
			SelectHeroPos.RIGHT: pygame.transform.flip(images['hero'][1]['surf'], True, False),
	}.get(CasePos, images['hero'][0]['surf'])

def SwitchBlockMap(code: LevelCode, level: int = 1):
	global surf_empty
	return {
			LevelCode.Wall: SwitchWall(level),
			LevelCode.Door: SwitchDoor(code),
			LevelCode.HatchBombs: SwitchHatchBombs(level),
			LevelCode.Ladder: SwitchLadder(level),
			LevelCode.LeftPistol: SwitchPistol(code),
			LevelCode.RightPistol: SwitchPistol(code),
	}.get(code, None)

class Block(pygame.sprite.Sprite):
	
	def __init__(self, surf, ontype: TypeBlock, CoordXY: Tuple[int, int], group = None, score = None, sound = None, onName = None):
		pygame.sprite.Sprite.__init__(self)
		self.image = surf
		self.ontype = ontype
		self.rect = self.image.get_rect(topleft=CoordXY)
		self.score = score
		self.sound = sound
		self.onName = onName
		if group != None:
			self.add(group)
	
	def update(self, *args):
		# self.rect.x = args[0]
		# self.rect.y = args[1]
		# self.kill()
		pass

class Helicopter(pygame.sprite.Sprite):
	
	def __init__(self):
		self.copters = (images['else'][3]['surf'], images['else'][4]['surf'], images['else'][5]['surf'], images['else'][6]['surf'])
		self.blade = (images['else'][14]['surf'], images['else'][15]['surf'])
		self.image = pygame.Surface.copy(self.copters[0])
		self.rect = self.image.get_rect(topleft=(coord_helicopter[0], coord_helicopter[1]))
		self.ontype = images['else'][1]['type']
		self.sound = effects['helicopter']
		self.isAnim = False
		self.isBlade = False
		self.last_update = pygame.time.get_ticks()
		self.frame = 0
		self.frame_rate = 500
		self.blade_last_update = pygame.time.get_ticks()
		self.blade_frame_rate = 30
		self.takeoff_last_update = pygame.time.get_ticks()
		self.takeoff_frame_rate = 50
		self.sound_last_update = pygame.time.get_ticks()
		self.sound_frame_rate = 600
		self.count = 0
		self.isTakeoff = False
		self.isFine = False
		self.blade_rear = pygame.Surface.copy(self.blade[0])
		self.blade_up = pygame.Surface.copy(self.blade[1])
	
	def reset(self):
		self.image = pygame.Surface.copy(self.copters[0])
		self.rect = self.image.get_rect(topleft=(coord_helicopter[0], coord_helicopter[1]))
		self.isAnim = False
		self.isBlade = False
		self.last_update = pygame.time.get_ticks()
		self.frame = 0
		self.frame_rate = 500
		self.blade_last_update = pygame.time.get_ticks()
		self.blade_frame_rate = 30
		self.takeoff_last_update = pygame.time.get_ticks()
		self.takeoff_frame_rate = 50
		self.sound_last_update = pygame.time.get_ticks()
		self.sound_frame_rate = 600
		self.count = 0
		self.isTakeoff = False
		self.isFine = False
		self.blade_rear = pygame.Surface.copy(self.blade[0])
		self.blade_up = pygame.Surface.copy(self.blade[1])
	
	def update(self, *args):
		if not self.isFine:
			if (self.rect.y + size_helicopter[1] <= 0):
				self.isFine = True
				self.isAnim = False
			else:
				if self.isAnim:
					now = pygame.time.get_ticks()
					if now - self.blade_last_update > self.blade_frame_rate:
						self.blade_last_update = now
						if self.isBlade:
							self.image = pygame.Surface.copy(self.copters[self.frame])
							self.blade_rear = self.rotate_surf(self.blade_rear, 90)
							self.image.blit(self.blade_rear, (coord_blade_side[0], coord_blade_side[1]))
							self.blade_up = self.rotate_surf(self.blade_up, 180)
							self.blade_up = pygame.transform.flip(self.blade_up, False, True)
							self.image.blit(self.blade_up, (coord_blade_up[0], coord_blade_up[1]))
					if now - self.takeoff_last_update > self.takeoff_frame_rate:
						self.takeoff_last_update = now
						if self.isBlade:
							self.count += 1
						if self.count == 10:
							self.isTakeoff = True
						if self.isTakeoff:
							self.rect.x += 1
							self.rect.y -= 1
					if now - self.sound_last_update > self.sound_frame_rate:
						self.sound_last_update = now
						if self.isBlade:
							self.sound.play()
					if now - self.last_update > self.frame_rate:
						self.last_update = now
						if self.frame == 3:
							self.isBlade = True
						else:
							self.image = pygame.Surface.copy(self.copters[self.frame])
							self.frame += 1

	def rotate_surf(self, surf, angle):
		loc = surf.get_rect().center
		rot_sprite = pygame.transform.rotate(surf, angle)
		rot_sprite.get_rect().center = loc
		return rot_sprite

helicopter = Helicopter()

def BuildLevel(surface, GroupMap, GroupDoor, GroupHatch, GroupPistol, level):
	global screen1
	global LevelMap
	global DoorMap
	global PistolMap
	global HatchBombMap
	global helicopter
	
	global size_blocks
	
	GroupMap.empty()
	GroupDoor.empty()
	GroupHatch.empty()
	GroupPistol.empty()
	surface.blit(SwitchClouds(level), (0, 0))
	with open(files_levels[level-1], 'r') as f:
		lines = f.readlines()
	x = y = 0
	DoorInOut = True
	for row in lines:
		for col in row.replace('\n', '').replace(' ','7'):
			if LevelCode.GetCodeValue(int(col)) != LevelCode.Empty:
				tmp = SwitchBlockMap(LevelCode.GetCodeValue(int(col)), level)
				if tmp[1] == TypeBlock.Door:
					if DoorInOut:
						block = Block(tmp[0], TypeBlock.DoorOut, (x, y), GroupMap)
						DoorInOut = False
					else:
						block = Block(tmp[0], TypeBlock.DoorIn, (x, y), GroupMap)
				else:
					block = Block(tmp[0], tmp[1], (x, y), GroupMap)
				if tmp[1] == TypeBlock.HatchBombs:
					GroupHatch.add(block)
				elif tmp[1] == TypeBlock.LeftPistol:
					GroupPistol.add(block)
				elif tmp[1] == TypeBlock.RightPistol:
					GroupPistol.add(block)
				elif tmp[1] == TypeBlock.Door:
					GroupDoor.add(block)
			x+=size_blocks
		y+=size_blocks
		x=0
	GroupMap.draw(surface)
	if level == 30:
		helicopter.reset()
		screen1.blit(surf_table, (0, 0))
		screen1.blit(helicopter.image, helicopter.rect)

def GenerateBonus(level: int):
	global LevelMap
	global BonusMap
	global row_table
	global col_table
	empty_surf = pygame.Surface((size_blocks, size_blocks), pygame.SRCALPHA, 32).convert_alpha()
	pygame.draw.rect(empty_surf, (0, 0, 0), (0, 0, size_blocks, size_blocks))
	empty_block = Block(empty_surf, TypeBlock.Unknown, (0, 0))
	rand_bonus_num = random.randint(0, 6)
	select_col = random.choice(bonus_line)
	on_col = select_col - 1
	y = empty_block.rect.y = on_col * size_blocks
	collisions = PosCollision.get(level, dict()).get(select_col, False)
	on_row = random.randint(1, col_table-2)
	x = empty_block.rect.x = on_row * size_blocks
	hits = pygame.sprite.spritecollide(empty_block, LevelMap, False)
	if collisions:
		while ((on_row in range(collisions[0]-1, collisions[1])) or hits):
			on_row = random.randint(1, col_table-2)
			x = empty_block.rect.x = on_row * size_blocks
			hits = pygame.sprite.spritecollide(empty_block, LevelMap, False)
	else:
		while (hits):
			on_row = random.randint(1, col_table-2)
			x = empty_block.rect.x = on_row * size_blocks
			hits = pygame.sprite.spritecollide(empty_block, LevelMap, False)
	block = Block(images['bonus'][rand_bonus_num]['surf'], images['bonus'][rand_bonus_num]['type'], (x, y), BonusMap, images['bonus'][rand_bonus_num]['score'], images['bonus'][rand_bonus_num]['sound'], images['bonus'][rand_bonus_num]['name'])
	LevelMap.add(block)
	
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

def DrawTotal(surface, score: int, level: int, live: int, isFull: bool = False, isBG: bool = False):
	global images
	global Old_Score
	global Old_Level
	global Old_Live
	
	global surf_score
	global surf_level
	global surf_lives
	
	global pos_live_x
	global pos_live_y
	
	if isBG:
		surface.blit(images['bg'][7]['surf'], (0, 0))
		surface.blit(images['bg'][8]['surf'], (coord_score_bg[0], coord_score_bg[1]))
	
	if isFull:
		DrawScore(surf_score, score)
		Old_Score = score
		DrawLevel(surf_level, level)
		Old_Level = level
		for i in range(1, live+1):
			DrawLive(surf_lives, images['else'][11]['surf'], (pos_live_x[i], 0))
		Old_Live = live
	
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
			DrawLive(surf_lives, images['else'][11]['surf'], (pos_live_x[live], 0))
		elif live == Old_Live:
			pass
		elif (live < Old_Live):
			if (Old_Live - live) == 1:
				DrawLive(surf_lives, images['else'][12]['surf'], (pos_live_x[Old_Live], 0))
			else:
				for i in range(Old_Live, live, -1):
					DrawLive(surf_lives, images['else'][12]['surf'], (pos_live_x[i], 0))
		surface.blit(surf_lives, (coord_live[0], coord_live[1]))
		Old_Live = live
	else:
		surface.blit(surf_lives, (coord_live[0], coord_live[1]))

def Restart(surface):
	global Old_Score
	global Old_Level
	global Old_Live
	
	global LevelMap
	global DoorMap
	global PistolMap
	global HatchBombMap
	global surf_table
	
	Old_Score = 0
	Old_Level = 1
	Old_Live = 4
	DrawTotal(surface, 0, 1, 4, True, True)
	BuildLevel(surf_table, LevelMap, DoorMap, HatchBombMap, PistolMap, 1)
	surface.blit(surf_table, (0, 0))

def SwitchInitImage(pos: Tuple[int, int], surface):
	global isGame
	global isStart
	global pos_clicked
	global W
	global H
	if (pos[0] >= 0) and (pos[0] <= W):
		if ((pos[1] >= 0) and (pos[1] <= H)):
			isGame = True
			isStart = False
			Restart(surface)
			pygame.display.update()

def MouseClicked(pos: Tuple[int, int], isValue):
	global isUp
	global isLeft
	global isRight
	global isDown
	global isJump
	global isGame
	global pos_clicked

	if isGame:
		if ((pos[0] >= pos_clicked[1][0][0]) and (pos[0] <= pos_clicked[1][1][0])):
			if ((pos[1] >= pos_clicked[1][0][1]) and (pos[1] <= pos_clicked[1][1][1])):
				isUp = isValue
			elif ((pos[1] >= pos_clicked[3][0][1]) and (pos[1] <= pos_clicked[3][1][1])):
				isJump = isValue
			elif ((pos[1] >= pos_clicked[5][0][1]) and (pos[1] <= pos_clicked[5][1][1])):
				isDown = isValue
		elif ((pos[0] >= pos_clicked[2][0][0]) and (pos[0] <= pos_clicked[2][1][0])):
			if ((pos[1] >= pos_clicked[2][0][1]) and (pos[1] <= pos_clicked[2][1][1])):
				isLeft = isValue
		elif ((pos[0] >= pos_clicked[4][0][0]) and (pos[0] <= pos_clicked[4][1][0])):
			if ((pos[1] >= pos_clicked[4][0][1]) and (pos[1] <= pos_clicked[4][1][1])):
				isRight = isValue
	# 0. (0, 0) - (434, 385) - work_table
	# 1. (516, 222) - (538, 246) - up
	# 2. (492, 246) - (516, 268) - left
	# 3. (516, 246) - (538, 268) - jump
	# 4. (538, 246) - (562, 268) - right
	# 5. (516, 268) - (538, 294) - down

def DrawHero(surface):
	# Hero Draw Test and how to animation legs ?
	surf_hero = pygame.Surface((15, 19), pygame.SRCALPHA, 32).convert_alpha()
	# Hero, images['hero'][1] - Hero-Side
	surf_hero.blit(images['hero'][0]['surf'], (0, 0))
	surf_left_legs = pygame.Surface((6, 4), pygame.SRCALPHA, 32).convert_alpha()
	pygame.draw.rect(surf_left_legs, (139, 139, 139), (4, 0, 2, 4))
	pygame.draw.rect(surf_left_legs, (139, 139, 139), (0, 2, 6, 2))
	surf_hero.blit(surf_left_legs, (0, 15))
	# surf_hero.blit(surf_left_legs, (6, 13))
	surf_right_legs = pygame.transform.flip(surf_left_legs, True, False)
	surf_hero.blit(surf_right_legs, (8, 15))
	surface.blit(surf_hero, (100, 100))

def main():
	global screen1
	global clock
	global FPS
	
	global isStart
	global surf_table
	
	global isUp
	global isLeft
	global isRight
	global isDown
	global isJump
	
	global surf_table
	global rect_table
	
	global LevelMap
	global DoorMap
	global PistolMap
	global HatchBombMap
	global helicopter
	
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
	
	#Restart(screen1)
	#DrawTotal(screen1, 0, 1, 4)
	#levels = 1
	#BuildLevel(surf_table, LevelMap, DoorMap, HatchBombMap, PistolMap, levels)
	#screen1.blit(surf_table, (0, 0))
	#helicopter.isAnim = True
	#for i in range(5):
	#	GenerateBonus(levels)
	#BonusMap.draw(screen1)
	
	surf_start_bg = pygame.transform.scale(images['bg'][6]['surf'], (W, H))
	screen1.blit(surf_start_bg, (0, 0))
	pygame.display.update()
	isStart = True
	
	RUN = True
	while RUN:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				RUN = False
				exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					isJump = True
				elif event.key == pygame.K_UP:
					isUp = True
				elif event.key == pygame.K_DOWN:
					isDown = True
				elif event.key == pygame.K_LEFT:
					isLeft = True
				elif event.key == pygame.K_RIGHT:
					isRight = True
			elif event.type == pygame.KEYUP:
				if event.key in [pygame.K_SPACE, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
					isUp = isDown = isLeft = isRight = isJump = False
				# elif event.key in []:
					# pass
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if isStart:
					SwitchInitImage((event.pos[0],event.pos[1]), screen1)
				elif isGame:
					MouseClicked((event.pos[0],event.pos[1]), True)
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				MouseClicked((event.pos[0],event.pos[1]), False)
				isStart = False
				#isGame = True
		
		if isUp:
			#print('Up')
			pass
		elif isDown:
			#print('Down')
			pass
		elif isLeft:
			#print('Left')
			pass
		elif isRight:
			#print('Right')
			pass
		elif isJump:
			#print('Jump')
			pass
		
		keys = pygame.key.get_pressed()
		# if keys[pygame.K_SPACE]:
		#	print('space')
		# elif keys[pygame.K_UP]:
		#	print('Up')
		# elif keys[pygame.K_DOWN]:
		#	print('Down')
		# elif keys[pygame.K_LEFT]:
		#	print('Left')
		# elif keys[pygame.K_RIGHT]:
		#	print('Right')
		# elif keys[pygame.K_F1]:
		#	print('F1')
		# elif keys[pygame.K_F2]:
		#	print('F2')
		# elif keys[pygame.K_F3]:
		#	print('F3')
		# elif keys[pygame.K_F8]:
		#	print('F8')
		# elif keys[pygame.K_F9]:
		#	print('F9')
		# elif keys[pygame.K_F10]:
		#	print('F10')
		# elif keys[pygame.K_F11]:
		#	print('F11')
		
		#screen1.blit(surf_table, (0, 0))
		#screen1.blit(helicopter.image, helicopter.rect)
		#pygame.display.update()
		#helicopter.update()
		
		clock.tick(FPS)

if __name__ == '__main__':
	main()
