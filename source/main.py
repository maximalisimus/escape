#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pathlib
from typing import Tuple
from enum import Enum

class NoValue(Enum):
	''' Base Enum class elements '''

	def __repr__(self):
		return f"{self.__class__}: {self.name}"
	
	def __str__(self):
		return f"{self.name}"
	
	def __call__(self):
		return f"{self.value}"

class LevelCode(NoValue):
	Tile = 1
	Ladder = 2
	Door = 3
	HatchBombs = 4
	LeftPistol = 5
	RightPistol = 6
	
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
	Bomb = 4
	Shot = 5
	HatchBombs = 6
	Pistol = 7
	DoorOut = 8
	DoorIn = 9
	Empty = 10
	Hero = 11
	Explotion = 12
	Clouds = 13
	Helicopter = 14
	BG = 15
	Unknown = 16
	
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

pygame.mixer.pre_init(44100, -16, 2, 512) # важно прописать до pygame.init()
pygame.init()

W, H = 596, 385
sc = pygame.display.set_mode((W, H))
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

size_blocks = 24

# 16 row x 18 column (24 pixel x 24 pixel)
size_table = (432, 384)
surf_table = pygame.Surface((size_table[0], size_table[1]), pygame.SRCALPHA, 32).convert_alpha()

coord_score = (475,40)
coord_level = (510, 110.5)
coord_live = (460, 160)
coord_score_bg = (450, 0)

