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

W, H = 596, 385
FPS = 60

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
infoObject = pygame.display.Info()
w = infoObject.current_w
h = infoObject.current_h
display1 = pygame.display.set_mode((w , h))
pygame.display.set_caption("Menu")
#pygame.display.set_icon(pygame.image.load(str(pathlib.Path('./config/').joinpath('logo.png').resolve())))

current_scene = None

clock = pygame.time.Clock()

def CreateEmtySurf(SizeWidth: int = 24, SizeHeight: int = 24):
	return pygame.Surface((SizeWidth, SizeHeight), pygame.SRCALPHA, 32).convert_alpha()

def LoadSurf(paths):
	return pygame.image.load(str(paths)).convert_alpha()

running = True

def SwitchScene(scene):
	global current_scene
	current_scene = scene

def Work():
	global display1, clock
	
	pygame.display.set_caption("Menu")
	
	display1.fill((64, 64, 64))
	pygame.display.update()
	
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				SwitchScene(None)
			elif event.type == pygame.KEYDOWN:
				#if event.key == pygame.K_F2:
				pass	
			elif event.type == pygame.KEYUP:
				# if event.key in []:
				pass
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				pass
			elif  event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				pass
			elif event.type == pygame.MOUSEMOTION:
				pass
		
		#keys = pygame.key.get_pressed()
		#pressed = pygame.mouse.get_pressed()
		#if pressed[0]:
		#	pos = pygame.mouse.get_pos()
		#	print(pos)
		
		clock.tick(FPS)

def main():
	SwitchScene(Work)
	while current_scene is not None:
		current_scene()

if __name__ == '__main__':
	main()
