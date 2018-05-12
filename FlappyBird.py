import pygame 
import os
import random 

pygame.init()
pygame.font.init()

# colors 
white = (255, 255, 255)
blue = (0, 0, 200)

height = 640
width = 360

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Pickin Sticks")

def load_image(name, colorkey = None): 
	try: 
		image = pygame.image.load(name)
	except pygame.error as error: 
		print("Cannot load image: ", name)
		raise systemExit(message)
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1: 
			colorkey = image.get_at((0, 0))
		image.set_colorkey(colorkey, pygame.RLEACCEL)
	return image



class Pipes(pygame.sprite.Sprite): 

	def __init__(self, the_player): 
		# load the images
		self.player = the_player
		self.bottom_image = load_image("Pipe_Long_bottom.png")
		self.top_image = load_image("Pipe_Long.png")
		self.space_between = 160 + random.randint(0, 20) * 5
		self.did_collide = False
		
		# Positions
		self.xpos = 360
		self.ypos = round(random.randint(1, 33)* 20)

		#check to make sure the y position is within bounds
		while self.ypos > 620 or self.ypos < 130 + self.space_between: 
			self.ypos = round(random.randint(1, 33) * 20)
		

		# create rects
		self.bottom_rect = self.bottom_image.get_rect()
		self.bottom_rect.topleft = (self.xpos, self.ypos)
		self.top_rect = self.top_image.get_rect()
		self.top_rect.bottomleft = (self.xpos, self.ypos - self.space_between)

	def move_pipes(self): 
		if self.did_collide != True: 
			newpos = self.bottom_rect.move(-2, 0)
			self.bottom_rect = newpos

			newpos = self.top_rect.move(-2, 0)
			self.top_rect = newpos

			self.xpos -= 2


	def does_collide(self): 
		# function to check if the player and pipe collide
		# will set did_collide to true or false
		if self.bottom_rect.colliderect(self.player): 
			if self.did_collide != True: 
				print("collision detected")
			self.did_collide = True

		if self.top_rect.colliderect(self.player): 
			if self.did_collide != True: 
				print("collision detected")
			self.did_collide = True
			




	def update(self): 
		self.does_collide()		
		self.move_pipes()


	def offscren(self): 
		if self.top_rect.right < 0: 
			return True
		return False



 



class Player(pygame.sprite.Sprite): 
	# This class will create a player class with
	# 	- a sprite image and rect
	# 	- x and y poss

	def __init__(self): 
		
		# sprite properties 
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("bird_sprite.jpg", -1)
		self.image = pygame.transform.scale(self.image, (100, 100))
		self.rect = self.image.get_rect()
		self.ypos = 300
		self.xpos = 120
		self.rect.topleft = (self.xpos, self.ypos)
		self.is_dead = False
		
		# physics properties
		self.gravity = 0.5
		self.lift = 20
		self.velocity = 0
		self.air_resistance = 0.95

	def jump(self): 
		self.velocity -= self.lift		

	"""def did_collide(self): 
		if self.rect.colliderect():
			print("collision detected") 
			self.is_dead = True """

	def update(self): 
		# this funciton upadates all the values of the player's bird

		# update the birds position
		self.velocity += self.gravity
		self.velocity *= self.air_resistance
		newpos = self.rect.move(0, self.velocity)
		self.rect = newpos

		# check to make sure the bird isn't too low or too high
	
		if self.rect.top < 0: 
			newpos = self.rect.move(0, self.rect.top)
			self.velocity *= -0.85
		if self.rect.bottom > 640: 
			self.is_dead = True

		#check to make sure the player is alive
		#self.did_collide()



class Background(pygame.sprite.Sprite): 
	# This class creates a background object and loads the image into the game
	# Image: Asian Mountain Forest BG by Crisisworks 
	# URL: https://opengameart.org/content/asian-mountain-forest-bg
	def __init__(self, imageFile, location): 
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image(imageFile)
		self.rect = self.image.get_rect()
		self.rect.left, self.rect.top = location



def game_loop(): 


 
	player = Player()
	BackGround = Background("imageBackground.png", [0,0])	

	game_exit = False
	bird_sprite = pygame.sprite.RenderPlain((player))

	pipe_list = []
	pipe_list.append(Pipes(player))

	clock = pygame.time.Clock()

	while not game_exit: 
		# lock the game to 50 fps
		clock.tick(50)

		#Event Handling
		for event in pygame.event.get(): 
			# if the player is trying to quit
			if event.type == pygame.QUIT: 
				game_exit = True
			# exit if the player has died
			if player.is_dead == True: 
				game_exit = True
			# handle jumping 
			if event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_SPACE:
					if pipe_list[0].did_collide == False:  
						player.jump()

		if player.is_dead == True: 
				game_exit = True

		 
		 # space out the last element correctcly
		if pipe_list[-1].xpos < 20: 
			pipe_list.append(Pipes(player))
		if pipe_list[0].offscren(): 
			pipe_list.pop(0) 


		screen.blit(BackGround.image, BackGround.rect)

		bird_sprite.update()

		for each_pipe in pipe_list: 
			each_pipe.update()
			screen.blit(each_pipe.bottom_image, each_pipe.bottom_rect)
			screen.blit(each_pipe.top_image, each_pipe.top_rect)


		
		bird_sprite.draw(screen)
		pygame.display.update()

	pygame.quit()
	quit()

game_loop()