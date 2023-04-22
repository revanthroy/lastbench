import pygame
import random
import button

pygame.init()

clock = pygame.time.Clock()
fps = 60


#game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

# Set up the display
screen1 = pygame.display.set_mode((400, 300))
pygame.display.set_caption('User Details')

# load the background image for user details
background_image2 = pygame.image.load("Background/background.png").convert_alpha()


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle')



#define game variables
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 15
attack = False
potion = False
potion_effect = 15
clicked = False
game_over = 0


#define fonts
font = pygame.font.SysFont('Times New Roman', 26)
font = pygame.font.Font(None, 30)

#define colours
red = (255, 0, 0)
green = (0, 255, 0)

#load images
#background image
background_img = pygame.image.load('Background/background.png').convert_alpha()
#panel image
panel_img = pygame.image.load('Icons/panel.png').convert_alpha()
#button images
potion_img = pygame.image.load('Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('Icons/restart.png').convert_alpha()
#load victory and defeat images
victory_img = pygame.image.load('Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('Icons/defeat.png').convert_alpha()
#sword image
sword_img = pygame.image.load('Icons/sword.png').convert_alpha()


#create function for drawing text
def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	screen.blit(img, (x, y))


#function for drawing background
def draw_bg():
	screen.blit(background_img, (0, 0))

#function for drawing background user details
def draw_bg_user_details():
	screen1.blit(background_image2, (0, 0))

#function for drawing panel
def draw_panel():
	#draw panel rectangle
	screen.blit(panel_img, (0, screen_height - bottom_panel))
	#show knight stats
	draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
	for count, i in enumerate(bandit_list):
		#show name and health
		draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel + 10) + count * 60)

# Get username input
username = ""
username_input = ""
username_active = False
username_rect = pygame.Rect(325, 65, 200, 30)

# Get age input
age = ""
age_input = ""
age_active = False
age_rect = pygame.Rect(300, 145, 200, 30)

# Get Email input
Email = ""
Email_input = ""
Email_active = False
Email_rect = pygame.Rect(300, 190, 200, 30)


# Main game loop
running = True
while running:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if username input is active
            if username_rect.collidepoint(event.pos):
                username_active = True
            else:
                username_active = False
            # Check if age input is active
            if age_rect.collidepoint(event.pos):
                age_active = True
            else:
                age_active = False
            # Check if age input is active
            if Email_rect.collidepoint(event.pos):
                Email_active = True
            else:
                Email_active = False
               
        if event.type == pygame.KEYDOWN:
            if username_active:
                if event.unicode.isalpha() or event.unicode == " ":
                    username_input += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    username_input = username_input[:-1]
            if age_active:
                if event.unicode.isnumeric():
                    age_input += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    age_input = age_input[:-1]
            if Email_active:
                if event.unicode.isalpha() or event.unicode == " ":
                    Email_input += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    Email_input = Email_input[:-1]       
                if event.unicode.isnumeric():
                    Email_input += event.unicode
                if event.key == pygame.K_BACKSPACE:
                    Email_input = Email_input[:-1]
                
    # Render text
    username_text = font.render("Enter your username:", True, (0, 0, 0))
    age_text = font.render("Enter your age:", True, (0, 0, 0))
    Email_text = font.render("Enter your Email:", True, (0, 0, 0))
    username_surface = font.render(username_input, True, (0, 0, 0))
    age_surface = font.render(age_input, True, (0, 0, 0))
    Email_surface = font.render(Email_input, True, (0, 0, 0))

    
    # Draw to screen
    screen1.fill((255, 255, 255))
    screen1.blit(username_text, (100, 70))
    screen1.blit(age_text, (100, 150))
    screen1.blit(Email_text, (100, 200))
    pygame.draw.rect(screen1, (200, 0, 0), username_rect, 2)
    pygame.draw.rect(screen1, (200, 0, 0), age_rect, 2)
    pygame.draw.rect(screen1, (200, 0, 0), Email_rect, 2)
    screen1.blit(username_surface, (327,68))
    screen1.blit(age_surface, (302, 148))
    screen1.blit(Email_surface, (300, 192))
    pygame.display.update()
    
    
