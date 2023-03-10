#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pathlib
from typing import Tuple
from enum import Enum
import random
import json
import time

class TDict(object):
	
	#__slots__ = '__dict__'
	__slots__ = ['__g', '__tmp']
	
	def __init__(self, *args):
		super(TDict, self).__init__()
		self.__g = dict(*args)
	
	def __setitem__(self, key, item):
		if not type(key) in (float, int, str, tuple, frozenset, bool, None):
			raise TypeError('Please, enter the \'key\' in (float, int, str, tuple, bool or frozenset)!')
		self.__g[key] = item

	def __getitem__(self, key):
		return self.__g[key] if self.has_key(key) else None
	
	def __call__(self):
		return self.__g
	
	def get(self, k, v = None):
		return self.__g.get(k, v)
	
	def __repr__(self):
		return self.__g.__str__()

	def __len__(self):
		return len(self.__g)

	def __delitem__(self, key):
		del self.__g[key]

	def clear(self):
		return self.__g.clear()

	def copy(self):
		return self.__g.copy()

	def update(self, *args, **kwargs):
		return self.__g.update(*args, **kwargs)

	def keys(self):
		return self.__g.keys()

	def values(self):
		return self.__g.values()

	def items(self):
		return self.__g.items()

	def pop(self, *args):
		return self.__g.pop(*args)

	def setdefault(self, k, d = None):
		return self.__g.setdefault(k, d)

	def fromkeys(self, iterable, value = None):
		if hasattr(iterable, '__iter__'):
			if not hasattr(value, '__iter__') and type(value) != str:
				for item in iterable:
					self.__g[item] = value
			elif type(value) == str:
				for item in iterable:
					self.__g[item] = value
			else:
				if len(value) >= len(iterable):
					for count in range(len(iterable)):
						self.__g[iterable[count]] = value[count]
				elif len(value) < len(iterable):
					for count in range(len(value)):
						self.__g[iterable[count]] = value[count]			
		return self
	
	def __sortOD(self, od, iskey: bool = True, revers: bool = False):
		def CheckToSTR(on_dict, on_key, on_value, reverse_value):
			if hasattr(on_value,'__iter__') and type(on_value) != str:
				tp = type(on_value)
				on_dict[on_key] = tp(sorted(on_value, reverse = reverse_value))
			else:
				on_dict[on_key] = on_value	
		res = TDict()
		if not TDict in set(map(type, od.values())):
			if iskey:
				if len(set(map(type,od.keys()))) == 1:
					for k, v in sorted(od.items(), key=lambda i: i[0], reverse = revers):
						CheckToSTR(res, k, v, revers)
				else:
					for k, v in sorted(od.items(), key=lambda i: str(i[0]), reverse = revers):
						CheckToSTR(res, k, v, revers)
			else:
				if len(set(map(type,od.values()))) == 1:
					for k, v in sorted(od.items(), key=lambda i: i[1], reverse = revers):
						CheckToSTR(res, k, v, revers)
				else:
					for k, v in sorted(od.items(), key=lambda i: str(i[1]), reverse = revers):
						CheckToSTR(res, k, v, revers)
		else:
			if len(set(map(type,od.keys()))) == 1:
				for k, v in sorted(od.items(), reverse = revers):
					if isinstance(v, TDict):
						res[k] = self.__sortOD(v)
					else:
						CheckToSTR(res, k, v, revers)
			else:
				for k, v in sorted(od.items(), key=lambda i: str(i[0]), reverse = revers):
					if isinstance(v, TDict):
						res[k] = self.__sortOD(v)
					else:
						CheckToSTR(res, k, v, revers)
		return res
	
	def sort(self, iskey: bool = True, revers: bool = False):
		tmp = self.__sortOD(self.__g.copy(), iskey, revers)
		self.__g = tmp.copy()
		return self
	
	def popitem(self):
		return self.__g.popitem()

	def __or__(self, other):
		if not isinstance(other, TDict):
			return NotImplemented
		new = TDict(self)
		new.update(other)
		return new

	def __ror__(self, other):
		if not isinstance(other, TDict):
			return NotImplemented
		new = TDict(other)
		new.update(self)
		return new

	def __ior__(self, other):
		TDict.update(self, other)
		return self
	
	def __reversed__(self):
		if len(set(map(type, self.keys()))) == 1:
			self.__g = dict(sorted(self.__g.items(), key=lambda i: i[0], reverse=True))
		else:
			self.__g = dict(sorted(self.__g.items(), key=lambda i: str(i[0]), reverse=True))
		return self

	def __str__(self):
		return self.__g.__str__()

	def __cmp__(self, dict_):
		return self.__cmp__(self.__g, dict_)

	def __iter__(self):
		return iter(self.__g)

	def __unicode__(self):
		return unicode(repr(self.__g))
	
	def is_emty(self):
		return len(self.__g) == 0
	
	def __contains__(self, item):
		return item in self.__g
	
	def has_key(self, k):
		return k in self.__g

	def has_value(self, v):
		return v in self.__g.values()

	def __enter__(self):
		self.__tmp = self.__g.copy()
		return self.__tmp
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		if exc_type is None:
			self.__g = self.__tmp.copy()
		return False

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
	Center = 1
	Left = 2
	Right = 3
	
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

