import swapeng.swapeng016.swapcore as swapcore
import pygame
from pygame.constants import *
import random
import time
from os import path

img_dir = path.join(path.dirname(__file__), "data/images")
snd_dir = path.join(path.dirname(__file__), "data/sounds")

WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 32
GREY = (50,50,50)
WHITE = (255,255,255)
# DARK_BROWN = (87, 35, 7)
DARK_BROWN = (112, 53, 7)
BROWN = (150, 70, 7)
BACKGROUND = (255, 255, 255)
BLACK = (0,0,0)
GREY = (20,20,20)

ORIGIN = (0, 0)
TRANSPARENT = (0,0,0,0)
DEFAULT_ALPHA_MAK_COLOR = (255, 255, 255, 16)

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Darwin's Nightmare")
clock = pygame.time.Clock()
#font_name = pygame.font.match_font('arial')
font_name = swapcore.kernel.Font('data/swapfont.swptf')

# ========== DATA ==========

# images
player_lives1 = pygame.image.load(path.join(img_dir, "heart.png")).convert_alpha()
player_lives = pygame.transform.scale(player_lives1, (64, 64)).convert_alpha()
player_Shieldlives1 = pygame.image.load(path.join(img_dir, "shield_heart.png")).convert_alpha()
player_Shieldlives = pygame.transform.scale(player_Shieldlives1, (64, 64)).convert_alpha()
arrow_img_base = pygame.image.load(path.join(img_dir, "arrow.png")).convert_alpha()
arrow_img = pygame.transform.scale(arrow_img_base, (10,25)).convert_alpha()
player_bow = pygame.image.load(path.join(img_dir, "bow.png")).convert_alpha()
inventory_img = pygame.image.load(path.join(img_dir, "inventory.png")).convert_alpha()

# sounds
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Shoot.wav'))

# ==========================


#png text
text_1 = ["Bonjour", "Comment allez-vous ?", "Moi ça va bien, merci !"]

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
        x += 40

def shield(surf, x, y, shield, img):
    for i in range(shield):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
        x += 40

