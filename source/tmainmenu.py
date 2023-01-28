import pygame
import pathlib
from typing import Tuple
from enum import Enum

def CreateEmtySurf(SizeWidth: int = 24, SizeHeight: int = 24):
	return pygame.Surface((SizeWidth, SizeHeight), pygame.SRCALPHA, 32).convert_alpha()

def LoadSurf(paths):
	return pygame.image.load(str(paths)).convert_alpha()

checkmark_font_file = pathlib.Path('./config/SegoeUISymbol.ttf').resolve()

class NoValue(Enum):
	''' Base Enum class elements '''

	def __repr__(self):
		return f"{self.__class__}: {self.name}"
	
	def __str__(self):
		return f"{self.name}"
	
	def __call__(self):
		return f"{self.value}"

class TypeMenu(NoValue):
	Menu = 0
	Sep = 1
	
	@classmethod
	def GetTypeMenuValue(cls, value):
		for x in cls:
			if value == x.value:
				return x
		return None
	
	@classmethod
	def GetTypeMenuName(cls, OnName):
		for x in cls:
			if OnName == x:
				return x
		return None

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

class GetScreenW:
	
	def __get__(self, obj, objtype = None):
		return pygame.display.Info().current_w

class GetScreenH:
	
	def __get__(self, obj, objtype = None):
		return pygame.display.Info().current_h

class GetMarkRect:
	
	def __get__(self, obj, objtype = None):
		return TConfig.font.mark().get_rect()

class TConfig:
	
	screen_w = GetScreenW()
	screen_h = GetScreenH()
	font = TFont(ismark = True)
	bg_color = (64, 64, 64)
	menu_color = (240, 240, 240)
	frame_color = (166, 166, 166)
	select_color = (48, 150, 250)
	text_color = (0, 0, 0)
	step = (10, 5)
	frame_width = 2
	dmw_max = 0
	mark_rect = GetMarkRect()

	@classmethod
	def GetTextRectWH(cls, text):
		surf = cls.font().render(text, 1, cls.font.color)
		width = surf.get_rect().width
		height = surf.get_rect().height
		return (width, height)

