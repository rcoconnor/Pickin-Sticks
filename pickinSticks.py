import os
import sys
import pygame
import random
import time

character_size = 50
screen_width = 600
screen_height = 600

pygame.init()
pygame.font.init()

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 205, 0)

pygame.display.set_caption("Pickin Sticks")
screen = pygame.display.set_mode((screen_width, screen_height))

comic_sans = pygame.font.SysFont('Comic Sans MS', 30)
smaller_font = pygame.font.SysFont('Comic Sans MS', 15)

up = (0, -character_size)
down = (0, character_size)
left = (-character_size, 0)
right = (character_size, 0)

def load_image(name, colorkey=None): 
	try: 
		image = pygame.image.load(name)
	except pygame.error as error: 
		print("cannot load image: ", name)
		raise systemExit(message)
	image = image.convert()
	if colorkey is not None: 
		if colorkey is -1: 
			colorkey = 	image.get_at((0, 0))
		image.set_colorkey(colorkey, pygame.RLEACCEL)
	return image, image.get_rect()



class Stick(pygame.sprite.Sprite): 
	def __init__(self): 
		pygame.sprite.Sprite.__init__(self)
		self.image, self.rect = load_image("banana2.png", -1)
		self.image = pygame.transform.scale(self.image, (character_size, character_size))
		self.name = "stick"
		self.xpos = round(random.randint(0, screen_width)/character_size) * character_size
		self.ypos = round(random.randint(0, screen_height)/character_size) * character_size
		self.rect = pygame.Rect(self.xpos, self.ypos, character_size, character_size)

	def move(self): 
		self.xpos = round(random.randint(0, screen_width)/character_size) * character_size
		self.ypos = round(random.randint(0, screen_height)/character_size) * character_size
		print(str(self.xpos) + ", " + str(self.ypos) + "\n")
		while self.xpos > screen_width - character_size or self.xpos < 0: 
			print("----Over Limit----\n")
			self.xpos = round (random.randint(0, 600)/character_size) * character_size

		while self.ypos > screen_height - (character_size * 2) or self.ypos < character_size: 
			print("----Over Limit----\n")
			self.ypos = round(random.randint(0, 600)/character_size) * character_size

		self.rect.topleft = (self.xpos, self.ypos)
		self.check_in_bounds()

	def check_in_bounds(self): 
		if self.rect.top < 0: 
			self.move()
		if self.rect.bottom > 550: 
			self.move()
		if self.rect.left < 0: 
			self.move()
		if self.rect.right > 550: 
			self.move()

class Player(pygame.sprite.Sprite): 
	def __init__(self): 
		#call sprite initializer
		pygame.sprite.Sprite.__init__(self) 
		self.image, self.rect = load_image("chimp.bmp", -1)
		self.image = pygame.transform.scale(self.image, (character_size, character_size))
		self.xpos = 250
		self.ypos = 250
		self.rect.topleft = (self.xpos, self.ypos)
		self.rect = pygame.Rect(self.xpos, self.ypos, character_size, character_size)
		self.score = 0

	def move(self, direction): 
		newpos = self.rect.move(direction)
		self.rect = newpos

	def increase_score(self, stick): 
		if self.rect.colliderect(stick.rect): 
			self.score += 1

	def wrap_up(self): 
		newpos = self.rect.move(0, -600)
		self.rect = newpos

	def wrap_down(self): 
		newpos = self.rect.move(0, 600)
		self.rect = newpos

	def wrap_left(self): 
		newpos = self.rect.move(600, 0)
		self.rect = newpos

	def wrap_right(self): 
		newpos = self.rect.move(-600, 0)
		self.rect = newpos


def message_to_screen(msg, color): 
	screen_text = comic_sans.render(msg, True, (color))
	screen.blit(screen_text, [250, 250])

def game_over(score): 

	score_string = "Score: " + str(score)
	game_over_str = "Game Over"
	play_again_string = "Press Space to play again"


	game_over_msg = comic_sans.render(game_over_str, False, (0, 0, 0))
	score_msg = comic_sans.render(score_string, False, (0, 0, 0))
	play_again_msg = smaller_font.render(play_again_string, False, (0, 0, 0))

	screen.blit(game_over_msg, (200, 225))
	screen.blit(score_msg, (217, 300)) 
	screen.blit(play_again_msg, (200, 375))


def main(): 
	#initialize everything

	
	clock = pygame.time.Clock()
	counter = 10
	is_game_over = False

	pygame.time.set_timer(pygame.USEREVENT, 1000)

	player = Player()
	stick = Stick()
	stick.check_in_bounds()
	allsprites = pygame.sprite.RenderPlain((player, stick))

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill(green)

	game_exit = False

	while not game_exit: 

		while is_game_over == True: 
			screen.fill(green)
			game_over(player.score)
			pygame.display.update()


			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN: 
					if event.key == pygame.K_SPACE: 
						is_game_over = False 
						counter = 10
						player.score = 0
				if event.type == pygame.QUIT: 
					game_exit = True
					is_game_over = False


		for event in pygame.event.get(): 
			#quit the game
			if event.type == pygame.QUIT: 
				game_exit = True
				pygame.quit()

			#countdown the time
			if event.type == pygame.USEREVENT: 
				counter -= 1

			#handle character movement
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP: 
					player.move(up)
				if event.key == pygame.K_DOWN: 
					player.move(down)
				if event.key == pygame.K_LEFT: 
					player.move(left)
				if event.key == pygame.K_RIGHT: 
					player.move(right)


		if counter <= 0: 
			is_game_over = True


		#handle the scoring 
		if player.rect.colliderect(stick.rect): 
			player.increase_score(stick)
			stick.move()

		#handle wrap arounds
		if player.rect.top > 600 - character_size: 
			player.wrap_up()
		if player.rect.top < 0: 
			player.wrap_down()
		if player.rect.right > 600: 
			player.wrap_right()
		if player.rect.left < 0: 
			player.wrap_left()

		score_string = "Score: " + str(player.score)
		time_string = str(counter)

		textsurface = comic_sans.render(score_string, False, (0, 0, 0))
		time_surface = comic_sans.render(time_string, False, (0, 0, 0))
		

		allsprites.update()
		screen.blit(background, (0, 0))

		#if is_game_over == False: 
		screen.blit(textsurface, (0, 0))
		screen.blit(time_surface, (550, 0))
		allsprites.draw(screen)

		
		pygame.display.update()
	pygame.quit()
	quit()




main()
#screen = pygame.display.set_mode((600, 600))
#game_over(screen, 5)



