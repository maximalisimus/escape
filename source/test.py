#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pathlib

class TDict(object):
	
	__slots__ = '__dict__'
	
	def __init__(self, *args):
		super(TDict, self).__init__()
		self.__g = dict(*args)
	
	def __setitem__(self, key, item):
		if not type(key) in (float, int, str, tuple, frozenset, bool, None):
			raise TypeError('Please, enter the \'key\' in (float, int, str, tuple, bool or frozenset)!')
		self.__g[key] = item

	def __getitem__(self, key):
		return self.__g[key] if self.has_key(key) else None
	
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

def main():
	#score_tuple = ((1958, ''), (1054, 'mikl'), (633, ''), (577, ''), (519, ''),\
	#				(475, ''), (424, 'user'), (406, ''), (337, ''), (382, ''))
	#score_dict = TDict(score_tuple)
	#print(score_dict)
	#score_encode = json.dumps(score_dict.copy())
	#score_decode = json.loads(score_encode)
	#print(score_encode)
	#print(score_decode)
	#new_score = TDict(tuple((int(k), v) for k,v in tuple(json.loads(score_encode).items())))
	#print(new_score)
	#with open(pathlib.Path('./score.json').resolve(),'w') as f:
	#	json.dump(score_dict.copy(), f, indent=2)
	#score_dict = TDict()
	with open(pathlib.Path('./score.json').resolve(),'r') as f:
		score_dict = TDict(tuple((int(k), v) for k,v in tuple(json.load(f).items())))
	print(score_dict)
	Old_Score = 341
	Old_Level = 4
	user_name = 'VanDame'
	if Old_Level > 1 and Old_Score > 100:
		score_dict[Old_Score] = user_name
		score_dict.sort(True, True)
		while len(score_dict) > 10:
			score_dict.popitem()
		print(type(score_dict), len(score_dict), score_dict)

if __name__ == '__main__':
	main()
