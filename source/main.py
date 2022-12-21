#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib

images = {'bonus': '1': {
						'name': 'alarm',
						'path': str(pathlib.Path('./images/alarm.png').resolve()),
						'score': 100,
						},
					'2': {
						'name': 'burger',
						'path': str(pathlib.Path('./images/burger.png').resolve()),
						'score': 50,
						},
					'3': {
						'name': 'clock',
						'path': str(pathlib.Path('./images/clock.png').resolve()),
						'score': 30,
						},
					'4': {
						'name': 'coffee',
						'path': str(pathlib.Path('./images/coffee.png').resolve()),
						'score': 20,
						},
					'5': {
						'name': 'cola',
						'path': str(pathlib.Path('./images/cola.png').resolve()),
						'score': 10,
						},
					'6': {
						'name': 'medicine_chest',
						'path': str(pathlib.Path('./images/medicine-chest.png').resolve()),
						'score': 1,
						},
					'7': {
						'name': 'stop',
						'path': str(pathlib.Path('./images/stop.png').resolve()),
						'score': 1,
						},
					'8': {
						'name': 'thermos',
						'path': str(pathlib.Path('./images/thermos.png').resolve()),
						'score': 1,
						},
		'wall': {
				1: str(pathlib.Path('./images/tile-1.png').resolve()),
				2: str(pathlib.Path('./images/tile-2.png').resolve()),
				3: str(pathlib.Path('./images/tile-3.png').resolve()),
				4: str(pathlib.Path('./images/tile-4.png').resolve()),
				5: str(pathlib.Path('./images/tile-5.png').resolve()),
				6: str(pathlib.Path('./images/tile-6.png').resolve()),
				},
		'bg': {
				1:  str(pathlib.Path('./images/esc_1.png').resolve()),
				2:  str(pathlib.Path('./images/esc_2.png').resolve()),
				3:  str(pathlib.Path('./images/esc_3.png').resolve()),
				4:  str(pathlib.Path('./images/esc_4.png').resolve()),
				5:  str(pathlib.Path('./images/esc_5.png').resolve()),
				6:  str(pathlib.Path('./images/esc_6.png').resolve()),
				7:  str(pathlib.Path('./images/esc_t.png').resolve()),
				8:  str(pathlib.Path('./images/esc-bg.png').resolve()),
			},
		'else': {
					1:  str(pathlib.Path('./images/hatch-bombs.png').resolve()),
					2:  str(pathlib.Path('./images/hatch-bombs-2.png').resolve()),
					3:  str(pathlib.Path('./images/Helicopter_1.png').resolve()),
					4:  str(pathlib.Path('./images/Helicopter_2.png').resolve()),
					5:  str(pathlib.Path('./images/Helicopter_3.png').resolve()),
					6:  str(pathlib.Path('./images/Helicopter_4.png').resolve()),
					7:  str(pathlib.Path('./images/ladder.png').resolve()),
					8:  str(pathlib.Path('./images/ladder-2.png').resolve()),
					9:  str(pathlib.Path('./images/left-pistol.png').resolve()),
					10:  str(pathlib.Path('./images/right-pistol.png').resolve()),
					11:  str(pathlib.Path('./images/live-bg.png').resolve()),
					12:  str(pathlib.Path('./images/died-bg.png').resolve()),
					13:  str(pathlib.Path('./images/door.png').resolve()),
					14:  str(pathlib.Path('./images/blade-rear.png').resolve()),
					15:  str(pathlib.Path('./images/blade-up.png').resolve()),
				}
		}

levels = str(pathlib.Path('./levels/').resolve())

musics = str(pathlib.Path('./sounds/music.mp3').resolve())

sounds = {
			'alarm': str(pathlib.Path('./sounds/alarm.WAV').resolve()),
			'applause': str(pathlib.Path('./sounds/applause.WAV').resolve()),
			'bomb': str(pathlib.Path('./sounds/bomb.WAV').resolve()),
			'burger': str(pathlib.Path('./sounds/burger.WAV').resolve()),
			'clock': str(pathlib.Path('./sounds/clock.WAV').resolve()),
			'coffee': str(pathlib.Path('./sounds/coffee.WAV').resolve()),
			'cola': str(pathlib.Path('./sounds/cola.WAV').resolve()),
			'heart': str(pathlib.Path('./sounds/heart.WAV').resolve()),
			'jump': str(pathlib.Path('./sounds/jump.WAV').resolve()),
			'live': str(pathlib.Path('./sounds/live.WAV').resolve()),
			'final': str(pathlib.Path('./sounds/final.WAV').resolve()),
			'shot': str(pathlib.Path('./sounds/shot.WAV').resolve()),
			'start': str(pathlib.Path('./sounds/start.WAV').resolve()),
			'stop': str(pathlib.Path('./sounds/stop.WAV').resolve()),
			'thermos': str(pathlib.Path('./sounds/thermos.WAV').resolve())
		}

def main():
	pass

if __name__ == '__main__':
	main()
