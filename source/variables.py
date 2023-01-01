import pathlib
import pygame

W, H = 596, 385
FPS = 60

pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()
screen1 = pygame.display.set_mode((W, H))
pygame.display.set_caption("Esc")
pygame.display.set_icon(pygame.image.load(str(pathlib.Path('./config/').joinpath('logo.png').resolve())))

clock = pygame.time.Clock()

Old_Score = 0
Old_Level = 1
Old_Live = 4

isStart = True
isGame = False

size_surf_score = (92,22)
size_surf_level = (26, 22)
size_surf_lives = (128,32)
size_helicopter = (72, 48)

size_blocks = 24

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

bonus_line = (3, 6, 9, 12, 15)

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

medicine = pygame.image.load(pathlib.Path('./images/medicine-chest.png').resolve()).convert_alpha()
mdeicine_score = 1
medicine_name = 'medicine_chest'

all_bonuses = {
				0: {
					'name': 'alarm',
					'surf': pygame.image.load(pathlib.Path('./images/alarm.png').resolve()).convert_alpha(),
					'score': 100,
					},
				1: {
					'name': 'burger',
					'surf': pygame.image.load(pathlib.Path('./images/burger.png').resolve()).convert_alpha(),
					'score': 50,
					},
				2: {
					'name': 'clock',
					'surf': pygame.image.load(pathlib.Path('./images/clock.png').resolve()).convert_alpha(),
					'score': 30,
					},
				3: {
					'name': 'coffee',
					'surf': pygame.image.load(pathlib.Path('./images/coffee.png').resolve()).convert_alpha(),
					'score': 20,
					},
				4: {
					'name': 'cola',
					'surf': pygame.image.load(pathlib.Path('./images/cola.png').resolve()).convert_alpha(),
					'score': 10,
					},
				5: {
					'name': 'stop',
					'surf': pygame.image.load(pathlib.Path('./images/stop.png').resolve()).convert_alpha(),
					'score': 1,
					},
				6: {
					'name': 'thermos',
					'surf': pygame.image.load(pathlib.Path('./images/thermos.png').resolve()).convert_alpha(),
					'score': 1,
					},
			}

logo = pathlib.Path('./images/esc_t.png').resolve()

background = pathlib.Path('./images/esc-bg.png').resolve()
score_bg = pygame.image.load(pathlib.Path('./images/score-bg.png').resolve()).convert_alpha()
live_bg = pygame.image.load(pathlib.Path('./images/live-bg.png').resolve()).convert_alpha()
died_bg = pygame.image.load(pathlib.Path('./images/died-bg.png').resolve()).convert_alpha()

door_path = pathlib.Path('./images/door.png').resolve()

bomb_path = pathlib.Path('./images/bomb.png').resolve()
bomb_name = 'bomb'

shot_path = pathlib.Path('./images/bullet.png').resolve()
shot_name = 'shot'

heart_path = pathlib.Path('./images/heart.png').resolve()
heart_score = 5
heart_name = 'heart'

blade_rear_path = pathlib.Path('./images/blade-rear.png').resolve()
blade_up_path = pathlib.Path('./images/blade-up.png').resolve()

surf_table = pygame.Surface((size_table[0], size_table[1]), pygame.SRCALPHA, 32).convert_alpha()
rect_table = surf_table.get_rect(topleft=(0, 0))

src_surf_bonus = pygame.Surface((size_table[0], size_table[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_bonus = pygame.Surface.copy(src_surf_bonus)
rect_bonus = surf_bonus.get_rect(topleft=(0, 0))

surf_score = pygame.Surface((size_surf_score[0], size_surf_score[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_level = pygame.Surface((size_surf_level[0], size_surf_level[1]), pygame.SRCALPHA, 32).convert_alpha()
surf_lives = pygame.Surface((size_surf_lives[0], size_surf_lives[1]), pygame.SRCALPHA, 32).convert_alpha()

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

blocks = []

bonus_blocks = []
