from classes import *
# classes imports:
#   from init import *
#   init imports:
#     import platform
#     import os
#     import swapcore
#     from swapcore.constants import *
#     import pygame
#     from pygame.constants import *


# ==============================================================================
# ============================= INSTANCES CREATION =============================
# ==============================================================================


font = swapcore.kernel.Font('../../data/swapfont.swptf')

toolbar = swapcore.kernel.Toolbar(
    PROGRAM_WIDTH,
    DEFAULT_TOOLBAR_HEIGHT,
    0,
    0,
    DEFAULT_TOOLBAR_BACKGROUND_COLOR,
    DEFAULT_TOOLBAR_OVER_PARAMETER_COLOR,
    DEFAULT_TOOLBAR_DEMARCATION_HEIGHT,
    DEFAULT_TOOLBAR_DEMARCATION_COLOR)

dock = swapcore.kernel.Dock(
    PROGRAM_WIDTH,
    DEFAULT_DOCK_HEIGHT,
    0,
    DEFAULT_TOOLBAR_HEIGHT,
    DEFAULT_DOCK_BACKGROUND_COLOR,
    DEFAULT_DOCK_FOCUS_APP_COLOR,
    DEFAULT_DOCK_OVER_APP_COLOR,
    DEFAULT_DOCK_DOWN_APP_COLOR,
    DEFAULT_DOCK_OPEN_LINE_APP_COLOR)

appmanager = swapcore.kernel.AppManager()
appmanager.set_desk(PROGRAM_WIDTH, PROGRAM_HEIGHT-toolbar.height-dock.height,
                    0, toolbar.height+dock.height)
appmanager.set_possible_coords(min_y=toolbar.height+dock.height)

app_map = AppMap(font, appmanager)
app_blocks = AppBlocks(font, appmanager)
app_properties = AppProperties(font, appmanager)
app_layers = AppLayers(font, appmanager)

make_links_between(app_map, app_blocks, app_properties, app_layers)

app_map.load_data()

appmanager.add_apps_to_queue(app_map, app_blocks, app_properties, app_layers)
# appmanager.add_apps_to_queue(app_map)
# appmanager.add_apps_to_queue(app_blocks)
# appmanager.add_apps_to_queue(app_properties)
# appmanager.add_apps_to_queue(app_layers)

dock.add_apps(
    [app_map, app_map.dock_icon],
    [app_blocks, app_blocks.dock_icon],
    [app_properties, app_properties.dock_icon],
    [app_layers, app_layers.dock_icon])


# ==============================================================================
# ================================= MAIN LOOP ==================================
# ==============================================================================

# unzip_data()
initialize_undo()

while RUNNING:
    # clock.tick(FPS)
    # pygame.display.set_caption(str(int(clock.get_fps())))
    focus = swapcore.kernel.App.app_specs[0]
    mx, my = pygame.mouse.get_pos()  # m: mouse
    keystate = pygame.key.get_pressed()
    mousestate = pygame.mouse.get_pressed()
    # key_mods = pygame.key.get_mods()
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
            break
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:  # left button
                appmanager.check_for_mouse_event(mx, my, MOUSEBUTTONDOWN, keystate)
                dock.check_for_mouse_event(mx, my, MOUSEBUTTONDOWN)
            elif event.button == 3:  # right button
                appmanager.check_for_mouse_event(mx, my, MOUSERIGHTBUTTONDOWN, keystate)
            elif event.button == 4:  # wheel up
                appmanager.check_for_mouse_event(mx, my, MOUSEWHEELUP, keystate)
            elif event.button == 5:  # wheel down
                appmanager.check_for_mouse_event(mx, my, MOUSEWHEELDOWN, keystate)
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:  # boutton gauche
                appmanager.check_for_mouse_event(mx, my, MOUSEBUTTONUP, keystate)
                dock.check_for_mouse_event(mx, my, MOUSEBUTTONUP)
            elif event.button == 3:  # right button
                appmanager.check_for_mouse_event(mx, my, MOUSERIGHTBUTTONUP, keystate)
        elif event.type == MOUSEMOTION:
            appmanager.check_for_mouse_event(mx, my, MOUSEMOTION, keystate)
            dock.check_for_mouse_event(mx, my, MOUSEMOTION)
        elif event.type == KEYDOWN:
            if focus.id:  # an app has the keyboard focus
                focus.keyboard_event(event, keystate, mx, my)
            if event.key == K_ESCAPE:
                RUNNING = False
                break
        elif event.type == KEYUP:
            if focus.id:  # an app has the keyboard focus
                focus.keyboard_event(event, keystate, mx, my)
    if focus.id:  # an app has the keyboard focus
        focus.keyboard_state(keystate, mx, my)
        focus.mouse_state(mousestate)
    # print(swapcore.kernel.App.app_specs[0].id)
    screen.fill(DEFAULT_DESK_COLOR)
    toolbar.draw_on(screen)
    dock.draw_on(screen)
    appmanager.draw_apps_on(screen)
    pygame.display.flip()

pygame.quit()
unload_undo()
# zip_data()

for spread in app_properties.spreads:
    spread.join()
