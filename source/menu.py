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

def NewFont(fontname: str = 'arial', onsize: int = 14, \
			isbold: bool = False, isitalic: bool = False, \
			isunderline: bool = False):
	SysFontMenu = pygame.font.SysFont
	has_fonts = pygame.font.get_fonts
	if fontname in has_fonts():
		font_object = SysFontMenu(fontname, onsize, isbold, isitalic)
	else:
		font_object = SysFontMenu(None, onsize, isbold, isitalic)
	if isunderline:
		font_object.set_underline(True)
	return font_object

def RenderCheckMark(onsize: int = 14, color: Tuple[int, int, int] = (0, 0, 0), \
				isbold: bool = True, isitalic: bool = False, \
				isunderline: bool = False):
	FontMenu = pygame.font.Font
	global checkmark_font_file
	temp_font = FontMenu(str(checkmark_font_file), onsize)
	if isbold:
		temp_font.set_bold(True)
	if isitalic:
		temp_font.set_italic(True)
	if isunderline:
		temp_font.set_underline(True)
	mark_surf = temp_font.render('✓', 1, color)
	return mark_surf

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

def CreateFont(fontconfig: TFont = TFont()):
	SysFontMenu = pygame.font.SysFont
	has_fonts = pygame.font.get_fonts
	if fontconfig.fontname in has_fonts():
		font_object = SysFontMenu(fontconfig.fontname, fontconfig.size, fontconfig.bold, fontconfig.italic)
	else:
		font_object = SysFontMenu(None, fontconfig.size, fontconfig.bold, fontconfig.italic)
	if fontconfig.underline:
		font_object.set_underline(True)
	return font_object