def newscreen(screen):
    scale = 128 // 16  # the real inventory image is equal to a tilesize of length 16
    scale_item = 128 // 32  # because items are 32x32 surfaces
    m = min(WIDTH, HEIGHT)  # m: min
    border = m // 16
    inventory = swapcore.kernel.Area(
        WIDTH-2*border, HEIGHT-2*border,
        border, border, color=TRANSPARENT)
    third = inventory.width // 3
    # player inventory coord system is in inventory coord system
    piw, pih = inventory_img.get_width() * scale, inventory_img.get_height() * scale
    player_inventory = swapcore.kernel.Area(piw, pih, 0, 0, color=TRANSPARENT)
    player_inventory.surface = pygame.Surface((inventory.width, inventory.height), SRCALPHA)
    player_inventory.surface.blit(pygame.transform.scale(inventory_img, (piw, pih)), ORIGIN)
    # chest inventory coord system is in inventory coord system
    chest_inventory = swapcore.kernel.Area(piw, pih, 0, 0, color=BROWN)
    chest_inventory.x = inventory.width - chest_inventory.width
    chest_inventory.surface = pygame.Surface((inventory.width, inventory.height), SRCALPHA)
    chest_inventory.surface.blit(pygame.transform.scale(inventory_img, (piw, pih)), ORIGIN)
    # drawings
    inventory.surface = pygame.Surface((inventory.width, inventory.height), SRCALPHA)
    inventory.surface.blit(player_inventory.surface, player_inventory.topleft)
    inventory.surface.blit(chest_inventory.surface, chest_inventory.topleft)
    # maths
    # original: first case x: 4px, y: 4px +9 px + 4px = 17px
    case_x, case_y = 4 * scale, 17 * scale
    case_width = 16 * scale  # 16 case + 2 border
    case_total_width = 18 * scale  # 16 case + 2 border
    case_surface = pygame.Surface((case_width, case_width))
    case_surface.blit(player_inventory.surface, (-case_x, -case_y))
    case = swapcore.kernel.Area(case_width, case_width, case_x, case_y, case_surface)
    # item
    scaled_bow = pygame.transform.scale(
        player_bow, (player_bow.get_width()*scale_item, player_bow.get_height()*scale_item))
    items = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    for i, obj in enumerate(items):
        for j, item in enumerate(obj):
            if item == 1:  # bow
                inventory.surface.blit(
                    scaled_bow, (case.x+j*case_total_width, case.y+i*case_total_width))
    chest = [[0, 0, 0], [0, 0, 0], [0, 1, 0]]
    # alpha mask
    alpha_mask = pygame.Surface((case_width, case_width), SRCALPHA)
    alpha_mask.fill(DEFAULT_ALPHA_MAK_COLOR)

    waiting = True
    mouse_tile = None
    while waiting:
        clock.tick(FPS)
        keystate = pygame.key.get_pressed()
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                return False
            elif event.type == KEYDOWN and event.key == K_i:
                waiting = False
            elif event.type == MOUSEBUTTONDOWN:
                if mouse_tile:
                    (x, y), i, j, id = mouse_tile
                    if not id:  # mouse_tile on player inventory
                        item = items[i][j]  # get mouse_tile item
                        if item:
                            items[i][j] = 0  # remove item from player inventory
                            i, j = 0, 0
                            while chest[i][j] and i < 3:  # get first free space in chest
                                j += 1
                                if j > 2:  # new row
                                    i+= 1
                                    j = 0
                            chest[i][j] = item  # move item to chest
                            inventory.surface.blit(
                                scaled_bow,
                                (chest_inventory.x+case.x+j*case_total_width,
                                 chest_inventory.y+case.y+i*case_total_width))
            elif event.type == MOUSEMOTION:
                # mouse converted to inventory coord system
                mcx, mcy = mx - inventory.x, my - inventory.y
                mouse_tile = check_for_mouse_tile(
                    mcx, mcy, mouse_tile, case, case_total_width, alpha_mask, inventory,
                    player_inventory, chest_inventory)
        screen.blit(inventory.surface, inventory.topleft)
        pygame.display.flip()
    return True

def mouse_on_case(mcx, mcy, cx, cy, case_width):  # mc: converted to inventory coord system
    return cx <= mcx <= cx + case_width and cy <= mcy <= cy + case_width  # cx: case x

def check_for_mouse_tile(mcx, mcy, mouse_tile, case, case_total_width, alpha_mask, inventory, *subinventory):
    """
    mcx, mcy: mouse coords converted to inventory coord system
    """
    old = None
    for index, sub in enumerate(subinventory):
        if 0 <= mcx <= sub.width and 0 <= mcy <= sub.height:
            # convert again to subinventory coord system
            mcsx, mcsy = mcx - sub.x - case.x, mcy - sub.y - case.y  # s: sub(inventory)
            on_border = mcsx % case_total_width > case.width or mcsy % case_total_width > case.height
            if not on_border:
                j, i = mcsx // case_total_width, mcsy // case_total_width
                if 0 <= j <= 2 and 0 <= i <= 2:  # not (j == i == 2)
                    x, y = sub.x + case.x + j * case_total_width, sub.y + case.y + i * case_total_width
                    if not mouse_tile or mouse_tile[0] != (x, y):
                        inventory.surface.blit(alpha_mask, (x, y))
                        if mouse_tile:
                            old = mouse_tile[0]
                        mouse_tile = ((x, y), i, j, index)  # in inventory coord system
        if old:  # mouse_tile has changed
            inventory.surface.blit(case.surface, old)
        elif mouse_tile and not mouse_on_case(mcx, mcy, *mouse_tile[0], case.width):
            inventory.surface.blit(case.surface, mouse_tile[0])
            mouse_tile = None
    return mouse_tile

