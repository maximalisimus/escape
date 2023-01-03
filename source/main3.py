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
	Bonus = 8
	
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
	DoorIn = 8
	DoorOut = 9
	Explotion = 10
	Clouds = 11
	Helicopter = 12
	Hero = 13
	Unknown = 14
	
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

W, H = 596, 385
FPS = 60

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
screen1 = pygame.display.set_mode((W, H))
pygame.display.set_caption("Esc")
pygame.display.set_icon(pygame.image.load(str(pathlib.Path('./config/').joinpath('logo.png').resolve())))

clock = pygame.time.Clock()

Old_Score = 0
Old_Level = 1
Old_Live = 4

isStart = True
isGame = False

size_surf_score = (92,22)
size_surf_level = (26, 22)
size_surf_lives = (128,32)
size_helicopter = (72, 48)

size_blocks = 24

# 16 row x 18 column (24 pixel x 24 pixel)
row_table = 16
col_table = 18
size_table = (432, 384)

coord_score = (26,40)
coord_level = (60, 110)
coord_live = (10, 160)

coord_score_bg = (450, 0)
coord_helicopter = (216, 48)
coord_blade_side = (5, 15)
coord_blade_up = (22, 12)

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

pre_levels = map(lambda x: pathlib.Path('./levels/').joinpath(f"ESC_{x}.DAT").resolve(), range(1,31))
files_levels = tuple(map(lambda x: str(x), filter(lambda y: y.exists(), pre_levels)))
del pre_levels

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

medicine_image = pathlib.Path('./images/medicine-chest.png').resolve()
mdeicine_score = 1
medicine_name = 'medicine_chest'

all_bonuses = {
				0: {
					'name': 'alarm',
					'image': pathlib.Path('./images/alarm.png').resolve(),
					'score': 100,
					},
				1: {
					'name': 'burger',
					'image': pathlib.Path('./images/burger.png').resolve(),
					'score': 50,
					},
				2: {
					'name': 'clock',
					'image': pathlib.Path('./images/clock.png').resolve(),
					'score': 30,
					},
				3: {
					'name': 'coffee',
					'image': pathlib.Path('./images/coffee.png').resolve(),
					'score': 20,
					},
				4: {
					'name': 'cola',
					'image': pathlib.Path('./images/cola.png').resolve(),
					'score': 10,
					},
				5: {
					'name': 'stop',
					'image': pathlib.Path('./images/stop.png').resolve(),
					'score': 1,
					},
				6: {
					'name': 'thermos',
					'image': pathlib.Path('./images/thermos.png').resolve(),
					'score': 1,
					},
			}

logo = pathlib.Path('./images/esc_t.png').resolve()

background = pathlib.Path('./images/esc-bg.png').resolve()
score_bg = pygame.image.load(pathlib.Path('./images/score-bg.png').resolve()).convert_alpha()
live_bg = pygame.image.load(pathlib.Path('./images/live-bg.png').resolve()).convert_alpha()
died_bg = pygame.image.load(pathlib.Path('./images/died-bg.png').resolve()).convert_alpha()

door_path = pathlib.Path('./images/door.png').resolve()

bomb_path = pathlib.Path('./images/bomb.png').resolve()
bomb_name = 'bomb'

shot_path = pathlib.Path('./images/bullet.png').resolve()
shot_name = 'shot'

heart_path = pathlib.Path('./images/heart.png').resolve()
heart_score = 5
heart_name = 'heart'

blade_rear_path = pathlib.Path('./images/blade-rear.png').resolve()
blade_up_path = pathlib.Path('./images/blade-up.png').resolve()

surf_table = pygame.Surface((size_table[0], size_table[1]), pygame.SRCALPHA, 32).convert_alpha()
rect_table = surf_table.get_rect(topleft=(0, 0))