def work():
	global display1, clock, running, w, h
	
	bg_color = (64, 64, 64)
	menu_color = (240, 240, 240)
	frame_color = (166, 166, 166)
	select_color = (48, 150, 250)
	text_color = (0, 0, 0)
	
	display1.fill(bg_color)
	pygame.display.update()
	
	font_name = 'arial'
	font_size = 14
	
	font = pygame.font.SysFont(font_name, font_size)
	
	text1 = 'Игра'
	text2 = 'Помощь'
	
	up_menu_surf1 = font.render(text1, 1, text_color)
	up_menu_surf2 = font.render(text2, 1, text_color)
	
	step = (10, 5)
	frame_width = 2
	
	up_menu_surf_rect1 = up_menu_surf1.get_rect(topleft = (step[0], step[1]))
	w1 = up_menu_surf_rect1.width + step[0]*2
	h1 = up_menu_surf_rect1.height + step[1]*2
	up_menu1 = CreateEmtySurf(w1, h1)
	up_menu1.blit(up_menu_surf1, up_menu_surf_rect1)
	posx1 = 0
	posy1 = 0
	up_menu_rect1 = up_menu1.get_rect(topleft = (posx1, posy1))
	
	x2 = step[0]
	y2 = step[1]
	up_menu_surf_rect2 = up_menu_surf2.get_rect(topleft = (x2, y2))
	w2 = up_menu_surf_rect2.width + step[0]*2
	h2 = up_menu_surf_rect2.height + step[1]*2
	up_menu2 = CreateEmtySurf(w2, h2)
	up_menu2.blit(up_menu_surf2, up_menu_surf_rect2)
	posx2 = up_menu_rect1.x + up_menu_rect1.width
	posy2 = 0
	up_menu_rect2 = up_menu2.get_rect(topleft = (posx2, posy2))
	
	up_menu_full_width = pygame.display.Info().current_w
	up_menu_full_height = up_menu_surf1.get_rect()[3] + step[1]*2
	
	up_menu_surf = CreateEmtySurf(up_menu_full_width, up_menu_full_height)
	up_menu_rect = up_menu_surf.get_rect(topleft = (0, 0))
	
	#pygame.draw.rect(display1, menu_color, up_menu_rect)
	up_menu_surf.fill(menu_color)
	display1.blit(up_menu_surf, up_menu_rect)
	#pygame.draw.rect(display1, select_color, up_menu_rect1)
	#pygame.draw.rect(display1, select_color, up_menu_rect2)
	display1.blit(up_menu1, up_menu_rect1)
	display1.blit(up_menu2, up_menu_rect2)
	
	pygame.display.update()
	
	text111 = 'Сначала'
	text112 = 'F2'
	text121 = 'Перерыв'
	text122 = 'F3'
	text131 = 'Лучшие игроки'
	text132 = 'F5'
	text141 = 'Музыка'
	text142 = 'F6'
	text151 = 'Звук'
	text152 = 'F7'
	text161 = '-'
	text162 = '--'
	text171 = 'Выход'
	text172 = 'F4'
	
	dmenu_surf111 = font.render(text111, 1, text_color)
	dmenu_surf112 = font.render(text112, 1, text_color)
	dmenu_surf121 = font.render(text121, 1, text_color)
	dmenu_surf122 = font.render(text122, 1, text_color)
	dmenu_surf131 = font.render(text131, 1, text_color)
	dmenu_surf132 = font.render(text132, 1, text_color)
	dmenu_surf141 = font.render(text141, 1, text_color)
	dmenu_surf142 = font.render(text142, 1, text_color)
	dmenu_surf151 = font.render(text151, 1, text_color)
	dmenu_surf152 = font.render(text152, 1, text_color)
	dmenu_surf161 = font.render(text161, 1, text_color)
	dmenu_surf162 = font.render(text162, 1, text_color)
	dmenu_surf171 = font.render(text171, 1, text_color)
	dmenu_surf172 = font.render(text172, 1, text_color)
	
	dmw = (dmenu_surf111.get_rect().width, dmenu_surf121.get_rect().width, \
			dmenu_surf131.get_rect().width, dmenu_surf141.get_rect().width, \
			dmenu_surf151.get_rect().width, dmenu_surf161.get_rect().width)
	dmw_max = max(dmw)
	del dmw
	
	#ischeckmark = True
	mark_surf = RenderCheckMark(font_size)
	mark_rect = mark_surf.get_rect()
	
	dmenu_w = dmw_max + dmenu_surf112.get_rect().width + mark_rect.width + step[0]*6 + 8
	dmenu_h = (dmenu_surf111.get_rect().height + step[1])*8 + 8
	dmenu_surf1 = CreateEmtySurf(dmenu_w, dmenu_h)
	dm_x = up_menu_rect1.bottomleft[0]
	dm_y = up_menu_rect1.bottomleft[1]
	dmenu_surf_rect1 = dmenu_surf1.get_rect(topleft = (dm_x, dm_y))
	pygame.draw.rect(dmenu_surf1, frame_color, (0, 0, dmenu_w, dmenu_h), width = frame_width)
	pygame.draw.rect(dmenu_surf1, menu_color, (2, 2, dmenu_w - 4, dmenu_h - 4))
	display1.blit(dmenu_surf1, dmenu_surf_rect1)
	pygame.display.update()
	
	x111 = step[0]*2 + mark_rect.width
	y111 = step[1]
	dmenu_surf_rect111 = dmenu_surf111.get_rect(topleft = (x111, y111))
	w111 = dmw_max + dmenu_surf112.get_rect().width + mark_rect.width + step[0]*6
	h111 = dmenu_surf_rect111.height + step[1]*2
	d_menu_surf111 = CreateEmtySurf(w111, h111)
	d_menu_surf111.blit(dmenu_surf111, dmenu_surf_rect111)
	x112 = up_menu_rect1.bottomleft[0] + 4 + dmw_max + step[0]*6
	y112 = step[1]
	dmenu_surf_rect112 = dmenu_surf112.get_rect(topleft = (x112, y112))
	d_menu_surf111.blit(dmenu_surf112, dmenu_surf_rect112)
	x113 = up_menu_rect.bottomleft[0] + 4
	y113 = up_menu_rect.bottomleft[1] + 4
	d_menu_surf_rect111 = d_menu_surf111.get_rect(topleft = (x113, y113))
	
	x121 = step[0]*2 + mark_rect.width
	y121 = step[1]
	dmenu_surf_rect121 = dmenu_surf121.get_rect(topleft = (x121, y121))
	w121 = dmw_max + dmenu_surf122.get_rect().width + mark_rect.width + step[0]*6
	h121 = dmenu_surf_rect121.height + step[1]*2
	d_menu_surf121 = CreateEmtySurf(w121, h121)
	x123 = d_menu_surf_rect111.bottomleft[0]
	y123 = d_menu_surf_rect111.bottomleft[1]
	d_menu_surf_rect121 = d_menu_surf121.get_rect(topleft = (x123, y123))
	mark_x = step[0]
	mark_y = 2
	mark_new_rect = mark_surf.get_rect(topleft = (mark_x, mark_y))
	d_menu_surf121.blit(mark_surf, mark_new_rect)
	d_menu_surf121.blit(dmenu_surf121, dmenu_surf_rect121)
	x122 = up_menu_rect1.bottomleft[0] + 4 + dmw_max + step[0]*6
	y122 = step[1]
	dmenu_surf_rect122 = dmenu_surf122.get_rect(topleft = (x112, y112))
	d_menu_surf121.blit(dmenu_surf122, dmenu_surf_rect122)
	
	x131 = step[0]*2 + mark_rect.width
	y131 = step[1]
	dmenu_surf_rect131 = dmenu_surf131.get_rect(topleft = (x131, y131))
	w131 = dmw_max + dmenu_surf132.get_rect().width + mark_rect.width + step[0]*6
	h131 = dmenu_surf_rect131.height + step[1]*2
	d_menu_surf131 = CreateEmtySurf(w131, h131)
	x133 = d_menu_surf_rect121.bottomleft[0]
	y133 = d_menu_surf_rect121.bottomleft[1]
	d_menu_surf_rect131 = d_menu_surf131.get_rect(topleft = (x133, y133))
	mark_x = step[0]
	mark_y = 2
	mark_new_rect = mark_surf.get_rect(topleft = (mark_x, mark_y))
	#d_menu_surf131.blit(mark_surf, mark_new_rect)
	d_menu_surf131.blit(dmenu_surf131, dmenu_surf_rect131)
	x132 = up_menu_rect1.bottomleft[0] + 4 + dmw_max + step[0]*6
	y132 = step[1]
	dmenu_surf_rect132 = dmenu_surf132.get_rect(topleft = (x132, y132))
	d_menu_surf131.blit(dmenu_surf132, dmenu_surf_rect132)
	
	x141 = step[0]*2 + mark_rect.width
	y141 = step[1]
	dmenu_surf_rect141 = dmenu_surf141.get_rect(topleft = (x141, y141))
	w141 = dmw_max + dmenu_surf142.get_rect().width + mark_rect.width + step[0]*6
	h141 = dmenu_surf_rect141.height + step[1]*2
	d_menu_surf141 = CreateEmtySurf(w141, h141)
	x143 = d_menu_surf_rect131.bottomleft[0]
	y143 = d_menu_surf_rect131.bottomleft[1]
	d_menu_surf_rect141 = d_menu_surf141.get_rect(topleft = (x143, y143))
	mark_x = step[0]
	mark_y = 2
	mark_new_rect = mark_surf.get_rect(topleft = (mark_x, mark_y))
	d_menu_surf141.blit(mark_surf, mark_new_rect)
	d_menu_surf141.blit(dmenu_surf141, dmenu_surf_rect141)
	x142 = up_menu_rect1.bottomleft[0] + 4 + dmw_max + step[0]*6
	y142 = step[1]
	dmenu_surf_rect142 = dmenu_surf142.get_rect(topleft = (x142, y142))
	d_menu_surf141.blit(dmenu_surf142, dmenu_surf_rect142)
	
	x151 = step[0]*2 + mark_rect.width
	y151 = step[1]
	dmenu_surf_rect151 = dmenu_surf151.get_rect(topleft = (x151, y151))
	w151 = dmw_max + dmenu_surf152.get_rect().width + mark_rect.width + step[0]*6
	h151 = dmenu_surf_rect151.height + step[1]*2
	d_menu_surf151 = CreateEmtySurf(w151, h151)
	x153 = d_menu_surf_rect141.bottomleft[0]
	y153 = d_menu_surf_rect141.bottomleft[1]
	d_menu_surf_rect151 = d_menu_surf151.get_rect(topleft = (x153, y153))
	mark_x = step[0]
	mark_y = 2
	mark_new_rect = mark_surf.get_rect(topleft = (mark_x, mark_y))
	d_menu_surf151.blit(mark_surf, mark_new_rect)
	d_menu_surf151.blit(dmenu_surf151, dmenu_surf_rect151)
	x152 = up_menu_rect1.bottomleft[0] + 4 + dmw_max + step[0]*6
	y152 = step[1]
	dmenu_surf_rect152 = dmenu_surf152.get_rect(topleft = (x152, y152))
	d_menu_surf151.blit(dmenu_surf152, dmenu_surf_rect152)
	
	x161 = step[0]*2 + mark_rect.width
	y161 = step[1]
	dmenu_surf_rect161 = dmenu_surf151.get_rect(topleft = (x161, y161))
	w161 = dmw_max + dmenu_surf152.get_rect().width + mark_rect.width + step[0]*6
	h161 = (dmenu_surf_rect161.height + step[1])//2 + 2
	d_menu_surf161 = CreateEmtySurf(w161, h161)
	x163 = d_menu_surf_rect151.bottomleft[0]
	y163 = d_menu_surf_rect151.bottomleft[1]
	d_menu_surf_rect161 = d_menu_surf161.get_rect(topleft = (x163, y163))
	lr_x1 = step[0]
	lr_y1 = d_menu_surf_rect161.height / 2
	lr_x2 = d_menu_surf_rect161.width - 5
	lr_y2 = d_menu_surf_rect161.height / 2
	pygame.draw.line(d_menu_surf161, frame_color, (lr_x1, lr_y1), (lr_x2, lr_y1), width = frame_width)
	
	x171 = step[0]*2 + mark_rect.width
	y171 = step[1]
	dmenu_surf_rect171 = dmenu_surf171.get_rect(topleft = (x171, y171))
	w171 = dmw_max + dmenu_surf152.get_rect().width + mark_rect.width + step[0]*6
	h171 = dmenu_surf_rect151.height + step[1]*2
	d_menu_surf171 = CreateEmtySurf(w171, h171)
	x173 = d_menu_surf_rect161.bottomleft[0]
	y173 = d_menu_surf_rect161.bottomleft[1]
	d_menu_surf_rect171 = d_menu_surf171.get_rect(topleft = (x173, y173))
	mark_x = step[0]
	mark_y = 2
	mark_new_rect = mark_surf.get_rect(topleft = (mark_x, mark_y))
	#d_menu_surf171.blit(mark_surf, mark_new_rect)
	d_menu_surf171.blit(dmenu_surf171, dmenu_surf_rect151)
	x172 = up_menu_rect1.bottomleft[0] + 4 + dmw_max + step[0]*6
	y172 = step[1]
	dmenu_surf_rect172 = dmenu_surf172.get_rect(topleft = (x172, y172))
	d_menu_surf171.blit(dmenu_surf172, dmenu_surf_rect172)
	
	display1.blit(dmenu_surf1, dmenu_surf_rect1)
	#pygame.draw.rect(display1, select_color, d_menu_surf_rect111)
	#pygame.draw.rect(display1, select_color, d_menu_surf_rect121)
	#pygame.draw.rect(display1, select_color, d_menu_surf_rect131)
	#pygame.draw.rect(display1, select_color, d_menu_surf_rect141)
	#pygame.draw.rect(display1, select_color, d_menu_surf_rect151)
	#pygame.draw.rect(display1, select_color, d_menu_surf_rect171)
	display1.blit(d_menu_surf111, d_menu_surf_rect111)
	display1.blit(d_menu_surf121, d_menu_surf_rect121)
	display1.blit(d_menu_surf131, d_menu_surf_rect131)
	display1.blit(d_menu_surf141, d_menu_surf_rect141)
	display1.blit(d_menu_surf151, d_menu_surf_rect151)
	display1.blit(d_menu_surf161, d_menu_surf_rect161)
	display1.blit(d_menu_surf171, d_menu_surf_rect171)
	pygame.display.update()
	
	text211 = 'О программе'
	text212 = 'F8'
	
	#myfont = TFont('arial', 30, ismark = True)
	#myfont.mark.bold = False
	#myfont.mark.update()
	#new_text = myfont().render('Text', 1, myfont.color)
	#display1.blit(myfont.mark.mark, (200, 200))
	#display1.blit(new_text, (250, 200))
	#pygame.display.update()
	#print(dir(myfont))
	#print(dir(myfont.mark))
	#print(myfont.mark.mark)
	
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
				pass
			elif  event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				pass
			elif event.type == pygame.MOUSEMOTION:
				pass
		
		#keys = pygame.key.get_pressed()
		# if keys[pygame.K_SPACE]:
		#	pass
		#pressed = pygame.mouse.get_pressed()
		#if pressed[0]:
		#	pos = pygame.mouse.get_pos()
		#	print(pos)
		
		clock.tick(FPS)

def main():
	SwitchScene(work)
	while current_scene is not None:
		current_scene()

if __name__ == '__main__':
	main()