class SubMenu(pygame.sprite.Sprite):
	
	ID = 0
	
	def __init__(self, MenuType: TypeMenu = TypeMenu.Menu, \
				fmark: bool = True, ismark = False, text: str = '', \
				hotkey: str = '', old_rect = None, up_rect = None, group = None, \
				callback = None):
		pygame.sprite.Sprite.__init__(self)
		SubMenu.ID += 1
		self.uid = SubMenu.ID
		self.up_rect = up_rect
		self.typemenu = MenuType
		self.fmark = fmark
		self.ismark = ismark
		self.text = text
		self.hotkey = hotkey
		self.old_rect = old_rect
		self.callback = callback
		if group != None:
			self.add(group)
		self.ismenu = False
		self.text_surf = TConfig.font().render(self.text, 1, TConfig.font.color)
		self.hotkey_surf = TConfig.font().render(self.hotkey, 1, TConfig.font.color)
		self.text_rect = self.text_surf.get_rect()
		self.hotkey_rect = self.hotkey_surf.get_rect()
		self.image = None
		self.rect = None
		self.rebuildsize()
		self.build()

	def rebuildsize(self):
		dmw = []
		for item in self.groups()[0].sprites():
			dmw.append(item.text_rect.width)
		TConfig.dmw_max = max(dmw)

	def build(self, hotkey_text: str = 'F2'):
		if self.typemenu == TypeMenu.Menu:
			x111 = 0
			y111 = 0
			w111 = 0
			h111 = 0
			x112 = 0
			y112 = 0
			x113 = 0
			y113 = 0
			if self.fmark:
				x111 = TConfig.step[0]*2 + TConfig.mark_rect.width
				w111 = TConfig.dmw_max + TConfig.GetTextRectWH(hotkey_text)[0] + TConfig.mark_rect.width + TConfig.step[0]*6
				x112 = self.up_rect.bottomleft[0] + 4 + TConfig.dmw_max + TConfig.step[0]*6
				y111 = TConfig.step[1]
				y112 = TConfig.step[1]
				h111 = self.text_rect.height + TConfig.step[1]*2
			else:
				x111 = TConfig.step[0]*2
				w111 = TConfig.dmw_max + TConfig.GetTextRectWH(hotkey_text)[0] + TConfig.step[0]*6
				x112 = TConfig.dmw_max + TConfig.step[0]*5
				y111 = TConfig.step[1]
				y112 = TConfig.step[1]
				h111 = self.text_rect.height + TConfig.step[1]*2
			self.text_rect.topleft = (x111, y111)
			self.hotkey_rect.topleft = (x112, y112)
			self.image = CreateEmtySurf(w111, h111)
			if len(self.groups()[0].sprites()) == 1:
				x113 = self.old_rect.bottomleft[0] + 4
				y113 = self.old_rect.bottomleft[1] + 4
			else:
				if self.fmark:
					x113 = self.old_rect.bottomleft[0]
					y113 = self.old_rect.bottomleft[1]
				else:
					if len(self.groups()[0].sprites()) > 1:
						x113 = self.old_rect.bottomleft[0] + 2
						y113 = self.old_rect.bottomleft[1] + 2
					else:
						x113 = self.old_rect.bottomleft[0]
						y113 = self.old_rect.bottomleft[1]
			self.rect = self.image.get_rect(topleft = (x113, y113))
			self.image.blit(self.text_surf, self.text_rect)
			self.image.blit(self.hotkey_surf, self.hotkey_rect)
			if self.fmark:
				mark_x = TConfig.step[0] + self.rect.x
				mark_y = 2 + self.rect.y
				self.mark_rect = TConfig.font.mark().get_rect(topleft = (mark_x, mark_y))
		else:
			if self.fmark:
				w111 = TConfig.dmw_max + TConfig.GetTextRectWH(hotkey_text)[0] + TConfig.mark_rect.width + TConfig.step[0]*6
			else:
				w111 = TConfig.dmw_max + TConfig.GetTextRectWH(hotkey_text)[0] + TConfig.step[0]*4
			h111 = (self.old_rect.height + TConfig.step[1])//2 + 2
			self.image = CreateEmtySurf(w111, h111)
			x111 = self.old_rect.bottomleft[0]
			y111 = self.old_rect.bottomleft[1]
			self.rect = self.image.get_rect(topleft = (x111, y111))
			lr_x1 = TConfig.step[0]
			lr_y1 = self.rect.height / 2
			lr_x2 = self.rect.width - 5
			lr_y2 = self.rect.height / 2
			pygame.draw.line(self.image, TConfig.frame_color, (lr_x1, lr_y1), (lr_x2, lr_y1), width = TConfig.frame_width)

	def update(self, pos):
		self.ismenu = self.rect.collidepoint(pos)
	
	def updateclick(self, pos, ismark = None, obj = None):
		if self.rect.collidepoint(pos):
			for item in self.groups()[0].sprites():
				item.ismenu = False
			if ismark is not None:
				self.ismark = ismark
			if obj is not None:
				if hasattr(obj, 'ismenu'):
					obj.ismenu = False
					MainMenu.isactive = False
			if self.callback is not None:
				self.callback()
	
	def draw(self, surf):
		surf.blit(self.image, self.rect)

class TSub:
	
	def __init__(self, up_rect, ismark: bool = True):
		super(TSub, self).__init__()
		self.up_rect = up_rect
		self.menu = pygame.sprite.Group()
		self.menu.updateclick = self.updatesubclick
		self.menu.edit = self.edit
		self.ismark = ismark
		self.image = None
		self.rect = None
		self.dmh = 0
		self.dmw = 0
		self.ismenu = False
	
	def edit(self, uid: int):
		for item in self.menu.sprites():
			if item.uid == uid:
				return item
		return self.menu.sprites()[0]
	
	def updatesubclick(self, pos, ismark = None, obj = None):
		for item in self.menu.sprites():
			item.updateclick(pos, ismark, obj)
	
	def add(self, menutype: TypeMenu = TypeMenu.Menu, ismark = False, text: str = '', hotkey: str = '', callback = None):
		if len(self.menu.sprites()) == 0:
			SubMenu(menutype, self.ismark, ismark, text, hotkey, self.up_rect, self.up_rect, self.menu, callback)
		else:
			SubMenu(menutype, self.ismark, ismark, text, hotkey, self.menu.sprites()[-1].rect, self.up_rect, self.menu, callback)
		self.dmh = 0
		self.dmw = 0
		on_dmw = []
		for item in self.menu.sprites():
			self.dmh += item.rect.height
			on_dmw.append(item.rect.width)
		self.dmw = max(on_dmw)

	def build(self, hotkey: str = 'F2'):
		dmenu_w = 0
		dmenu_h = 0
		dmenu_w = self.dmw + TConfig.GetTextRectWH(hotkey)[0] - 8
		dmenu_h = self.dmh + 8
		self.image = CreateEmtySurf(dmenu_w, dmenu_h)
		dm_x = self.up_rect.bottomleft[0]
		dm_y = self.up_rect.bottomleft[1]
		self.rect = self.image.get_rect(topleft = (dm_x, dm_y))
		pygame.draw.rect(self.image, TConfig.frame_color, (0, 0, dmenu_w, dmenu_h), width = TConfig.frame_width)
		pygame.draw.rect(self.image, TConfig.menu_color, (2, 2, dmenu_w - 4, dmenu_h - 4))
		for sprite in self.menu.sprites():
			sprite.build(hotkey)
		self.menu.sprites()[0].rect.topleft = (self.up_rect.bottomleft[0] + 4, self.up_rect.bottomleft[1] + 4)
		self.menu.sprites()[0].mark_rect.topleft = (TConfig.step[0] + self.menu.sprites()[0].rect.x, 2 + self.menu.sprites()[0].rect.y)

	def update(self, pos):
		self.menu.update(pos)
	
	def updateclick(self, pos, ismark = None, obj = None):
		self.menu.updateclick(self.menu, pos, ismark, obj)
	
	def draw(self, surface):
		surface.blit(self.image, self.rect)
		for sprite in self.menu.sprites():
			if sprite.ismenu and sprite.typemenu != TypeMenu.Sep:
				pygame.draw.rect(surface, TConfig.select_color, sprite.rect)
			if sprite.fmark and sprite.ismark:
				surface.blit(TConfig.font.mark.mark, sprite.mark_rect)
			sprite.draw(surface)

