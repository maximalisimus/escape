#import pygame
#import pathlib
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

class Block:
	
	def __init__(self, ontype: TypeBlock, RectXY: Tuple[int, int]):
		self.ontype = ontype
		self.rect = pygame.Rect((RectXY[0], RectXY[1], size_blocks, size_blocks))

def CollideRectAB(obj_a_rect, obj_b_rect):
	if obj_a_rect.right > obj_b_rect.left and obj_a_rect.left < obj_b_rect.right and obj_a_rect.bottom > obj_b_rect.top and obj_a_rect.top < obj_b_rect.bottom:
		return True

def LoadSurf(paths):
	return pygame.image.load(paths).convert_alpha()

def PosCollision(level: int):
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
	return {
			0: LoadSurf(door_path),
	}.get(0, LoadSurf(door_path))

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

def SwitchInitImage(surface):
	global isGame
	global isStart
	isGame = True
	isStart = False
	surface.blit(LoadSurf(background), (0, 0))
	surface.blit(LoadSurf(score_bg), (coord_score_bg[0], coord_score_bg[1]))
	Restart(surface)

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

def BuildLevel(surface, group: list, level: int):
	global screen1
	global door_path
	global surf_table
	global rect_table
	global door_path
	
	group.clear()
	
	clouds = SwitchClouds(level)
	wall = SwitchWall(level)
	hatchbombs = SwitchHatchBombs(level)
	leftpistol = SwitchPistol(0)
	rightpistol = SwitchPistol(1)
	ladder = SwitchLadder(level)
	door = LoadSurf(door_path)
	
	surface.blit(clouds, (0, 0))
	x = y = 0
	DoorInOut = True
	with open(files_levels[level-1], 'r') as f:
		data_level = f.readlines()
	for row in data_level:
		for col in row.replace('\n', '').replace(' ','7'):
			code = LevelCode.GetCodeValue(int(col))
			if code != LevelCode.Empty:
				if code == LevelCode.Wall:
					surface.blit(wall, (x, y))
					group.append(Block(TypeBlock.Wall, (x, y)))
				elif code == LevelCode.Door:
					if DoorInOut:
						DoorInOut = False
						surface.blit(door, (x, y))
						group.append(Block(TypeBlock.DoorOut, (x, y)))
					else:
						surface.blit(door, (x, y))
						group.append(Block(TypeBlock.DoorIn, (x, y)))
				elif code == LevelCode.HatchBombs:
					surface.blit(hatchbombs, (x, y))
					group.append(Block(TypeBlock.HatchBombs, (x, y)))
				elif code == LevelCode.Ladder:
					surface.blit(ladder, (x, y))
					group.append(Block(TypeBlock.Ladder, (x, y)))
				elif code == LevelCode.LeftPistol:
					surface.blit(leftpistol, (x, y))
					group.append(Block(TypeBlock.LeftPistol, (x, y)))
				elif code == LevelCode.RightPistol:
					surface.blit(rightpistol, (x, y))
					group.append(Block(TypeBlock.RightPistol, (x, y)))
			x+=size_blocks
		y+=size_blocks
		x=0
	if level == 30:
		# helicopter
		pass
	pygame.display.update()

def Restart(surf):
	global Old_Score
	global Old_Level
	global Old_Live
	global surf_table
	Old_Score = 0
	Old_Level = 1
	Old_Live = 4
	DrawTotal(surf, 0, 1, 4, True)
	pygame.display.update()
