import pygame
import pathlib
from typing import Tuple
from enum import Enum
import random
from variables import *

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

def CollideRectAB(obj_a_rect, obj_b_rect):
	if obj_a_rect.right > obj_b_rect.left and obj_a_rect.left < obj_b_rect.right and obj_a_rect.bottom > obj_b_rect.top and obj_a_rect.top < obj_b_rect.bottom:
		return True

def LoadSurf(paths):
	return pygame.image.load(paths).convert_alpha()

def PosCollisions(level: int):
	return {
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
	}.get(level, dict())

def SelectBonus(num):
	return {
			0: {
				'name': 'alarm',
				'path': pathlib.Path('./images/alarm.png').resolve(),
				'score': 100,
				'type': TypeBlock.Bonus,
				},
			1: {
				'name': 'burger',
				'path': pathlib.Path('./images/burger.png').resolve(),
				'score': 50,
				'type': TypeBlock.Bonus,
				},
			2: {
				'name': 'clock',
				'path': pathlib.Path('./images/clock.png').resolve(),
				'score': 30,
				'type': TypeBlock.Bonus,
				},
			3: {
				'name': 'coffee',
				'path': pathlib.Path('./images/coffee.png').resolve(),
				'score': 20,
				'type': TypeBlock.Bonus,
				},
			4: {
				'name': 'cola',
				'path': pathlib.Path('./images/cola.png').resolve(),
				'score': 10,
				'type': TypeBlock.Bonus,
				},
			5: {
				'name': 'stop',
				'path': pathlib.Path('./images/stop.png').resolve(),
				'score': 1,
				'type': TypeBlock.Bonus,
				},
			6: {
				'name': 'thermos',
				'path': pathlib.Path('./images/thermos.png').resolve(),
				'score': 1,
				'type': TypeBlock.Bonus,
				},
	}.get(num, dict())

def SwitchHeart():
	return {
				'name': 'heart',
				'path': pathlib.Path('./images/heart.png').resolve(),
				'score': 1,
				'type': TypeBlock.Bonus,
			}

def SwitchMedicine():
	return {
				'name': 'medicine_chest',
				'path': pathlib.Path('./images/medicine-chest.png').resolve(),
				'score': 1,
				'type': TypeBlock.Bonus,
			}