class TGroup(TDict):
	
	def __init__(self, *args):
		super(TGroup, self).__init__(*args)
	
	def add(self, *args):
		if len(args) > 0:
			if len(args) == 1:
				if not self.has_value(args[0]):
					if hasattr(args[0], 'i') and hasattr(args[0], 'j'):
						if args[0].i != None and args[0].j != None:
							self.add(args[0].i, args[0].j, args[0])
						else:
							self[len(self)+1] = args[0]
					else:
						self[len(self)+1] = args[0]
			elif len(args) == 2:
				self[args[0]] = args[1]
			elif len(args) == 3:
				if not self.has_key(args[0]):
					self[args[0]] = TDict()
				if type(self[args[0]]) == TDict:
					self[args[0]][args[1]] = args[2]
	
	def removekeys(self, *keys):
		if len(keys) > 0 and len(keys) < 3:
			if len(keys) == 1:
				self.pop(keys[0], False)
			elif len(keys) == 2:
				self[keys[0]].pop(keys[1], False)
	
	def remove(self, *args):
		for item in args:
			for k1, v1 in self.copy().items():
				if type(v1) == TDict:
					for k2, v2 in v1.copy().items():
						if v2 == item:
							self[k1].pop(k2, False)
				else:
					self.pop(k1, False)
	
	def has(self, *sprites) -> bool:
		if not sprites:
			return False
		if len(sprites) == 1:
			return self.has_internal(sprites[0])
		else:
			tmp = []
			for sprite in sprites:
				tmp.append(self.has_internal(sprite))
			return tuple(tmp)
	
	def haspos(self, *keys):
		if not keys:
			return False
		if len(keys) == 1:
			return self.searchkey(keys[0])
		else:
			return self.searchkey(*keys)

	def sprites(self, isTuple: bool = False):
		res = []
		for row in self.values():
			if type(row) == TDict:
				for col in row.values():
					res.append(col)
			else:
				res.append(row)
		if isTuple:
			return tuple(res)
		else:
			return res
	
	def updates(self, *args, **kwargs):
		for row in self.values():
			if type(row) == TDict:
				for col in row.values():
					if hasattr(col, 'update'):
						col.update(*args, **kwargs)
			else:
				if hasattr(row, 'update'):
					row.update(*args)
	
	def draw(self, surf, isDisplayUpdate: bool = False):
		for row in self.values():
			if type(row) == TDict:
				for col in row.values():
					if hasattr(col, 'image') and hasattr(col, 'rect'):
						surf.blit(col.image, col.rect)
						if isDisplayUpdate:
							pygame.display.update()
			else:
				if hasattr(row, 'image') and hasattr(row, 'rect'):
					surf.blit(row.image, row.rect)
					if isDisplayUpdate:
						pygame.display.update()

	def CollidePos(self, sprite, SizeWH: Tuple[int, int], dokill: bool = False, collided = None):
		if not hasattr(sprite, 'rect'):
			return None
		ipos = sprite.rect.y // SizeWH[1]
		jpos = sprite.rect.x // SizeWH[0]
		out_blocks = []
		in_blocks = set(self.get(ipos, TDict()).get(jpos, False), \
						self.get(ipos, TDict()).get(jpos+1, False), \
						self.get(ipos+1, TDict()).get(jpos, False), \
						self.get(ipos+1, TDict()).get(jpos+1, False))
		in_blocks.discard(False)
		for group_sprite in in_blocks:
			if collided is not None:
				if collided(sprite, group_sprite):
					out_blocks.append(group_sprite)
					if dokill:
						group.remove(group_sprite)
			else:
				if pygame.sprite.collide_rect(sprite, group_sprite):
					out_blocks.append(group_sprite)
					if dokill:
						group.remove(group_sprite)
		return tuple(out_blocks)
	
	def collidepoint(self, pos, dokill: bool = False):
		out_blocks = []
		for k1, v1 in self.copy().items():
			if type(v1) == TDict:
				for k2, v2 in v1.copy().items():
					if hasattr(v2, 'rect'):
						if v2.rect.collidepoint(pos):
							out_blocks.append(v2)
							if dokill:
								self.removekeys(k1, k2)
			else:
				if hasattr(v1, 'rect'):
					if v1.rect.collidepoint(pos):
						out_blocks.append(v1)
						if dokill:
							self.removekeys(k1)
		return tuple(out_blocks)
	
	def collide(self, sprite, dokill: bool = False, collided = None):
		if not hasattr(sprite, 'rect'):
			return None
		out_blocks = []
		for k1, v1 in self.copy().items():
			if type(v1) == TDict:
				for k2, v2 in v1.copy().items():
					if collided is not None and hasattr(v2, 'rect'):
						if collided(sprite, v2):
							out_blocks.append(v2)
							if dokill:
								self.removekeys(k1, k2)
					elif hasattr(v2, 'rect'):
						if pygame.sprite.collide_rect(sprite, v2):
							out_blocks.append(v2)
							if dokill:
								self.removekeys(k1, k2)
			else:
				if collided is not None and hasattr(v1, 'rect'):
					if collided(sprite, v1):
						out_blocks.append(v1)
						if dokill:
							self.removekeys(k1)
				elif hasattr(v1, 'rect'):
					if pygame.sprite.collide_rect(sprite, v1):
						out_blocks.append(v1)
						if dokill:
							self.removekeys(k1)
		return tuple(out_blocks)