class Chest(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((TILESIZE,TILESIZE))
		self.image.fill((0,0,255))
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x*TILESIZE
		self.rect.y = y*TILESIZE

	#def update(self):
	#	screen.blit(self.image, (self.rect.x, self.rect.y))

def draw_text(font_name, surf, text, size, x, y):
	# font = pygame.font.Font(font_name, size)
	text_surface = font_name.render(text, size, BACKGROUND)
	# text_surface = font.render(text, True, (BACKGROUND))
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x,y)
	surf.blit(text_surface, (x, y))

def draw_grid():
    for x in range(0, WIDTH, TILESIZE):
        pygame.draw.line(screen, ((102,102,102)), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pygame.draw.line(screen, ((102,102,102)), (0, y), (WIDTH, y))

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = player_bow
		self.bow_image = player_bow
		#self.image.fill((255,0,0))
		self.rect = self.image.get_rect()
		self.rect.x = 10*TILESIZE
		self.rect.y = 10*TILESIZE
		self.lives = 3
		self.max_lives = 3
		self.shield = 3
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		self.last_lives = pygame.time.get_ticks()
		self.last_move = 0
		self.repeat = 0.2
		self.blocs = {}
		self.dir = 1
		self.exp = 0

	def move(self, keystate, blocs):
		if time.time() - self.last_move >= self.repeat:
			keystate = pygame.key.get_pressed()
			if keystate[pygame.K_RIGHT]:
				try:
					blocs["%d_%d" % (self.rect.x + TILESIZE, self.rect.y)]
				except KeyError:
					self.image = pygame.transform.rotate(self.bow_image, -90)
					self.dir = 2
					self.rect.x += TILESIZE
					self.last_move = time.time()
			elif keystate[pygame.K_LEFT]:
				try:
					blocs["%d_%d" % (self.rect.x - TILESIZE, self.rect.y)]
				except KeyError:
					self.image = pygame.transform.rotate(self.bow_image, 90)
					self.dir = 4
					self.rect.x -= TILESIZE
					self.last_move = time.time()
			elif keystate[pygame.K_UP]:
				try:
					blocs["%d_%d" % (self.rect.x, self.rect.y - TILESIZE)]
				except KeyError:
					self.image = self.bow_image
					self.dir = 1
					self.rect.y -= TILESIZE
					self.last_move = time.time()
			elif keystate[pygame.K_DOWN]:
				try:
					blocs["%d_%d" % (self.rect.x, self.rect.y + TILESIZE)]
				except KeyError:
					self.image = pygame.transform.rotate(self.bow_image, 180)
					self.dir = 3
					self.rect.y += TILESIZE
					self.last_move = time.time()
			elif keystate[pygame.K_SPACE]:
				self.shoot()
			elif keystate[pygame.K_p]:
				now = pygame.time.get_ticks()
				if now - self.last_lives > self.shoot_delay:
					self.last_lives = now
					if self.shield > 0:
						self.shield -= 1
						return
					else:
						self.lives >= 0
						self.lives -= 1
						return
				#if self.lives == 0:
					#gameover_screen(screen)

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			shoot_sound.play()
			arrow = Arrow(self.rect.centerx, self.rect.centery)
			all_sprites.add(arrow)
			arrows.add(arrow)

			if self.dir == 1:  # haut
				self.image = self.bow_image
				arrow.speedy = -10
				arrow.speedx = 0
				arrow.rect.y += arrow.speedy
			elif self.dir == 2:  # droite
				arrow.image = pygame.transform.rotate(arrow_img, -90)
				self.image = pygame.transform.rotate(self.bow_image, -90)
				arrow.rect = arrow.image.get_rect()
				arrow.rect.center = self.rect.center
				arrow.speedx = 10
				arrow.speedy = 0
				arrow.rect.x += arrow.speedx
			elif self.dir == 3:  # bas
				arrow.image = pygame.transform.rotate(arrow_img, 180)
				self.image = pygame.transform.rotate(self.bow_image, 180)
				arrow.rect = arrow.image.get_rect()
				arrow.rect.center = self.rect.center
				arrow.speedy = 10
				arrow.speedx = 0
				arrow.rect.y += arrow.speedy
			elif self.dir == 4:  # gauche
				arrow.image = pygame.transform.rotate(arrow_img, 90)
				self.image = pygame.transform.rotate(self.bow_image, 90)
				arrow.rect = arrow.image.get_rect()
				arrow.rect.center = self.rect.center
				arrow.speedx = -10
				arrow.speedy = 0
				arrow.rect.x += arrow.speedx

	def update(self):
		keys = pygame.key.get_pressed()
		self.move(keys, self.blocs)
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        pygame.sprite.Sprite.__init__(self)
        self.image = arrow_img
        self.rect = self.image.get_rect()
        # self.rect.bottom = y
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = -10
        self.speedx = 10

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.bottom < 0:
            self.kill()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((TILESIZE,TILESIZE))
        self.image.fill((25,123,75))
        self.rect = self.image.get_rect()
        self.rect.x = x*TILESIZE
        self.rect.y = y*TILESIZE
        self.last_move = time.time()
        self.last_direction = 0  # 0: x, 1: y
        self.repeat_move = 0.3
        self.timer = None

    def follow(self):
        if time.time() - self.last_move < self.repeat_move:
            return
        px = player.rect.x  # p: player
        py = player.rect.y  # p: player
        width = (px - self.rect.x)
        height = (py - self.rect.y)
        if (self.last_direction or not height) and width:
            if width > 0:
                self.rect.x += TILESIZE
            else:
                self.rect.x -= TILESIZE
            self.last_direction = 0  # 0: x
        elif height:
            if height > 0:
                self.rect.y += TILESIZE
            else:
                self.rect.y -= TILESIZE
            self.last_direction = 1  # 1: y
        self.last_move = time.time()

    def update(self):
    	self.follow()
    	if self.rect.x > WIDTH or self.rect.x < 0 or self.rect.y > HEIGHT or self.rect.y < 0:
    		self.kill()

    def attack(self):
    	if not self.timer:
    		self.timer = time.time()
    	elif 0.75 <= time.time() - self.timer:
    		if player.shield <= 0:
    			player.lives -= 1
    		else:
    			player.shield -= 1
    		self.timer = time.time()

class Boss(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_orig = pygame.Surface((TILESIZE,TILESIZE))
		self.image_orig.fill((25,12,175))
		self.image_orig = pygame.transform.scale(self.image_orig, (128,128)).convert_alpha()
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - TILESIZE)
		self.rect.y = random.randrange(HEIGHT - TILESIZE)
		self.speedy = random.randrange(-150, 150)
		self.speedx = random.randrange(-150,150)
		self.rot = 0
		self.rot_speed = random.randrange(-8,8)
		self.last_update = pygame.time.get_ticks()
		self.velocity = [self.speedx,self.speedy]

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			self.rot = (self.rot + self.rot_speed) % 360
			new_image = pygame.transform.rotate(self.image_orig, self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		self.ricocher()
		self.rotate()

	def ricocher(self):
		self.rect.x += self.velocity[0]
		self.rect.y += self.velocity[1]
		if self.rect.x + self.rect.width > WIDTH or self.rect.x < 0:
			self.velocity[0] = -self.velocity[0]
		if self.rect.y + self.rect.width > HEIGHT or self.rect.y < 0:
			self.velocity[1] = -self.velocity[1]
		pygame.draw.rect(screen, ((0,0,0)), [self.rect.x, self.rect.y, TILESIZE,TILESIZE])

def newmob(x, y):
    m = Mob(x, y)
    all_sprites.add(m)
    mobs.add(m)

def gameover_screen():
	pass

def spawn_boss():
	pass

def respawn_point(player, mode=0):
	"""
	mode: 0: load, 1: save
	"""
	if not mode:
		try:
			with open('playerpos.txt', 'r') as file:
				player.rect.x, player.rect.y, player.exp, player.lives, player.shield = [int(coord) for coord in file.readline().rstrip().split()]
		except FileNotFoundError:
			pass
	else:
		with open('playerpos.txt', 'w') as file:
			file.write('%d %d %d %d %d' % (player.rect.x, player.rect.y, player.exp, player.lives, player.shield))

def upgrade_with_props(player):
	pass

def gameover_screen(screen, player):
	over = True
	while over:
		screen.fill(BLACK)
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				return False
			elif event.type == KEYDOWN and event.key == K_r:
				cycle.time = time.time()
				return True
			elif event.type == KEYDOWN and event.key == K_t:
				cycle.time = time.time()
				title_screen(screen, player)
		draw_text(font_name, screen, "you died", 128, WIDTH//2, HEIGHT//5)
		draw_text(font_name, screen, "press echap to quit", 32, WIDTH//2, HEIGHT-HEIGHT//2)
		draw_text(font_name, screen, "press r to respawn", 32, WIDTH//2, HEIGHT-HEIGHT//3)
		draw_text(font_name, screen, "press t to titlte screen", 32, WIDTH//2, HEIGHT-HEIGHT//4)
		pygame.display.flip()

def title_screen(screen, player):
	over = True
	while over:
		screen.fill(BLACK)
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				return False
			elif event.type == KEYDOWN and event.key == K_r:
				cycle.time = time.time()
				if player.lives == 0:
					player.lives = player.max_lives
					return True
				else:
					return True
		draw_text(font_name, screen, "darwin s nightmare", 128, WIDTH//2, HEIGHT//5)
		draw_text(font_name, screen, "press echap to quit", 32, WIDTH//2, HEIGHT-HEIGHT//2)
		draw_text(font_name, screen, "press r to start", 32, WIDTH//2, HEIGHT-HEIGHT//3)
		pygame.display.flip()

def talk_with_png(font_name, text):
	m = min(WIDTH, HEIGHT)
	x = int(m * 0.40)
	w = WIDTH - (2 * x)
	h = HEIGHT - (2 * x)
	text_screen = pygame.Surface((w,h))
	text_screen.fill((100,100,100))
	# font = pygame.font.Font(font_name, 15)
	# text_surface = font.render(text[0], True, ((0,0,0)))
	text_surface = font_name.render(text[0], 18)
	text_screen.blit(text_surface, (w//2 - x//2 + TILESIZE, h//2))
	suiv = 1
	waiting = True
	while waiting:
		clock.tick(FPS)
		keystate = pygame.key.get_pressed()
		for event in pygame.event.get():
			if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
				return False
			elif event.type == KEYDOWN and event.key == K_SPACE:
				if suiv >= len(text):
					waiting = False
					break
				text_surface = font_name.render(text[suiv], 18)
				text_screen.fill((100, 100, 100))
				text_screen.blit(text_surface, (w//2 - x//2 + TILESIZE, h//2))
				suiv += 1

		screen.blit(text_screen, (x, HEIGHT - 7 * TILESIZE, w, h))
		pygame.display.flip()
	return True

def trouDeMerde(player):
	player.x = 0
	player.y = 0
	print("Tu l'a dans le cul ! ;) <3")
	respawn_point(player, 1)

#def nuitDeMerde():
#	shift = HEIGHT//2
#	coords = (WIDTH//2, HEIGHT//2)
#	border_right = pygame.Surface((WIDTH, HEIGHT))
#	border_right.fill(GREY)
#	pygame.draw.circle(border_right, WHITE, coords, HEIGHT//2 + shift)
#	return border_right

class jourNuit():
	def __init__(self):
		self.coords = (WIDTH//2, HEIGHT//2)
		self.rad = HEIGHT//16
		self.rad_final = HEIGHT//self.rad
		self.border = None  # au debut, pas de border
		self.time = time.time()
		self.night_time = None  # pas de nuit au debut
		self.night_start = 2
		self.steps = 12
		self.night_end_start = self.night_start + self.steps // 2
		self.day_time = time.time()
		self.day_start = self.night_end_start + 6
		self.day_end_start = self.day_start + self.steps // 2
        self.one_day_time = 0

	def update(self, surface):
		if self.night_start <= time.time() - self.time <= self.night_end_start:
			self.commencer_nuit()
		elif self.day_start <= time.time() - self.time <= self.day_end_start:
			self.commencer_jour()
		if self.border:
			surface.blit(self.border, ORIGIN, special_flags=BLEND_MULT)

	def commencer_nuit(self):
		if not self.night_time:
			self.border = pygame.Surface((WIDTH, HEIGHT))
			self.rad_final = HEIGHT
			self.border.fill(GREY)
			pygame.draw.circle(self.border, WHITE, self.coords, self.rad_final)
			self.night_time = time.time()
		if int(2*time.time()) > int(2*self.night_time):
			#print(int(time.time()), int(self.night_time))
			self.rad_final -= self.rad
			self.border.fill(GREY)
			pygame.draw.circle(self.border, WHITE, self.coords, self.rad_final)
			self.night_time = time.time()

	def commencer_jour(self):
		if int(2*time.time()) > int(2*self.day_time):
			#print(int(time.time()), int(self.day_time))
			self.rad_final += self.rad
			self.border.fill(GREY)
			pygame.draw.circle(self.border, WHITE, self.coords, self.rad_final)
			self.day_time = time.time()
		#if (self.day_end_start + self.day_start) < (self.time - self.day_end_start):
		#	self.time = time.time()
		#	self.night_time = None
		#	self.day_time = time.time()

all_sprites = pygame.sprite.Group()
arrows = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
#border = nuitDeMerde()
cycle = jourNuit()
respawn_point(player)
boss = Boss()
chest1 = Chest(8,11)
chest4 = Chest(6,6)
chest3 = Chest(2,9)
chest2 = Chest(13,15)
all_sprites.add(player)
#all_sprites.add(boss)
all_sprites.add(chest1)
newmob(12, 2)
player.blocs["%d_%d" % (chest1.x*TILESIZE, chest1.y*TILESIZE)] = 0

titleScreen = True
running = True
while running:
	clock.tick(FPS)
	if titleScreen:
		running = title_screen(screen, player)
		titleScreen = False
	for event in pygame.event.get():
		if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
			running = False
		elif event.type == KEYDOWN and event.key == K_i:
			mask = pygame.Surface((WIDTH, HEIGHT), SRCALPHA)
			mask.fill((0, 0, 0, 200))
			screen.blit(mask, (0, 0))
			draw_text(font_name, screen, "inventory", 64, WIDTH//2, 5)
			running = newscreen(screen)
		elif event.type == KEYDOWN and event.key == K_e:
			running = talk_with_png(font_name, text_1)
		elif event.type == KEYDOWN and event.key == K_s:
			respawn_point(player, 1)
	hits = pygame.sprite.groupcollide(mobs, arrows, True, True)
	for hit in hits:
		player.exp += 1
		newmob(12, 2)
	if player.lives == 0:
		running = gameover_screen(screen, player)
		if running:
			player.lives = player.max_lives

	hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_rect)
	timer = time.time()
	for hit in hits:
		hit.attack()

	all_sprites.update()
	screen.fill(BACKGROUND)
	draw_grid()
	all_sprites.draw(screen)
	#screen.blit(border, ORIGIN, special_flags=BLEND_MULT)
	cycle.update(screen)
	draw_lives(screen, 5, 5, player.lives, player_lives)
	shield(screen, 5, 5, player.shield, player_Shieldlives)
	pygame.display.flip()

pygame.quit()
