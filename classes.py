from init import *


# ===== constants =====


IMG_DIR = 'data/images'
SND_DIR = 'data/sounds'
img_dir = os.path.join(path.dirname(__file__), "data/images")
snd_dir = os.path.join(path.dirname(__file__), "data/sounds")

TILESIZE = 128

# images
player_lives1 = pygame.image.load(path.join(img_dir, "heart.png")).convert_alpha()
fond_text = pygame.image.load(path.join(img_dir, "frame.png")).convert_alpha()
Boss = pygame.image.load(path.join(img_dir, "329_00.png")).convert_alpha()
Boss1 = pygame.transform.scale(Boss, (128,128)).convert_alpha()
rock = pygame.image.load(path.join(img_dir, "rock.png")).convert_alpha()
rock1 = pygame.transform.scale(rock, (32,32)).convert_alpha()
player_lives = pygame.transform.scale(player_lives1, (64, 64)).convert_alpha()
player_Shieldlives1 = pygame.image.load(path.join(img_dir, "shield_heart.png")).convert_alpha()
player_Shieldlives = pygame.transform.scale(player_Shieldlives1, (64, 64)).convert_alpha()
arrow_img_base = pygame.image.load(path.join(img_dir, "arrow.png")).convert_alpha()
arrow_img = pygame.transform.scale(arrow_img_base, (64, 64)).convert_alpha()
player_bow = pygame.image.load(path.join(img_dir, "bow.png")).convert_alpha()
inventory_img = pygame.image.load(path.join(img_dir, "inventory.png")).convert_alpha()
idole1 = pygame.image.load(path.join(img_dir, "114_031.png")).convert_alpha()
idole2 = pygame.image.load(path.join(img_dir, "114_032.png")).convert_alpha()
idole3 = pygame.image.load(path.join(img_dir, "114_033.png")).convert_alpha()
idole_final = pygame.image.load(path.join(img_dir, "114_030.png")).convert_alpha()

font_name = swapcore.kernel.Font('data/swapfont.swptf')

#png text
text_1 = ["bonjour", "comment allez-vous ?", "moi ca va bien, merci"]
text_2 = ["je ne vous connais pas", "laissez moi !"]
text_3 = ["vous recherchez la montagne ?", "elle se situe au nord ouest.", "mais on raconte...","qu'elle est maudite !"]
text_4 = ["si j'etais vous", "j'eviterais de m'aventurer...","...dans la foret.", "quiconque y est rentre...","...n'est jamais revenu."]
text_5 = ["quel beau temps !"]
text_6 = ["dechaine mooooi !!!"]
text_7 = ["la", "baignoire", "est", "dans le sac", "je répète,", "la baignoire...","est dans le sac !!"]
text_8 = ["ma mere ma raconte"," une histoire un jour", "la legende d'un héro...", "qui se serait aventure"," dans un lieu...", "au sud ouest d'ici...","mais je n'ai jamais"," oser y mettre les pieds."]
text_9 = ["la legende de cette ile raconte...", "que si on derobe"," les 3 idoles sacrees,...", "un ancien s'abatrat sur l'île,...", "a partir des ruines"," situees au nord est...", "si le mal est combattu,", "l'ile sera libere de son fardeau"]
text_10 = ["est ce que tu aimes manger ?", "moi j'adore ca !", "d'ailleurs !", "10 kiwis pour 2 !","au lieu de 3.50 !", "affaire a saisir !", "...", "aah ca me jambe la gratte !"]
text_11 = ["on s'est fait berner !"," par les coquelicots !!!"]
text_12 = ["un jour,...","j'ai saute dans un trou","comme celui ci !", "depuis, je suis invincible!!!"]

TALK = {'17_170': text_12, '177_171': text_2, '232_140': text_10,
        '158_140': text_4, '154_169': text_1, '141_157': text_3,
        '196_155': text_8, '203_152': text_9, '135_155': text_7,
        '95_76': text_12, '283_112': text_6, '245_212': text_6, '215_196': text_5}


