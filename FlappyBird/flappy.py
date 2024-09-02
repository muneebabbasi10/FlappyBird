import pygame, sys, random

def draw_floor():
	screen.blit(floor_surface, (floor_x_position, 900))
	screen.blit(floor_surface, (floor_x_position + 576, 900))

def create_pipe():
	random_pipe_position = random.choice(pipe_height)
	bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_position))
	top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_position - 300))
	return bottom_pipe, top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 1024:
			screen.blit(pipe_surface, pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe, pipe)

def check_collision(pipes):
	for pipe in pipes:
		if bird_rectangle.colliderect(pipe):
			death_sound.play()
			return False

	if bird_rectangle.top <= -100 or bird_rectangle.bottom >= 900:
		return False

	return True

def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rectangle = new_bird.get_rect(center=(100, bird_rectangle.centery))
	return new_bird, new_bird_rectangle

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
		score_rectangle = score_surface.get_rect(center=(288, 100))
		screen.blit(score_surface, score_rectangle)

	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
		score_rectangle = score_surface.get_rect(center=(288, 100))
		screen.blit(score_surface, score_rectangle)

		high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
		high_score_rectangle = high_score_surface.get_rect(center=(288, 185))
		screen.blit(high_score_surface, high_score_rectangle)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

# Function to initialize pygame
pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('./assets/04B_19.TTF', 40)

# Variables for the game
gravity = 0.25
bird_movement = 0
game_active = False  # Start with the game inactive
score = 0
high_score = 0

# Background surface
background_surface = pygame.image.load('assets/background-day.png').convert()
background_surface = pygame.transform.scale2x(background_surface)

# Floor surface
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_position = 0

# Bird animation frames
bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/bluebird-midflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rectangle = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

# Pipe surface
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)  # Event triggered every 1.2 seconds
pipe_height = [400, 600, 800]

# Game over surface
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rectangle = game_over_surface.get_rect(center=(288, 512))

# Text for the start screen
start_text_surface = game_font.render('Created By Muneeb Abbasi', True, (255, 255, 255))
start_text_rectangle = start_text_surface.get_rect(center=(288, 400))

title_text_surface = game_font.render('FlappyBird', True, (255, 255, 255))
title_text_rectangle = title_text_surface.get_rect(center=(288, 460))

instruction_text_surface = game_font.render('Press Space to Start', True, (255, 255, 255))
instruction_text_rectangle = instruction_text_surface.get_rect(center=(288, 520))

# Sounds
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if game_active:
					bird_movement = 0
					bird_movement -= 8  # Reduced jump speed
					flap_sound.play()
				else:
					game_active = True
					pipe_list.clear()
					bird_rectangle.center = (100, 512)
					bird_movement = 0
					score = 0

		if event.type == SPAWNPIPE and game_active:
			pipe_list.extend(create_pipe())

		if event.type == BIRDFLAP and game_active:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0
			bird_surface, bird_rectangle = bird_animation()

	# Background
	screen.blit(background_surface, (0, 0))

	if game_active:
		# Bird movement
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rectangle.centery += bird_movement
		screen.blit(rotated_bird, bird_rectangle)
		game_active = check_collision(pipe_list)

		# Pipes
		pipe_list = move_pipes(pipe_list)
		draw_pipes(pipe_list)

		# Score
		score += 0.01
		score_display('main_game')
		score_sound_countdown -= 1
		if score_sound_countdown <= 0:
			score_sound.play()
			score_sound_countdown = 100

	else:
		if score == 0:  # Display the start screen text only at the start
			screen.blit(start_text_surface, start_text_rectangle)
			screen.blit(title_text_surface, title_text_rectangle)
			screen.blit(instruction_text_surface, instruction_text_rectangle)
		else:
			screen.blit(game_over_surface, game_over_rectangle)
			high_score = update_score(score, high_score)
			score_display('game_over')

	# Floor movement
	floor_x_position -= 1
	draw_floor()
	if floor_x_position <= -576:
		floor_x_position = 0

	pygame.display.update()
	clock.tick(120)