class MainMenu(pygame.sprite.Sprite):
	
	isactive = False
	ID = 0
	
	def __init__(self, surf, group = None, callback = None):
		pygame.sprite.Sprite.__init__(self)
		MainMenu.ID += 1
		self.uid = MainMenu.ID
		self.image = surf
		self.rect = self.image.get_rect()
		self.ismenu = False
		self.callback = callback
		if group != None:
			self.add(group)
		if callback == None:
			pass
	
	def update(self, pos):
		self.ismenu = self.rect.collidepoint(pos)

	def updateclick(self, pos, ismark = None):
		if self.rect.collidepoint(pos):
			if self.callback != None:
				self.ismenu = False
				MainMenu.isactive = False
				self.callback()
	
	def draw(self, surf):
		surf.blit(self.image, self.rect)

class TMenu:
	
	def __init__(self, menu = [], *oncallback):
		self.text = list(menu)[:]
		TConfig.font.color = TConfig.text_color
		TConfig.font.update()
		self.menu = pygame.sprite.Group()
		self.menu.updateclick = self.updateclick
		self.menu.edit = self.edit
		self.oncallback = list(oncallback)
		self.build()
	
	def edit(self, uid: int):
		for item in self.menu.sprites():
			if item.uid == uid:
				return item
		return self.menu.sprites()[0]
	
	def updateclick(self, pos, ismark = None):
		for item in self.menu.sprites():
			item.updateclick(pos, ismark)
	
	def build(self):
		for count in range(len(self.text)):
			text_surf = TConfig.font().render(self.text[count], 1, TConfig.font.color)
			x = TConfig.step[0]
			y = TConfig.step[1]
			text_rect = text_surf.get_rect(topleft = (x, y))
			w1 = text_rect.width + x*2
			h1 = text_rect.height + y*2
			if len(self.oncallback) > count:
				menu = MainMenu(CreateEmtySurf(w1, h1), self.menu, self.oncallback[count])
			else:
				menu = MainMenu(CreateEmtySurf(w1, h1), self.menu)
			menu.image.blit(text_surf, text_rect)
			if count == 0:
				posx = 0
			else:
				posx = self.menu.sprites()[count-1].rect.x + self.menu.sprites()[count-1].rect.width
			posy = 0
			menu.rect.topleft = (posx, posy)
		mw = TConfig.screen_w
		mh = self.menu.sprites()[0].rect.height
		self.image = CreateEmtySurf(mw, mh)
		self.rect = self.image.get_rect(topleft = (0, 0))
		self.image.fill(TConfig.menu_color)
	
	def update(self, pos):
		if MainMenu.isactive:
			self.menu.update(pos)
	
	def updateclick(self, pos, ismark = None):
		for item in self.menu.sprites():
			if item.rect.collidepoint(pos):
				MainMenu.isactive = not MainMenu.isactive
				if hasattr(item, 'updateclick'):
					item.updateclick(pos, ismark)
			if MainMenu.isactive:
				item.ismenu = item.rect.collidepoint(pos)
	
	def draw(self, surface):
		surface.blit(self.image, self.rect)
		if MainMenu.isactive:
			for item in self.menu.sprites():
				if item.ismenu:
					pygame.draw.rect(surface, TConfig.select_color, item.rect)
		self.menu.draw(surface)