ORIGIN = (0, 0)
CENTER = (PROGRAM_WIDTH // 2, PROGRAM_HEIGHT // 2)

EVENTS = pygame.event.get()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (50, 50, 50)
SEMI_GREY = (20, 20, 20)

TRANSPARENT = (0, 0, 0, 0)
BACKGROUND = WHITE

ALPHA_MASK_COLOR = (255, 255, 255, 16)
DARK_MASK_COLOR = (0, 0, 0, 200)

# INVENTORY_FONT_COLOR = (242, 214, 192)  #(242, 214, 192)
INVENTORY_FONT_COLOR = (242, 224, 210)
INVENTORY_FONT_SHADOW_COLOR = (38, 17, 1)

NOTEBOOK_COLOR = (229, 221, 211)

MAP_SHIFT_INTERVAL = 0.25
MAP_SHIFT = 1  # in tilesize

PLAYER_ATTACK_DELAY = 0.3
PLAYER_ATTACK_THIRD = 0.1

# ===== classes =====


def use_potion(unicode, player):
    if unicode == 'f':  # potion de vie
        if player.inventory.data[1][0]:
            item, number = player.inventory.data[1][0]
            player.lives = min(player.lives+(1 if item == 3 else 3), 3)
            player.inventory.data[1][0][1] -= 1
            if not player.inventory.data[1][0][1]:
                player.inventory.data[1][0] = 0
                player.inventory.draw_data()
    elif unicode == 'g':  # potion de shield
        if player.inventory.data[1][1]:
            item, number = player.inventory.data[1][1]
            player.shield = min(player.shield+(1 if item == 4 else 3), 3)
            player.inventory.data[1][1][1] -= 1
            if not player.inventory.data[1][1][1]:
                player.inventory.data[1][1] = 0
                player.inventory.draw_data()

def draw_text(font_name, surf, text, size, x, y, color):
    # font = pygame.font.Font(font_name, size)
    text_surface = font_name.render(text, size, color)
    # text_surface = font.render(text, True, (BACKGROUND))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface, (x, y))

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        scaled = pygame.transform.scale(img,(64,64))
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(scaled, img_rect)
        x += 40

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
        draw_text(font_name, screen, "you died", 128, WIDTH//3, HEIGHT//5, BACKGROUND)
        draw_text(font_name, screen, "press echap to quit", 32, WIDTH//3, HEIGHT-HEIGHT//2, BACKGROUND)
        # draw_text(font_name, screen, "press r to respawn", 32, WIDTH//3, HEIGHT-HEIGHT//3, BACKGROUND)
        # draw_text(font_name, screen, "press t to title screen", 32, WIDTH//3, HEIGHT-HEIGHT//4, BACKGROUND)
        pygame.display.flip()

def talk_with_png(font_name, text):
    m = min(WIDTH, HEIGHT)
    x = int(m * 0.40)
    w = WIDTH - (2 * x)
    h = HEIGHT - (2 * x)
    text_screen = fond_text
    text_screen = pygame.transform.scale(text_screen, (w,h)).convert_alpha()
    text_surface = font_name.render(text[0], 27)
    text_screen.blit(text_surface, (w - 2*x, h//2-10))
    affichage = swapcore.kernel.Area(w - 2*x, h//2-10, 0, PROGRAM_HEIGHT*3//4)
    affichage.surface = text_screen
    affichage.x = PROGRAM_WIDTH // 2 - affichage.width // 2
    suiv = 1
    waiting = True
    while waiting:
        keystate = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                return False
            elif event.type == KEYDOWN and event.key == K_e:
                if suiv >= len(text):
                    waiting = False
                    break
                text_surface = font_name.render(text[suiv], 27)
                text_screen = fond_text
                text_screen = pygame.transform.scale(text_screen, (w,h)).convert_alpha()
                text_screen.blit(text_surface, (w - 2*x, h//2-10))
                affichage = swapcore.kernel.Area(w - 2*x, h//2-10, 0, PROGRAM_HEIGHT*3//4)
                affichage.surface = text_screen
                affichage.x = PROGRAM_WIDTH // 2 - affichage.width // 2
                suiv += 1
        screen.blit(affichage.surface, affichage.topleft)
        pygame.display.flip()
    return True

def store_data_to_file(filename, *data):
    with open(filename, 'wb') as file:
        for d in data:
            pickle.dump(d, file)

def load_data_from_file(filename, amount=None, index=0):
    loaded_data = []
    i = 0
    with open(filename, 'rb') as file:
        while amount is None or amount:
            try:
                if i < index:
                    i += 1
                    pickle.load(file)
                else:
                    loaded_data.append(pickle.load(file))
                    if amount is not None:
                        amount -= 1
            except EOFError:  # no more objects to load
                break
    if len(loaded_data) > 1:
        return loaded_data
    else:  # only one element, so return only it and not a list of 1 element
        return loaded_data[0]


        #     with open('playerpos.txt', 'r') as file:
        #         player.rect.x, player.rect.y, player.exp, player.lives, player.shield = [int(coord) for coord in file.readline().rstrip().split()]
        # except FileNotFoundError:
        #     pass

def store_all_data(pos, lives, shield, inventory, chests):
    with open('data/playerpos.txt', 'w') as file:
        file.write('%d %d %d %d' % (*pos, lives, shield))
    store_data_to_file('data/inventory', inventory)
    store_data_to_file('data/chests', chests)

def load_all_data():
    with open('data/playerpos.txt', 'r') as file:
        x, y, lives, shield = [int(saved) for saved in file.readline().rstrip().split()]
    inventory = load_data_from_file('data/inventory')
    chests = load_data_from_file('data/chests')
    return x, y, lives, shield, inventory, chests

def update_mode(mode, player, inventory, camera):
    if mode:  # continue
        x, y, lives, shield, inv, chests = load_all_data()
    else:  # new game
        x, y, lives, shield = 168, 168, 3, 0
        inv = [[0, 0, 0], [[3, 1], [4, 1], [5, 10]], [0, [7, 3], None]]
        chests = {'158_176': [[[1, 1], [2, 1], 0], [0, 0, 0], [0, 0, 0]]}
    player.lives = lives
    player.shield = shield
    inventory.data = inv
    inventory.draw_data()
    camera.visual_start = (x, y)
    camera.map, camera.visual_data = camera.get_map_from_data(camera.data, camera.visual_start)
    camera.chests = chests


class Title:
    def __init__(self, background, title, newgame, continuer, barre, centerx, centery):
        self.background = background
        self.zoom_w = self.background.get_width()
        self.zoom_h = self.background.get_height()
        self.zoom = pygame.transform.scale(self.background, (self.zoom_w*3,self.zoom_h*3))
        self.zoom_x = 0
        self.zoom_y = 0
        self.title = title
        self.title1 = self.title.get_rect()
        self.title1.x = centerx
        self.title1.y = centery
        self.speedx = 1
        self.velocity = [self.speedx, self.speedx]
        self.newgame = newgame
        self.continuer = continuer
        self.barre = pygame.transform.scale(barre, (200, 64))
        self.draw_bar = None
        self.check = False
        #self.menu = menu
        #self.title_snd = snd

    def update(self, screen):
        over = True
        pygame.mixer.music.load(os.path.join(SND_DIR, 'theme.mp3'))
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(loops = -1)
        while over:
            screen.blit(self.zoom, (self.zoom_x, self.zoom_y))
            screen.blit(self.title, (PROGRAM_WIDTH//4, PROGRAM_HEIGHT//6))
            self.background_moved()
            #self.surf.blit(self.new_bg, (0,0))
            events = pygame.event.get()
            for event in events:
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_r:
                    pygame.mixer.music.stop()
                    return True
            # if self.check == True:
            #     return True
            mode = self.menu(events)
            if mode is not None:
                return mode
            pygame.display.flip()
            #self.surf.blit(menu, (WIDTH-1/8*WIDTH, HEIGHT-1/8*WIDTH))
            #background_moved()

    def background_moved(self):
        self.zoom_x -= self.velocity[0]
        self.zoom_y -= self.velocity[1]
        if -self.zoom_x + self.zoom_w > self.zoom_w*3 or self.zoom_x >=0:
            self.velocity[0] = -self.velocity[0]
        if -self.zoom_y + self.zoom_h > self.zoom_h*3 or self.zoom_y >=0:
            self.velocity[1] = -self.velocity[1]

    def menu(self, events):
        menu = pygame.Surface((PROGRAM_WIDTH//4, PROGRAM_HEIGHT//3), SRCALPHA)
        menu.fill(DARK_MASK_COLOR)
        W = PROGRAM_WIDTH - 1/3*PROGRAM_HEIGHT
        H = PROGRAM_HEIGHT - 1/2*PROGRAM_HEIGHT
        screen.blit(menu, (W, H))
        self.newgame = pygame.transform.scale(self.newgame, (200 , 128))
        ng = swapcore.kernel.Rect(200, 128, W, H-60)  # ng: new game
        screen.blit(self.newgame, ng.topleft)
        ct = swapcore.kernel.Rect(200, 128, W-15, H)  # ct: continue
        screen.blit(pygame.transform.scale(self.continuer,(200,128)), ct.topleft)
        mx, my = pygame.mouse.get_pos()
        for event in events:
            if event.type == MOUSEMOTION:
                if not self.check:
                    if ng.left <= mx <= ng.right and ng.top <= my <= ng.bottom:
                        self.draw_bar = (W+20,H)
                    elif ct.left <= mx <= ct.right and ct.top <= my <= ct.bottom:
                        self.draw_bar = (W+15,H+60)

                    elif self.draw_bar:
                        self.draw_bar = None
            elif event.type == MOUSEBUTTONDOWN:
                # if not self.check:
                    # if (W+20<mx<W+180 or H+30<mx<H+60) and (H+30<my<H+60 or W+20<my<W+180):
                    # if ng.left <= mx <= ng.right and ng.top <= my <= ng.bottom:
                if self.draw_bar:
                        pygame.mixer.music.stop()
                        return 0 if self.draw_bar == (W+20,H) else 1
                        # self.check = True
                    # elif (W+20<mx<W+150 or H+90<mx<H+120) and (H+90<my<H+120 or W+20<my<W+150):
                        # pygame.mixer.music.stop()
                        # self.check = True
        if self.draw_bar:
            screen.blit(self.barre, self.draw_bar)


class jourNuit():
    def __init__(self):
        self.coords = (PROGRAM_WIDTH//2, PROGRAM_HEIGHT//2)
        self.rad = PROGRAM_HEIGHT//16
        self.rad_final = PROGRAM_HEIGHT//self.rad
        self.border = None  # au debut, pas de border
        self.time = time.time()
        self.night_time = None  # pas de nuit au debut
        self.night_start = 2
        self.steps = 12
        self.night_end_start = self.night_start + self.steps // 2
        self.day_time = None
        self.day_start = self.night_end_start + 40
        self.day_end_start = self.day_start + self.steps // 2
        self.time_one_day = 120

    def update(self, surface):
        if self.night_start <= time.time() - self.time <= self.night_end_start:
            self.commencer_nuit()
        elif self.day_start <= time.time() - self.time <= self.day_end_start:
            self.commencer_jour()
        if self.border:
            surface.blit(self.border, ORIGIN, special_flags=BLEND_MULT)
        if self.time_one_day < time.time() - self.time:
            self.time = time.time()
            self.night_time = None
            self.day_time = None

    def commencer_nuit(self):
        if not self.night_time:
            self.border = pygame.Surface((PROGRAM_WIDTH, PROGRAM_HEIGHT))
            self.rad_final = PROGRAM_HEIGHT
            self.border.fill(SEMI_GREY)
            pygame.draw.circle(self.border, WHITE, self.coords, self.rad_final)
            self.night_time = time.time()
        if int(2*time.time()) > int(2*self.night_time):
            #print(int(time.time()), int(self.night_time))
            self.border = pygame.Surface((PROGRAM_WIDTH, PROGRAM_HEIGHT))
            self.rad_final -= self.rad
            self.border.fill(SEMI_GREY)
            pygame.draw.circle(self.border, WHITE, self.coords, self.rad_final)
            self.night_time = time.time()

    def commencer_jour(self):
        if not self.day_time :
            self.day_time = time.time()
        if int(2*time.time()) > int(2*self.day_time):
            #print(int(time.time()), int(self.day_time))
            pygame.Surface((PROGRAM_WIDTH, PROGRAM_HEIGHT))
            self.rad_final += self.rad
            self.border.fill(SEMI_GREY)
            pygame.draw.circle(self.border, WHITE, self.coords, self.rad_final)
            self.day_time = time.time()
        #if (self.day_end_start + self.day_start) < (self.time - self.day_end_start):
        #   self.time = time.time()
        #   self.night_time = None
        #   self.day_time = time.time()


class Clock:
    def __init__(self, interval=0.5):
        self.last_call = time.time()
        self.last_average = 0
        self.interval = interval
        self.counter = 0
        self.average = 0
        self.string_average = '0'
        self.fps = 0
        self.dt = 0

    def update(self):
        self.update_dt()
        self.update_fps()

    def update_dt(self):
        self.dt = time.time() - self.last_call  # time between 2 calls
        self.last_call = time.time()  # reset last call
        self.counter += 1

    def update_fps(self):
        if self.dt:
            self.fps = 1 / self.dt
            if time.time() - self.last_average >= self.interval:
                self.average = self.counter / (time.time() - self.last_average)
                self.string_average = str(round(self.average))
                self.last_average = time.time()
                self.counter = 0


class Images:
    def __init__(self, img_dir):
        self.heart = pygame.image.load(os.path.join(img_dir, 'heart.png')).convert_alpha()
        self.shield_heart = pygame.image.load(os.path.join(img_dir, 'shield_heart.png')).convert_alpha()
        self.arrow = pygame.image.load(os.path.join(img_dir, 'arrow.png')).convert_alpha()
        self.bow = pygame.image.load(os.path.join(img_dir, 'bow.png')).convert_alpha()
        self.sword = pygame.image.load(os.path.join(img_dir, 'sword.png')).convert_alpha()
        self.inventory = pygame.image.load(os.path.join(img_dir, 'inventory.png')).convert_alpha()
        self.inventory_slot = pygame.image.load(os.path.join(img_dir, 'inventory_slot.png')).convert_alpha()
        self.healing_potion = pygame.image.load(os.path.join(img_dir, 'healing_potion.png')).convert_alpha()
        self.gold_healing_potion = pygame.image.load(os.path.join(img_dir, 'gold_healing_potion.png')).convert_alpha()
        self.shield_potion = pygame.image.load(os.path.join(img_dir, 'shield_potion.png')).convert_alpha()
        self.gold_shield_potion = pygame.image.load(os.path.join(img_dir, 'gold_shield_potion.png')).convert_alpha()
        self.gold_coin = pygame.image.load(os.path.join(img_dir, 'gold_coin.png')).convert_alpha()
        self.alchemist = pygame.image.load(os.path.join(img_dir, 'alchemist.png')).convert_alpha()
        self.alchemist_slot = pygame.image.load(os.path.join(img_dir, 'alchemist_slot.png')).convert_alpha()
        self.iron = pygame.image.load(os.path.join(img_dir, 'iron.png')).convert_alpha()
        self.notebook = pygame.image.load(os.path.join(img_dir, 'notebook.png')).convert_alpha()
        self.chest = pygame.image.load(os.path.join(img_dir, 'chest.png')).convert_alpha()
        self.chest_slot = pygame.image.load(os.path.join(img_dir, 'chest_slot.png')).convert_alpha()
        self.smith = pygame.image.load(os.path.join(img_dir, 'smith.png')).convert_alpha()
        self.smith_slot = pygame.image.load(os.path.join(img_dir, 'smith_slot.png')).convert_alpha()
        self.background = pygame.image.load(os.path.join(img_dir, 'background.png')).convert_alpha()
        self.title = pygame.image.load(os.path.join(img_dir, 'title.png')).convert_alpha()
        self.new_game = pygame.image.load(os.path.join(img_dir, '134_00.png')).convert_alpha()
        self.continuer = pygame.image.load(os.path.join(img_dir, '134_01.png')).convert_alpha()
        self.barre = pygame.image.load(os.path.join(img_dir, '134_03.png')).convert_alpha()


class Sounds:
    def __init__(self, snd_dir):
        self.shoot = pygame.mixer.Sound(os.path.join(snd_dir, 'shoot.ogg'))
        self.transition = pygame.mixer.Sound(os.path.join(SND_DIR, 'shoot_2.ogg'))


class Arrow(pygame.sprite.Sprite):
    all = []
    new_id = 0
    def __init__(self, x, y, camera):
        super().__init__()
        self.image = arrow_img
        self.rect = self.image.get_rect()
        # self.rect.bottom = y
        self.rect.centerx = x + TILESIZE // 2
        self.rect.centery = y + TILESIZE // 2
        self.speedy = -10
        self.speedx = 10
        self.camera = camera
        self.id = Arrow.new_id
        Arrow.new_id += 1
        Arrow.all.append(self)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if not (0 <= self.rect.right and self.rect.left <= PROGRAM_WIDTH and \
                0 <= self.rect.bottom and self.rect.top <= PROGRAM_HEIGHT):
            self.kill()
        else:
            cx, cy = self.camera.center
            x, y = self.rect.x - cx, self.rect.y - cy
            si = y // TILESIZE  # s: shift
            sj = x // TILESIZE
            j, i = self.camera.player.j + sj, self.camera.player.i + si
            # i, j = self.camera.player.get_neighboring_tiles(i, j)[self.camera.player.direction-1]
            zombie = self.camera.zombie_spawn.tile_is_zombie(i, j)
            if zombie:
                zombie.lives -= 2
                self.kill()
            if self.camera.tile_is_wall(i, j, False):
                self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def kill(self):
        dex = None
        for index, arrow in enumerate(Arrow.all):
            if arrow.id == self.id:
                dex = index
                break
        if dex is not None:
            Arrow.all.pop(dex)


class Player(swapcore.kernel.Area):
    def __init__(self, camera, inventory):
        self.camera = camera
        self.inventory = inventory
        self.i, self.j = len(camera.visual_data[0]) // 2, len(camera.visual_data[0][0]) // 2
        super().__init__(TILESIZE, TILESIZE, self.j*TILESIZE, self.i*TILESIZE)
        self.images =  [pygame.transform.scale(pygame.image.load(
            'data/player/788_%d0.png' % i).convert_alpha(), (TILESIZE, TILESIZE))
            for i in range(1, 5)]
        self._direction = 2
        self._surface = self.images[self.direction-1]
        camera.player = self
        camera.center = (CENTER[0] - self.width // 2, CENTER[1] - self.height // 2)
        camera.ncenter = (-self.x + camera.center[0], -self.y + camera.center[1])
        self.last_attack = 0
        self.attacking = 0
        self.animation = None  # when initialized: surface object
        self._lives = 3
        self.shield = 0
        self.respawn_point = self.camera.visual_start
        self.last_shot = 0
        self.shoot_delay = 0.5

    def update(self):
        if self.attacking:
            if time.time() - self.last_attack > PLAYER_ATTACK_DELAY:
                self.attacking = 0
            else:
                self.update_attack_animation()

    def shoot(self):
        if time.time() - self.last_shot >= self.shoot_delay:
            self.last_shot = time.time()
            arrow = Arrow(*self.camera.center, self.camera)
            # top bottom left right
            cx, cy = self.camera.center
            coords = cx + TILESIZE // 2, cy + TILESIZE // 2
            if self.direction == 1:  # haut
                arrow.speedy = -10
                arrow.speedx = 0
                arrow.rect.y += arrow.speedy
            elif self.direction == 4:  # droite
                arrow.image = pygame.transform.rotate(arrow_img, -90)
                arrow.rect = arrow.image.get_rect()
                arrow.rect.center = coords
                arrow.speedx = 10
                arrow.speedy = 0
                arrow.rect.x += arrow.speedx
            elif self.direction == 2:  # bas
                arrow.image = pygame.transform.rotate(arrow_img, 180)
                arrow.rect = arrow.image.get_rect()
                arrow.rect.center = coords
                arrow.speedy = 10
                arrow.speedx = 0
                arrow.rect.y += arrow.speedy
            elif self.direction == 3:  # gauche
                arrow.image = pygame.transform.rotate(arrow_img, 90)
                arrow.rect = arrow.image.get_rect()
                arrow.rect.center = coords
                arrow.speedx = -10
                arrow.speedy = 0
                arrow.rect.x += arrow.speedx

    def update_attack_animation(self):
        frame = round((time.time() - self.last_attack) / PLAYER_ATTACK_THIRD)
        if frame == 1:
            self._surface = self.animation
        else:
            self._surface = self.images[self.direction-1]

    def mouse_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # left button
                self.close_attack()
            elif event.button == 3:  # right button
                self.range_attack()

    def close_attack(self):
        if time.time() - self.last_attack > PLAYER_ATTACK_DELAY:
            weapon = self.inventory.data[0][0]
            zombie = self.camera.zombie_spawn.tile_is_zombie(
                *self.get_neighboring_tiles(self.i, self.j)[self.direction-1])
            if not weapon:  # fist
                self.attacking = 1
                self.animation = pygame.transform.scale(pygame.image.load(
                    'data/player/fist/788_%d%d.png' % (self.direction, random.randint(0, 1))).convert_alpha(),
                    (TILESIZE, TILESIZE))
            else:  # sword
                self.attacking = 2
                self.animation = pygame.Surface((TILESIZE, TILESIZE), SRCALPHA)
                self.animation.blit(self._surface, ORIGIN)
                sword = pygame.transform.scale(
                    pygame.image.load('data/images/sword.png').convert_alpha(),
                    (TILESIZE//2, TILESIZE//2))
                xbool = True if self.direction > 2 else False
                ybool = True if (self.direction == 2 or self.direction == 4) else False
                sword = pygame.transform.flip(sword, False, ybool)
                if xbool:
                    sword = pygame.transform.rotate(sword, 90)
                shift = self.width // 2 - sword.get_width() // 2
                self.animation.blit(sword, (shift, shift))
            if zombie:
                zombie.lives -= self.attacking
            self.last_attack = time.time()

    def range_attack(self):
        self.shoot()

    def get_image_from_chrono(self, chrono):
        pass
        # [pygame.transform.scale(pygame.image.load(
        #     'data/zombie/328_0%d.png' % i).convert_alpha(), (TILESIZE, TILESIZE))
        #     for i in range(4)]

    @staticmethod
    def get_neighboring_tiles(i, j):
        """
        order: top bottom left right to match self.direction indexes
        """
        return [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value != self.direction:
            self._direction = value
            self._surface = self.images[value-1]

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value
        if self.lives <= 0:
            self.lives = 3
            self.camera.zombie_spawn.zombies = []
            self.camera.visual_start = self.respawn_point
            self.camera.map, self.camera.visual_data = \
                self.camera.get_map_from_data(self.camera.data, self.camera.visual_start)


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = Boss1
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2
        self.rect.y = HEIGHT // 2
        self.speedy = 15
        self.speedx = 15
        self.rot = 0
        self.rot_speed = 8
        self.last_update = pygame.time.get_ticks()
        self.velocity = [self.speedx,self.speedy]
        self.i = 0

    def update(self):
        self.ricocher()
        #self.rotate()
        for i in range(self.i):
            if random.random() > 0.1:
                proj = Projectiles(self.rect.x, self.rect.y)
                all_sprites.add(proj)
                a_eviter.add(proj)
                self.i = 0

    def ricocher(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.x + self.rect.width > WIDTH or self.rect.x < 0:
            self.velocity[0] = -self.velocity[0]
            self.i = 1

        if self.rect.y + self.rect.width > HEIGHT or self.rect.y < 0:
            self.velocity[1] = -self.velocity[1]
            self.i = 1
        #pygame.draw.rect(screen, ((0,0,0)), [self.rect.x, self.rect.y, TILESIZE,TILESIZE])


class Projectiles(pygame.sprite.Sprite):
    def __init__(self, x, y) :
        pygame.sprite.Sprite.__init__(self)
        self.image = rock1
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        #kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()



class Idoles(pygame.sprite.Sprite):
    def __init__ (self):
       pygame.sprite.Sprite.__init__(self)
       self.idole1 = idole1
       self.idole1_rect = self.idole1.get_rect()
       self.idole1_rect.x = 10*TILESIZE
       self.idole1_rect.y = 10*TILESIZE
       self.idole1_id = 1
       self.idole2 = idole2
       self.idole2_rect = self.idole2.get_rect()
       self.idole2_rect.x = 15*TILESIZE
       self.idole2_rect.y = 15*TILESIZE
       self.idole2_id = 1
       self.idole3 = idole3
       self.idole3_rect = self.idole3.get_rect()
       self.idole3_rect.x = 20*TILESIZE
       self.idole3_rect.y = 20*TILESIZE
       self.idole3_id = 1
       self.idole_final = idole_final
       self.idoleF_rect = self.idole_final.get_rect()
       self.idoleF_rect.x = 10*TILESIZE
       self.idoleF_rect.y = 20*TILESIZE
       self.idoleF_id = 1
       self.nbr_idole = 0

    def update(self, player):
        verif1 = self.verif_bloc(self.idole1_rect.x,self.idole1_rect.y, player.rect.x, player.rect.y)
        verif2 = self.verif_bloc(self.idole2_rect.x,self.idole2_rect.y, player.rect.x, player.rect.y)
        verif3 = self.verif_bloc(self.idole3_rect.x,self.idole3_rect.y, player.rect.x, player.rect.y)
        if verif1 or verif2 or verif3:
            draw_text(font_name, screen, "press j to take it", 63, WIDTH//2, HEIGHT//4, BLACK)
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_j:
                    if verif1:
                        self.nbr_idole += self.idole1_id
                        self.idole1_id = 0
                        self.refresh()

                    elif verif2:
                        self.nbr_idole += self.idole2_id
                        self.idole2_id = 0
                        self.refresh()

                    elif verif3:
                        self.nbr_idole += self.idole3_id
                        self.idole3_id = 0
                        self.refresh()

                    print(self.nbr_idole)

        if self.nbr_idole == 3 and self.verif_bloc(self.idoleF_rect.x,self.idoleF_rect.y, player.rect.x, player.rect.y):
            self.refresh()
            draw_text(font_name, screen, "press l to invoc", 63, WIDTH//2, HEIGHT//4, BLACK)
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_l:
                    boss = Boss()
                    all_sprites.add(boss)
                    return

    def verif_bloc(self, x, y, player_x, player_y):
        return (x - 1 == player_x) or (x + 1 == player_x) or (x == player_x) or (y - 1 == player_y) or (y + 1 == player_y) or (y == player_y)

    def draw(self, surface):
        surface.blit(self.idole1, self.idole1_rect.topleft)
        surface.blit(self.idole2, self.idole2_rect.topleft)
        surface.blit(self.idole3, self.idole3_rect.topleft)
        surface.blit(self.idole_final, self.idoleF_rect.topleft)

    def refresh(self):
        all_sprites.update()
        screen.fill(BACKGROUND)
        draw_grid()
        all_sprites.draw(screen)



class Zombie(swapcore.kernel.Area):
    def __init__(self, x, y, player, camera, spawn):
        super().__init__(TILESIZE, TILESIZE, x, y)
        self.images = [pygame.transform.scale(pygame.image.load(
            'data/zombie/328_0%d.png' % i).convert_alpha(), (TILESIZE, TILESIZE))
            for i in range(4)]
        self._surface = self.images[1]
        self.last_move = time.time()
        self._last_direction = 0  # 0/2: x, 1/3: y
        self.repeat_move = 0.5
        # self.repeat_move = 0.01
        self.player = player
        self.camera = camera
        self.spawn = spawn
        self.reached = None
        self._lives = 3
        self.id = None  # initialized by zombie spawn
        self.timer = 0

    def follow(self):
        if time.time() - self.last_move < self.repeat_move:
            return
        if self.reached is not None:
            self.update_reached()
        if self.reached is None:
            px = self.player.x  # p: player
            py = self.player.y  # p: player
            width = (px - self.x)
            height = (py - self.y)
            self.last_move = time.time()
            if self.last_direction % 2 or not height or \
              (self.top_is_wall if height < 0 else self.bottom_is_wall):
                if width > 0 and not self.right_is_wall:
                        self.x += TILESIZE
                        self.last_direction = 0  # 0: x, right
                        return self.check_if_reached()
                elif width < 0 and not self.left_is_wall:
                    self.x -= TILESIZE
                    self.last_direction = 2  # 2: x, left
                    return self.check_if_reached()
                elif width:
                    if height >= 0 and not self.bottom_is_wall:
                        self.y += TILESIZE
                        self.last_direction = 1  # 1: y, bottom
                        return self.check_if_reached()
                    elif height <= 0 and not self.top_is_wall:
                        self.y -= TILESIZE
                        self.last_direction = 3  # 1: y, top
                        return self.check_if_reached()
            if not self.last_direction % 2 or not width or \
              (self.left_is_wall if width < 0 else self.right_is_wall):
                if height > 0 and not self.bottom_is_wall:
                    self.y += TILESIZE
                    self.last_direction = 1  # 1: y, bottom
                    return self.check_if_reached()
                elif height < 0 and not self.top_is_wall:
                    self.y -= TILESIZE
                    self.last_direction = 3  # 1: y, top
                    return self.check_if_reached()
                elif height:
                    if width >= 0 and not self.right_is_wall:
                        self.x += TILESIZE
                        self.last_direction = 0  # 0: x, right
                        return self.check_if_reached()
                    elif width <= 0 and not self.left_is_wall:
                        self.x -= TILESIZE
                        self.last_direction = 2  # 0: x, left
                        return self.check_if_reached()

    def attack(self):
        if time.time() - self.timer > 0.75:
            if self.player.shield <= 0:
                self.player.lives -= 1
            else:
                self.player.shield -= 1
            self.timer = time.time()

    def check_if_reached(self):
        for index, (i, j) in enumerate(self.get_neighboring_tiles(self.i, self.j)):
            if self.camera.tile_is_player(i, j):
                self.reached = index
                self.last_direction = index
                if not self.timer:
                    self.timer = time.time()
                return index

    def update_reached(self):
        updated = self.check_if_reached()
        if updated is None:
            self.reached = None
            self.timer = None
        else:
            self.attack()

    @staticmethod
    def get_neighboring_tiles(i, j):
        """
        order: right bottom left top to match self.images indexes
        """
        return [(i, j + 1), (i + 1, j), (i, j - 1), (i - 1, j)]

    @property
    def i(self):
        return self.y // self.camera.tilesize

    @property
    def j(self):
        return self.x // self.camera.tilesize

    @property
    def right_is_wall(self):
        return self.camera.tile_is_wall(self.i, self.j+1)

    @property
    def left_is_wall(self):
        return self.camera.tile_is_wall(self.i, self.j-1)

    @property
    def top_is_wall(self):
        return self.camera.tile_is_wall(self.i-1, self.j)

    @property
    def bottom_is_wall(self):
        return self.camera.tile_is_wall(self.i+1, self.j)

    @property
    def last_direction(self):
        return self._last_direction

    @last_direction.setter
    def last_direction(self, value):
        if value != self._last_direction:
            self._last_direction = value
            self._surface = self.images[value]

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value
        if self._lives <= 0:
            self.spawn.kill_zombie(self.id)


class ZombieSpawn:
    def __init__(self, player, camera):
        self.player = player
        self.camera = camera
        self.last_spawn = 0
        self.next_spawn = 0
        self.zombies = []
        camera.zombie_spawn = self
        self.new_id = 1

    def update(self):
        if time.time() - self.last_spawn >= self.next_spawn and not self.camera.in_house:
            self.spawn_new_zombie()
        for zombie in self.zombies:
            zombie.follow()

    def spawn_new_zombie(self):
        start = time.time()
        max_i, max_j = len(self.camera.visual_data[0]) - 1, len(self.camera.visual_data[0][0]) - 1
        forbidden_i = self.player.i - self.camera.vth // 2
        forbidden_max_i = self.player.i + self.camera.vth // 2
        forbidden_j = self.player.j - self.camera.vtw // 2
        forbidden_max_j = self.player.j + self.camera.vtw // 2
        i, j = random.randint(0, max_i), random.randint(0, max_j)
        while forbidden_i <= i <= forbidden_max_i or self.camera.tile_is_wall(i, j):
            i = random.randint(0, max_i)
            if time.time() - start > 0.5:
                return
        while forbidden_j <= j <= forbidden_max_j or self.camera.tile_is_wall(i, j):
            j = random.randint(0, max_j)
            if time.time() - start > 0.5:
                return
        self.zombies.append(Zombie(j*TILESIZE, i*TILESIZE, self.player, self.camera, self))
        self.zombies[-1].id = self.new_id
        self.new_id += 1
        self.last_spawn = time.time()
        self.next_spawn = random.randint(5, 10)

    def kill_zombie(self, id):
        index = None
        for dex, zombie in enumerate(self.zombies):
            if zombie.id == id:
                index = dex
        if index is not None:
            self.zombies.pop(index)
            gold = random.randint(1, 5)
            iron = random.randint(0, 1)
            if not self.player.inventory.data[1][2]:
                self.player.inventory.data[1][2] = [5, gold]
            else:
                self.player.inventory.data[1][2][1] += gold
            if not self.player.inventory.data[2][1]:
                self.player.inventory.data[2][1] = [7, iron]
            else:
                self.player.inventory.data[2][1][1] += iron
            self.player.inventory.draw_data()

    def draw_on(self, surface):
        x, y = self.camera.ncenter
        for zombie in self.zombies:
            surface.blit(zombie.surface, (x+zombie.x, y+zombie.y))

    def apply_shift(self, shiftx, shifty):
        for zombie in self.zombies:
            zombie.x += shiftx
            zombie.y += shifty

    def tile_is_zombie(self, i, j):
        for zombie in self.zombies:
            if i == zombie.i and j == zombie.j:
                return zombie
        return False

class GUI(swapcore.kernel.Area):
    def __init__(self, type, data, item_images, item_scale, font, fontcolor,
                 id, image, scale, slot, slot_scale, x, y):
        """
        type: 0: chest, 1: inventory, 2: shop
        data: list of rows and columns used to store the inventory items
        format: [[[item, number], [item, number], [item, number]], ...]
        empty row: [0, 0, 0]
        item_images: dict of correspondences between data id and real images (not scaled)
        self.holes: list of (i, j) coords slots that are not slots
        holes row: [None, None, None]
        """
        self.type = type
        self.scale = scale
        self.item_scale = item_scale
        width, height = image.get_width() * self.scale, image.get_height() * self.scale
        surface = pygame.Surface((width, height), SRCALPHA)
        surface.blit(pygame.transform.scale(image, (width, height)), ORIGIN)
        super().__init__(width, height, x, y, color=TRANSPARENT)
        self.surface = surface
        self.data = data if not self.type else data[0]
        self.item_position = None if self.type != 1 else data[1]
        self.recipes = None if self.type != 2 else data[1]
        self.item_images = item_images
        self.font, self.fontsize = font, font.height * slot_scale
        self.fontcolor = fontcolor
        self.font_bottomright = (14 * slot_scale, 14 * slot_scale)
        self.rows = len(self.data)
        self.columns = len(self.data[0])
        self.holes = self.get_holes_from_data(self.data)
        self.id = id
        self.mslot = None  # mslot: mouse slot
        # original: first slot x: 4px, y: 4px +9 px + 4px = 17px
        self.slot_scale = slot_scale # because slots are 16x16 surfaces
        slot_x, slot_y = 4 * self.slot_scale, 17 * self.slot_scale
        slot_width = 16 * self.slot_scale
        slot_surface = pygame.transform.scale(slot, (slot_width, slot_width))
        # slot is an empty slot at the coords of the first slot
        self.slot = swapcore.kernel.Area(slot_width, slot_width, slot_x, slot_y, slot_surface)
        self.slot_twidth = 18 * self.slot_scale  # t: total, 16 slot + 2 border
        self.alpha_mask = pygame.Surface((slot_width, slot_width), SRCALPHA)
        self.alpha_mask.fill(ALPHA_MASK_COLOR)
        self._opened = False
        self._linked = None  # can be another GUI object
        self.draw_data()

    def update(self, surface):
        if self.opened:
            surface.blit(self.surface, self.topleft)

    def mouse_event(self, event, mx, my):
        if event.type == MOUSEMOTION:
            self.update_mslot(mx, my)
        elif event.type == MOUSEBUTTONDOWN:
            self.perform_click_event()

    def update_mslot(self, mx, my):
        old_mslot = None
        if self.mouse_on_self(mx, my):
            # convert mouse to set origin to the first slot (x, y)
            mcx, mcy = mx - self.x - self.slot.x, my - self.y - self.slot.y
            if not self.mouse_on_border(mcx, mcy):
                i, j = mcy // self.slot_twidth, mcx // self.slot_twidth
                if self.are_slot_coords_valid(i, j):
                    coords = (self.slot.x + j * self.slot_twidth, self.slot.y + i * self.slot_twidth)
                    if not self.mslot or self.mslot[0] != coords:  # coords = (x, y)
                        self.surface.blit(self.alpha_mask, coords)
                        if self.mslot:
                            old_mslot = self.mslot
                        self.mslot = (coords, i, j)  # coords are in self coord system
        if old_mslot:  # mouse_tile has changed
            self.draw_item(*old_mslot)
        elif self.mslot and not self.mouse_on_slot(mx, my, *self.mslot[0]):
            self.draw_item(*self.mslot)
            self.mslot = None

    def perform_click_event(self):
        if self.mslot:  # mouse is on a slot
            if self.linked.type == 1:  # linked to inventory
                if self.type == 2:
                    self.update_shop()
                else:  # chest
                    self.return_item()
                    self.draw_data()
                    self.linked.draw_data()
            elif self.linked.type == 2:  # linked to a shop
                self.linked.update_purchase(self.mslot[1], self.mslot[2])
            elif self.linked.type == 0:  # linked to a chest
                self.send_item()

    def update_purchase(self, i, j):
        if self.linked.data[i][j]:
            item, number = self.linked.data[i][j]
            index = 1 if self.data[2][0] else 0
            if index and self.data[2][1]:
                return  # 2 items already in shop
            self.data[2][index] = [item, number]
            self.linked.data[i][j] = 0
            f = self.data[2][0][0]  # f: first
            self.update_recipe()
            self.draw_data()
            self.linked.draw_data()

    def update_recipe(self, draw=False):
        returned = None
        f = self.data[2][0][0] if self.data[2][0] else None# f: first
        s = self.data[2][1][0] if self.data[2][1] else None  # s: second
        string_recipe = '{}/{}'.format(f, s)
        try:
            recipe = self.recipes[string_recipe]
            # from now recipe is valid
            first, second, final, n = recipe  # n: number
            f_number = self.data[2][0][1] if f else 0 # f: first
            s_number = self.data[2][1][1] if s else 0 # s: second
            if first <= f_number and second <= s_number:  # enough item
                self.data[2][2] = [final, n]
                returned = [recipe, f, f_number, s, s_number]
            elif self.data[2][2]:  # remove final item if any
                self.data[2][2] = 0
        except KeyError:  # invalid recipe
            if self.data[2][2]:  # remove final item if any
                self.data[2][2] = 0
        if draw:
            self.draw_data()
            self.linked.draw_data()
        return returned

    def return_item(self, slot=None):
        i, j = slot if slot is not None else (self.mslot[1], self.mslot[2])
        if self.data[i][j]:
            item, number = self.data[i][j]
            k, l = self.linked.item_position[item]
            if self.linked.data[k][l]:
                self.linked.data[k][l][1] += number
            else:
                self.linked.data[k][l] = [item, number]
            self.data[i][j] = 0

    def send_item(self, slot=None):
        i, j = slot if slot is not None else (self.mslot[1], self.mslot[2])
        free, same, m, n = None, None, None, None
        if self.data[i][j]:
            item, number = self.data[i][j]
            for k, row in enumerate(self.linked.data):
                for l, column in enumerate(row):
                    if not column and not free:
                        free = (k, l)
                    elif column and column[0] == item:
                        same = (k, l)
            if same:
                m, n = same
            elif free:
                m, n = free
            if m is not None and n is not None:
                if self.linked.data[m][n]:
                    self.linked.data[m][n][1] += number
                else:
                    self.linked.data[m][n] = [item, number]
                self.data[i][j] = 0
            self.draw_data()
            self.linked.draw_data()

    def update_shop(self):
        _, i, j = self.mslot
        if j < 2:  # click on element, not final
            self.return_item()
        elif self.data[2][2]:  # click on final and final exists
            r = self.update_recipe()  # r: recipe
            if r:  # recipe valid
                recipe, f, f_number, s, s_number = r  # f: first, s: second
                first, second, final, n = recipe  # n: number
                f_remaining = f_number - first
                s_remaining = s_number - second
                f_pos, s_pos = None, None  # pos: position
                if f_remaining:  # we have to make sure that the player can get it back
                    f_pos = self.linked.item_position[f]
                if s_remaining:
                    s_pos = self.linked.item_position[s]
                try:
                    pos = self.linked.item_position[final]
                    # both remaining items and final can be placed:
                    if (final == f or pos != f_pos) and (final == s or pos != s_pos):
                        k, l = pos
                        if self.linked.data[k][l]:  # item already in inventory
                            self.linked.data[k][l][1] += n
                        else:  # item not in inventory, so add it
                            self.linked.data[k][l] = [final, n]
                        if f_remaining:  # we have to make sure that the player can get it back
                            self.data[2][0][1] = f_remaining
                        elif self.data[2][0]:
                            self.data[2][0] = 0
                        if s_remaining:
                            self.data[2][1][1] = s_remaining
                        elif self.data[2][1]:
                            self.data[2][1] = 0
                except KeyError:  # item can't be in inventory
                    pass
        self.update_recipe(True)

    def mouse_on_self(self, mx, my):
        return self.left <= mx <= self.right and self.top <= my <= self.bottom

    def mouse_on_slot(self, mx, my, cx, cy):  # cx, cy: slot x, y in self coord system
        x, y  = self.x + cx, self.y + cy
        return x <= mx <= x + self.slot.width and y <= my <= y + self.slot.width

    def mouse_on_border(self, mcx, mcy):  # c: origin converted to firt slot origin
        return mcx % self.slot_twidth > self.slot.width or mcy % self.slot_twidth > self.slot.height

    def are_slot_coords_valid(self, i, j):
        return 0 <= i < self.rows and 0 <= j < self.columns and (i, j) not in self.holes

    def draw_alpha_mask(self):
        if self.mslot:
            self.surface.blit(self.alpha_mask, self.mslot[0])

    def draw_number(self, number, x, y):
        """
        x, y: topleft of the slot
        """
        a, b = 15 * self.slot_scale, 15 * self.slot_scale
        shadow = self.font.render(str(number), self.fontsize, INVENTORY_FONT_SHADOW_COLOR)
        self.surface.blit(shadow, (x+a-shadow.get_width(), y+b-shadow.get_height()))
        surface = self.font.render(str(number), self.fontsize, INVENTORY_FONT_COLOR)
        fx, fy = self.font_bottomright  # f: font
        self.surface.blit(surface, (x+fx-surface.get_width(), y+fy-surface.get_height()))

    def draw_item(self, coords, i, j):
        self.surface.fill(self.color, (*coords, self.slot.width, self.slot.width))
        self.surface.blit(self.slot.surface, coords)
        if self.data[i][j]:
            image = self.item_images[self.data[i][j][0]]
            scaled = pygame.transform.scale(image,
                (image.get_width()*self.item_scale,
                image.get_height()*self.item_scale))
            self.surface.blit(scaled, coords)
            number = self.data[i][j][1]
            if number > 1:
                self.draw_number(number, *coords)

    def draw_data(self):
        for i, row in enumerate(self.data):
            for j, column in enumerate(row):
                if j is not None and self.are_slot_coords_valid(i, j):
                    coords = (self.slot.x + j * self.slot_twidth,
                              self.slot.y + i * self.slot_twidth)
                    self.draw_item(coords, i, j)
        self.draw_alpha_mask()

    def clear_mslot(self):
        if self.mslot:
            self.draw_item(*self.mslot)
            self.mslot = None

    def clear_shop(self):
        if self.type == 2:
            self.return_item((2, 0))
            self.return_item((2, 1))
            self.update_recipe(True)

    @property
    def opened(self):
        return self._opened

    @opened.setter
    def opened(self, value):
        self._opened = value
        if self._opened:
            self.update_mslot(*pygame.mouse.get_pos())
        else:
            self.clear_mslot()
            self.clear_shop()

    @property
    def linked(self):
        return self._linked

    @linked.setter
    def linked(self, value):
        self._linked = value
        if value is not None:
            value._linked = self

    @staticmethod
    def get_holes_from_data(data):
        holes = []
        for i, row in enumerate(data):
            for j, column in enumerate(row):
                if column is None:
                    holes.append((i, j))
        return holes


class NoteBook(swapcore.kernel.Area):
    def __init__(self, image, scale, color, font, fontsize, fontcolor, centerx, centery):
        self.scale = scale
        width, height = image.get_width() * self.scale, image.get_height() * self.scale
        surface = pygame.Surface((width, height), SRCALPHA)
        surface.blit(pygame.transform.scale(image, (width, height)), ORIGIN)
        x, y = centerx - width // 2, centery - height // 2
        super().__init__(width, height, x, y, color=color)
        self.surface = surface
        self.font = font
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self._opened = False
        self.data = ['', '', '', '', '', '', '', '', '', '']
        self.string_pos = (5 * self.scale, 2 * self.scale)  # pos of the first string
        self.string_len =  25 * self.scale
        self.focus_string = None
        self.line_height = 5 * self.scale
        self.line_number = 5

    def update(self, surface):
        if self.opened:
            surface.blit(self._surface, self.topleft)

    def mouse_event(self, event, mx, my):
        reset = True
        if event.type == MOUSEBUTTONDOWN:
            if self.mouse_on_self(mx, my):
                    x, y = self.string_pos
                    mcx, mcy = mx - self.x, my - self.y  # converted to notebook coord system
                    if x <= mcx <= self.width - x and y <= mcy <= y + len(self.data) / 2 * self.line_height:
                        mcsx, mcsy = mcx - x, mcy - y  # set origin to first string pos
                        line = mcsy // self.line_height
                        if mcx > self.width // 2:
                            line += 5
                        self.focus_string = line
                        reset = False
        if reset:
            self.clear()

    def update_focus_string(self, event):
        """
        should only be called if focus string exists
        """
        if event.unicode.isalnum() or event.unicode == ' ' or event.key == K_BACKSPACE:
            string = self.data[self.focus_string]
            if event.key == K_BACKSPACE:
                string = string[:-1]
                rendered = self.font.render(string if string else ' ', self.fontsize, self.fontcolor)
            else:
                rendered = self.font.render(string+event.unicode, self.fontsize, self.fontcolor)
                if rendered.get_width() <= self.string_len:
                    string += event.unicode
                else:
                    rendered = self.font.render(string, self.fontsize, self.fontcolor)
            self.data[self.focus_string] = string
            x = (self.string_pos[0] if self.focus_string < len(self.data) // 2 else \
                 self.width - self.string_pos[0] - self.string_len)
            y = self.string_pos[1] + self.line_height * (self.focus_string % (len(self.data) // 2)) \
                + 4 * self.scale - rendered.get_height()
            self._surface.fill(self.color, (x, y, self.string_len, rendered.get_height()))
            self._surface.blit(rendered, (x, y))
        elif event.key == K_RETURN:
            self.clear()

    def mouse_on_self(self, mx, my):
        return self.left <= mx <= self.right and self.top <= my <= self.bottom

    def clear(self):
        if self.focus_string is not None:
            self.focus_string = None

    @property
    def opened(self):
        return self._opened

    @opened.setter
    def opened(self, value):
        self._opened = value
        if not self._opened:
            self.clear()


class Camera:
    def __init__(self, data, id_to_path, tilesize, visual_start, images, chests, cwidth=13, cheight=8, csize=32):
        self.data = data
        self.id_to_path = id_to_path
        self.tilesize = tilesize
        self.scale = self.tilesize // 32
        self.visual_start = visual_start
        self.cwidth, self.cheight, self.csize = cwidth, cheight, csize  # c: chunk
        self.twidth, self.theight = cwidth * csize, cheight * csize  # t: tile
        self.vtw = PROGRAM_WIDTH // self.tilesize + 1  # rtw: visible tile width
        self.vth = PROGRAM_HEIGHT // self.tilesize + 1  # rtw: visible tile width
        self.map, self.visual_data = self.get_map_from_data(data, visual_start)
        self.shift_key = 0
        self.last_shift = 0
        self.zombie_spawn = None  # must be initialized during zombie spawn creation
        self.player = None  # must be initialized during player creation
        self.center, self.ncenter = None, None  # must be initialized during player creation
        self.in_house = None
        self.house_mask = None  # when initialized, its a surface object
        self.images = images
        self.chests = chests
        # self.center = (CENTER[0] - CENTER[0] % self.tilesize, CENTER[1] - CENTER[1] % self.tilesize)
        # self.ncenter = (-self.center[0], -self.center[1])  # n: negative

    def keyboard_event(self, event, keystate, notebook=None):
        if event.type == KEYDOWN:
            if event.unicode == 'e' and not notebook.opened:
                self.check_for_interactions()
            elif event.key == K_LEFT:
                self.shift_key = K_LEFT
            elif event.key == K_UP:
                self.shift_key = K_UP
            elif event.key == K_RIGHT:
                self.shift_key = K_RIGHT
            elif event.key == K_DOWN:
                self.shift_key = K_DOWN
        if event.type == KEYUP:
            if event.key != K_RIGHT and keystate[K_RIGHT]:
                self.shift_key = K_RIGHT
            elif event.key != K_DOWN and keystate[K_DOWN]:
                self.shift_key = K_DOWN
            elif event.key != K_LEFT and keystate[K_LEFT]:
                self.shift_key = K_LEFT
            elif event.key != K_UP and keystate[K_UP]:
                self.shift_key = K_UP

    def keyboard_state(self, keystate, notebook):
        if time.time() - self.last_shift > MAP_SHIFT_INTERVAL and \
          not (self.player.inventory.opened or notebook.opened):
            map_modified = False
            if keystate[K_RIGHT] and self.shift_key == K_RIGHT and \
              self.visual_start[0] + len(self.visual_data[0][0]) < \
              self.cwidth * len(self.data[0][0][1][0]):
                self.player.direction = 4
                if not self.tile_is_wall(self.player.i, self.player.j+1) and \
                  not self.player.attacking:
                    self.map.x -= MAP_SHIFT * self.tilesize
                    self.zombie_spawn.apply_shift(-self.tilesize, 0)
                    map_modified = True
            if keystate[K_DOWN] and self.shift_key == K_DOWN and \
              self.visual_start[1] + len(self.visual_data[0]) < \
              self.cheight * len(self.data[0][0][1]):
                self.player.direction = 2
                if not self.tile_is_wall(self.player.i+1, self.player.j) and \
                  not self.player.attacking:
                    self.map.y -= MAP_SHIFT * self.tilesize
                    self.zombie_spawn.apply_shift(0, -self.tilesize)
                    map_modified = True
            if keystate[K_LEFT] and self.shift_key == K_LEFT and self.visual_start[0]:
                self.player.direction = 3
                if not self.tile_is_wall(self.player.i, self.player.j-1) and \
                  not self.player.attacking:
                    self.map.x += MAP_SHIFT * self.tilesize
                    self.zombie_spawn.apply_shift(self.tilesize, 0)
                    map_modified = True
            if keystate[K_UP] and self.shift_key == K_UP and self.visual_start[1]:
                self.player.direction = 1
                if not self.tile_is_wall(self.player.i-1, self.player.j) and \
                  not self.player.attacking:
                    self.map.y += MAP_SHIFT * self.tilesize
                    self.zombie_spawn.apply_shift(0, self.tilesize)
                    map_modified = True
            if map_modified:
                self.last_shift = time.time()
                self.update_visual_data()
                self.update_visual()

    def tile_is_wall(self, i, j, entity=True):
        x, y = self.visual_start
        chunk_id, k, l = self.convert_y_x_to_chunk_id(i+y, j+x)
        key = '%d_%d' % (j+x, i+y)
        for layer_id in range(len(self.visual_data)):
            try:
                self.data[layer_id][chunk_id][0][key]['w']
                return True
            except KeyError:
                pass
        if entity and (self.tile_is_player(i, j) or self.zombie_spawn.tile_is_zombie(i, j)):
            return True
        return False

    def tile_is_player(self, i, j):
        return i == self.player.i and j == self.player.j

    def get_map_from_data(self, data, visual_start):
        max_tw = 2 * PROGRAM_WIDTH // self.tilesize  # tw: tile width
        max_th = 2 * PROGRAM_HEIGHT // self.tilesize  # th: tile height
        tw, th = min(self.twidth, max_tw), min(self.theight, max_th)
        map = swapcore.kernel.Area(tw*self.tilesize, th*self.tilesize, 0, 0)
        visual_data = self.get_visual_data_from_layer_tw_th(len(data), tw, th)
        self.load_visual_data_from_data(visual_data, visual_start, data)
        self.load_map_from_visual_data(map.surface, visual_data)
        return map, visual_data

    def load_visual_data_from_data(self, visual_data, visual_start, data):
        width, height = len(visual_data[0][0]), len(visual_data[0])
        x1, y1 = visual_start
        x2, y2 = x1 + width, y1 + height
        for layer_id in range(len(data)):
            x = x1
            while x < x2:
                y = y1
                while y < y2:
                    chunk_id, i, j = self.convert_y_x_to_chunk_id(y, x)
                    id = data[layer_id][chunk_id][1][i][j]
                    visual_data[layer_id][y-y1][x-x1] = id
                    y += 1
                x += 1

    def load_map_from_visual_data(self, map, visual_data):
        for layer_id, layer in enumerate(visual_data):
            for i, row in enumerate(layer):
                for j, column in enumerate(row):
                    self.draw_block(i, j, map, visual_data)

    def get_properties_from_layer_i_j(self, layer, i, j):
        x, y = self.visual_start
        chunk_id, k, l = self.convert_y_x_to_chunk_id(y+i, x+j)
        try:
            return self.data[layer][chunk_id][0]['%d_%d' % (x+j, y+i)]
        except KeyError:
            return {}

    def update_visual(self):
        for layer_id in range(len(self.visual_data)):
            properties = self.get_properties_from_layer_i_j(layer_id, self.player.i, self.player.j)
            for property in properties:
                if property == 'd':  # d: door
                    self.in_house = (self.visual_start[1] + self.player.i,
                                     self.visual_start[0] + self.player.j)
                    self.zombie_spawn.zombies = []
                if property == 'h':  # hole
                    self.visual_start = (4, 162)
                    self.map, self.visual_data = self.get_map_from_data(self.data, self.visual_start)
        if self.in_house:
            self.go_in_house()

    def go_in_house(self):
        if (self.visual_start[1] + self.player.i == self.in_house[0] + 1 and \
          self.visual_start[0] + self.player.j == self.in_house[1]):
            self.in_house = None
            self.house_mask = None
        else:
            surface = pygame.Surface((self.map.width, self.map.height))
            for i, row in enumerate(self.visual_data[0]):
                for j, column in enumerate(row):
                    properties = self.get_properties_from_layer_i_j(0, i, j)
                    try:
                        properties['g']  # g: ground
                        self.draw_block(i, j, surface, property='r')  # r: roof
                    except KeyError:
                        pass
            self.house_mask = surface

    def check_for_interactions(self):
        if self.player.inventory.opened and self.player.inventory.linked:
            self.player.inventory.opened = False
            self.player.inventory.linked.opened = False
            self.player.inventory.linked = None
            return
        if self.player.inventory.opened:
            return
        x, y = self.visual_start
        i, j = self.player.get_neighboring_tiles(self.player.i, self.player.j)[self.player.direction-1]
        for layer_id in range(len(self.visual_data)):
            properties = self.get_properties_from_layer_i_j(layer_id, i, j)
            for property in properties:
                if property == 'c':
                    self.player.inventory.linked = GUI(0,
                        self.chests['%d_%d' % (y+i, x+j)],
                        self.player.inventory.item_images, 4, self.player.inventory.font, INVENTORY_FONT_COLOR, 0,
                        self.images.chest, 8, self.images.chest_slot, 8,
                        self.player.inventory.x, self.player.inventory.y)
                    self.player.inventory.linked.x = \
                        PROGRAM_WIDTH - self.player.inventory.x - self.player.inventory.width
                    self.player.inventory.opened = True
                    self.player.inventory.linked.opened = True
                elif property == 't':
                    RUNNING = talk_with_png(font_name, TALK['%d_%d' % (x+j, y+i)])
                elif property == 's':
                    store_all_data(self.visual_start, self.player.lives,
                                   self.player.shield, self.player.inventory.data, self.chests)
                    self.player.respawn_point = self.visual_start
                elif property == 'a':
                    self.player.inventory.linked = self.alchemist
                    self.player.inventory.opened = True
                    self.player.inventory.linked.opened = True
                elif property == 'f':
                    self.player.inventory.linked = self.smith
                    self.player.inventory.opened = True
                    self.player.inventory.linked.opened = True

    def update_visual_data(self):
        start_x, start_y = self.visual_start
        tile_shift_width = self.map.x // self.tilesize
        map = pygame.Surface((self.map.width, self.map.height))
        map.blit(self.map.surface, (self.map.left, 0))
        data_to_save = []
        if tile_shift_width < 0:  # load right, save left
            for _ in range(-tile_shift_width):
                for layer_id in range(len(self.visual_data)):
                    j = start_x % self.csize
                    chunk_j = (start_x - j) // self.csize
                    # to load data:
                    new_x = start_x + len(self.visual_data[layer_id][0])
                    new_j = new_x % self.csize
                    new_chunk_j = (new_x - new_j) // self.csize
                    for row in range(len(self.visual_data[layer_id])):  # range(i)
                        current_y = start_y + row
                        i = current_y % self.csize
                        chunk_i = (current_y - i) // self.csize
                        chunk_id = chunk_i * self.cwidth + chunk_j
                        id = self.visual_data[layer_id][row].pop(0)
                        data_to_save.append([layer_id, chunk_id, i, j, id])
                        # to load data:
                        new_i = current_y % self.csize
                        new_chunk_i = (current_y - new_i) // self.csize
                        new_chunk_id = new_chunk_i * self.cwidth + new_chunk_j
                        new_id = self.data[layer_id][new_chunk_id][1][new_i][new_j]
                        self.visual_data[layer_id][row].append(new_id)
                        if new_id:
                            block = self.get_block_by_id(new_id)
                        else:
                            block = pygame.Surface((self.tilesize, self.tilesize), SRCALPHA)
                        x = (len(self.visual_data[layer_id][row]) - 1) * self.tilesize
                        y = row * self.tilesize
                        if not layer_id:
                            map.fill(BLACK, (x, y, self.tilesize, self.tilesize))
                        map.blit(block, (x, y))
                start_x += 1
        elif tile_shift_width > 0:  # load left, save right
            for _ in range(tile_shift_width):
                for layer_id in range(len(self.visual_data)):
                    end_x = start_x + len(self.visual_data[layer_id][0]) - 1
                    j = end_x % self.csize
                    chunk_j = (end_x - j) // self.csize
                    # to load data :
                    new_x = start_x - 1
                    new_j = new_x % self.csize
                    new_chunk_j = (new_x - new_j) // self.csize
                    for row in range(len(self.visual_data[layer_id])):  # range(i)
                        current_y = start_y + row
                        i = current_y % self.csize
                        chunk_i = (current_y - i) // self.csize
                        chunk_id = chunk_i * self.cwidth + chunk_j
                        id = self.visual_data[layer_id][row].pop()
                        data_to_save.append([layer_id, chunk_id, i, j, id])
                        # to load data:
                        new_i = current_y % self.csize
                        new_chunk_i = (current_y - new_i) // self.csize
                        new_chunk_id = new_chunk_i * self.cwidth + new_chunk_j
                        new_id = self.data[layer_id][new_chunk_id][1][new_i][new_j]
                        self.visual_data[layer_id][row].insert(0, new_id)
                        if new_id:
                            block = self.get_block_by_id(new_id)
                        else:
                            block = pygame.Surface((self.tilesize, self.tilesize), SRCALPHA)
                        y = row * self.tilesize
                        if not layer_id:
                            map.fill(BLACK, (0, y, self.tilesize, self.tilesize))
                        map.blit(block, (0, y))
                start_x -= 1
        self.save_data(data_to_save)
        tile_shift_height = self.map.y // self.tilesize
        save = map
        map = pygame.Surface((self.map.width, self.map.height))
        map.blit(save, (0, self.map.top))
        data_to_save = []
        if tile_shift_height < 0:  # load bottom, save top
            for _ in range(-tile_shift_height):
                for layer_id in range(len(self.visual_data)):
                    i = start_y % self.csize
                    chunk_i = (start_y - i) // self.csize
                    # to load data:
                    new_y = start_y + len(self.visual_data[layer_id])
                    new_i = new_y % self.csize
                    new_chunk_i = (new_y - new_i) // self.csize
                    self.visual_data[layer_id].append([])
                    for columns in range(len(self.visual_data[layer_id][0])):  # range(j)
                        current_x = start_x + columns
                        j = current_x % self.csize
                        chunk_j = (current_x - j) // self.csize
                        chunk_id = chunk_i * self.cwidth + chunk_j
                        id = self.visual_data[layer_id][0][columns]
                        data_to_save.append([layer_id, chunk_id, i, j, id])
                        # to load data:
                        new_j = current_x % self.csize
                        new_chunk_j = (current_x - new_j) // self.csize
                        new_chunk_id = new_chunk_i * self.cwidth + new_chunk_j
                        new_id = self.data[layer_id][new_chunk_id][1][new_i][new_j]
                        self.visual_data[layer_id][-1].append(new_id)
                        if new_id:
                            block = self.get_block_by_id(new_id)
                        else:
                            block = pygame.Surface((self.tilesize, self.tilesize), SRCALPHA)
                        x = columns * self.tilesize
                        y = (len(self.visual_data[layer_id]) - 2) * self.tilesize
                        # -2 because we created new empty list
                        if not layer_id:
                            map.fill(BLACK, (x, y, self.tilesize, self.tilesize))
                        map.blit(block, (x, y))
                    self.visual_data[layer_id].pop(0)
                start_y += 1
        elif tile_shift_height > 0:  # load top, save bottom
            for _ in range(tile_shift_height):
                for layer_id in range(len(self.visual_data)):
                    end_y = start_y + len(self.visual_data[layer_id]) - 1
                    i = end_y % self.csize
                    chunk_i = (end_y - i) // self.csize
                    # to load data :
                    new_y = start_y - 1  # -1 because start_y has not been incremented yet
                    new_i = new_y % self.csize
                    new_chunk_i = (new_y - new_i) // self.csize
                    self.visual_data[layer_id].insert(0, [])
                    for columns in range(len(self.visual_data[layer_id][1])):  # range(j)
                        current_x = start_x + columns
                        j = current_x % self.csize
                        chunk_j = (current_x - j) // self.csize
                        chunk_id = chunk_i * self.cwidth + chunk_j
                        id = self.visual_data[layer_id][-1][columns]
                        data_to_save.append([layer_id, chunk_id, i, j, id])
                        # to load data:
                        new_j = current_x % self.csize
                        new_chunk_j = (current_x - new_j) // self.csize
                        new_chunk_id = new_chunk_i * self.cwidth + new_chunk_j
                        new_id = self.data[layer_id][new_chunk_id][1][new_i][new_j]
                        self.visual_data[layer_id][0].append(new_id)
                        if new_id:
                            block = self.get_block_by_id(new_id)
                        else:
                            block = pygame.Surface((self.tilesize, self.tilesize), SRCALPHA)
                        x = columns * self.tilesize
                        if not layer_id:
                            map.fill(BLACK, (x, 0, self.tilesize, self.tilesize))
                        map.blit(block, (x, 0))
                    self.visual_data[layer_id].pop()
                start_y -= 1
        self.save_data(data_to_save)
        self.map.surface = map
        self.map.topleft = ORIGIN
        self.visual_start = start_x, start_y

    def save_data(self, data):
        for layer_id, chunk_id, i, j, id in data:
            self.data[layer_id][chunk_id][1][i][j] = id

    def get_block_by_id(self, id):
        path, i, j = self.id_to_path[id]
        path = path[6:]  # delete '../../'
        path = path.split('\\')
        p = ''
        for pa in path:
            p += pa + '/'
        path = p[:-1]
        i_scaled, j_scaled = i * self.tilesize, j * self.tilesize
        block = pygame.Surface((self.tilesize, self.tilesize), SRCALPHA)
        try:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(
                image, (image.get_width()*self.scale, image.get_height()*self.scale))
            block.blit(image, (-j_scaled, -i_scaled))
        except pygame.error:
            pass
        return block

    def draw_block(self, i, j, surface=None, visual_data=None, property=None):
        if surface is None:
            surface = self.map.surface
        i_scaled, j_scaled = i * self.tilesize, j * self.tilesize
        surface.fill(BLACK, (j_scaled, i_scaled, self.tilesize, self.tilesize))
        vdata = visual_data if visual_data is not None else self.visual_data
        for layer_id in range(len(vdata)):
            if property:
                properties = self.get_properties_from_layer_i_j(layer_id, i, j)
                try:
                    properties[property]
                    continue
                except KeyError:
                    pass
            id = vdata[layer_id][i][j]
            block = pygame.Surface((self.tilesize, self.tilesize), SRCALPHA)
            if id:
                path, k, l = self.id_to_path[id]
                path = path[6:]  # delete '../../'
                path = path.split('\\')
                p = ''
                for pa in path:
                    p += pa + '/'
                path = p[:-1]
                try:
                    image = pygame.image.load(path).convert_alpha()
                    image = pygame.transform.scale(
                        image, (image.get_width()*self.scale, image.get_height()*self.scale))
                    block.blit(image, (-l*self.tilesize, -k*self.tilesize))
                except pygame.error:  # image has been deleted
                    pass
            surface.blit(block, (j_scaled, i_scaled))

    def draw_on(self, surface):
        if self.in_house:
            surface.blit(self.house_mask, self.ncenter)
        else:
            surface.blit(self.map.surface, self.ncenter)
        self.zombie_spawn.draw_on(surface)
        surface.blit(self.player.surface, self.center)

    def convert_y_x_to_chunk_id(self, y, x):
        i = y % self.csize
        chunk_i = (y - i) // self.csize
        j = x % self.csize
        chunk_j = (x - j) // self.csize
        chunk_id = chunk_i * self.cwidth + chunk_j
        return chunk_id, i, j

    @staticmethod
    def get_visual_data_from_layer_tw_th(layer, tw, th):  # tw, th: tile width, height
        return [[[0 for _ in range(tw)] for _ in range(th)] for _ in range(layer)]
