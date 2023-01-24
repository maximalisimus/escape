#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pathlib
from typing import Tuple
import time

FPS = 60
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
infoObject = pygame.display.Info()
w = infoObject.current_w
h = infoObject.current_h
display1 = pygame.display.set_mode((w , h))
pygame.display.set_caption("Test")
#pygame.display.set_icon(pygame.image.load(str(pathlib.Path('./config/').joinpath('logo.png').resolve())))

current_scene = None
clock = pygame.time.Clock()
running = True

def CreateEmtySurf(SizeWidth: int = 24, SizeHeight: int = 24):
	return pygame.Surface((SizeWidth, SizeHeight), pygame.SRCALPHA, 32).convert_alpha()

def LoadSurf(paths):
	return pygame.image.load(str(paths)).convert_alpha()

def SwitchScene(scene):
	global current_scene
	current_scene = scene

checkmark_font_file = pathlib.Path('./config/SegoeUISymbol.ttf').resolve()

class TCheckMark:
	
	__slots__ = ['__size', '__color', '__mark', '__checkmark_font_file', \
				'__markbold', '__markitalic', '__markunderline', 'font']
	
	def __init__(self, onsize: int = 14, \
				color: Tuple[int, int, int] = (0, 0, 0), \
				markfontfile = checkmark_font_file, \
				ismarkbold: bool = True, \
				ismarkitalic: bool = False, ismarkunderline: bool = False):
		FontMenu = pygame.font.Font
		self.__size = onsize
		self.__color = color
		if markfontfile.exists():
			self.__checkmark_font_file = str(markfontfile)
		else:
			self.__checkmark_font_file = None
		self.__markbold = ismarkbold
		self.__markitalic = ismarkitalic
		self.__markunderline = ismarkunderline
		self.font = FontMenu(self.__checkmark_font_file, self.__size)
		if self.__markbold:
			self.font.set_bold(True)
		if self.__markitalic:
			self.font.set_italic(True)
		if self.__markunderline:
			self.font.set_underline(True)
		self.__mark = self.font.render('✓', 1, self.__color)

	def __getattr__(self, name):
		return None
	
	def __repr__(self):
		return f"{self.__class__}: font = {self.font}, size = {self.__size}, " + \
				f"color = {self.__color}, " + \
				f"markbold = {self.__markbold}, markitalic = {self.__markitalic}, markunderline = {self.__markunderline}."
	
	def __str__(self):
		return f"['{self.__checkmark_font_file}', {self.__size}, {self.__color}, " + \
				f"{self.__markbold}, {self.__markitalic}, {self.__markunderline}]"
	
	def __call__(self):
		return self.__mark
	
	def update(self):
		FontMenu = pygame.font.Font
		self.font = FontMenu(self.__checkmark_font_file, self.__size)
		if self.__markbold:
			self.font.set_bold(True)
		if self.__markitalic:
			self.font.set_italic(True)
		if self.__markunderline:
			self.font.set_underline(True)
		self.__mark = self.font.render('✓', 1, self.__color)

	@property
	def size(self):
		return self.__size
	
	@size.setter
	def size(self, value):
		if type(value) != int:
			raise TypeError('Please, enter the integer type!')
		self.__size = value
	
	@size.deleter
	def size(self):
		del self.__size
	
	@property
	def color(self):
		return self.__color
	
	@color.setter
	def color(self, value):
		if type(value) != tuple:
			if len(value) != 3:
				raise TypeError('Please, enter the tuple!')
		self.__color = value
	
	@color.deleter
	def color(self):
		del self.__color
	
	@property
	def markfontfile(self):
		return self.__checkmark_font_file
	
	@markfontfile.setter
	def markfontfile(self, value):
		if type(value) != str:
			raise TypeError('Please, enter the integer type!')
		if pathlib.Path(value).resolve().exists():
			self.__checkmark_font_file = str(pathlib.Path(value).resolve())
		else:
			self.__checkmark_font_file = None
	
	@markfontfile.deleter
	def markfontfile(self):
		del self.__checkmark_font_file

	@property
	def bold(self):
		return self.__markbold
	
	@bold.setter
	def bold(self, value):
		if type(value) != bool:
			raise TypeError('Please, enter the integer type!')
		self.__markbold = value
	
	@bold.deleter
	def bold(self):
		del self.__markbold
	
	@property
	def italic(self):
		return self.__markitalic
	
	@italic.setter
	def italic(self, value):
		if type(value) != bool:
			raise TypeError('Please, enter the integer type!')
		self.__markitalic = value
	
	@italic.deleter
	def italic(self):
		del self.__markitalic

	@property
	def underline(self):
		return self.__markunderline
	
	@underline.setter
	def underline(self, value):
		if type(value) != bool:
			raise TypeError('Please, enter the integer type!')
		self.__markunderline = value
	
	@underline.deleter
	def underline(self):
		del self.__markunderline

	@property
	def mark(self):
		return self.__mark

	@mark.deleter
	def mark(self):
		del self.__mark

