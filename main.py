from classes import *


# ===== instances creation =====


font = swapcore.kernel.Font('data/swapfont.swptf')
fontlite = swapcore.kernel.Font('data/swapfontlite.swptf', 5)
images = Images(IMG_DIR)
sounds = Sounds(SND_DIR)
clock = Clock()
# data = load_data_from_file('data/map.swptm')
data = load_data_from_file('swapeng/swapeng016/map.swptm', amount=1, index=5)
path_to_id, id_to_path = load_data_from_file('data/path.swptm')
dark_mask = pygame.Surface((PROGRAM_WIDTH, PROGRAM_HEIGHT), SRCALPHA)
dark_mask.fill(DARK_MASK_COLOR)

cycle = jourNuit()
chests = {'158_176': [[0, 0, 0], [0, 0, 0], [0, 0, 0]]}


title_screen = Title(images.background, images.title, images.new_game, images.continuer, images.barre, 0, 0)
title_on = True

if title_on == True:
    # if title_screen.check == True:
    #     title_screen.check = False
    mode = title_screen.update(screen)


items_images = {
    1: images.sword,
    2: images.bow,
    3: images.healing_potion,
    4: images.shield_potion,
    5: images.gold_coin,
    7: images.iron,
    8: images.gold_healing_potion,
    9: images.gold_shield_potion}

border = min(PROGRAM_WIDTH, PROGRAM_HEIGHT) // 16


x, y, lives, shield, inv = load_all_data()

# [[[1, 1], 0, 0], [[3, 1], [4, 1], [5, 10]], [0, [7, 13], None]]
inventory = GUI(1,
    [inv,
     {1: (0, 0), 2: (0, 1), 3: (1, 0), 4: (1, 1),
      5: (1, 2), 7: (2, 1), 8: (1, 0), 9: (1, 1)}],
    items_images, 4, fontlite, INVENTORY_FONT_COLOR, 0,
    images.inventory, 8, images.inventory_slot, 8, border, border)

alchemist = GUI(2,
    [[[None, None, None], [None, None, None], [0, 0, 0]],
     {'5/None':(20, 0, 3, 1), '4/7':(1, 5, 9, 1)}],
    items_images, 4, fontlite, INVENTORY_FONT_COLOR, 0,
    images.alchemist, 2, images.alchemist_slot, 8, border, border)
alchemist.x = PROGRAM_WIDTH - border - alchemist.width

smith = GUI(2,
    [[[None, None, None], [None, None, None], [0, 0, 0]],
     {'5/None':(30, 0, 4, 1), '4/7':(1, 1, 4, 1), '3/5':(1, 60, 8, 1), '4/5':(1, 60, 9, 1)}],
    items_images, 4, fontlite, INVENTORY_FONT_COLOR, 0,
    images.smith, 2, images.smith_slot, 8, border, border)
smith.x = PROGRAM_WIDTH - border - smith.width


del border
# (90, 92)
camera = Camera(data, id_to_path, TILESIZE, (x, y), images, chests)  #(174, 174) (201, 186)(90, 92)(196, 152)
player = Player(camera, inventory)
player.lives = lives
player.shield = shield
zombie_spawn = ZombieSpawn(player, camera)

# player = Player()
# respawn_point(player)
# boss = Boss()
# chest1 = Chest(8,11)
# chest4 = Chest(6,6)
# chest3 = Chest(2,9)
# chest2 = Chest(13,15)
# newmob(12, 2)
# player.blocs["%d_%d" % (chest1.x*TILESIZE, chest1.y*TILESIZE)] = 0

# 45: 3 * scale = 48 - 3 to fit font height (9):
notebook = NoteBook(images.notebook, 16, NOTEBOOK_COLOR, font, 45, BLACK,
                    PROGRAM_WIDTH//2, PROGRAM_HEIGHT//2)

all_sprites = pygame.sprite.Group()
arrows = pygame.sprite.Group()
a_eviter = pygame.sprite.Group()
respawn_point(player)
idole = Idoles()

# ===== main loop =====


while RUNNING:
    clock.update()
    keystate = pygame.key.get_pressed()
    # mousestate = pygame.mouse.get_pressed()
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            RUNNING = False
        elif event.type == KEYDOWN and event.key == K_r:
            # if title_screen.check == True:
            #     title_screen.check = False
            RUNNING = title_screen.update(screen)
        elif event.type == KEYDOWN and event.key == K_t:
            running = talk_with_png(font_name, text_12  )
        # ======================
        elif event.type == MOUSEMOTION:
            if inventory.opened:
                inventory.mouse_event(event, mx, my)
                if inventory.linked:
                    inventory.linked.mouse_event(event, mx, my)
        elif event.type == MOUSEBUTTONDOWN:
            if inventory.opened and inventory.linked:
                inventory.mouse_event(event, mx, my)
                inventory.linked.mouse_event(event, mx, my)
            elif notebook.opened:
                notebook.mouse_event(event, mx, my)
            else:
                player.mouse_event(event)
        elif event.type == KEYDOWN:
            if notebook.focus_string is not None:
                notebook.update_focus_string(event)
            else:
                if event.unicode == 'n' and not inventory.opened:
                    notebook.opened = not notebook.opened
                elif event.unicode == 'i' and not notebook.opened and not inventory.linked:
                    inventory.opened = not inventory.opened
                camera.keyboard_event(event, keystate, notebook)
        elif event.type == KEYUP:
            camera.keyboard_event(event, keystate)
    camera.keyboard_state(keystate, notebook)
    zombie_spawn.update()
    player.update()
    # ==========
    # hits = pygame.sprite.groupcollide(mobs, arrows, True, True)
    # for hit in hits:
    #     player.exp += 1
    #     #newmob(12, 2)
    # if player.lives == 0:
    #     running = gameover_screen(screen, player)
    #     if running:
    #         player.lives = player.max_lives

    # hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_rect)
    # timer = time.time()
    # for hit in hits:
    #     hit.attack()
    # all_sprites.update()
    # idole.update(player)
    idole.draw(screen)
    # =============
    screen.fill(BLACK)
    camera.draw_on(screen)
    cycle.update(screen)
    if inventory.opened or notebook.opened:
        screen.blit(dark_mask, ORIGIN)
        if inventory.opened:
            inventory.update(screen)
            if inventory.linked:
                inventory.linked.update(screen)
        else:
            notebook.update(screen)
    draw_lives(screen, 5, 5, player.lives, images.heart)
    # shield(screen, 5, 5, player.shield, images.shield_heart)
    pygame.display.flip()

pygame.quit()
store_all_data(camera.visual_start, player.lives, player.shield, inventory.data)