class TMenu:
	
	def __init__(self):
		global w
		self.w = w
		self.menu_w = w
		self.menu_h = 25
		self.image = CreateEmtySurf(self.menu_w, self.menu_h)
		self.rect = self.image.get_rect(topleft = (0, 0))
		menu_font = pygame.font.SysFont('arial', 14)
		
		self.menu1 = menu_font.render('????????', 1, (0, 0, 0))
		self.menu2 = menu_font.render('????????????', 1, (0, 0, 0))
		self.menu111 = menu_font.render('??????????????', 1, (0, 0, 0))
		self.menu112 = menu_font.render('F2', 1, (0, 0, 0))
		self.menu121 = menu_font.render('??????????????', 1, (0, 0, 0))
		self.menu122 = menu_font.render('F3', 1, (0, 0, 0))
		self.menu131 = menu_font.render('???????????? ????????????', 1, (0, 0, 0))
		self.menu132 = menu_font.render('F5', 1, (0, 0, 0))
		self.menu141 = menu_font.render('????????????', 1, (0, 0, 0))
		self.menu142 = menu_font.render('F6', 1, (0, 0, 0))
		self.menu151 = menu_font.render('????????', 1, (0, 0, 0))
		self.menu152 = menu_font.render('F7', 1, (0, 0, 0))
		self.menu161 = menu_font.render('??????????', 1, (0, 0, 0))
		self.menu162 = menu_font.render('F4', 1, (0, 0, 0))
		self.menu211 = menu_font.render('?? ??????????????????', 1, (0, 0, 0))
		self.menu212 = menu_font.render('F8', 1, (0, 0, 0))
		
		self.menu111_rect = self.menu111.get_rect(topleft = (30, 10))
		self.menu112_rect = self.menu112.get_rect(topleft = (150, 10))
		self.menu121_rect = self.menu121.get_rect(topleft = (30, 35))
		self.menu122_rect = self.menu122.get_rect(topleft = (150, 35))
		self.menu131_rect = self.menu131.get_rect(topleft = (30, 60))
		self.menu132_rect = self.menu132.get_rect(topleft = (150, 60))
		self.menu141_rect = self.menu141.get_rect(topleft = (30, 85))
		self.menu142_rect = self.menu142.get_rect(topleft = (150, 85))
		self.menu151_rect = self.menu151.get_rect(topleft = (30, 110))
		self.menu152_rect = self.menu152.get_rect(topleft = (150, 110))
		self.menu161_rect = self.menu161.get_rect(topleft = (30, 145))
		self.menu162_rect = self.menu162.get_rect(topleft = (150, 145))
		self.menu211_rect = self.menu211.get_rect(topleft = (20, 7))
		self.menu212_rect = self.menu212.get_rect(topleft = (130, 7))
		
		self.menu111_sel_rect = pygame.Rect(4, 4, 177, 25)
		self.menu111_col_rect = pygame.Rect(4, 29, 177, 25)
		self.menu121_sel_rect = pygame.Rect(4, 29, 177, 25)
		self.menu121_col_rect = pygame.Rect(4, 54, 177, 25)
		self.menu131_sel_rect = pygame.Rect(4, 54, 177, 25)
		self.menu131_col_rect = pygame.Rect(4, 79, 177, 25)
		self.menu141_sel_rect = pygame.Rect(4, 79, 177, 25)
		self.menu141_col_rect = pygame.Rect(4, 104, 177, 25)
		self.menu151_sel_rect = pygame.Rect(4, 104, 177, 25)
		self.menu151_col_rect = pygame.Rect(4, 129, 177, 25)
		self.menu161_sel_rect = pygame.Rect(4, 139, 177, 25)
		self.menu161_col_rect = pygame.Rect(4, 164, 177, 25)
		
		self.sub_image1 = CreateEmtySurf(185, 169)
		self.sub_image2 = CreateEmtySurf(165, 30)
		
		self.sub_rect1 = self.sub_image1.get_rect(topleft = (0, 25))
		self.sub_rect2 = self.sub_image2.get_rect(topleft = (60, 25))
		
		self.bg_color = (64, 64, 64)
		self.menu_color = (240, 240, 240)
		self.frame_color = (166, 166, 166)
		self.select_color = (48, 150, 250)
		
		self.menu_rect1 = self.menu1.get_rect(topleft = (10, 5))
		self.menu_rect2 = self.menu1.get_rect(topleft = (60, 5))
		self.menu_sel_rect1 = pygame.Rect(0, 0, self.menu1.get_rect()[2] + 20, 25)
		self.menu_sel_rect2 = pygame.Rect(self.menu1.get_rect()[2] + 20, 0, self.menu2.get_rect()[2] + 20, 25)
		
		self.submenu_line_x1y1 = (10, 135)
		self.submenu_line_x2y2 = (175, 135)
		
		self.checkmark_surf = LoadSurf(pathlib.Path('./images/checkmark-round.png').resolve())
		self.checkmark_surf = pygame.transform.scale(self.checkmark_surf, (10, 10))
		
		self.menu121_checkmark_rect = self.checkmark_surf.get_rect(topleft = (10, 38))
		self.menu141_checkmark_rect = self.checkmark_surf.get_rect(topleft = (10, 88))
		self.menu151_checkmark_rect = self.checkmark_surf.get_rect(topleft = (10, 113))
		
		self.isactivate = False
		self.ismenu1 = False
		self.ismenu_active1 = False
		self.ismenu2 = False
		self.ismenu_active2 = False
		self.issubmenu11 = False
		self.issubmenu12 = False
		self.issubmenu13 = False
		self.issubmenu14 = False
		self.issubmenu15 = False
		self.issubmenu16 = False
		self.issubmenu21 = False
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 80
	
	def draw(self, surface):
		global isGame, ismusic, issound
		pygame.draw.rect(self.image, self.menu_color, self.rect)
		if self.isactivate:
			if self.ismenu1:
				pygame.draw.rect(self.image, self.select_color, self.menu_sel_rect1)
			if self.ismenu2:
				pygame.draw.rect(self.image, self.select_color, self.menu_sel_rect2)
		self.image.blit(self.menu1, self.menu_rect1)
		self.image.blit(self.menu2, self.menu_rect2)
		if self.isactivate:
			if self.ismenu_active1:
				pygame.draw.rect(self.sub_image2, self.bg_color, (0, 0, self.sub_rect2.width, self.sub_rect2.height))
				pygame.draw.rect(self.sub_image1, self.frame_color, (0, 0, self.sub_rect1.width, self.sub_rect1.height), width = 2)
				pygame.draw.rect(self.sub_image1, self.menu_color, (2, 2, self.sub_rect1.width - 4, self.sub_rect1.height - 4))
				pygame.draw.line(self.sub_image1, self.frame_color, self.submenu_line_x1y1, self.submenu_line_x2y2)
				
				if self.issubmenu11:
					pygame.draw.rect(self.sub_image1, self.select_color, self.menu111_sel_rect)
				if self.issubmenu12:
					pygame.draw.rect(self.sub_image1, self.select_color, self.menu121_sel_rect)
				if self.issubmenu13:
					pygame.draw.rect(self.sub_image1, self.select_color, self.menu131_sel_rect)
				if self.issubmenu14:
					pygame.draw.rect(self.sub_image1, self.select_color, self.menu141_sel_rect)
				if self.issubmenu15:
					pygame.draw.rect(self.sub_image1, self.select_color, self.menu151_sel_rect)
				if self.issubmenu16:
					pygame.draw.rect(self.sub_image1, self.select_color, self.menu161_sel_rect)
				
				self.sub_image1.blit(self.menu111, self.menu111_rect)
				self.sub_image1.blit(self.menu112, self.menu112_rect)
				self.sub_image1.blit(self.menu121, self.menu121_rect)
				self.sub_image1.blit(self.menu122, self.menu122_rect)
				self.sub_image1.blit(self.menu131, self.menu131_rect)
				self.sub_image1.blit(self.menu132, self.menu132_rect)
				self.sub_image1.blit(self.menu141, self.menu141_rect)
				self.sub_image1.blit(self.menu142, self.menu142_rect)
				self.sub_image1.blit(self.menu151, self.menu151_rect)
				self.sub_image1.blit(self.menu152, self.menu152_rect)
				self.sub_image1.blit(self.menu161, self.menu161_rect)
				self.sub_image1.blit(self.menu162, self.menu162_rect)
				if isGame:
					self.sub_image1.blit(self.checkmark_surf, self.menu121_checkmark_rect)
				if ismusic:
					self.sub_image1.blit(self.checkmark_surf, self.menu141_checkmark_rect)
				if issound:
					self.sub_image1.blit(self.checkmark_surf, self.menu151_checkmark_rect)
			if self.ismenu_active2:
				pygame.draw.rect(self.sub_image1, self.bg_color, (0, 0, self.sub_rect1.width, self.sub_rect1.height))
				pygame.draw.rect(self.sub_image2, self.frame_color, (0, 0, self.sub_rect2.width, self.sub_rect2.height), width = 2)
				pygame.draw.rect(self.sub_image2, self.menu_color, (2, 2, self.sub_rect2.width - 4, self.sub_rect2.height - 4))
				if self.issubmenu21:
					pygame.draw.rect(self.sub_image2, self.select_color, (2, 2, self.sub_rect2.width - 4, self.sub_rect2.height - 4))
				self.sub_image2.blit(self.menu211, self.menu211_rect)
				self.sub_image2.blit(self.menu212, self.menu212_rect)
		pygame.draw.rect(surface, self.bg_color, self.sub_rect1)
		pygame.draw.rect(surface, self.bg_color, self.sub_rect2)
		surface.blit(self.image, self.rect)
		if self.isactivate:
			if self.ismenu_active1:
				surface.blit(self.sub_image1, self.sub_rect1)
			if self.ismenu_active2:
				surface.blit(self.sub_image2, self.sub_rect2)
	
	def update(self, onposition):
		new_tick = pygame.time.get_ticks()
		mouse_pos = onposition
		if new_tick - self.last_update > self.frame_rate:
			self.last_update = new_tick
			if self.isactivate:
				self.ismenu1 = self.menu_sel_rect1.collidepoint(mouse_pos)
				self.ismenu2 = self.menu_sel_rect2.collidepoint(mouse_pos)
				if self.ismenu1:
					self.ismenu_active1 = True
					self.ismenu_active2 = False
				if self.ismenu2:
					self.ismenu_active2 = True
					self.ismenu_active1 = False
				if self.ismenu_active1:
					self.issubmenu11 = self.menu111_col_rect.collidepoint(mouse_pos)
					self.issubmenu12 = self.menu121_col_rect.collidepoint(mouse_pos)
					self.issubmenu13 = self.menu131_col_rect.collidepoint(mouse_pos)
					self.issubmenu14 = self.menu141_col_rect.collidepoint(mouse_pos)
					self.issubmenu15 = self.menu151_col_rect.collidepoint(mouse_pos)
					self.issubmenu16 = self.menu161_col_rect.collidepoint(mouse_pos)
				elif self.ismenu_active2:
					self.issubmenu21 = self.sub_rect2.collidepoint(mouse_pos)
	
	def updateclick(self, onposition):
		mouse_pos = onposition
		if self.menu_sel_rect1.collidepoint(mouse_pos) or self.menu_sel_rect2.collidepoint(mouse_pos):
			self.isactivate = not self.isactivate
			if self.isactivate:
				self.ismenu_active1 = self.menu_sel_rect1.collidepoint(mouse_pos)
				self.ismenu_active2 = self.menu_sel_rect2.collidepoint(mouse_pos)
		if not self.menu_sel_rect1.collidepoint(mouse_pos) and \
			not self.menu_sel_rect2.collidepoint(mouse_pos) and \
			not self.sub_rect1.collidepoint(mouse_pos) and \
			not self.sub_rect2.collidepoint(mouse_pos):
			self.__ResetCheckers()
		if self.ismenu_active1:
			if self.menu111_col_rect.collidepoint(mouse_pos):
				self.MenuRestartClick()
			if self.menu121_col_rect.collidepoint(mouse_pos):
				self.MenuPauseClick()
			if self.menu131_col_rect.collidepoint(mouse_pos):
				self.MenuScoreClick()
			if self.menu141_col_rect.collidepoint(mouse_pos):
				self.MenuMusicClick()
			if self.menu151_col_rect.collidepoint(mouse_pos):
				self.MenuSoundClick()
			if self.menu161_col_rect.collidepoint(mouse_pos):
				self.MenuExitClick()
		if self.ismenu_active2:
			if self.sub_rect2.collidepoint(mouse_pos):
				self.MenuAboutClick()

	def __ResetCheckers(self):
		self.isactivate = False
		self.ismenu1 = False
		self.ismenu_active1 = False
		self.ismenu2 = False
		self.ismenu_active2 = False
		self.issubmenu11 = False
		self.issubmenu12 = False
		self.issubmenu13 = False
		self.issubmenu14 = False
		self.issubmenu15 = False
		self.issubmenu16 = False
		self.issubmenu21 = False

	def MenuRestartClick(self):
		self.__ResetCheckers()
		global isGame, running
		Restart()
		isGame = True
		self.isactivate = False
		self.ismenu1 = False
		self.ismenu2 = False
		SwitchScene(GameScene)
		running = False
	
	def MenuPauseClick(self):
		global isGame
		isGame = not isGame
		self.__ResetCheckers()
	
	def MenuScoreClick(self):
		self.__ResetCheckers()
		global isGame, running
		isGame = False
		SwitchScene(ScoreScene)
		running = False

	def MenuMusicClick(self):
		global ismusic, ismusicstart, ismusicfine
		ismusic = not ismusic
		if not ismusicstart:
			ismusicstart = True
			pygame.mixer.music.play()
		else:
			if ismusic:
				if ismusicfine:
					pygame.mixer.music.rewind()
					pygame.mixer.music.play()
					ismusicfine = False
				else:
					if pygame.mixer.music.get_pos() != 0 and not pygame.mixer.music.get_busy():
						pygame.mixer.music.unpause()
			else:
				if pygame.mixer.music.get_busy():
					pygame.mixer.music.pause()
		self.__ResetCheckers()
	
	def MenuSoundClick(self):
		global issound
		issound = not issound
		self.__ResetCheckers()
	
	def MenuExitClick(self):
		self.__ResetCheckers()
		global running
		running = False
		SwitchScene(None)
	
	def MenuAboutClick(self):
		self.__ResetCheckers()
		global isGame, running
		isGame = False
		SwitchScene(about_scene)
		running = False