class TFont:
	
	__slots__ = ['__fontname', '__size', '__bold', \
				'__italic', '__underline', '__color', \
				'font', '__ismark', 'mark']
	
	def __init__(self, fontname: str = 'arial', onsize: int = 14, \
				color: Tuple[int, int, int] = (0, 0, 0), \
				isbold: bool = False, isitalic: bool = False, \
				isunderline: bool = False, \
				ismark: bool = False):
		SysFontMenu = pygame.font.SysFont
		has_fonts = pygame.font.get_fonts
		if fontname in has_fonts():
			self.__fontname = fontname
		else:
			self.__fontname = None
		self.__size = onsize
		self.__color = color
		self.__bold = isbold
		self.__italic = isitalic
		self.__underline = isunderline
		self.__ismark = ismark
		self.font = SysFontMenu(self.__fontname, self.__size, self.__bold, self.__italic)
		if self.__underline:
			self.font.set_underline(True)
		if self.__ismark:
			self.mark = TCheckMark(self.__size, self.__color)
		else:
			self.mark = None
	
	def __getattr__(self, name):
		return None
	
	def __repr__(self):
		return f"{self.__class__}: fontname = '{self.__fontname}', size = {self.__size}, " + \
				f"color = {self.__color}, " + \
				f"bold = {self.__bold}, italic = {self.__italic}, " + \
				f"underline = {self.__underline}, " + \
				f"ismark = {self.__ismark}, mark = {self.mark}."
	
	def __str__(self):
		return f"['{self.__fontname}', {self.__size}, {self.__color}, " + \
			f"{self.__bold}, {self.__italic}, {self.__underline}, " +\
			f"{self.__ismark}, {self.mark}]"
	
	def __call__(self):
		return self.font
	
	def update(self):
		SysFontMenu = pygame.font.SysFont
		self.font = SysFontMenu(self.__fontname, self.__size, self.__bold, self.__italic)
		if self.__underline:
			self.font.set_underline(True)
		if self.__ismark:
			if hasattr(self.mark, 'update'):
				self.mark.update()
	
	@property
	def fontname(self):
		return self.__fontname
	
	@fontname.setter
	def fontname(self, value):
		if type(value) != str:
			raise TypeError('Please, enter the string type!')
		has_fonts = pygame.font.get_fonts
		if value in has_fonts():
			self.__fontname = value
		else:
			self.__fontname = None
	
	@fontname.deleter
	def fontname(self):
		del self.__fontname
	
	@property
	def size(self):
		return self.__size
	
	@size.setter
	def size(self, value):
		if type(value) != int:
			raise TypeError('Please, enter the integer type!')
		self.__size = value
	
	@size.deleter
	def size(self):
		del self.__size
	
	@property
	def bold(self):
		return self.__bold
	
	@bold.setter
	def bold(self, value):
		if type(value) != bool:
			raise TypeError('Please, enter the integer type!')
		self.__bold = value
	
	@bold.deleter
	def bold(self):
		del self.__bold
	
	@property
	def italic(self):
		return self.__italic
	
	@bold.setter
	def bold(self, value):
		if type(value) != bool:
			raise TypeError('Please, enter the integer type!')
		self.__bold = value
	
	@bold.deleter
	def bold(self):
		del self.__bold
	
	@property
	def underline(self):
		return self.__underline
	
	@underline.setter
	def underline(self, value):
		if type(value) != bool:
			raise TypeError('Please, enter the integer type!')
		self.__underline = value
	
	@underline.deleter
	def underline(self):
		del self.__underline
	
	@property
	def color(self):
		return self.__color
	
	@color.setter
	def color(self, value):
		if type(value) != tuple:
			if len(value) != 3:
				raise TypeError('Please, enter the tuple!')
		self.__color = value
	
	@color.deleter
	def color(self):
		del self.__color

	@property
	def ismark(self):
		return self.__ismark
	
	@ismark.setter
	def ismark(self, value):
		if type(value) != bool:
			raise TypeError('Please, enter the integer type!')
		self.__ismark = value
	
	@ismark.deleter
	def ismark(self):
		del self.__ismark