#fighter class
class Fighter():
	def __init__(self, x, y, name, max_hp, strength, potions):
		self.name = name
		self.max_hp = max_hp
		self.hp = max_hp
		self.strength = strength
		self.start_potions = potions
		self.potions = potions
		self.alive = True
		self.animation_list = []
		self.frame_index = 0
		self.action = 0#0:idle, 1:attack, 2:hurt, 3:dead
		self.update_time = pygame.time.get_ticks()
		#load idle images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'{self.name}/Idle/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load attack images
		temp_list = []
		for i in range(8):
			img = pygame.image.load(f'{self.name}/Attack/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load hurt images
		temp_list = []
		for i in range(3):
			img = pygame.image.load(f'{self.name}/Hurt/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		#load death images
		temp_list = []
		for i in range(10):
			img = pygame.image.load(f'{self.name}/Death/{i}.png')
			img = pygame.transform.scale(img, (img.get_width() * 3, img.get_height() * 3))
			temp_list.append(img)
		self.animation_list.append(temp_list)
		self.image = self.animation_list[self.action][self.frame_index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)


	def update(self):
		animation_cooldown = 100
		#handle animation
		#update image
		self.image = self.animation_list[self.action][self.frame_index]
		#check if enough time has passed since the last update
		if pygame.time.get_ticks() - self.update_time > animation_cooldown:
			self.update_time = pygame.time.get_ticks()
			self.frame_index += 1
		#if the animation has run out then reset back to the start
		if self.frame_index >= len(self.animation_list[self.action]):
			if self.action == 3:
				self.frame_index = len(self.animation_list[self.action]) - 1
			else:
				self.idle()


	
	def idle(self):
		#set variables to idle animation
		self.action = 0
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()


	def attack(self, target):
		#deal damage to enemy
		rand = random.randint(-5, 5)
		damage = self.strength + rand
		target.hp -= damage
		#run enemy hurt animation
		target.hurt()
		#check if target has died
		if target.hp < 1:
			target.hp = 0
			target.alive = False
			target.death()
		damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
		damage_text_group.add(damage_text)
		#set variables to attack animation
		self.action = 1
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def hurt(self):
		#set variables to hurt animation
		self.action = 2
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()

	def death(self):
		#set variables to death animation
		self.action = 3
		self.frame_index = 0
		self.update_time = pygame.time.get_ticks()


	def reset (self):
		self.alive = True
		self.potions = self.start_potions
		self.hp = self.max_hp
		self.frame_index = 0
		self.action = 0
		self.update_time = pygame.time.get_ticks()


	def draw(self):
		screen.blit(self.image, self.rect)



class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp


	def draw(self, hp):
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))



class DamageText(pygame.sprite.Sprite):
	def __init__(self, x, y, damage, colour):
		pygame.sprite.Sprite.__init__(self)
		self.image = font.render(damage, True, colour)
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.counter = 0


	def update(self):
		#move damage text up
		self.rect.y -= 1
		#delete the text after a few seconds
		self.counter += 1
		if self.counter > 30:
			self.kill()



damage_text_group = pygame.sprite.Group()


knight = Fighter(200, 260, 'Knight', 40, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

#create buttons
potion_button = button.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = button.Button(screen, 330, 120, restart_img, 120, 30)

run = True
while run:

	clock.tick(fps)

	#draw background
	draw_bg()

	#draw panel
	draw_panel()
	knight_health_bar.draw(knight.hp)
	bandit1_health_bar.draw(bandit1.hp)
	bandit2_health_bar.draw(bandit2.hp)

	#draw fighters
	knight.update()
	knight.draw()
	for bandit in bandit_list:
		bandit.update()
		bandit.draw()

	#draw the damage text
	damage_text_group.update()
	damage_text_group.draw(screen)

	#control player actions
	#reset action variables
	attack = False
	potion = False
	target = None
	#make sure mouse is visible
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	for count, bandit in enumerate(bandit_list):
		if bandit.rect.collidepoint(pos):
			#hide mouse
			pygame.mouse.set_visible(False)
			#show sword in place of mouse cursor
			screen.blit(sword_img, pos)
			if clicked == True and bandit.alive == True:
				attack = True
				target = bandit_list[count]
	if potion_button.draw():
		potion = True
	#show number of potions remaining
	draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)


	if game_over == 0:
		#player action
		if knight.alive == True:
			if current_fighter == 1:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					#look for player action
					#attack
                    
					if attack == True and target != None:
						knight.attack(target)
						current_fighter += 1
						action_cooldown = 0
					#potion
					if potion == True:
						if knight.potions > 0:
							#check if the potion would heal the player beyond max health
							if knight.max_hp - knight.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = knight.max_hp - knight.hp
							knight.hp += heal_amount
							knight.potions -= 1
							damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
							damage_text_group.add(damage_text)
							current_fighter += 1
							action_cooldown = 0
		else:
			game_over = -1


		#enemy action
		for count, bandit in enumerate(bandit_list):
			if current_fighter == 2 + count:
				if bandit.alive == True:
					action_cooldown += 1
					if action_cooldown >= action_wait_time:
						#check if bandit needs to heal first
						if (bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
							#check if the potion would heal the bandit beyond max health
							if bandit.max_hp - bandit.hp > potion_effect:
								heal_amount = potion_effect
							else:
								heal_amount = bandit.max_hp - bandit.hp
							bandit.hp += heal_amount
							bandit.potions -= 1
							damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
							damage_text_group.add(damage_text)
							current_fighter += 1
							action_cooldown = 0
						#attack
						else:
							bandit.attack(knight)
							current_fighter += 1
							action_cooldown = 0
				else:
					current_fighter += 1

		#if all fighters have had a turn then reset
		if current_fighter > total_fighters:
			current_fighter = 1


	#check if all bandits are dead
	alive_bandits = 0
	for bandit in bandit_list:
		if bandit.alive == True:
			alive_bandits += 1
	if alive_bandits == 0:
		game_over = 1


	#check if game is over
	if game_over != 0:
		if game_over == 1:
			screen.blit(victory_img, (250, 50))
		if game_over == -1:
			screen.blit(defeat_img, (290, 50))
		if restart_button.draw():
			knight.reset()
			for bandit in bandit_list:
				bandit.reset()
			current_fighter = 1
			action_cooldown
			game_over = 0



	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else:
			clicked = False

	pygame.display.update()

pygame.quit()

# Get user details
print(f"Username: {username_input}")
print(f"Age: {age_input}")