W, H = 596, 385
FPS = 60

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
infoObject = pygame.display.Info()
w = infoObject.current_w
h = infoObject.current_h
display1 = pygame.display.set_mode((w , h))
pygame.display.set_caption("Escape")
pygame.display.set_icon(pygame.image.load(str(pathlib.Path('./config/').joinpath('logo.png').resolve())))

screen1 = pygame.Surface((W, H), pygame.SRCALPHA, 32).convert_alpha()
infoObject = pygame.display.Info()
pygame.draw.rect(display1, (64, 64, 64), (0, 0, infoObject.current_w, infoObject.current_h))
spx = (infoObject.current_w - W)//2 # screen position x
spy = (infoObject.current_h - H)//2 # screen position y

current_scene = None

clock = pygame.time.Clock()

size_blocks = 24

def CreateEmtySurf(SizeWidth: int = size_blocks, SizeHeight: int = size_blocks):
	return pygame.Surface((SizeWidth, SizeHeight), pygame.SRCALPHA, 32).convert_alpha()

def LoadSurf(paths):
	return pygame.image.load(str(paths)).convert_alpha()

Old_Score = 0
Old_Level = 1
Old_Live = 4

user_name = ''

isStart = True
isGame = False
isFine = False
ismusic = False
ismusicfine = False
ismusicstart = False
issound = True

