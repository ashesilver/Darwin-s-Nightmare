from classes import *


# ===== instances creation =====


font = swapcore.kernel.Font('data/swapfont.swptf')
fontlite = swapcore.kernel.Font('data/swapfontlite.swptf', 5)
images = Images(IMG_DIR)
sounds = Sounds(SND_DIR)
clock = Clock()
# data = load_data_from_file('data/map.swptm')
data = load_data_from_file('swapeng/swapeng016/map.swptm', amount=1, index=5)
path_to_id, id_to_path = load_data_from_file('swapeng/swapeng016/map.swptm', amount=2, index=1)
dark_mask = pygame.Surface((PROGRAM_WIDTH, PROGRAM_HEIGHT), SRCALPHA)
dark_mask.fill(DARK_MASK_COLOR)

cycle = jourNuit()

title_screen = Title(images.background, images.title, images.new_game, images.continuer, images.barre, 0, 0)
title_on = True

if title_on == True:
    # if title_screen.check == True:
    #     title_screen.check = False
    mode = title_screen.update(screen)
    if mode:  # continue
        x, y, lives, shield, inv, chests = load_all_data()
    else:  # new game
        x, y, lives, shield = 168, 168, 3, 0
        inv = [[0, 0, 0], [[3, 1], [4, 1], [5, 10]], [0, [7, 3], None]]
        chests = {'158_176': [[[1, 1], [2, 1], 0], [0, 0, 0], [0, 0, 0]]}

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

# x, y, lives, shield, inv = load_all_data()
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
camera.alchemist = alchemist
camera.smith = smith

# 45: 3 * scale = 48 - 3 to fit font height (9):
notebook = NoteBook(images.notebook, 16, NOTEBOOK_COLOR, font, 45, BLACK,
                    PROGRAM_WIDTH//2, PROGRAM_HEIGHT//2)


# ===== main loop =====


while RUNNING:
    clock.update()
    keystate = pygame.key.get_pressed()
    # mousestate = pygame.mouse.get_pressed()
    mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
            zombie_spawn.zombies = []
            camera.check_for_interactions()
            camera.in_house = None
            camera.house_mask = None
            player.inventory.opened = False
            if player.inventory.linked:
                player.inventory.linked.opened = False
                player.inventory.linked = None
            update_mode(title_screen.update(screen), player, player.inventory, camera)
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
                elif event.unicode == 'f' or event.unicode == 'g':
                    use_potion(event.unicode, player)
                camera.keyboard_event(event, keystate, notebook)
        elif event.type == KEYUP:
            camera.keyboard_event(event, keystate)
    camera.keyboard_state(keystate, notebook)
    zombie_spawn.update()
    player.update()
    for arrow in Arrow.all:
        arrow.update()
    # =============
    screen.fill(BLACK)
    camera.draw_on(screen)
    for arrow in Arrow.all:
        arrow.draw(screen)
    if not camera.in_house:
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
    draw_lives(screen, 5, 5, player.shield, images.shield_heart)
    pygame.display.flip()

pygame.quit()
# store_all_data(camera.visual_start, player.lives, player.shield, inventory.data)