src_surf_bonus = pygame.Surface((size_table[0], size_table[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_bonus = pygame.Surface.copy(src_surf_bonus)
rect_bonus = surf_bonus.get_rect(topleft=(0, 0))

surf_score = pygame.Surface((size_surf_score[0], size_surf_score[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_level = pygame.Surface((size_surf_level[0], size_surf_level[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_lives = pygame.Surface((size_surf_lives[0], size_surf_lives[1]), pygame.SRCALPHA, 32).convert_alpha()

pygame.mixer.music.load(str(pathlib.Path('./sounds/music.mp3').resolve()))

effects = {
			'applause': pygame.mixer.Sound(str(pathlib.Path('./sounds/applause.WAV').resolve())),
			'jump': pygame.mixer.Sound(str(pathlib.Path('./sounds/jump.WAV').resolve())),
			'final': pygame.mixer.Sound(str(pathlib.Path('./sounds/final.WAV').resolve())),
			'start': pygame.mixer.Sound(str(pathlib.Path('./sounds/start.WAV').resolve())),
			'helicopter': pygame.mixer.Sound(str(pathlib.Path('./sounds/helicopter.WAV').resolve())),
			'alarm': pygame.mixer.Sound(str(pathlib.Path('./sounds/alarm.WAV').resolve())),
			'burger': pygame.mixer.Sound(str(pathlib.Path('./sounds/burger.WAV').resolve())),
			'clock': pygame.mixer.Sound(str(pathlib.Path('./sounds/clock.WAV').resolve())),
			'coffee': pygame.mixer.Sound(str(pathlib.Path('./sounds/coffee.WAV').resolve())),
			'cola': pygame.mixer.Sound(str(pathlib.Path('./sounds/cola.WAV').resolve())),
			'stop': pygame.mixer.Sound(str(pathlib.Path('./sounds/stop.WAV').resolve())),
			'thermos': pygame.mixer.Sound(str(pathlib.Path('./sounds/thermos.WAV').resolve())),
			'heart': pygame.mixer.Sound(str(pathlib.Path('./sounds/heart.WAV').resolve())),
			'medicine_chest': pygame.mixer.Sound(str(pathlib.Path('./sounds/live.WAV').resolve())),
			'bomb': pygame.mixer.Sound(str(pathlib.Path('./sounds/bomb.WAV').resolve())),
			'shot': pygame.mixer.Sound(str(pathlib.Path('./sounds/shot.WAV').resolve())),
		}

def LoadSurf(paths):
	return pygame.image.load(str(paths)).convert_alpha()

def SelectWall(num):
	return {
			0: pathlib.Path('./images/tile-1.png').resolve(),
			1: pathlib.Path('./images/tile-2.png').resolve(),
			2: pathlib.Path('./images/tile-3.png').resolve(),
			3: pathlib.Path('./images/tile-4.png').resolve(),
			4: pathlib.Path('./images/tile-5.png').resolve(),
			5: pathlib.Path('./images/tile-6.png').resolve(),
	}.get(num, pathlib.Path('./images/tile-1.png').resolve())

def SelectClouds(num):
	return {
			0: pathlib.Path('./images/esc_1.png').resolve(),
			1: pathlib.Path('./images/esc_2.png').resolve(),
			2: pathlib.Path('./images/esc_3.png').resolve(),
			3: pathlib.Path('./images/esc_4.png').resolve(),
			4: pathlib.Path('./images/esc_5.png').resolve(),
			5: pathlib.Path('./images/esc_6.png').resolve(),
	}.get(num, pathlib.Path('./images/esc_1.png').resolve())

def SelectHatchBombs(num):
	return {
			0: pathlib.Path('./images/hatch-bombs.png').resolve(),
			1: pathlib.Path('./images/hatch-bombs-2.png').resolve(),
	}.get(num, pathlib.Path('./images/hatch-bombs.png').resolve())

def SelectHelicopter(num):
	return {
			0: pathlib.Path('./images/Helicopter_1.png').resolve(),
			1: pathlib.Path('./images/Helicopter_2.png').resolve(),
			2: pathlib.Path('./images/Helicopter_3.png').resolve(),
			3: pathlib.Path('./images/Helicopter_4.png').resolve(),
	}.get(num, pathlib.Path('./images/Helicopter_1.png').resolve())

def SelectLadder(num):
	return {
			0: pathlib.Path('./images/ladder.png').resolve(),
			1: pathlib.Path('./images/ladder-2.png').resolve(),
	}.get(num, pathlib.Path('./images/ladder.png').resolve())

def SelectPistol(pistol: LevelCode):
	return {
			LevelCode.LeftPistol: pathlib.Path('./images/left-pistol.png').resolve(),
			LevelCode.RightPistol: pathlib.Path('./images/right-pistol.png').resolve(),
	}.get(pistol, False)

def SelectHero(num):
	return {
			0: pathlib.Path('./images/hero.png').resolve(),
			1: pathlib.Path('./images/hero-side-left.png').resolve(),
			2: pathlib.Path('./images/hero-side-right.png').resolve(),
	}.get(num, pathlib.Path('./images/hero.png').resolve())

def SelectExplotion(num):
	return {
			0: pathlib.Path('./images/exp-1.png').resolve(),
			1: pathlib.Path('./images/exp-2.png').resolve(),
			2: pathlib.Path('./images/exp-3.png').resolve(),
			3: pathlib.Path('./images/exp-4.png').resolve(),
			4: pathlib.Path('./images/exp-5.png').resolve(),
			5: pathlib.Path('./images/exp-6.png').resolve(),
	}.get(num, pathlib.Path('./images/exp-1.png').resolve())

def SwitchPistol(CasePos):
	return {
			0: LoadSurf(SelectPistol(LevelCode.LeftPistol)),
			1: LoadSurf(SelectPistol(LevelCode.RightPistol)),
	}.get(CasePos, LoadSurf(SelectPistol(LevelCode.LeftPistol)))

def SwitchShot(CaseShot: LevelCode):
	return {
			LevelCode.LeftPistol: LoadSurf(shot_path),
			LevelCode.RightPistol: pygame.transform.flip(LoadSurf(shot_path), True, False),
	}.get(CaseShot, LoadSurf(shot_path))

def SwitchDoor():
	return LoadSurf(door_path)

def SwitchHatchBombs(CaseLevel):
	return {
			1: LoadSurf(SelectHatchBombs(0)),
			2: LoadSurf(SelectHatchBombs(0)),
			3: LoadSurf(SelectHatchBombs(0)),
			4: LoadSurf(SelectHatchBombs(0)),
			5: LoadSurf(SelectHatchBombs(0)),
			6: LoadSurf(SelectHatchBombs(0)),
			7: LoadSurf(SelectHatchBombs(0)),
			8: LoadSurf(SelectHatchBombs(0)),
			9: LoadSurf(SelectHatchBombs(0)),
			10: LoadSurf(SelectHatchBombs(0)),
			11: LoadSurf(SelectHatchBombs(0)),
			12: LoadSurf(SelectHatchBombs(0)),
			13: LoadSurf(SelectHatchBombs(0)),
			14: LoadSurf(SelectHatchBombs(0)),
			15: LoadSurf(SelectHatchBombs(0)),
			16: LoadSurf(SelectHatchBombs(0)),
			17: LoadSurf(SelectHatchBombs(0)),
			18: LoadSurf(SelectHatchBombs(0)),
			19: LoadSurf(SelectHatchBombs(0)),
			20: LoadSurf(SelectHatchBombs(0)),
			21: LoadSurf(SelectHatchBombs(0)),
			22: LoadSurf(SelectHatchBombs(0)),
			23: LoadSurf(SelectHatchBombs(0)),
			24: LoadSurf(SelectHatchBombs(0)),
			25: LoadSurf(SelectHatchBombs(0)),
			26: LoadSurf(SelectHatchBombs(0)),
			27: LoadSurf(SelectHatchBombs(0)),
			28: LoadSurf(SelectHatchBombs(0)),
			29: LoadSurf(SelectHatchBombs(0)),
			30: LoadSurf(SelectHatchBombs(1)),
	}.get(CaseLevel, LoadSurf(SelectHatchBombs(0)))

def SwitchLadder(CaseLevel):
	return {
			1: LoadSurf(SelectLadder(0)),
			2: LoadSurf(SelectLadder(0)),
			3: LoadSurf(SelectLadder(0)),
			4: LoadSurf(SelectLadder(0)),
			5: LoadSurf(SelectLadder(0)),
			6: LoadSurf(SelectLadder(0)),
			7: LoadSurf(SelectLadder(0)),
			8: LoadSurf(SelectLadder(0)),
			9: LoadSurf(SelectLadder(0)),
			10: LoadSurf(SelectLadder(0)),
			11: LoadSurf(SelectLadder(0)),
			12: LoadSurf(SelectLadder(0)),
			13: LoadSurf(SelectLadder(0)),
			14: LoadSurf(SelectLadder(0)),
			15: LoadSurf(SelectLadder(0)),
			16: LoadSurf(SelectLadder(0)),
			17: LoadSurf(SelectLadder(0)),
			18: LoadSurf(SelectLadder(0)),
			19: LoadSurf(SelectLadder(0)),
			20: LoadSurf(SelectLadder(0)),
			21: LoadSurf(SelectLadder(0)),
			22: LoadSurf(SelectLadder(0)),
			23: LoadSurf(SelectLadder(0)),
			24: LoadSurf(SelectLadder(0)),
			25: LoadSurf(SelectLadder(0)),
			26: LoadSurf(SelectLadder(0)),
			27: LoadSurf(SelectLadder(0)),
			28: LoadSurf(SelectLadder(0)),
			29: LoadSurf(SelectLadder(0)),
			30: LoadSurf(SelectLadder(1)),
	}.get(CaseLevel, LoadSurf(SelectLadder(0)))

def SwitchWall(CaseLevel):
	return {
			1: LoadSurf(SelectWall(0)),
			2: LoadSurf(SelectWall(0)),
			3: LoadSurf(SelectWall(0)),
			4: LoadSurf(SelectWall(0)),
			5: LoadSurf(SelectWall(0)),
			6: LoadSurf(SelectWall(1)),
			7: LoadSurf(SelectWall(1)),
			8: LoadSurf(SelectWall(1)),
			9: LoadSurf(SelectWall(1)),
			10: LoadSurf(SelectWall(1)),
			11: LoadSurf(SelectWall(1)),
			12: LoadSurf(SelectWall(2)),
			13: LoadSurf(SelectWall(2)),
			14: LoadSurf(SelectWall(2)),
			15: LoadSurf(SelectWall(2)),
			16: LoadSurf(SelectWall(2)),
			17: LoadSurf(SelectWall(2)),
			18: LoadSurf(SelectWall(3)),
			19: LoadSurf(SelectWall(3)),
			20: LoadSurf(SelectWall(3)),
			21: LoadSurf(SelectWall(3)),
			22: LoadSurf(SelectWall(3)),
			23: LoadSurf(SelectWall(3)),
			24: LoadSurf(SelectWall(4)),
			25: LoadSurf(SelectWall(4)),
			26: LoadSurf(SelectWall(4)),
			27: LoadSurf(SelectWall(4)),
			28: LoadSurf(SelectWall(4)),
			29: LoadSurf(SelectWall(4)),
			30: LoadSurf(SelectWall(5)),
	}.get(CaseLevel, LoadSurf(SelectWall(0)))

def SwitchClouds(CaseLevel):
	return {
			1: LoadSurf(SelectClouds(0)),
			2: LoadSurf(SelectClouds(0)),
			3: LoadSurf(SelectClouds(0)),
			4: LoadSurf(SelectClouds(0)),
			5: LoadSurf(SelectClouds(0)),
			6: LoadSurf(SelectClouds(1)),
			7: LoadSurf(SelectClouds(1)),
			8: LoadSurf(SelectClouds(1)),
			9: LoadSurf(SelectClouds(1)),
			10: LoadSurf(SelectClouds(1)),
			11: LoadSurf(SelectClouds(1)),
			12: LoadSurf(SelectClouds(2)),
			13: LoadSurf(SelectClouds(2)),
			14: LoadSurf(SelectClouds(2)),
			15: LoadSurf(SelectClouds(2)),
			16: LoadSurf(SelectClouds(2)),
			17: LoadSurf(SelectClouds(2)),
			18: LoadSurf(SelectClouds(3)),
			19: LoadSurf(SelectClouds(3)),
			20: LoadSurf(SelectClouds(3)),
			21: LoadSurf(SelectClouds(3)),
			22: LoadSurf(SelectClouds(3)),
			23: LoadSurf(SelectClouds(3)),
			24: LoadSurf(SelectClouds(4)),
			25: LoadSurf(SelectClouds(4)),
			26: LoadSurf(SelectClouds(4)),
			27: LoadSurf(SelectClouds(4)),
			28: LoadSurf(SelectClouds(4)),
			29: LoadSurf(SelectClouds(4)),
			30: LoadSurf(SelectClouds(5)),
	}.get(CaseLevel, LoadSurf(SelectClouds(0)))

def SelectLCD(num: str):
	return {
			'0': pathlib.Path('./images/LCD/lcd-0.png').resolve(),
			'1': pathlib.Path('./images/LCD/lcd-1.png').resolve(),
			'2': pathlib.Path('./images/LCD/lcd-2.png').resolve(),
			'3': pathlib.Path('./images/LCD/lcd-3.png').resolve(),
			'4': pathlib.Path('./images/LCD/lcd-4.png').resolve(),
			'5': pathlib.Path('./images/LCD/lcd-5.png').resolve(),
			'6': pathlib.Path('./images/LCD/lcd-6.png').resolve(),
			'7': pathlib.Path('./images/LCD/lcd-7.png').resolve(),
			'8': pathlib.Path('./images/LCD/lcd-8.png').resolve(),
			'9': pathlib.Path('./images/LCD/lcd-9.png').resolve(),
	}.get(num, pathlib.Path('./images/LCD/lcd-0.png').resolve())

def SwitchLCD(CaseNum: str):
	return {
			'0': LoadSurf(SelectLCD('0')),
			'1': LoadSurf(SelectLCD('1')),
			'2': LoadSurf(SelectLCD('2')),
			'3': LoadSurf(SelectLCD('3')),
			'4': LoadSurf(SelectLCD('4')),
			'5': LoadSurf(SelectLCD('5')),
			'6': LoadSurf(SelectLCD('6')),
			'7': LoadSurf(SelectLCD('7')),
			'8': LoadSurf(SelectLCD('8')),
			'9': LoadSurf(SelectLCD('9')),
	}.get(CaseNum, LoadSurf(SelectLCD('0')))

def SwitchHero(CasePos):
	return {
			0: LoadSurf(SelectHero(0)),
			1: LoadSurf(SelectHero(1)),
			2: LoadSurf(SelectHero(2)),
	}.get(CasePos, LoadSurf(SelectHero(0)))

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
	global size_surf_score
	global pos_score_x
	global pos_score_y
	pygame.draw.rect(surf, (0, 0, 0), (0, 0, size_surf_score[0], size_surf_score[1]))
	OnScore = tuple(print_score(on_score))
	for i in range(len(OnScore)):
		surf.blit(SwitchLCD(OnScore[i]), (pos_score_x[i], pos_score_y))

def DrawLevel(surf, on_level: int):
	global size_surf_level
	global pos_score_x
	global pos_score_y
	pygame.draw.rect(surf, (0, 0, 0), (0, 0, size_surf_level[0], size_surf_level[1]))
	OnLevel = tuple(print_level(on_level))
	for i in range(len(OnLevel)):
		surf.blit(SwitchLCD(OnLevel[i]), (pos_score_x[i], pos_score_y))

def DrawLive(screen_surf, surf, coord: Tuple[int, int]):
	screen_surf.blit(surf, (coord[0], coord[1]))

def DrawTotal(surface, score: int, level: int, live: int, isFull: bool = False):
	global Old_Score
	global Old_Level
	global Old_Live
	
	global surf_score
	global surf_level
	global surf_lives
	
	global live_bg
	global died_bg
	
	global pos_live_x
	global pos_live_y
	
	if isFull:
		DrawScore(surf_score, score)
		Old_Score = score
		DrawLevel(surf_level, level)
		Old_Level = level
		for i in range(1, live+1):
			DrawLive(surf_lives, live_bg, (pos_live_x[i], 0))
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
			DrawLive(surf_lives, live_bg, (pos_live_x[live], 0))
		elif live == Old_Live:
			pass
		elif (live < Old_Live):
			if (Old_Live - live) == 1:
				DrawLive(surf_lives, died_bg, (pos_live_x[Old_Live], 0))
			else:
				for i in range(Old_Live, live, -1):
					DrawLive(surf_lives, died_bg, (pos_live_x[i], 0))
		surface.blit(surf_lives, (coord_live[0], coord_live[1]))
		Old_Live = live
	else:
		surface.blit(surf_lives, (coord_live[0], coord_live[1]))

class Helicopter:
	
	def __init__(self):
		self.copters = (LoadSurf(SelectHelicopter(0)), LoadSurf(SelectHelicopter(1)), LoadSurf(SelectHelicopter(2)), LoadSurf(SelectHelicopter(3)))
		self.blade = (LoadSurf(blade_rear_path), LoadSurf(blade_up_path))
		self.image = pygame.Surface.copy(self.copters[0])
		self.rect = self.image.get_rect(topleft=(coord_helicopter[0], coord_helicopter[1]))
		self.ontype = TypeBlock.Helicopter
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
							effects['helicopter'].play()
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

	def draw(self, surf):
		surf.blit(self.image, self.rect)

def SwitchInitImage(surface):
	global isGame
	global isStart
	isGame = True
	isStart = False
	surface.blit(LoadSurf(background), (0, 0))
	surface.blit(score_bg, (coord_score_bg[0], coord_score_bg[1]))
	#Restart(surface)
	pygame.display.update()

def main():
	global screen1
	global clock
	
	global surf_table
	global rect_table
	global surf_bonus
	global rect_bonus
	
	global score_bg
	global coord_score_bg
	
	global isStart
	global isGame
	
	global logo	
	surf_start_bg = pygame.transform.scale(LoadSurf(logo), (W, H))
	screen1.blit(surf_start_bg, (0, 0))
	pygame.display.update()
	del surf_start_bg, logo
	
	RUN = True
	
	### Debug
	
	score = 0
	live = 4
	level = 1
	
	SwitchInitImage(screen1)
	DrawTotal(score_bg, score, level, live, True)
	screen1.blit(score_bg, (coord_score_bg[0], coord_score_bg[1]))
	pygame.display.update()
	
	### Debug
	
	while RUN:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				RUN = False
				exit()
			elif event.type == pygame.KEYDOWN:
				# event.key
				pass
			elif event.type == pygame.KEYUP:
				# if event.key in []:
				pass
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if isStart:
					SwitchInitImage(screen1)
				elif isGame:
					pass
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				pass
		
		#keys = pygame.key.get_pressed()
		#pressed = pygame.mouse.get_pressed()
		#if pressed[0]:
		#	pos = pygame.mouse.get_pos()
		#	print(pos)
		
		#if isGame:
		#	DrawTotal(score_bg, score, level, live, True)
		#	screen1.blit(score_bg, (coord_score_bg[0], coord_score_bg[1]))
		#	pygame.display.update()
		
		clock.tick(FPS)

if __name__ == '__main__':
	main()