STOPPED_PLAYING = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(STOPPED_PLAYING)

size_surf_score = (92,22)
size_surf_level = (26, 22)
size_surf_lives = (128,32)
size_helicopter = (72, 48)

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

medicine_image = LoadSurf(pathlib.Path('./images/medicine-chest.png').resolve())
mdeicine_score = 1
medicine_name = 'medicine_chest'

all_bonuses = {
				0: {
					'name': 'alarm',
					'surf': LoadSurf(pathlib.Path('./images/alarm.png').resolve()),
					'score': 100,
					},
				1: {
					'name': 'burger',
					'surf': LoadSurf(pathlib.Path('./images/burger.png').resolve()),
					'score': 50,
					},
				2: {
					'name': 'clock',
					'surf': LoadSurf(pathlib.Path('./images/clock.png').resolve()),
					'score': 30,
					},
				3: {
					'name': 'coffee',
					'surf': LoadSurf(pathlib.Path('./images/coffee.png').resolve()),
					'score': 20,
					},
				4: {
					'name': 'cola',
					'surf': LoadSurf(pathlib.Path('./images/cola.png').resolve()),
					'score': 10,
					},
				5: {
					'name': 'stop',
					'surf': LoadSurf(pathlib.Path('./images/stop.png').resolve()),
					'score': 1,
					},
				6: {
					'name': 'thermos',
					'surf': LoadSurf(pathlib.Path('./images/thermos.png').resolve()),
					'score': 1,
					},
			}