class TextMenu(pygame.sprite.Sprite):
	
	def __init__(self, surf, group = None):
		super(TextMenu, self).__init__()
		self.image = surf
		self.rect = self.image.get_rect()
		self.ismenu = False
		if group != None:
			self.add(group)
	
	def update(self, pos):
		if self.rect.collidepoint(pos):
			self.ismenu = True
		else:
			self.ismenu = False

class TMenu:
	
	screen_w = pygame.display.Info().current_w
	screen_h = pygame.display.Info().current_h
	
	def __init__(self, upmenu: list = []):
		self.text = upmenu[:]
		self.font = TFont(ismark = True)
		self.bg_color = (64, 64, 64)
		self.menu_color = (240, 240, 240)
		self.frame_color = (166, 166, 166)
		self.select_color = (48, 150, 250)
		self.text_color = (0, 0, 0)
		self.step = (10, 5)
		self.frame_width = 2
		self.isactive = False
		self.upmenu = pygame.sprite.Group()
		for count in range(len(self.text)):
			text_surf = self.font().render(self.text[count], 1, self.font.color)
			x = self.step[0]
			y = self.step[1]
			text_rect = text_surf.get_rect(topleft = (x, y))
			w1 = text_rect.width + x*2
			h1 = text_rect.height + y*2
			menu = TextMenu(CreateEmtySurf(w1, h1), self.upmenu)
			menu.image.blit(text_surf, text_rect)
			if count == 0:
				posx = 0
			else:
				posx = self.upmenu.sprites()[count-1].rect.x + self.upmenu.sprites()[count-1].rect.width
			posy = 0
			menu.rect.topleft = (posx, posy)
		mw = TMenu.screen_w
		mh = self.upmenu.sprites()[0].rect.height
		self.image = CreateEmtySurf(mw, mh)
		self.rect = self.image.get_rect(topleft = (0, 0))
		self.image.fill(self.menu_color)
	
	def update(self, pos):
		if self.isactive:
			self.upmenu.update(pos)
	
	def updateclick(self, pos):
		hits = []
		for item in self.upmenu.sprites():
			if item.rect.collidepoint(pos):
				hits.append(item)
		if len(hits) >= 1:
			self.isactive = True
		else:
			self.isactive = False
		if not self.isactive:
			for item in self.upmenu.sprites():
				item.ismenu = False
	
	def draw(self, surface):
		surface.blit(self.image, self.rect)
		if self.isactive:
			for item in self.upmenu.sprites():
				if item.ismenu:
					pygame.draw.rect(surface, self.select_color, item.rect)
		self.upmenu.draw(surface)

def work():
	global display1, clock, running, w, h
		
	display1.fill((64, 64, 64))
	pygame.display.update()
	
	main_menu = TMenu(['Игра', 'Помощь'])
	
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				SwitchScene(None)
			#elif event.type == STOPPED_PLAYING:
				# pass
			elif event.type == pygame.KEYDOWN:
				# if event.key == pygame.K_F2:
				#	pass
				pass
			elif event.type == pygame.KEYUP:
				# if event.key in []:
				pass
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				main_menu.updateclick(event.pos)
			elif  event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				pass
			elif event.type == pygame.MOUSEMOTION:
				main_menu.update(event.pos)
		
		#keys = pygame.key.get_pressed()
		# if keys[pygame.K_SPACE]:
		#	pass
		#pressed = pygame.mouse.get_pressed()
		#if pressed[0]:
		#	pos = pygame.mouse.get_pos()
		#	print(pos)
		
		main_menu.draw(display1)
		pygame.display.update()
		
		clock.tick(FPS)

def main():
	SwitchScene(work)
	while current_scene is not None:
		current_scene()

if __name__ == '__main__':
	main()