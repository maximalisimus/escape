import pygame
import pathlib
from typing import Tuple
from enum import Enum

class TDict(object):
	
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
		return f"TDict:{self.__g.__str__()}"

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

class TGroup(TDict):
	
	def __init__(self, *args):
		super(TGroup, self).__init__(*args)
	
	def add(self, *args):
		if len(args) == 1:
			if not self.has_value(args[0]):
				self[len(self)+1] = args[0]
		elif len(args) > 1:
			if len(args) == 2:
				if not self.has_value(args[1]):
					self[args[0]] = args[1]
			elif len(args) == 3:
				if not self.has_key(args[0]):
					self[args[0]] = TDict()	
				if type(self[args[0]]) == TDict:
					self[args[0]][args[1]] = args[2]
	
	def has(self, v):
		return self.has_value(v)
	
	def remove(self, *args):
		if len(args) > 0 and len(args) < 3:
			if len(args) == 1:
				if self.get(args[0], False):
					del self[args[0]]
			elif len(args) == 2:
				if self.get(args[0], TDict()).get(args[1], False):
					del self[args[0]][args[1]]
	
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
	
	def empty(self):
		self.clear()
	
	def updates(self, *args, **kwargs):
		for row in self.values():
			if type(row) == TDict:
				for col in row.values():
					if hasattr(col, 'update'):
						col.update(*args, **kwargs)
			else:
				if hasattr(row, 'update'):
					row.update(*args, **kwargs)
	
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