ok_up_surf = LoadSurf(pathlib.Path('./images/ok-up.png').resolve())
ok_down_surf = LoadSurf(pathlib.Path('./images/ok-down.png').resolve())
btn_rect = ok_up_surf.get_rect(topleft=(0, 0))
ok_font = pygame.font.SysFont('arial', 18)
ok_text = ok_font.render('Ok', 1, (0, 0, 0))
ok_pos = ok_text.get_rect(center=((btn_rect[2]//2) - 2, (btn_rect[3]//2) - 1))
ok_up_surf.blit(ok_text, ok_pos)
ok_down_surf.blit(ok_text, ok_pos)
# score_ok_rect = ok_up_surf.get_rect(topleft=(W - btn_rect[2] - 15, H - btn_rect[3] - 15))
score_ok_rect = ok_up_surf.get_rect(topleft=(15, H - btn_rect[3] - 15))
ok_about_rect = ok_up_surf.get_rect(topleft=(W - btn_rect[2] - 15, H - btn_rect[3] - 15))
del btn_rect, ok_font, ok_text, ok_pos

logo = pathlib.Path('./images/esc_t.png').resolve()

score_bg = LoadSurf(pathlib.Path('./images/score-bg.png').resolve())
live_bg = LoadSurf(pathlib.Path('./images/live-bg.png').resolve())
died_bg = LoadSurf(pathlib.Path('./images/died-bg.png').resolve())

door_path = pathlib.Path('./images/door.png').resolve()

bomb_surf = LoadSurf(pathlib.Path('./images/bomb.png').resolve())
bomb_name = 'bomb'

shot_surf_left = LoadSurf(pathlib.Path('./images/bullet.png').resolve())
shot_surf_right = pygame.transform.flip(shot_surf_left, True, False)
shot_name = 'shot'

heart_surf = LoadSurf(pathlib.Path('./images/heart.png').resolve())
heart_score = 5
heart_name = 'heart'

blade_rear_path = pathlib.Path('./images/blade-rear.png').resolve()
blade_up_path = pathlib.Path('./images/blade-up.png').resolve()

surf_table = CreateEmtySurf(size_table[0], size_table[1])
rect_table = surf_table.get_rect(topleft=(0, 0))

surf_score = CreateEmtySurf(size_surf_score[0], size_surf_score[1])
surf_level = CreateEmtySurf(size_surf_level[0], size_surf_level[1])
surf_lives = CreateEmtySurf(size_surf_lives[0], size_surf_lives[1])

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

score_file = pathlib.Path('./config/score.json').resolve()

running = True

menu = TMenu()

def ReadScoreFile():
	global score_file
	score_dict = TDict()
	if score_file.exists():
		with open(score_file,'r') as f:
			score_dict = TDict(tuple((int(k), v) for k,v in tuple(json.load(f).items())))
	else:
		score_tuple = ((1958, ''), (1054, ''), (633, ''), (577, ''), (519, ''), \
					(475, ''), (424, ''), (406, ''), (337, ''), (382, ''))
		score_dict = TDict(score_tuple)
		score_dict.sort(True, True)
	return score_dict

dict_score = ReadScoreFile()

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

def SelectBombHeart(num):
	return {
			0: {
					'type': TypeBlock.Weapon,
					'name': bomb_name,
					'surf': bomb_surf,
					'score': None,
				},
			1: {
					'type': TypeBlock.Bonus,
					'name': heart_name,
					'surf': heart_surf,
					'score': heart_score,
				},
	}.get(num, {'type': TypeBlock.Weapon, 'name': bomb_name, 'surf': bomb_surf,})

def SwitchBombHeart(CaseNum):
	return {
			0: SelectBombHeart(0),
			1: SelectBombHeart(1),
	}.get(CaseNum, SelectBombHeart(0))

def SwitchPistol(CasePos: LevelCode):
	return LoadSurf(SelectPistol(CasePos))

def SwitchShot(CaseShot: TypeBlock):
	return {
			TypeBlock.LeftPistol: shot_surf_left,
			TypeBlock.RightPistol: shot_surf_right,
	}.get(CaseShot, shot_surf_left)

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

def SwitchHero(CasePos: SelectHeroPos):
	return {
			SelectHeroPos.Center: LoadSurf(SelectHero(0)),
			SelectHeroPos.Left: LoadSurf(SelectHero(1)),
			SelectHeroPos.Right: LoadSurf(SelectHero(2)),
	}.get(CasePos, LoadSurf(SelectHero(0)))

def SwitchScene(scene):
	global current_scene
	current_scene = scene

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

def rotate_surf(surf, angle):
	loc = surf.get_rect().center
	rot_sprite = pygame.transform.rotate(surf, angle)
	rot_sprite.get_rect().center = loc
	return rot_sprite

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
							self.blade_rear = rotate_surf(self.blade_rear, 90)
							self.image.blit(self.blade_rear, (coord_blade_side[0], coord_blade_side[1]))
							self.blade_up = rotate_surf(self.blade_up, 180)
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

	def draw(self, surf):
		surf.blit(self.image, self.rect)

class Block(pygame.sprite.Sprite):
	
	def __init__(self, OnType: TypeBlock = TypeBlock.Unknown, \
				surf = None, \
				CoordXY: Tuple[int, ...] = (0, 0), \
				group = None, \
				score = None, sound = None, name = None, \
				SizeWH: Tuple[int, int] = (size_blocks, size_blocks), \
				isEmptySurf: bool = False):
		pygame.sprite.Sprite.__init__(self)
		self.type = OnType
		if surf != None:
			self.image = surf
			self.rect = self.image.get_rect(topleft=(CoordXY[0], CoordXY[1]))
		else:
			self.rect = pygame.Rect((CoordXY[0], CoordXY[1], SizeWH[0], SizeWH[1]))
			if isEmptySurf:
				self.image = CreateEmtySurf(SizeWH[0], SizeWH[1])
			else:
				self.image = surf
		if len(CoordXY) == 4:
			self.i = CoordXY[2]
			self.j = CoordXY[3]
		self.SizeWH = SizeWH
		self.score = score
		self.sound = sound
		self.name = name
		if group != None:
			self.add(group)
	
	def update(self, *args):
		pass

class BombHeart(Block):
	
	def __init__(self, \
				caseNum: int = 1, \
				CoordXY: Tuple[int, ...] = (0, 0), \
				group = None, \
				sound = None, \
				SizeWH: Tuple[int, int] = (size_blocks, size_blocks), \
				isEmptySurf: bool = False):
		bh = SwitchBombHeart(caseNum)
		super(Bomb, self).__init__(bh['type'], bh['surf'], CoordXY, group, bh['score'], sound, bh['name'], SizeWH, isEmptySurf)
		self.last_update = pygame.time.get_ticks()
		self.frame = 0
		self.frame_rate = 60
	
	def update(self, *args):
		pass

def BuildLevel(surf):
	pass

def Restart():
	global isGame
	global score_bg
	
	isGame = True
	DrawTotal(score_bg, 0, 1, 4, True)
	pygame.display.update()

if isStart:
	isStart = False
	Restart()

def StartScene():
	global display1, spx, spy, screen1, clock, logo, ismusic, issound, running, menu
	surf_start_bg = pygame.transform.scale(LoadSurf(logo), (W, H))
	screen1.blit(surf_start_bg, (0, 0))
	screen_rect = screen1.get_rect(topleft = (spx, spy))
	display1.blit(screen1, screen_rect)
	pygame.display.update()
	del surf_start_bg, logo
	
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				SwitchScene(None)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F2:
					SwitchScene(GameScene)
					running = False
					if issound:
						effects['start'].play()
					break
					break
				elif event.key == pygame.K_F6:
					ismusic = not ismusic
				elif event.key == pygame.K_F7:
					issound = not issound
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				menu.updateclick(event.pos)
				if screen_rect.collidepoint(event.pos):
					SwitchScene(GameScene)
					running = False
					if issound:
						effects['start'].play()
					break
					break
			elif event.type ==  pygame.MOUSEBUTTONUP and event.button == 1:
				pass
		
		mousepos = pygame.mouse.get_pos()
		
		menu.draw(display1)
		pygame.display.update()
		menu.update(mousepos)
		
		clock.tick(FPS)

def ScoreScene():
	global display1, spx, spy, screen1, isGame, clock, W, H, ok_up_surf, ok_down_surf, score_ok_rect
	global dict_score, ismusic, issound, STOPPED_PLAYING, ismusicfine, ismusicstart, running
	global menu
	
	ok_score_pos_rect = ok_up_surf.get_rect(topleft = (score_ok_rect.x + spx, score_ok_rect.y + spy))
	
	pygame.display.set_caption("???????????? ????????????")
	pygame.draw.rect(screen1, (240, 240, 240), (0, 0, W, H))	
	screen1.blit(ok_up_surf, score_ok_rect)
	pygame.draw.rect(display1, (166, 166, 166), (spx - 4, spy - 4, W + 8, H + 8), width = 4)
	display1.blit(screen1, (spx, spy))
	pygame.display.update()
	
	text_font = pygame.font.SysFont('arial', 20)
	x = y = 20
	count = 1
	len_count = len(dict_score)
	for key, value in dict_score.items():
		text = text_font.render(f"{count}.     {value}", 1, (0, 0, 0))
		if count != len_count:
			text_rect = text.get_rect(topleft=(x, y))
		else:
			text_rect = text.get_rect(topleft=(x-10, y))
		screen1.blit(text, text_rect)
		text = text_font.render(f"{key}", 1, (0, 0, 0))		
		text_rect = text.get_rect(topleft=(x+400, y))
		screen1.blit(text, text_rect)
		y+=30
		count+=1
		display1.blit(screen1, (spx, spy))
		pygame.display.update()
	
	is_ok = False
	ok_last_update = pygame.time.get_ticks()
	ok_frame_rate = 60
	
	running = True
	while running:
		if is_ok:
			ok_update = pygame.time.get_ticks()
			if ok_update - ok_last_update > ok_frame_rate:
				ok_last_update = ok_update
				isGame = True
				SwitchScene(GameScene)
				running = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				SwitchScene(None)
			elif event.type == STOPPED_PLAYING:
				ismusicfine = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F2:
					Restart()
					isGame = True
					SwitchScene(GameScene)
					running = False
				elif event.key == pygame.K_F3:
					isGame = False
				elif event.key == pygame.K_F4:
					running = False
					SwitchScene(None)
				elif event.key == pygame.K_F5:
					# SwitchScene(ScoreScene)
					# running = False
					isGame = True
					SwitchScene(GameScene)
					running = False
				elif event.key == pygame.K_F6:
					ismusic = not ismusic
					if not ismusicstart:
						ismusicstart = True
						pygame.mixer.music.play()
					else:
						if ismusic:
							if ismusicfine:
								pygame.mixer.music.rewind()
								pygame.mixer.music.play()
								ismusicfine = False
							else:
								if pygame.mixer.music.get_pos() != 0 and not pygame.mixer.music.get_busy():
									pygame.mixer.music.unpause()
						else:
							if pygame.mixer.music.get_busy():
								pygame.mixer.music.pause()
				elif event.key == pygame.K_F7:
					issound = not issound
				elif event.key == pygame.K_F8:
					isGame = False
					SwitchScene(about_scene)
					running = False
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				menu.updateclick(event.pos)
				if ok_score_pos_rect.collidepoint(event.pos):
					screen1.blit(ok_down_surf, score_ok_rect)
					display1.blit(screen1, (spx, spy))
					pygame.display.update()
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if ok_score_pos_rect.collidepoint(event.pos):
					screen1.blit(ok_up_surf, score_ok_rect)
					display1.blit(screen1, (spx, spy))
					pygame.display.update()
					is_ok = True
				else:
					screen1.blit(ok_up_surf, score_ok_rect)
					display1.blit(screen1, (spx, spy))
					pygame.display.update()
		
		mousepos = pygame.mouse.get_pos()
		
		menu.draw(display1)
		pygame.display.update()
		menu.update(mousepos)
		
		clock.tick(FPS)

def enter_name_scene():
	global display1, spx, spy, screen1, isGame, clock, W, H, ok_up_surf, ok_down_surf, score_ok_rect
	global Old_Score, user_name, dict_score, score_file, running
	global ismusic, issound, STOPPED_PLAYING, ismusicfine, ismusicstart
	
	global menu
	
	ok_enter_pos_rect = ok_up_surf.get_rect(topleft = (score_ok_rect.x + spx, score_ok_rect.y + spy))
	
	pygame.display.set_caption("")
	pygame.draw.rect(screen1, (240, 240, 240), (0, 0, W, H))	
	screen1.blit(ok_up_surf, score_ok_rect)
	pygame.draw.rect(display1, (166, 166, 166), (spx - 4, spy - 4, W + 8, H + 8), width = 4)
	display1.blit(screen1, (spx, spy))
	pygame.display.update()
	
	header_font = pygame.font.SysFont('arial', 20)
	header_text = header_font.render('?????????????? ???????? ??????:', 1, (0, 0, 0))
	
	text_area_rect = pygame.Rect((32, 67, W-64, 32))
	text_surf = header_font.render(user_name, 1, (0, 0, 0))
	text_rect = text_surf.get_rect(topleft = (34, 69))
	cursor = pygame.Rect(text_rect.topright, (2, text_rect.height))
	
	pygame.draw.rect(screen1, (98, 98, 98), (15, 15, W-30, 112), width=2)
	screen1.blit(header_text, (35,30))
	pygame.draw.rect(screen1, (158, 158, 158), (30, 65, W-60, 36), width=2)
	pygame.draw.rect(screen1, (255, 255, 255), text_area_rect)
	display1.blit(screen1, (spx, spy))
	pygame.display.update()
	
	ok_last_update = pygame.time.get_ticks()
	ok_frame_rate = 60
	
	is_ok = False
	
	running = True
	while running:
		if is_ok:
			ok_update = pygame.time.get_ticks()
			if ok_update - ok_last_update > ok_frame_rate:
				ok_last_update = ok_update
				if Old_Score > tuple(dict_score.keys())[-1]:
					dict_score[Old_Score] = user_name
					dict_score.sort(True, True)
					while len(dict_score) > 10:
						dict_score.popitem()
					with open(score_file,'w') as f:
						json.dump(dict_score(), f, indent=2)
				isGame = True
				SwitchScene(GameScene)
				running = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				SwitchScene(None)
			elif event.type == STOPPED_PLAYING:
				ismusicfine = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE:
					if len(user_name) > 0:
						user_name = user_name[:-1]
					else:
						user_name += event.unicode
				else:	
					user_name += event.unicode
				text_surf = header_font.render(user_name, 1, (0, 0, 0))
				text_rect = text_surf.get_rect(topleft = (34, 69))
				cursor.topleft = text_rect.topright
				if event.key == pygame.K_F6:
					ismusic = not ismusic
					if not ismusicstart:
						ismusicstart = True
						pygame.mixer.music.play()
					else:
						if ismusic:
							if ismusicfine:
								pygame.mixer.music.rewind()
								pygame.mixer.music.play()
								ismusicfine = False
							else:
								if pygame.mixer.music.get_pos() != 0 and not pygame.mixer.music.get_busy():
									pygame.mixer.music.unpause()
						else:
							if pygame.mixer.music.get_busy():
								pygame.mixer.music.pause()
				elif event.key == pygame.K_F7:
					issound = not issound
				elif event.key == pygame.K_RETURN:
					is_ok = True
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				menu.updateclick(event.pos)
				if ok_enter_pos_rect.collidepoint(event.pos):
					screen1.blit(ok_down_surf, score_ok_rect)
					display1.blit(screen1, (spx, spy))
					pygame.display.update()
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if ok_enter_pos_rect.collidepoint(event.pos):
					screen1.blit(ok_up_surf, score_ok_rect)
					display1.blit(screen1, (spx, spy))
					pygame.display.update()
					is_ok = True
				else:
					screen1.blit(ok_up_surf, score_ok_rect)
					display1.blit(screen1, (spx, spy))
					pygame.display.update()
		
		mousepos = pygame.mouse.get_pos()
		
		pygame.draw.rect(screen1, (255, 255, 255), text_area_rect)
		screen1.blit(text_surf, text_rect)
		if time.time() % 1 > 0.5:
			pygame.draw.rect(screen1, (0, 0, 0), cursor)
		display1.blit(screen1, (spx, spy))
		pygame.display.update()
				
		menu.draw(display1)
		pygame.display.update()
		menu.update(mousepos)
		
		clock.tick(FPS)

def about_scene():
	global display1, spx, spy, screen1, isGame, clock, W, H, ok_up_surf, ok_down_surf, ok_about_rect
	global ismusic, issound, live_bg, STOPPED_PLAYING, ismusicfine, ismusicstart, running
	global menu
	
	ok_about_pos_rect = ok_up_surf.get_rect(topleft=(ok_about_rect.x + spx, ok_about_rect.y + spy))
	
	pygame.display.set_caption("?? ??????????????????")
	pygame.draw.rect(screen1, (240, 240, 240), (0, 0, W, H))
	screen1.blit(ok_up_surf, ok_about_rect)
	screen1.blit(live_bg, (27, 30))
	pygame.draw.rect(display1, (166, 166, 166), (spx-4, spy-4, W+8, H+8), width = 4)
	display1.blit(screen1, (spx, spy))
	pygame.display.update()
	
	text_font = pygame.font.SysFont('arial', 18)
	screen1.blit(text_font.render('??????????.', 1, (0, 0, 0)), (77, 30))
	screen1.blit(text_font.render('????????????????????????????????: ?????????? ??????????.', 1, (0, 0, 0)), (20, 75))
	screen1.blit(text_font.render('??????????????: ?????????????? ????????????????,', 1, (0, 0, 0)), (20, 100))
	screen1.blit(text_font.render('?????????????? ????????????????????', 1, (0, 0, 0)), (85, 125))
	screen1.blit(text_font.render('???????????? ?? ??????????: ?????????????????? ????????????????.', 1, (0, 0, 0)), (20, 150))
	screen1.blit(text_font.render('Copyright (c) 1995 Nikita, Ltd.', 1, (0, 0, 0)), (20, 195))
	screen1.blit(text_font.render('?????? ?????????? ????????????????.', 1, (0, 0, 0)), (43, 220))
	display1.blit(screen1, (spx, spy))
	pygame.display.update()
	
	is_ok = False
	ok_last_update = pygame.time.get_ticks()
	ok_frame_rate = 60
	
	running = True
	while running:
		if is_ok:
			ok_update = pygame.time.get_ticks()
			if ok_update - ok_last_update > ok_frame_rate:
				ok_last_update = ok_update
				isGame = True
				SwitchScene(GameScene)
				running = False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				SwitchScene(None)
			elif event.type == STOPPED_PLAYING:
				ismusicfine = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F2:
					Restart()
					isGame = True
					SwitchScene(GameScene)
					running = False
				elif event.key == pygame.K_F3:
					isGame = False
				elif event.key == pygame.K_F4:
					running = False
					SwitchScene(None)
				elif event.key == pygame.K_F5:
					isGame = False
					SwitchScene(ScoreScene)
					running = False
				elif event.key == pygame.K_F6:
					ismusic = not ismusic
					if not ismusicstart:
						ismusicstart = True
						pygame.mixer.music.play()
					else:
						if ismusic:
							if ismusicfine:
								pygame.mixer.music.rewind()
								pygame.mixer.music.play()
								ismusicfine = False
							else:
								if pygame.mixer.music.get_pos() != 0 and not pygame.mixer.music.get_busy():
									pygame.mixer.music.unpause()
						else:
							if pygame.mixer.music.get_busy():
								pygame.mixer.music.pause()
				elif event.key == pygame.K_F7:
					issound = not issound
				elif event.key == pygame.K_F8:
					# About scene
					isGame = True
					SwitchScene(GameScene)
					running = False
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				menu.updateclick(event.pos)
				if ok_about_pos_rect.collidepoint(event.pos):
					screen1.blit(ok_down_surf, ok_about_rect)
					display1.blit(screen1, (spx, spy))
					pygame.display.update()
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if ok_about_pos_rect.collidepoint(event.pos):
					screen1.blit(ok_up_surf, ok_about_rect)
					display1.blit(screen1, (spx, spy))
					pygame.display.update()
					is_ok = True
				else:
					screen1.blit(ok_up_surf, ok_about_rect)
					display1.blit(screen1, (spx, spy))
					pygame.display.update()
		
		mousepos = pygame.mouse.get_pos()
		
		menu.draw(display1)
		pygame.display.update()
		menu.update(mousepos)
		
		clock.tick(FPS)

def GameScene():
	global display1, spx, spy, w, h, screen1, clock, surf_table, rect_table, score_bg, coord_score_bg, isGame, background
	global ismusic, issound, dict_score, STOPPED_PLAYING, ismusicfine, ismusicstart, running
	global menu
	
	pygame.display.set_caption("Escape")
	
	pygame.draw.rect(display1, (64, 64, 64), (spx - 4, spy - 4, W + 8, H + 8), width = 4)
	screen1.fill((64, 64, 64))
	screen1.blit(score_bg, (coord_score_bg[0], coord_score_bg[1]))
	display1.blit(screen1, (spx, spy))
	pygame.display.update()
	
	### Debug
	
	score = 0
	live = 4
	level = 1
		
	### Debug
	
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				SwitchScene(None)
			elif event.type == STOPPED_PLAYING:
				ismusicfine = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F2:
					Restart()
					isGame = True
				elif event.key == pygame.K_F3:
					isGame = not isGame
				elif event.key == pygame.K_F4:
					running = False
					SwitchScene(None)
				elif event.key == pygame.K_F5:
					isGame = False
					SwitchScene(ScoreScene)
					running = False
				elif event.key == pygame.K_F6:
					ismusic = not ismusic
					if not ismusicstart:
						ismusicstart = True
						pygame.mixer.music.play()
					else:
						if ismusic:
							if ismusicfine:
								pygame.mixer.music.rewind()
								pygame.mixer.music.play()
								ismusicfine = False
							else:
								if pygame.mixer.music.get_pos() != 0 and not pygame.mixer.music.get_busy():
									pygame.mixer.music.unpause()
						else:
							if pygame.mixer.music.get_busy():
								pygame.mixer.music.pause()
				elif event.key == pygame.K_F7:
					issound = not issound
				elif event.key == pygame.K_F8:
					isGame = False
					SwitchScene(about_scene)
					running = False
			elif event.type == pygame.KEYUP:
				# if event.key in []:
				pass
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				menu.updateclick(event.pos)
			elif  event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				pass
			elif event.type == pygame.MOUSEMOTION:
				pass
		
		#keys = pygame.key.get_pressed()
		#pressed = pygame.mouse.get_pressed()
		#if pressed[0]:
		#	pos = pygame.mouse.get_pos()
		#	print(pos)
		
		#pressed = pygame.mouse.get_pressed()
		#if pressed[0]:
		#	pos = pygame.mouse.get_pos()
		
		#if isGame:
		#	DrawTotal(score_bg, score, level, live, False)
		#	screen1.blit(score_bg, (coord_score_bg[0], coord_score_bg[1]))
		#	display1.blit(screen1, (w, h))
		#	pygame.display.update()
		
		#if Old_Score > dict_score[tuple(dict_score.keys())[-1]]:
		# Enter Name scene
		# Else Score Scene
		
		mousepos = pygame.mouse.get_pos()
		
		menu.draw(display1)
		pygame.display.update()	
		menu.update(mousepos)
		
		clock.tick(FPS)

def main():
	SwitchScene(StartScene)
	#SwitchScene(enter_name_scene)
	while current_scene is not None:
		current_scene()

if __name__ == '__main__':
	main()