surf_score = pygame.Surface((size_surf_score[0], size_surf_score[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_level = pygame.Surface((size_surf_level[0], size_surf_level[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_lives = pygame.Surface((size_surf_lives[0], size_surf_lives[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_empty= pygame.Surface((size_blocks, size_blocks), pygame.SRCALPHA, 32).convert_alpha()

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
						'name': 'medicine_chest',
						'surf': pygame.image.load(str(pathlib.Path('./images/medicine-chest.png').resolve())).convert_alpha(),
						'score': 1,
						'type': TypeBlock.Bonus,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/live.WAV').resolve())),
						},
					6: {
						'name': 'stop',
						'surf': pygame.image.load(str(pathlib.Path('./images/stop.png').resolve())).convert_alpha(),
						'score': 1,
						'type': TypeBlock.Bonus,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/stop.WAV').resolve())),
						},
					7: {
						'name': 'thermos',
						'surf': pygame.image.load(str(pathlib.Path('./images/thermos.png').resolve())).convert_alpha(),
						'score': 1,
						'type': TypeBlock.Bonus,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/thermos.WAV').resolve())),
						},
					8: {
						'name': 'heart',
						'surf': pygame.image.load(str(pathlib.Path('./images/heart.png').resolve())).convert_alpha(),
						'score': 1,
						'type': TypeBlock.Bonus,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/heart.WAV').resolve())),
						},
				},
		'wall': {
				0: {
					'surf': pygame.image.load(str(pathlib.Path('./images/tile-1.png').resolve())).convert_alpha(),
					'name': 'tile',
					'score': 0,
					'type': TypeBlock.Wall,
					'sound': None,
					},
				1: {
					'surf': pygame.image.load(str(pathlib.Path('./images/tile-2.png').resolve())).convert_alpha(),
					'name': 'tile',
					'score': 0,
					'type': TypeBlock.Wall,
					'sound': None,
					},
				2: {
					'surf': pygame.image.load(str(pathlib.Path('./images/tile-3.png').resolve())).convert_alpha(),
					'name': 'tile',
					'score': 0,
					'type': TypeBlock.Wall,
					'sound': None,
					},
				3: {
					'surf': pygame.image.load(str(pathlib.Path('./images/tile-4.png').resolve())).convert_alpha(),
					'name': 'tile',
					'score': 0,
					'type': TypeBlock.Wall,
					'sound': None,
					},
				4: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/tile-5.png').resolve())).convert_alpha(),
					'name': 'tile',
					'score': 0,
					'type': TypeBlock.Wall,
					'sound': None,
					},
				5: {
					'surf': pygame.image.load(str(pathlib.Path('./images/tile-6.png').resolve())).convert_alpha(),
					'name': 'tile',
					'score': 0,
					'type': TypeBlock.Wall,
					'sound': None,
					},
				},
		'bg': {
				0: {
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_1.png').resolve())).convert_alpha(),
					'name': 'bg',
					'score': 0,
					'type': TypeBlock.Clouds,
					'sound': None,
					},
				1: {
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_2.png').resolve())).convert_alpha(),
					'name': 'bg',
					'score': 0,
					'type': TypeBlock.Clouds,
					'sound': None,
					},
				2: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_3.png').resolve())).convert_alpha(),
					'name': 'bg',
					'score': 0,
					'type': TypeBlock.Clouds,
					'sound': None,
					},
				3: {
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_4.png').resolve())).convert_alpha(),
					'name': 'bg',
					'score': 0,
					'type': TypeBlock.Clouds,
					'sound': None,
					},
				4: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_5.png').resolve())).convert_alpha(),
					'name': 'bg',
					'score': 0,
					'type': TypeBlock.Clouds,
					'sound': None,
					},
				5: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_6.png').resolve())).convert_alpha(),
					'name': 'bg',
					'score': 0,
					'type': TypeBlock.Clouds,
					'sound': None,
					},
				6: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/esc_t.png').resolve())).convert_alpha(),
					'name': 'bg',
					'score': 0,
					'type': TypeBlock.BG,
					'sound': None,
					},
				7: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/esc-bg.png').resolve())).convert_alpha(),
					'name': 'bg',
					'score': 0,
					'type': TypeBlock.BG,
					'sound': None,
					},
				8: { 
					'surf': pygame.image.load(str(pathlib.Path('./images/score-bg.png').resolve())).convert_alpha(),
					'name': 'bg',
					'score': 0,
					'type': TypeBlock.BG,
					'sound': None,
					},
			},
		'weapon': {
					1: { 
							'name': 'bomb',
							'surf': pygame.image.load(str(pathlib.Path('./images/bomb.png').resolve())).convert_alpha(),
							'type': TypeBlock.Bomb,
							'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/bomb.WAV').resolve())),
							'score': 0,
						},
					2: { 
							'name': 'shot',
							'surf': pygame.image.load(str(pathlib.Path('./images/bullet.png').resolve())).convert_alpha(),
							'type': TypeBlock.Shot,
							'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/shot.WAV').resolve())),
							'score': 0,
						},
				},
		'else': {
					1: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/hatch-bombs.png').resolve())).convert_alpha(),
						'name': 'hatchbombs',
						'score': 0,
						'type': TypeBlock.HatchBombs,
						'sound': None,
						},
					2: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/hatch-bombs-2.png').resolve())).convert_alpha(),
						'name': 'hatchbombs',
						'score': 0,
						'type': TypeBlock.HatchBombs,
						'sound': None,
						},
					3: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/Helicopter_1.png').resolve())).convert_alpha(),
						'name': 'helicopter',
						'score': 0,
						'type': TypeBlock.Helicopter,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/helicopter.WAV').resolve())),
						},
					4: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/Helicopter_2.png').resolve())).convert_alpha(),
						'name': 'helicopter',
						'score': 0,
						'type': TypeBlock.Helicopter,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/helicopter.WAV').resolve())),
						},
					5: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/Helicopter_3.png').resolve())).convert_alpha(),
						'name': 'helicopter',
						'score': 0,
						'type': TypeBlock.Helicopter,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/helicopter.WAV').resolve())),
						},
					6: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/Helicopter_4.png').resolve())).convert_alpha(),
						'name': 'helicopter',
						'score': 0,
						'type': TypeBlock.Helicopter,
						'sound': pygame.mixer.Sound(str(pathlib.Path('./sounds/helicopter.WAV').resolve())),
						},
					7: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/ladder.png').resolve())).convert_alpha(),
						'name': 'ladder',
						'score': 0,
						'type': TypeBlock.Ladder,
						'sound': None,
						},
					8: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/ladder-2.png').resolve())).convert_alpha(),
						'name': 'ladder',
						'score': 0,
						'type': TypeBlock.Ladder,
						'sound': None,
						},
					9: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/left-pistol.png').resolve())).convert_alpha(),
						'name': 'pistol',
						'score': 0,
						'type': TypeBlock.Pistol,
						'sound': None,
						},
					10: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/right-pistol.png').resolve())).convert_alpha(),
						'name': 'pistol',
						'score': 0,
						'type': TypeBlock.Pistol,
						'sound': None,
						},
					11: {
						'surf': pygame.image.load(str(pathlib.Path('./images/live-bg.png').resolve())).convert_alpha(),
						'name': 'live-bg',
						'score': 0,
						'type': TypeBlock.Unknown,
						'sound': None,
						},
					12: { 
						'surf': pygame.image.load(str(pathlib.Path('./images/died-bg.png').resolve())).convert_alpha(),
						'name': 'died-bg',
						'score': 0,
						'type': TypeBlock.Unknown,
						'sound': None,
						},
					13: {
						'surf': pygame.image.load(str(pathlib.Path('./images/door.png').resolve())).convert_alpha(),
						'name': 'door',
						'score': 0,
						'type': TypeBlock.Unknown,
						'sound': None,
						},
					14: {
						'surf': pygame.image.load(str(pathlib.Path('./images/blade-rear.png').resolve())).convert_alpha(),
						'name': 'blade-rear',
						'score': 0,
						'type': TypeBlock.Unknown,
						'sound': None,
						},
					15: {
						'surf': pygame.image.load(str(pathlib.Path('./images/blade-up.png').resolve())).convert_alpha(),
						'name': 'blade-up',
						'score': 0,
						'type': TypeBlock.Unknown,
						'sound': None,
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
							'score': 0,
							'type': TypeBlock.Hero,
							'sound': None,
							},
						1: { 
							'surf': pygame.image.load(str(pathlib.Path('./images/hero-side-left.png').resolve())).convert_alpha(),
							'name': 'hero',
							'score': 0,
							'type': TypeBlock.Hero,
							'sound': None,
							},
					},
			'explotion': {
							0: {
								'surf': pygame.image.load(str(pathlib.Path('./images/exp-1.png').resolve())).convert_alpha(),
								'name': 'hero',
								'score': 0,
								'type': TypeBlock.Explotion,
								'sound': None,
								},
							1: {
								'surf': pygame.image.load(str(pathlib.Path('./images/exp-2.png').resolve())).convert_alpha(),
								'name': 'hero',
								'score': 0,
								'type': TypeBlock.Explotion,
								'sound': None,
								},
							2: {
								'surf': pygame.image.load(str(pathlib.Path('./images/exp-3.png').resolve())).convert_alpha(),
								'name': 'hero',
								'score': 0,
								'type': TypeBlock.Explotion,
								'sound': None,
								},
							3: {
								'surf': pygame.image.load(str(pathlib.Path('./images/exp-4.png').resolve())).convert_alpha(),
								'name': 'hero',
								'score': 0,
								'type': TypeBlock.Explotion,
								'sound': None,
								},
							4: {
								'surf': pygame.image.load(str(pathlib.Path('./images/exp-5.png').resolve())).convert_alpha(),
								'name': 'hero',
								'score': 0,
								'type': TypeBlock.Explotion,
								'sound': None,
								},
							5: {
								'surf': pygame.image.load(str(pathlib.Path('./images/exp-6.png').resolve())).convert_alpha(),
								'name': 'hero',
								'score': 0,
								'type': TypeBlock.Explotion,
								'sound': None,
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

objects = pygame.sprite.Group()

def SwitchShot(CasePos):
	return {
			LevelCode.LeftPistol: images['weapon'][2]['surf'],
			LevelCode.RightPistol: pygame.transform.flip(images['weapon'][2]['surf'], True, False),
	}.get(CasePos, images['weapon'][2]['surf'])

def SwitchDoor(level_code):
	return {
			LevelCode.Door: images['else'][13]['surf'],
	}.get(level_code, images['else'][13]['surf'])

def SwitchPistol(CasePos):
	return {
			LevelCode.LeftPistol: images['else'][9]['surf'],
			LevelCode.RightPistol: images['else'][10]['surf'],
	}.get(CasePos, images['else'][9]['surf'])

def SwitchHatchBombs(CaseLevel):
	return {
			1: images['else'][1]['surf'],
			2: images['else'][1]['surf'],
			3: images['else'][1]['surf'],
			4: images['else'][1]['surf'],
			5: images['else'][1]['surf'],
			6: images['else'][1]['surf'],
			7: images['else'][1]['surf'],
			8: images['else'][1]['surf'],
			9: images['else'][1]['surf'],
			10: images['else'][1]['surf'],
			11: images['else'][1]['surf'],
			12: images['else'][1]['surf'],
			13: images['else'][1]['surf'],
			14: images['else'][1]['surf'],
			15: images['else'][1]['surf'],
			16: images['else'][1]['surf'],
			17: images['else'][1]['surf'],
			18: images['else'][1]['surf'],
			19: images['else'][1]['surf'],
			20: images['else'][1]['surf'],
			21: images['else'][1]['surf'],
			22: images['else'][1]['surf'],
			23: images['else'][1]['surf'],
			24: images['else'][1]['surf'],
			25: images['else'][1]['surf'],
			26: images['else'][1]['surf'],
			27: images['else'][1]['surf'],
			28: images['else'][1]['surf'],
			29: images['else'][1]['surf'],
			30: images['else'][2]['surf'],
	}.get(CaseLevel, images['else'][1]['surf'])

def SwitchLadder(CaseLevel):
	return {
			1: images['else'][7]['surf'],
			2: images['else'][7]['surf'],
			3: images['else'][7]['surf'],
			4: images['else'][7]['surf'],
			5: images['else'][7]['surf'],
			6: images['else'][7]['surf'],
			7: images['else'][7]['surf'],
			8: images['else'][7]['surf'],
			9: images['else'][7]['surf'],
			10: images['else'][7]['surf'],
			11: images['else'][7]['surf'],
			12: images['else'][7]['surf'],
			13: images['else'][7]['surf'],
			14: images['else'][7]['surf'],
			15: images['else'][7]['surf'],
			16: images['else'][7]['surf'],
			17: images['else'][7]['surf'],
			18: images['else'][7]['surf'],
			19: images['else'][7]['surf'],
			20: images['else'][7]['surf'],
			21: images['else'][7]['surf'],
			22: images['else'][7]['surf'],
			23: images['else'][7]['surf'],
			24: images['else'][7]['surf'],
			25: images['else'][7]['surf'],
			26: images['else'][7]['surf'],
			27: images['else'][7]['surf'],
			28: images['else'][7]['surf'],
			29: images['else'][7]['surf'],
			30: images['else'][8]['surf'],
	}.get(CaseLevel, images['else'][7]['surf'])

def SwitchTile(CaseLevel):
	return {
		1: images['wall'][0]['surf'],
		2: images['wall'][0]['surf'],
		3: images['wall'][0]['surf'],
		4: images['wall'][0]['surf'],
		5: images['wall'][0]['surf'],
		6: images['wall'][1]['surf'],
		7: images['wall'][1]['surf'],
		8: images['wall'][1]['surf'],
		9: images['wall'][1]['surf'],
		10: images['wall'][1]['surf'],
		11: images['wall'][1]['surf'],
		12: images['wall'][2]['surf'],
		13: images['wall'][2]['surf'],
		14: images['wall'][2]['surf'],
		15: images['wall'][2]['surf'],
		16: images['wall'][2]['surf'],
		17: images['wall'][2]['surf'],
		18: images['wall'][3]['surf'],
		19: images['wall'][3]['surf'],
		20: images['wall'][3]['surf'],
		21: images['wall'][3]['surf'],
		22: images['wall'][3]['surf'],
		23: images['wall'][3]['surf'],
		24: images['wall'][4]['surf'],
		25: images['wall'][4]['surf'],
		26: images['wall'][4]['surf'],
		27: images['wall'][4]['surf'],
		28: images['wall'][4]['surf'],
		29: images['wall'][4]['surf'],
		30: images['wall'][5]['surf'],
	}.get(CaseLevel, images['wall'][1]['surf'])

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

class Block(pygame.sprite.Sprite):
	
	def __init__(self, OnType: TypeBlock, surf, CoordXY: Tuple[int, int], group, score: int = 0, speed: int = 0, sound = None, name = None):
		pygame.sprite.Sprite.__init__(self)
		self.Type = OnType
		self.image = surf
		self.rect = self.image.get_rect(topleft=(CoordXY[0], CoordXY[1]))
		self.speed = speed
		self.score = score
		self.name = name
		self.sound = sound
		self.add(group)
	
	def update(self, *args):
		# self.rect.x = args[0]
		# self.rect.y = args[1]
		# self.kill()
		pass

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
	
	Old_Score = 0
	Old_Level = 1
	Old_Live = 4
	DrawTotal(surface, 0, 1, 4, True, True)

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
	global sc
	global clock
	global FPS
	
	global isStart
	global surf_table
	
	global isUp
	global isLeft
	global isRight
	global isDown
	global isJump
	
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
	
	# Restart(sc)
	# DrawTotal(sc, 0, 1, 4)
	
	
	surf_start_bg = pygame.transform.scale(images['bg'][6]['surf'], (W, H))
	sc.blit(surf_start_bg, (0, 0))
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
					SwitchInitImage((event.pos[0],event.pos[1]), sc)
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
		# mouse_pressed = pygame.mouse.get_pressed()
		# if mouse_pressed[0]:
		#	mouse_pos = pygame.mouse.get_pos()
		#	MouseClicked((mouse_pos[0],mouse_pos[1]), sc)
		
		# objects.draw(sc)
		# pygame.display.update()
		# objects.update()
		
		clock.tick(FPS)

if __name__ == '__main__':
	main()
