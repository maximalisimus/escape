import pathlib

W, H = 596, 385
FPS = 60

Old_Score = 0
Old_Level = 1
Old_Live = 4

isStart = False
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

coord_score = (475,40)
coord_level = (510, 110.5)
coord_live = (460, 160)
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

medicine = {
			'name': 'medicine_chest',
			'path': pathlib.Path('./images/medicine-chest.png').resolve(),
			'score': 1,
			}

heart = {
			'name': 'heart',
			'path': pathlib.Path('./images/heart.png').resolve(),
			'score': 1,
		}

logo = pathlib.Path('./images/esc_t.png').resolve()
background = pathlib.Path('./images/esc-bg.png').resolve()
live_bg = pathlib.Path('./images/live-bg.png').resolve()
died_bg = pathlib.Path('./images/died-bg.png').resolve()

bomb_path = pathlib.Path('./images/bomb.png').resolve()

shot_path = pathlib.Path('./images/bullet.png').resolve()

blade_rear = pathlib.Path('./images/blade-rear.png').resolve()
blade_up = pathlib.Path('./images/blade-up.png').resolve()
