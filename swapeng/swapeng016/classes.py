from init import *
# init imports:
#   import platform
#   import os
#   import swapcore
#   from swapcore.constants import *
#   import pygame
#   from pygame.constants import *


# CONSTANTS


MOUSEWHEELUP = 7
MOUSEWHEELDOWN = 8
MOUSERIGHTBUTTONDOWN = 9
MOUSERIGHTBUTTONUP = 10

DEFAULT_GREEN = (89, 238, 133)
DEFAULT_GREEN_OVER = (178, 247, 198)
DEFAULT_GREEN_DOWN = (21, 208, 76)

DEFAULT_YELLOW = (242, 242, 116)
DEFAULT_YELLOW_OVER = (250, 250, 206)
DEFAULT_YELLOW_DOWN = (202, 202, 19)

DEFAULT_RED = (239, 56, 77)
DEFAULT_RED_OVER = (246, 147, 158)
DEFAULT_RED_DOWN =  (200, 16, 37)

DEFAULT_OVER_ALPHA_MASK_COLOR = (255, 255, 255, 64)
DEFAULT_DOWN_ALPHA_MASK_COLOR = (255, 255, 255, 32)

DEFAULT_APP_BORDER_PERCENT = 1
DEFAULT_APP_BORDER_REFERENCE = 380  # 400 (app height) - 20 (titlebar height)

DEFAULT_LIST_FONT_SIZE = 18

DEFAULT_LIST_NAME_COLOR = DEFAULT_APP_NAME_COLOR

DEFAULT_SCROLLBAR_THICKNESS = 9  # 18 // 2, 18: list font size
DEFAULT_SCROLLBAR_WHEEL_SPEED = 15

DEFAULT_SCROLLBAR_COLOR = DEFAULT_APP_NAME_COLOR

DEFAULT_MAP_CHUNK_WIDTH = 32
DEFAULT_MAP_CHUNK_HEIGHT = 32
DEFAULT_MAP_CHUNK_SIZE = 32  # in tilesize
DEFAULT_MAP_TILESIZE_WIDTH = 1024
DEFAULT_MAP_TILESIZE_HEIGHT = 1024
DEFAULT_MAP_SHIFT = 1  # in tilesize
DEFAULT_MAP_SHIFT_INTERVAL = 0.15
DEFAULT_MAP_ZOOM = 1

DEFAULT_MAP_GRID_COLOR = DEFAULT_TOOLBAR_DEMARCATION_COLOR
DEFAULT_MAP_ALPHA_MAK_COLOR = (255, 255, 255, 64)

DEFAULT_LAYERS_LIST_FONT_SIZE = 18
DEFAULT_LAYERS_LIST_ICON_TILESIZE = DEFAULT_LAYERS_LIST_FONT_SIZE // 6
# both (font_size, icon_tilesize) must be the same size
DEFAULT_LAYERS_LIST_ICON_LINESIZE = max(DEFAULT_LAYERS_LIST_ICON_TILESIZE//4, 1)

DEFAULT_LAYERS_LIST_NAME_COLOR = DEFAULT_APP_NAME_COLOR


# FUNCTIONS


def percent_border_to_px(app_width, app_height, titlebar_width, titlebar_height, percent, reference=0):
    usable_width = app_width - titlebar_width
    usable_height = app_height - titlebar_height
    minimum_length = min(usable_width, usable_height)
    length = reference if reference else minimum_length
    foreground_pos = int(length * percent // 100)   # pos = x = y
    foreground_width = usable_width - 2 * foreground_pos
    foreground_height = usable_height - 2 * foreground_pos
    return foreground_width, foreground_height, foreground_pos, foreground_pos

def draw_icon(name, t, l, color):  # t: tilesize, l: linesize
    icon = pygame.Surface((6*t, 6*t), SRCALPHA)
    if name == 'map':
        pygame.draw.polygon(icon, color,
            ((  0, 2*t), (2*t,   0), (4*t, 2*t), (6*t,   0),
             (6*t, 4*t), (4*t, 6*t), (2*t, 4*t), (  0, 6*t)))
        pygame.draw.line(icon, TRANSPARENT, (2*t, 0), (2*t, 6*t), l)
        pygame.draw.line(icon, TRANSPARENT, (4*t, 0), (4*t, 6*t), l)
    elif name == 'blocks':
        icon.fill(color)
        pygame.draw.line(icon, TRANSPARENT, (4*t, 0), (4*t, 3*t), l)
        pygame.draw.line(icon, TRANSPARENT, (0, 3*t), (6*t, 3*t), l)
        pygame.draw.line(icon, TRANSPARENT, (2*t, 3*t), (2*t, 6*t), l)
    elif name == 'properties':
        pygame.draw.polygon(icon, color,
            ((  0, 3*t), (2*t, 3*t), (3*t, 2*t), (3*t,   0), (5*t,   0),
             (4*t,   t), (5*t, 2*t), (6*t,   t), (6*t, 3*t),
             (4*t, 3*t), (3*t, 4*t), (3*t, 6*t), (  t, 6*t),
             (2*t, 5*t), (  t, 4*t), (  0, 5*t)))
    elif name == 'layers':
        h = l // 2  # h: half, for adjustments
        pygame.draw.polygon(icon, color, ((  0,   t), (  t,   0), (6*t,   0), (5*t, 1*t), (6*t, 1*t),
                               (6*t, 2*t), (5*t, 3*t), (6*t, 3*t), (6*t, 4*t),
                               (4*t, 6*t), (  0, 6*t), (  0, 5*t), (  t, 4*t),
                               (  0, 4*t), (  0, 3*t), (  t, 2*t), (  0, 2*t)))
        pygame.draw.line(icon, TRANSPARENT, (  0, 2*t), (4*t, 2*t), l)
        pygame.draw.line(icon, TRANSPARENT, (4*t-h, 2*t+h), (6*t,   0), l)
        pygame.draw.line(icon, TRANSPARENT, (  0, 4*t), (4*t, 4*t), l)
        pygame.draw.line(icon, TRANSPARENT, (4*t-h, 4*t+h), (7*t, 1*t), l)
    elif name == 'opened_padlock' or name == 'closed_padlock':
        pygame.draw.polygon(icon, color, ((  t, 2*t), (3*t,   0), (5*t, 2*t), (5*t, 5*t),
                                          (4*t, 6*t), (2*t, 6*t), (  t, 5*t)))
        pygame.draw.polygon(icon, TRANSPARENT, ((2*t, 4*t), (4*t, 4*t), (3*t, 5*t)))
        if name == 'opened_padlock':
            pygame.draw.polygon(icon, TRANSPARENT, ((2*t, 2*t), (3*t, 1*t), (6*t, 4*t),
                                                    (6*t, 5*t), (4*t, 3*t), (2*t, 3*t)))
        else:  # name == 'closed_padlock'
            pygame.draw.polygon(icon, TRANSPARENT, ((2*t, 2*t), (3*t, 1*t), (4*t, 2*t),
                                                    (4*t, 3*t), (2*t, 3*t)))
        pygame.draw.line(icon, TRANSPARENT, (  0, 5*t), (3*t, 2*t), l)
        pygame.draw.line(icon, TRANSPARENT, (3*t, 2*t), (6*t, 5*t), l)
    elif name == 'opened_eye' or name == 'closed_eye':
        pygame.draw.polygon(icon, color, ((  0, 3*t), (3*t,   0),
                                          (6*t, 3*t), (3*t, 6*t)))
        pygame.draw.polygon(icon, TRANSPARENT, ((2*t, 3*t), (3*t, 2*t),
                                                (4*t, 3*t), (3*t, 4*t)))
        if name == 'closed_eye':
            u = max(3, t)
            v = max(1, t//2)
            if u % 2 != v % 2:
                v -= 1  # both are odd or even
            pygame.draw.line(icon, TRANSPARENT, (  0, 6*t),(6*t,  0), u)
            pygame.draw.line(icon, color, (  0, 6*t),(6*t,  0), v)
            pygame.draw.polygon(icon, TRANSPARENT, ((  0, 5*t), (  t, 6*t), (  0, 6*t)))
            pygame.draw.polygon(icon, TRANSPARENT, ((5*t,   0), (6*t,   0), (6*t,   t)))
    return icon

def make_links_between(map, blocks, properties, layers):
    map.app_blocks = blocks
    map.app_properties = properties
    map.app_layers = layers
    blocks.app_map = map
    blocks.app_properties = properties
    blocks.app_layers = layers
    properties.app_map = map
    properties.app_blocks = blocks
    properties.app_layers = layers
    layers.app_map = map
    layers.app_blocks = blocks
    layers.app_properties = properties

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

# def zip_data(file='map.swptm', zipname='map'):
#     zip = zipfile.ZipFile('%s.zip' % zipname, 'w')
#     zip.write(file)
#     zip.close()
#
# def unzip_data(filename='map.swptm', mode='wb', zipname='map'):
#     try:
#         zip = zipfile.ZipFile('%s.zip' % zipname, 'r')
#         with open(filename, mode) as file:
#             file.write(zip.read(filename))
#         zip.close()
#     except FileNotFoundError:
#         return  # invalid filename

def initialize_undo(file='undo.swptu'):
    with open(file, 'w'):
        pass

def unload_undo(file='undo.swptu'):
    os.remove(file)

def add_undo(filename='undo.swptu', separator='|'):
    with open(filename, 'a+') as file:
        current = file.tell()
        file.seek(0, os.SEEK_END)
        if file.tell():  # file is not empty
            file.seek(current, os.SEEK_SET)
            file.write(separator)

def set_undo(undos, filename='undo.swptu'):
    with open(filename, 'a+') as file:
        for layer_id, id, chunk_id, i, j in undos:
            file.write('%d %d %d %d %d ' % (layer_id, chunk_id, i, j, id))

def get_undo(filename='undo.swptu', separator='|'):
    with open(filename, 'r+') as file:
        file.seek(0, os.SEEK_END)
        current = 3
        end = file.tell()
        if end >= 3:
            file.seek(end-current, os.SEEK_SET)
            while file.read(1) != separator and end - current:
                current += 1
                file.seek(end-current, os.SEEK_SET)
            shift = 1 if end - current else 0
            # if not end - current then we are at the beginning of the file
            # so the first char must not be omitted & shift = 0
            if not shift:  # go to the first char omitted in the while
                file.seek(end-current, os.SEEK_SET)
            start = end - current + shift  # shift because file.read(1) in while
            line = file.read(current-2).rstrip().split()
            final = []
            for index, value in enumerate(line):
                if not index % 5:  # new block
                    # final.append([int(value)])
                    final.insert(0, [int(value)])
                else:
                    # final[-1].append(int(value))
                    final[0].append(int(value))
            file.seek(start, os.SEEK_SET)
            file.truncate()
            return final  # layer_id, chunk_id, i, j, id
        return 0


# CLASSES


class Button(swapcore.kernel.Area):
    def __init__(self, identifier, radius, centerx, centery, color_up, color_over, color_down, color):
        width = 2 * radius + 1
        super().__init__(width, width, centerx-radius, centery-radius, color=color)
        self.identifier = identifier
        self.radius = radius
        self.color_up = color_up
        self.color_over = color_over
        self.color_down = color_down
        self.colour = color_up
        self.state = 0  # 0: up, 1: over, 2: down
        pygame.gfxdraw.filled_circle(self._surface, radius, radius, radius, self.colour)
        pygame.gfxdraw.aacircle(self._surface, radius, radius, radius, self.colour)

    def update_state(self, mcx, mcy, action_type):
        on_self = self.left <= mcx <= self.right and self.top <= mcy <= self.bottom
        queries = 0
        if self.state and not on_self:
            self.state = 0
            self.colour = self.color_up
            queries = 1
        elif on_self:
            if (mcx - self.centerx) ** 2 + (mcy - self.centery) ** 2 <= self.radius ** 2:
                if action_type == MOUSEMOTION and not self.state:
                    self.state = 1
                    self.colour = self.color_over
                    queries = 1
                elif action_type == MOUSEBUTTONDOWN and self.state != 2:
                    self.state = 2
                    self.colour = self.color_down
                    queries = 1
                elif action_type == MOUSEBUTTONUP and self.state == 2:
                    self.state = 1
                    self.colour = self.color_over
                    queries = 2
        if queries:
            self.draw_state()
        return queries

    def draw_state(self):
        self._surface.fill(self.color)
        pygame.gfxdraw.filled_circle(self._surface, self.radius, self.radius, self.radius, self.colour)
        pygame.gfxdraw.aacircle(self._surface, self.radius, self.radius, self.radius, self.colour)


class ScrollBar:
    def __init__(self, window, area):
        if isinstance(window, swapcore.kernel.Area) or isinstance(window, ScrollArea):
            self.window = window
        else:
            self.window = swapcore.kernel.Area(
                1, 1, 0, DEFAULT_APP_TITLEBAR_HEIGHT+3,  # +3: border_width
                0, DEFAULT_APP_FOREGROUND_COLOR)
            self.window.surface = window
        self.area = area
        self.vertical = 0
        self.horizontal = 0
        self.vertical_speed = 1
        self.horizontal_speed = 1
        self.old_mcsy = 0  # mouse y converted to vertical scrollbar coord system
        self.old_mcsx = 0  # mouse x converted to horizontal scrollbar coord system

    def mouse_event(self, mouse_on_app, action_type, mcx=None, mcy=None):
        queries = 0
        if mouse_on_app:
            # scrollbar coords are in self window coord system, so we have co convert mcx, mcy
            mcwx = mcx - self.window.x  # cw: converted (to) window (coord system)
            mcwy = mcy - self.window.y
        if action_type == MOUSEBUTTONDOWN and mouse_on_app:
            if self.horizontal and self.is_mouse_on_scrollbar(self.horizontal, mcwx, mcwy):
                self.old_mcsx = mcwx - self.horizontal.x
            if self.vertical and self.is_mouse_on_scrollbar(self.vertical, mcwx, mcwy):
                self.old_mcsy = mcwy - self.vertical.y
        elif (action_type == MOUSEWHEELUP or action_type == MOUSEWHEELDOWN) and mouse_on_app:
            queries = self.update_with_wheel(action_type, mcwx, mcwy)
        elif action_type == MOUSEMOTION:
            if mouse_on_app:
                if self.old_mcsx:  # horizontal scrollbar is being moved
                    max_x = (self.window.width - self.horizontal.width if not self.vertical \
                        else self.window.width - self.horizontal.width - self.vertical.width)
                    self.horizontal.x = min(max_x, max(0, mcwx - self.old_mcsx))
                    queries = self.draw()
                if self.old_mcsy:  # vertical scrollbar is being moved
                    max_y = (self.window.height - self.vertical.height if not self.horizontal \
                        else self.window.height - self.vertical.height - self.horizontal.height)
                    self.vertical.y = min(max_y, max(0, mcwy - self.old_mcsy))
                    queries = self.draw()
            else:
                if self.old_mcsx:  # not mouse_on_app but scrollbar has the focus
                    self.old_mcsx = 0
                if self.old_mcsy:
                    self.old_mcsy = 0
        elif action_type == MOUSEBUTTONUP:
            if self.old_mcsx:
                self.old_mcsx = 0
            if self.old_mcsy:
                self.old_mcsy = 0
        return queries

    def update(self):
        self.update_vertical()
        self.update_horizontal()

    def update_vertical(self):
        available = (self.window.height if not self.horizontal \
            else self.window.height - self.horizontal.height)
        if self.area.height <= available:
            if self.vertical:
                self.vertical = 0  # no more scrollbar needed
                self.update_horizontal()
            return
        h = 2 * available - self.area.height  # h: height
        minsize = 4 * DEFAULT_SCROLLBAR_THICKNESS
        speed = 1
        if h < minsize:
            th = available - h  # tw: theoretical height
            rh = available - minsize  # rh: real height
            h = minsize
            speed = th / rh
        w = DEFAULT_SCROLLBAR_THICKNESS  # w: width
        x = self.window.width - w
        if not (self.vertical and self.vertical.y):
            y = 0
        else:
            y = max(1, self.vertical.y * self.vertical_speed / speed)
            if y + h > available:
                y = available - h
        if not self.vertical or not self.scrollbar_equals(self.vertical, w, h, x, y) \
          or self.vertical_speed != speed:
            self.vertical = swapcore.kernel.Area(w, h, x, y, color=DEFAULT_SCROLLBAR_COLOR)
            self.vertical_speed = speed
            self.update_horizontal()

    def update_horizontal(self):
        available = self.window.width if not self.vertical else self.window.width - self.vertical.width
        if self.area.width <= available:
            if self.horizontal:
                self.horizontal = 0  # no more scrollbar needed
                self.update_vertical()
            return
        w = 2 * available - self.area.width  # w: width
        minsize = 4 * DEFAULT_SCROLLBAR_THICKNESS
        speed = 1
        if w < minsize:
            tw = available - w  # tw: theoretical width
            rw = available - minsize  # rw: real width
            w = minsize
            speed = tw / rw
        h = DEFAULT_SCROLLBAR_THICKNESS  # h: height
        if not (self.horizontal and self.horizontal.x):
            x = 0
        else:
            x = max(1, self.horizontal.x * self.horizontal_speed / speed)
            if x + w > available:
                x = available - w
        y = self.window.height - h
        if not self.horizontal or not self.scrollbar_equals(self.horizontal, w, h, x, y) \
          or self.horizontal_speed != speed:
            self.horizontal = swapcore.kernel.Area(w, h, x, y, color=DEFAULT_SCROLLBAR_COLOR)
            self.horizontal_speed = speed
            self.update_vertical()

    def update_with_wheel(self, action_type, mcwx, mcwy):
        if self.vertical:
            # if mouse is over self window
            if 0 <= mcwx <= self.window.width and 0 <= mcwy <= self.window.height:
                if action_type == MOUSEWHEELUP:
                    shift = (self.vertical.y \
                        if self.vertical.y - DEFAULT_SCROLLBAR_WHEEL_SPEED < 0 \
                        else DEFAULT_SCROLLBAR_WHEEL_SPEED)
                elif action_type == MOUSEWHEELDOWN:
                    max_y = (self.window.height - self.vertical.height if not self.horizontal \
                        else self.window.height - self.vertical.height - self.horizontal.height)
                    shift = -(max_y - self.vertical.y \
                        if self.vertical.y + DEFAULT_SCROLLBAR_WHEEL_SPEED > max_y \
                        else DEFAULT_SCROLLBAR_WHEEL_SPEED)
                self.vertical.y -= shift
                if self.old_mcsy:  # if the scrollbar is being moved with the mouse
                    self.old_mcsy += shift
                return self.draw()
        return 0

    def draw(self, *scrollbar):
        iterator = (scrollbar if scrollbar \
            else [scroll for scroll in [self.horizontal, self.vertical] if scroll])
        if not scrollbar:
            self.window.surface.fill(self.window.color)
            self.window.surface.blit(self.area.surface, self.shift_topleft)
        for scroll in iterator:
            self.window.surface.blit(scroll.surface, scroll.topleft)
        return 1  # request redraw on app surface

    @staticmethod
    def is_mouse_on_scrollbar(scrollbar, mcwx, mcwy):
        return scrollbar.left <= mcwx <= scrollbar.right and scrollbar.top <= mcwy <= scrollbar.bottom

    @staticmethod
    def scrollbar_equals(scrollbar, w, h, x, y):
        return scrollbar.width == w and scrollbar.height == h and scrollbar.x == x and scrollbar.y == y

    @property
    def shift_x(self):
        return round(-self.horizontal.x * self.horizontal_speed) if self.horizontal else 0

    @property
    def shift_y(self):
        return round(-self.vertical.y * self.vertical_speed) if self.vertical else 0

    @property
    def shift_topleft(self):
        return (self.shift_x, self.shift_y)


class ScrollArea(swapcore.kernel.Area):
    def __init__(self, width, height, x, y, surface=0, color=0):
        super().__init__(width, height, x, y, surface, color)
        self.list = swapcore.kernel.Area(width, 1, 0, 0, color=color)
        self.listing = [1, None, None]  # [height, over, down, [surface, *arg], ...]
        self.scrollbar = ScrollBar(self, self.list)

    def mouse_over_self(self, mcx, mcy):
        return self.left <= mcx <= self.right and self.top <= mcy <= self.bottom

    def mouse_event(self, mouse_on_app, action_type, mcx=None, mcy=None):
        queries = [0]  # index 0: redraw
        if self.scrollbar.mouse_event(mouse_on_app, action_type, mcx, mcy):
            queries[0] = 1  # request redraw
        if action_type == MOUSEBUTTONDOWN and mouse_on_app:
            if self.mouse_over_self(mcx, mcy) and not self.scrollbar.old_mcsx and not self.scrollbar.old_mcsy:
                mcsy = mcy - self._y - self.scrollbar.shift_y  # self
                height = self.listing[0]
                over, down = self.listing[1:3]
                y = mcsy - mcsy % height
                index = 3 + y // height
                if y != down and index < len(self.listing):  # y != down
                    for state in [s for s in [down, over] if s is not None]:
                        self.clear_state(state)
                    self.draw_alpha_mask(1, y, True)
                    self.listing[1:3] = y, y
                    queries[0] = 1
                    queries.append([2, index])  # request click action
        elif action_type == MOUSEMOTION:
            if mouse_on_app:
                if self.mouse_over_self(mcx, mcy):
                    if not self.scrollbar.old_mcsx and not self.scrollbar.old_mcsy and len(self.listing) > 3:
                        mcsy = mcy - self._y - self.scrollbar.shift_y  # self
                        height = self.listing[0]
                        over, down = self.listing[1:3]
                        y = mcsy - mcsy % height
                        if y != over:
                            if over is not None:
                                self.clear_state(over)
                            if down is not None and over == down:
                                self.draw_alpha_mask(1, down)
                            if y == down:
                                self.clear_state(down)
                            self.draw_alpha_mask(0, y, True)
                            self.listing[1] = y
                            queries[0] = 1
                elif self.update_state():
                    queries[0] = 1
            elif self.update_state():
                queries[0] = 1
        return queries

    def draw_list(self):
        if self.scrollbar.vertical or self.scrollbar.horizontal:
            self.scrollbar.draw()
        else:
            self._surface.fill(self._color)
            self._surface.blit(self.list.surface, self.scrollbar.shift_topleft)

    def draw_alpha_mask(self, mode, y, draw_on_self=False):
        alpha_mask = pygame.Surface((self.list.width, self.listing[0]), SRCALPHA)
        alpha_mask.fill(DEFAULT_DOWN_ALPHA_MASK_COLOR if mode else DEFAULT_OVER_ALPHA_MASK_COLOR)
        self.list.surface.blit(alpha_mask, (0, y))
        if draw_on_self:
            self.draw_list()

    def clear_state(self, y, draw_on_self=False):
        index = 3 + y // self.listing[0]
        if index < len(self.listing):
            self.list.surface.fill(self.list.color, (0, y, self.list.width, self.listing[0]))
            self.list.surface.blit(self.listing[index][0], (0, y))
            if draw_on_self:
                self.draw_list()

    def update_state(self):
        if self.listing[1] is not None:
            self.clear_state(self.listing[1])
            if self.listing[1] == self.listing[2]:
                alpha_mask = pygame.Surface((self.list.width, self.listing[0]), SRCALPHA)
                alpha_mask.fill((DEFAULT_DOWN_ALPHA_MASK_COLOR))
                self.list.surface.blit(alpha_mask, (0, self.listing[2]))
            self.draw_list()
            self.listing[1] = None
            return 1
        return 0

    # def draw_listing(self, reset_focus=True):
    #     height = self.listing[0]
    #     for i, (surface, *_) in enumerate(self.listing[3:]):
    #         y = height * i
    #         w, h = surface.get_width(), y + height
    #         if w > self.list.width:
    #             self.list.width = w
    #         if h > self.list.height:
    #             self.list.height = h
    #         self.list.surface.blit(surface, (0, y))
    #     self.draw_list()
    #     if reset_focus:
    #         self.listing[1], self.listing[2] = None, None


class ScrollWidget:
    def __init__(self, app, scrollarea, toolbar, generic_row_name='row', button_y=None):
        self.app = app
        self.scrollarea = scrollarea
        self.toolbar = toolbar
        self.generic_row_name = generic_row_name
        button_y = button_y if button_y is not None else toolbar.height // 2
        # button's x & y are in toolbar coord system:
        self.add_button = Button(
            0, app.titlebar_button_radius, app.titlebar_button_radius, button_y,
            DEFAULT_GREEN, DEFAULT_GREEN_OVER, DEFAULT_GREEN_DOWN, toolbar.color)
        self.delete_button = Button(
            1, app.titlebar_button_radius, 4*app.titlebar_button_radius, button_y,
            DEFAULT_RED, DEFAULT_RED_OVER, DEFAULT_RED_DOWN, toolbar.color)
        # button identifier: 0: add, 1: delete
        self.focus_string = None  # after init: [string, base, y]
        self.new_row_id = 1
        self.draw_toolbar_button()

    def mouse_event(self, mouse_on_app, action_type, mx=None, my=None, mcx=None, mcy=None):
        """
        if mouse_on_app, mcx, mcy are not None
        if not mouse_on_app, mx, my are not None
        """
        queries = [0]  # index 0: redraw
        old_selected_row = None if self.scrollarea.listing[2] is None else self.scrollarea.listing[2]
        if mouse_on_app:
            if self.is_mouse_on_toolbar(self.toolbar, mcx, mcy) \
              or self.add_button.state or self.delete_button.state:
                self.update_toolbar_button(mcx-self.toolbar.x, mcy-self.toolbar.y, action_type)
            queries = self.scrollarea.mouse_event(mouse_on_app, action_type, mcx, mcy)
        else:
            if self.add_button.state or self.delete_button.state:
                self.update_toolbar_button(mx-self.app.x-self.toolbar.x, my-self.app.y-self.toolbar.y, action_type)
            queries = self.scrollarea.mouse_event(mouse_on_app, action_type)
        if action_type == MOUSEBUTTONDOWN:
            if self.focus_string:
                self.reset_focus_string()
        if queries[0]:
            self.app.perform_queries(queries, old_selected_row)
            self.app.surface.blit(self.scrollarea.surface, self.scrollarea.topleft)

    def keyboard_event(self, event, keystate, mx, my):
        if event.type == KEYDOWN:
            if self.focus_string is not None:
                if event.key == K_BACKSPACE:
                    if self.focus_string[0]:
                        self.focus_string[0] = self.focus_string[0][:-1]
                        self.update_focus_string()
                elif event.key == K_RETURN:
                    self.reset_focus_string()
                elif event.unicode.isalnum() or event.unicode in ".,!?:'\"-" or event.key == K_SPACE:
                    self.focus_string[0] += event.unicode
                    self.update_focus_string()

    def update_focus_string(self):
        string, base, y = self.focus_string
        if not string:
            string = ' '
        x = base.get_width()
        name = self.app.font.render(string, DEFAULT_LIST_FONT_SIZE, DEFAULT_LIST_NAME_COLOR)
        w, h = x + name.get_width() + self.app.border_width, self.scrollarea.listing[0]
        row = pygame.Surface((w, h), SRCALPHA)
        row.blit(base, ORIGIN)
        row.blit(name, (x, self.app.border_width))
        width = row.get_width()
        index = 3 + y // h
        self.scrollarea.listing[index][:3] = row, string, width
        if width > self.scrollarea.list.width:
            self.scrollarea.list.width = width
        available = (self.scrollarea.width if not self.scrollarea.scrollbar.vertical \
            else self.scrollarea.width - self.scrollarea.scrollbar.vertical.width)
        maximum = max(available, max([layer[2] for layer in self.scrollarea.listing[3:]]))
        if self.scrollarea.list.width > maximum:
            self.scrollarea.list.width = maximum
        self.scrollarea.scrollbar.update_horizontal()
        if self.scrollarea.scrollbar.horizontal and w > available:
            shift = w - available
            x = shift // self.scrollarea.scrollbar.horizontal_speed
            self.scrollarea.scrollbar.horizontal.x = \
                min(x, self.scrollarea.width-self.scrollarea.scrollbar.horizontal.width)
        elif self.scrollarea.scrollbar.horizontal:
            self.scrollarea.scrollbar.horizontal.x = 0
        area = (0, y, self.scrollarea.list.width, h)
        self.scrollarea.list.surface.fill(self.scrollarea.list.color, (0, y, self.scrollarea.list.width, h))
        self.scrollarea.list.surface.blit(row, (0, y))
        if self.scrollarea.listing[2] is not None:
            self.scrollarea.clear_state(self.scrollarea.listing[2])
            self.scrollarea.draw_alpha_mask(1, self.scrollarea.listing[2])
        if y == self.scrollarea.listing[1] is not None:
            self.scrollarea.clear_state(self.scrollarea.listing[1])
            self.scrollarea.draw_alpha_mask(0, self.scrollarea.listing[1])
        self.scrollarea.draw_list()
        self.app.surface.blit(self.scrollarea.surface, self.scrollarea.topleft)

    def reset_focus_string(self):
        if not self.focus_string[0]:
            self.focus_string[0] = '%s %d' % (self.generic_row_name, self.new_row_id-1)
            # -1 because we're doing +1 at the end of add_row method
            self.update_focus_string()
        if not self.app.is_focus_string_valid(self.focus_string[0]):
            self.app.delete_row(self.scrollarea.listing[0] * (len(self.scrollarea.listing)-4))
        else:
            self.app.perform_row_creation(self.focus_string[0])
        self.focus_string = None

    def add_row(self, name=' ', surface=None, x=None):
        if surface is None:
            noun = self.app.font.render(name, DEFAULT_LIST_FONT_SIZE, DEFAULT_LIST_NAME_COLOR)
            double = 2 * self.app.border_width
            width = double + noun.get_width()
            height = DEFAULT_LIST_FONT_SIZE + double
            row = pygame.Surface((width, height), SRCALPHA)
            row.blit(noun, (self.app.border_width, self.app.border_width))
        else:
            row = surface
            width = row.get_width()
            height = row.get_height()
        self.scrollarea.listing[0] = height
        if width > self.scrollarea.list.width:
            self.scrollarea.list.width = width
        total_height = height * (len(self.scrollarea.listing) - 2)  # -2: + 1 for new, -3 for height, over, down
        if total_height > self.scrollarea.list.height:
            self.scrollarea.list.height = total_height
        self.scrollarea.scrollbar.update_vertical()
        if self.scrollarea.scrollbar.vertical:
            available = self.scrollarea.width - self.scrollarea.scrollbar.vertical.width
            max_width = max([row[0].get_width() for row in self.scrollarea.listing[3:]])
            if max_width <= available and self.scrollarea.list.width > available:
                self.scrollarea.list.width = available
        self.scrollarea.scrollbar.update_horizontal()
        y = height * (len(self.scrollarea.listing) - 3)
        self.scrollarea.list.surface.blit(row, (0, y))
        self.scrollarea.listing.append([row])
        self.scrollarea.draw_list()
        self.app.surface.blit(self.scrollarea.surface, self.scrollarea.topleft)
        self.new_row_id += 1
        if name == ' ':
            base = pygame.Surface((x if x is not None else self.app.border_width, height), SRCALPHA)
            base.blit(row, ORIGIN)
            self.focus_string = ['', base, y]
        return width

    def delete_row(self, y):
        if y is None:
            return
        height = self.scrollarea.listing[0]
        index = 3 + y // height
        if self.scrollarea.listing[3:]:
            deleted_layer = self.scrollarea.listing.pop(index)
            if not self.scrollarea.listing[3:]:
                self.scrollarea.list.width = 1
                self.scrollarea.list.height = 1
            else:
                if deleted_layer[2] == self.scrollarea.list.width:
                    self.scrollarea.list.width = max([layer[2] for layer in self.scrollarea.listing[3:]])
                surface = pygame.Surface((self.scrollarea.list.width, self.scrollarea.list.height-height))
                surface.blit(self.scrollarea.list.surface, ORIGIN, area=(0, 0, self.scrollarea.list.width, y))
                surface.blit(
                    self.scrollarea.list.surface, (0, y),
                    (0, y+height, self.scrollarea.list.width, self.scrollarea.list.height-y-height))
                self.scrollarea.list.surface = surface
                if y == self.scrollarea.listing[2]:  # y = down
                    self.scrollarea.listing[2] = None
                    # self.app_map.layer_id = 0
            self.scrollarea.scrollbar.update()
            available = (self.scrollarea.width if not self.scrollarea.scrollbar.vertical \
                else self.scrollarea.width - self.scrollarea.scrollbar.vertical.width)
            if available > self.scrollarea.list.width:
                self.scrollarea.list.width = available
            self.scrollarea.draw_list()
            self.app.surface.blit(self.scrollarea.surface, self.scrollarea.topleft)

    def update_toolbar_button(self, mctx, mcty, action_type, *button):
        """
        mctx, mcty: mouse (x, y) converted to toolbar coord system
        """
        iterator = button if button else [self.add_button, self.delete_button]
        updated = []
        for b in iterator:  # b: button
            queries = b.update_state(mctx, mcty, action_type)
            if queries:
                updated.append(b)
                if queries == 2:  # request action
                    if not b.identifier:  # add button
                        self.app.add_row()
                    else:  # delete layer button
                        self.app.delete_row(self.scrollarea.listing[2])
        self.draw_toolbar_button(*updated)

    def draw_toolbar_button(self, *button):
        iterator = button if button else [self.add_button, self.delete_button]
        for b in iterator:  # b: button
            b.draw_on(self.toolbar.surface)
        self.app.surface.blit(self.toolbar.surface, self.toolbar.topleft)

    @staticmethod
    def is_mouse_on_toolbar(toolbar, mcx, mcy):
        return toolbar.left <= mcx <= toolbar.right and toolbar.top <= mcy <= toolbar.bottom


class PropertySpreadingThread(threading.Thread):
    def __init__(self, app_map, property):
        super().__init__()
        self.app_map = app_map
        self.app_blocks = app_map.app_blocks
        self.property = property

    def apply_property_on_one_tile(self, layer_id, chunk_id, key, name, packed):
        """packed = [mode, value]"""
        try:
            self.app_map.data[layer_id][chunk_id][0][key][name] = packed
        except KeyError:  # the tile don't have any property
            self.app_map.data[layer_id][chunk_id][0][key] = {name: packed}

    def packed_equals_property(self, packed, layer_id, chunk_id, key, name):
        try:
            return packed == self.app_map.data[layer_id][chunk_id][0][key][name]
        except KeyError:
            return False

    def run(self):
        """
        mode list: default (no letter: same id), p (same Path), d (same Dir), i (Identical)
        spread list: o (Only), b (Bucket), a (All visible), v (oVerhaul)
        """
        name, mode, value = self.property
        spread, type = mode[0], mode[1:]
        x, y = self.app_map.get_tile_x_y_from_visual(*self.app_map.ptile)
        chunk_id, i, j = self.app_map.convert_y_x_to_chunk_id(y, x)
        key = '%d_%d' % (x, y)
        packed = [mode, value]
        number = 0
        if spread == 'o':  # only
            self.apply_property_on_one_tile(self.app_map.layer_id, chunk_id, key, name, packed)
        elif spread == 'b':  # bucket
            original = self.app_map.data[self.app_map.layer_id][chunk_id][1][i][j]
            if not self.packed_equals_property(packed, self.app_map.layer_id, chunk_id, key, name):
                self.apply_property_on_one_tile(self.app_map.layer_id, chunk_id, key, name, packed)
                number += 1
                if not original:
                    print("property %s has finished spreading on %d tiles" % (self.property, number))
                    return  # can't spread on void tile for safety reason (avoid almost infinite loop)
                todo_coords = [(x, y)]
                while todo_coords:
                    cx, cy = todo_coords[0]  # c: current
                    for (z, t) in self.get_neighboring_tiles(cx, cy):  # (z, t) for (x, y)
                        try:
                            if z >= 0 and t >= 0:
                                cid, m, n = self.app_map.convert_y_x_to_chunk_id(t, z)  # cid: chunk_id
                                if self.app_map.data[self.app_map.layer_id][cid][1][m][n] == original:
                                    k = '%d_%d' % (z, t)  # k : key
                                    if not self.packed_equals_property(
                                      packed, self.app_map.layer_id, cid, k, name):
                                        self.apply_property_on_one_tile(
                                            self.app_map.layer_id, cid, k, name, packed)
                                        number += 1
                                        todo_coords.append((z, t))
                        except IndexError:  # coords out of map
                            pass
                    todo_coords.pop(0)
        elif spread == 'a':
            sx, sy = self.app_map.visual_start  # s: start
            original = self.app_map.data[self.app_map.layer_id][chunk_id][1][i][j]
            for layer_id, layer in enumerate(self.app_map.visual_data):
                for i, row in enumerate(layer):
                    for j, column in enumerate(row):
                        chunk_id, k, l = self.app_map.convert_y_x_to_chunk_id(sy+i, sx+j)
                        if self.app_map.data[layer_id][chunk_id][1][k][l] == original:
                            key = '%d_%d' % (sx+j, sy+i)
                            if not self.packed_equals_property(packed, layer_id, chunk_id, key, name):
                                self.apply_property_on_one_tile(layer_id, chunk_id, key, name, packed)
                                number += 1
        elif spread == 'v':
            original = self.app_map.data[self.app_map.layer_id][chunk_id][1][i][j]
            for layer_id, layer in enumerate(self.app_map.data):
                for chunk_id, chunk in enumerate(layer):
                    for i, row in enumerate(chunk[1]):
                        for j, column in enumerate(row):
                            if self.app_map.data[layer_id][chunk_id][1][i][j] == original:
                                chunk_i, chunk_j = self.app_map.get_chunk_i_j_from_id(chunk_id)
                                y = chunk_i * DEFAULT_MAP_CHUNK_SIZE + i
                                x = chunk_j * DEFAULT_MAP_CHUNK_SIZE + j
                                key = '%d_%d' % (x, y)
                                if not self.packed_equals_property(packed, layer_id, chunk_id, key, name):
                                    self.apply_property_on_one_tile(layer_id, chunk_id, key, name, packed)
                                    number += 1
                            # if self.app_map.data[layer_id][chunk_id][1][i][j] == 0:
                            #     chunk_i, chunk_j = self.app_map.get_chunk_i_j_from_id(chunk_id)
                            #     y = chunk_i * DEFAULT_MAP_CHUNK_SIZE + i
                            #     x = chunk_j * DEFAULT_MAP_CHUNK_SIZE + j
                            #     key = '%d_%d' % (x, y)
                            #     del self.app_map.data[layer_id][chunk_id][0][key]
        print("property %s has finished spreading on %d tiles" % (self.property, number))
        return  # the spread of the property is complete

    @staticmethod
    def get_neighboring_tiles(x, y):
        return [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]


class AppMap(swapcore.kernel.App):
    def __init__(self, font, appmanager):
        self.icon = draw_icon(
            'map', DEFAULT_APP_ICON_TILESIZE, DEFAULT_APP_ICON_LINESIZE,
            DEFAULT_ICON_MAP_COLOR)
        self.dock_icon = draw_icon(
            'map', DEFAULT_DOCK_APP_ICON_TILESIZE,
            DEFAULT_DOCK_APP_ICON_LINESIZE,
            DEFAULT_ICON_MAP_COLOR)
        self.borders = percent_border_to_px(
            appmanager.desk.width, appmanager.desk.height,
            0, DEFAULT_APP_TITLEBAR_HEIGHT,
            DEFAULT_APP_BORDER_PERCENT, DEFAULT_APP_BORDER_REFERENCE)
        self.border_width = self.borders[2]
        super().__init__(
            self.icon,
            'map',
            DEFAULT_APP_NAME_COLOR,
            font,
            appmanager.desk.width,
            appmanager.desk.height,
            0, 0,
            DEFAULT_APP_BACKGROUND_COLOR,
            0,
            DEFAULT_APP_TITLEBAR_HEIGHT,
            DEFAULT_APP_TITLEBAR_COLOR,
            DEFAULT_APP_TITLEBAR_BUTTON_RADIUS,
            *self.borders,
            DEFAULT_APP_FOREGROUND_COLOR,
            DEFAULT_MINIMIZE_BUTTON_COLOR,
            DEFAULT_MINIMIZE_BUTTON_OVER_COLOR,
            DEFAULT_MINIMIZE_BUTTON_DOWN_COLOR,
            DEFAULT_MAXIMIZE_BUTTON_COLOR,
            DEFAULT_MAXIMIZE_BUTTON_OVER_COLOR,
            DEFAULT_MAXIMIZE_BUTTON_DOWN_COLOR,
            DEFAULT_CLOSE_BUTTON_COLOR,
            DEFAULT_CLOSE_BUTTON_OVER_COLOR,
            DEFAULT_CLOSE_BUTTON_DOWN_COLOR,
            0, 0,
            PROGRAM_WIDTH,
            PROGRAM_HEIGHT)
        self.appmanager = appmanager
        self.filename = 'map.swptm'
        # must be initialized later with a linking function:
        self.app_blocks, self.app_layers, self.app_properties = None, None, None
        self.tilesize = DEFAULT_TILESIZE
        self.vtilesize = DEFAULT_TILESIZE  # v: visual
        self.twidth = DEFAULT_MAP_TILESIZE_WIDTH  # t: tilesize
        self.theight = DEFAULT_MAP_TILESIZE_HEIGHT  # t: tilesize
        # self.cwidth, self.cheight = DEFAULT_MAP_CHUNK_WIDTH, DEFAULT_MAP_CHUNK_HEIGHT
        self.cwidth, self.cheight = 13, 8
        # self.map = swapcore.kernel.Area(
        #     self.twidth*self.tilesize, self.theight*self.tilesize,
        #     0, 0, color=self.foreground_color)
        self.layers = [1]
        self.block_id = 0
        # self.map, self.data, self.visual_data, self.visual_start = self.initialize_data()
        self.map = swapcore.kernel.Area(1, 1, 0, 0, color=self.foreground_color)
        self.data, self.visual_data, self.visual_start = None, None, None
        self.lossless_map = 0  # initialized later
        self.mouse_tile = 0  # initialized later with: (x, y, tilesize)
        # self.grid = 0 # if grid creation requested, self.grid is a pygame.Surface object
        self.grid = None
        self.last_shift = 0
        self.shift_x_key = 0
        self.shift_y_key = 0
        # self.draw_map()
        # self._surface.blit(self.foreground, self.foreground_topleft)
        self.draw_mode = 0  # 0: pen, 1: bucket
        self.layer_id = 0
        self.should_add_undo = False
        self.undo_numbers = 0
        self.ptile = None  # p: property, the tile that has its properties displayed

    def additional_mouse_event(self, mx, my, action_type, actions, mouse_on_app,
                               on_titlebar_button, keystate):
        if mouse_on_app:
            mcx, mcy = mx - self._x, my - self._y  # c: converted (to app coord system)
            mcfx = mcx - self.foreground_left  # cf: converted (to) foreground (coord system)
            mcfy = mcy - self.foreground_top
        if action_type == MOUSEBUTTONDOWN:
            if mouse_on_app:
                self.update_mouse_tile(mouse_on_app, mcfx, mcfy, True, False)
                self.update_block()
        elif action_type == MOUSERIGHTBUTTONDOWN:
            if mouse_on_app:
                actions.append(1)  # request focus
                self.update_mouse_tile(mouse_on_app, mcfx, mcfy, True, False)
                self.update_block(mode=1)
        elif action_type == MOUSEMOTION:
            if mouse_on_app:
                if not self.mouse_tile:
                    actions.append(1)
                    self.update_mouse_tile(mouse_on_app, mcfx, mcfy, True)
                else:
                    self.update_mouse_tile(mouse_on_app, mcfx, mcfy)
            elif self.mouse_tile:
                self.update_mouse_tile(False)
        elif (action_type == MOUSEBUTTONUP or action_type == MOUSERIGHTBUTTONUP) \
          and self.should_add_undo and self.undo_numbers:
            self.should_add_undo = False
            add_undo()
        # elif action_type == MOUSEWHEELUP:
        #     if mouse_on_app:
        #         actions.append(1)
        #         self.update_zoom(keystate)
        #         self.update_mouse_tile(mouse_on_app, mcfx, mcfy, True)
        # elif action_type == MOUSEWHEELDOWN:
        #     if mouse_on_app:
        #         actions.append(1)
        #         self.update_unzoom(keystate)
        #         self.update_mouse_tile(mouse_on_app, mcfx, mcfy, True)

    def mouse_state(self, mousestate):
        if mousestate[0] and self.mouse_tile and not self.mouse_tile[3]:
            self.update_block()
        elif mousestate[2] and self.mouse_tile:
            self.update_block(mode=1)

    def keyboard_event(self, event, keystate, mx, my):
        if event.type == KEYDOWN:
            if event.unicode == 'g':
                self.grid = 0 if self.grid else self.create_grid()
                self.draw_map()
                if self.mouse_tile:
                    self.draw_alpha_mask_on_tile(self.mouse_tile[0], self.mouse_tile[1], False)
            elif event.unicode == 'p' and self.draw_mode:
                print('Pen mode enabled')
                self.draw_mode = 0
            elif event.unicode == 'b' and not self.draw_mode:
                print('Bucket mode enabled')
                self.draw_mode = 1
            elif event.unicode == 's':
                layers_name = [row[1] for row in self.app_layers.scrollwidget.scrollarea.listing[3:]]
                store_data_to_file(self.filename, layers_name,
                    self.app_blocks.path_to_id, self.app_blocks.id_to_path,
                    self.visual_start, self.visual_data, self.data)
                print('Data saved')
            elif event.unicode == 'o' and self.mouse_tile:
                j, i = self.mouse_tile[0] // self.vtilesize, self.mouse_tile[1] // self.vtilesize
                id = self.visual_data[self.layer_id][i][j]
                if id:
                    path, *_ = self.app_blocks.id_to_path[id]
                    self.block_id = (path, *self.app_blocks.path_to_id[path+'/0/0'])
                else:
                    self.block_id = 0
                print('ID selected: %d' % (self.block_id if not self.block_id else self.block_id[1]))
            elif event.unicode == 'z' and self.undo_numbers and not pygame.mouse.get_pressed()[0]:
                undo = get_undo()
                if undo:
                    self.perform_undo(undo)
            # elif event.unicode == 'v':
            #     self.reduce_map()
            if event.key == K_LCTRL:
                self.update_ptile(True)
            elif event.key == K_LEFT:
                self.shift_x_key = K_LEFT
                self.last_shift = 0
            elif event.key == K_UP:
                self.shift_y_key = K_UP
                self.last_shift = 0
            elif event.key == K_RIGHT:
                self.shift_x_key = K_RIGHT
                self.last_shift = 0
            elif event.key == K_DOWN:
                self.shift_y_key = K_DOWN
                self.last_shift = 0
        if event.type == KEYUP:
            if event.key == K_LEFT and keystate[K_RIGHT]:
                self.shift_x_key = K_RIGHT
                self.last_shift = 0
            elif event.key == K_UP and keystate[K_DOWN]:
                self.shift_y_key = K_DOWN
                self.last_shift = 0
            elif event.key == K_RIGHT and keystate[K_LEFT]:
                self.shift_x_key = K_LEFT
                self.last_shift = 0
            elif event.key == K_DOWN and keystate[K_UP]:
                self.shift_y_key = K_UP
                self.last_shift = 0

    def keyboard_state(self, keystate, mx, my):
        if time.time() - self.last_shift > DEFAULT_MAP_SHIFT_INTERVAL:
            map_modified = False
            if keystate[K_RIGHT] and self.shift_x_key == K_RIGHT and \
              self.visual_start[0] + len(self.visual_data[self.layer_id][0]) < \
              self.cwidth * len(self.data[self.layer_id][0][1][0]):
                self.map.x -= DEFAULT_MAP_SHIFT * self.vtilesize
                map_modified = True
            if keystate[K_DOWN] and self.shift_y_key == K_DOWN and \
              self.visual_start[1] + len(self.visual_data[self.layer_id]) < \
              self.cheight * len(self.data[self.layer_id][0][1]):
                self.map.y -= DEFAULT_MAP_SHIFT * self.vtilesize
                map_modified = True
            if keystate[K_LEFT] and self.shift_x_key == K_LEFT and self.visual_start[0]:
                self.map.x += DEFAULT_MAP_SHIFT * self.vtilesize
                map_modified = True
            if keystate[K_UP] and self.shift_y_key == K_UP and self.visual_start[1]:
                self.map.y += DEFAULT_MAP_SHIFT * self.vtilesize
                map_modified = True
            if map_modified:
                self.last_shift = time.time()
                mcfx, mcfy = mx - self._x - self.foreground_left, my - self._y - self.foreground_top
                self.update_mouse_tile(True, mcfx, mcfy, False)
                self.update_visual_data(False)
                self.update_mouse_tile(True, mcfx, mcfy)
                self.update_ptile(True)
                # print(self.visual_start)
        if keystate[K_LCTRL]:
            self.update_ptile()

    def update_zoom(self, keystate):
        """should only be called if mouse on self"""
        if self.vtilesize != self.tilesize << 4:
            if keystate[K_LCTRL]:
                if keystate[K_LSHIFT]:
                    shift = abs(self.tilesize.bit_length() - self.vtilesize.bit_length())
                    if self.tilesize > self.vtilesize:
                        closest = self.tilesize >> shift
                        self.vtilesize = (closest if closest > self.vtilesize \
                            else self.tilesize >> shift - 1)
                    else:
                        closest = self.tilesize << shift
                        self.vtilesize = (closest if closest > self.vtilesize \
                            else self.tilesize << shift + 1)
                else:
                    self.vtilesize += DEFAULT_MAP_ZOOM
                self.vtilesize = min(self.vtilesize, self.tilesize << 4)
                self.create_map()
                self.draw_map()

    def update_unzoom(self, keystate):
        """should only be called if mouse on self"""
        if self.vtilesize != 1:
            if keystate[K_LCTRL]:
                if keystate[K_LSHIFT]:
                    shift = abs(self.tilesize.bit_length() - self.vtilesize.bit_length())
                    if self.tilesize >= self.vtilesize:
                        closest = self.tilesize >> shift
                        self.vtilesize = (closest if closest < self.vtilesize \
                            else self.tilesize >> shift + 1)
                    else:
                        closest = self.tilesize << shift
                        self.vtilesize = (closest if closest < self.vtilesize \
                            else self.tilesize << shift - 1)
                else:
                    self.vtilesize -= DEFAULT_MAP_ZOOM
                self.vtilesize = max(self.vtilesize, 1)
                self.create_map()
                self.draw_map()

    def draw_block(self, i, j, surface=None, visual_data=None):
        if surface is None:
            surface = self.map.surface
        i_scaled, j_scaled = i * self.vtilesize, j * self.vtilesize
        surface.fill(self.background_color, (j_scaled, i_scaled, self.vtilesize, self.vtilesize))
        vdata = visual_data if visual_data is not None else self.visual_data
        for layer_id in range(len(vdata)):
            id = vdata[layer_id][i][j]
            block = pygame.Surface((self.vtilesize, self.vtilesize), SRCALPHA)
            if id:
                path, k, l = self.app_blocks.id_to_path[id]
                path = path.split('\\')
                p = ''
                for pa in path:
                    p += pa + '/'
                path = p[:-1]
                try:
                    image = pygame.image.load(path).convert_alpha()
                except pygame.error:  # image has been deleted
                    image = pygame.Surface((self.vtilesize, self.vtilesize), SRCALPHA)
                block.blit(image, (-l*self.vtilesize, -k*self.vtilesize))
            elif not layer_id:
                block.fill(self.map.color)
            if not layer_id:
                surface.fill(self.background_color, (j_scaled, i_scaled, self.vtilesize, self.vtilesize))
            surface.blit(block, (j_scaled, i_scaled))

    def get_block_by_id(self, id):
        path, i, j = self.app_blocks.id_to_path[id]
        path = path.split('\\')
        p = ''
        for pa in path:
            p += pa + '/'
        path = p[:-1]
        i_scaled, j_scaled = i * self.vtilesize, j * self.vtilesize
        block = pygame.Surface((self.vtilesize, self.vtilesize), SRCALPHA)
        try:
            image = pygame.image.load(path).convert_alpha()
            block.blit(image, (-j_scaled, -i_scaled))
        except pygame.error:
            pass
        return block

    def apply_bucket(self, id, i, j):
        old_id = self.visual_data[self.layer_id][i][j]
        if old_id != id:
            vx, vy = self.visual_start  # v: visual
            undos = [[self.layer_id, old_id, *self.convert_y_x_to_chunk_id(vy+i, vx+j)]]
            if not self.should_add_undo:
                self.should_add_undo = True
            self.visual_data[self.layer_id][i][j] = id
            self.draw_block(i, j)
            todo_coords = [(i, j)]
            while todo_coords:
                ci, cj = todo_coords[0]  # c: current
                for (k, l) in self.get_neighboring_tiles(ci, cj):
                    try:
                        if k >= 0 and l >= 0:
                            if self.visual_data[self.layer_id][k][l] == old_id:
                                undos.append([self.layer_id, old_id, *self.convert_y_x_to_chunk_id(vy+k, vx+l)])
                                if not self.should_add_undo:
                                    self.should_add_undo = True
                                self.visual_data[self.layer_id][k][l] = id
                                self.draw_block(k, l)
                                todo_coords.append((k, l))
                    except IndexError:  # coords out of map
                        pass
                todo_coords.pop(0)
            if undos:
                set_undo(undos)

    def update_block(self, draw_on_self=True, mode=0):
        """
        mode: 0: place block, 1: delete block
        """
        if self.mouse_tile and self.layer_id is not None:
            draw = False
            old_undo = self.should_add_undo
            undos = []
            vx, vy = self.visual_start  # v: visual
            x, y = self.mouse_tile[0], self.mouse_tile[1]
            j, i = x // self.vtilesize, y // self.vtilesize
            if not mode and self.block_id:  # place block
                path, id, rows, columns = self.block_id
                if not self.draw_mode:  # pen mode
                    for k in range(rows):
                        for l in range(columns):
                            try:
                                ci, cj = i + k, j + l  # c: current
                                saved_id = self.visual_data[self.layer_id][ci][cj]
                                undos.append([ \
                                    self.layer_id, saved_id,
                                    *self.convert_y_x_to_chunk_id(vy+ci, vx+cj)])
                                if not self.should_add_undo:
                                    self.should_add_undo = True
                                self.visual_data[self.layer_id][ci][cj] = \
                                    self.app_blocks.path_to_id['%s/%d/%d' % (path, k, l)][0]
                                self.draw_block(ci, cj)
                            except IndexError:
                                pass  # the block can not be drawn in the visual area
                else:  # bucket mode
                    self.apply_bucket(id, i, j)
                self.mouse_tile[3] = 1  # the block has been placed
                draw = True
            elif self.visual_data[self.layer_id][i][j]:  # delete block
                if not self.draw_mode:
                    saved_id = self.visual_data[self.layer_id][i][j]
                    undos.append([self.layer_id, saved_id, *self.convert_y_x_to_chunk_id(vy+i, vx+j)])
                    if not self.should_add_undo:
                        self.should_add_undo = True
                    self.visual_data[self.layer_id][i][j] = 0
                else:
                    self.apply_bucket(0, i, j)
                self.mouse_tile[3] = 0  # the block can be replaced
                self.draw_block(i, j)
                draw = True
            if draw:
                self.draw_map(False)
                self.draw_alpha_mask_on_tile(x, y, False, draw_on_self)
            if undos:
                set_undo(undos)
            if not old_undo and self.should_add_undo:
                self.undo_numbers += 1

    def update_visual_data(self, draw_on_self=True):
        start_x, start_y = self.visual_start
        tile_shift_width = self.map.x // self.vtilesize
        map = pygame.Surface((self.map.width, self.map.height))
        map.blit(self.map.surface, (self.map.left, 0))
        data_to_save = []
        if tile_shift_width < 0:  # load right, save left
            for _ in range(-tile_shift_width):
                for layer_id in range(len(self.visual_data)):
                    j = start_x % DEFAULT_MAP_CHUNK_SIZE
                    chunk_j = (start_x - j) // DEFAULT_MAP_CHUNK_SIZE
                    # to load data:
                    new_x = start_x + len(self.visual_data[layer_id][0])
                    new_j = new_x % DEFAULT_MAP_CHUNK_SIZE
                    new_chunk_j = (new_x - new_j) // DEFAULT_MAP_CHUNK_SIZE
                    for row in range(len(self.visual_data[layer_id])):  # range(i)
                        current_y = start_y + row
                        i = current_y % DEFAULT_MAP_CHUNK_SIZE
                        chunk_i = (current_y - i) // DEFAULT_MAP_CHUNK_SIZE
                        chunk_id = chunk_i * self.cwidth + chunk_j
                        id = self.visual_data[layer_id][row].pop(0)
                        # print(layer_id, chunk_id, i, j, id)
                        data_to_save.append([layer_id, chunk_id, i, j, id])
                        # to load data:
                        new_i = current_y % DEFAULT_MAP_CHUNK_SIZE
                        new_chunk_i = (current_y - new_i) // DEFAULT_MAP_CHUNK_SIZE
                        new_chunk_id = new_chunk_i * self.cwidth + new_chunk_j
                        new_id = self.data[layer_id][new_chunk_id][1][new_i][new_j]
                        # print(layer_id, new_chunk_id, new_i, new_j, new, id)
                        self.visual_data[layer_id][row].append(new_id)
                        if new_id:
                            block = self.get_block_by_id(new_id)
                        else:
                            block = pygame.Surface((self.vtilesize, self.vtilesize), SRCALPHA)
                            block.fill(self.map.color if not layer_id else TRANSPARENT)
                        x = (len(self.visual_data[layer_id][row]) - 1) * self.vtilesize
                        y = row * self.vtilesize
                        if not layer_id:
                            map.fill(self.background_color, (x, y, self.vtilesize, self.vtilesize))
                        map.blit(block, (x, y))
                start_x += 1
        elif tile_shift_width > 0:  # load left, save right
            for _ in range(tile_shift_width):
                for layer_id in range(len(self.visual_data)):
                    end_x = start_x + len(self.visual_data[layer_id][0]) - 1
                    j = end_x % DEFAULT_MAP_CHUNK_SIZE
                    chunk_j = (end_x - j) // DEFAULT_MAP_CHUNK_SIZE
                    # to load data :
                    new_x = start_x - 1
                    new_j = new_x % DEFAULT_MAP_CHUNK_SIZE
                    new_chunk_j = (new_x - new_j) // DEFAULT_MAP_CHUNK_SIZE
                    for row in range(len(self.visual_data[layer_id])):  # range(i)
                        current_y = start_y + row
                        i = current_y % DEFAULT_MAP_CHUNK_SIZE
                        chunk_i = (current_y - i) // DEFAULT_MAP_CHUNK_SIZE
                        chunk_id = chunk_i * self.cwidth + chunk_j
                        id = self.visual_data[layer_id][row].pop()
                        data_to_save.append([layer_id, chunk_id, i, j, id])
                        # to load data:
                        new_i = current_y % DEFAULT_MAP_CHUNK_SIZE
                        new_chunk_i = (current_y - new_i) // DEFAULT_MAP_CHUNK_SIZE
                        new_chunk_id = new_chunk_i * self.cwidth + new_chunk_j
                        new_id = self.data[layer_id][new_chunk_id][1][new_i][new_j]
                        # print(new_id, new_i, new_j, new_chunk_id)
                        self.visual_data[layer_id][row].insert(0, new_id)
                        if new_id:
                            block = self.get_block_by_id(new_id)
                        else:
                            block = pygame.Surface((self.vtilesize, self.vtilesize), SRCALPHA)
                            block.fill(self.map.color if not layer_id else TRANSPARENT)
                        y = row * self.vtilesize
                        if not layer_id:
                            map.fill(self.background_color, (0, y, self.vtilesize, self.vtilesize))
                        map.blit(block, (0, y))
                start_x -= 1
        self.save_data(data_to_save)
        tile_shift_height = self.map.y // self.vtilesize
        save = map
        map = pygame.Surface((self.map.width, self.map.height))
        map.blit(save, (0, self.map.top))
        data_to_save = []
        if tile_shift_height < 0:  # load bottom, save top
            for _ in range(-tile_shift_height):
                for layer_id in range(len(self.visual_data)):
                    i = start_y % DEFAULT_MAP_CHUNK_SIZE
                    chunk_i = (start_y - i) // DEFAULT_MAP_CHUNK_SIZE
                    # to load data:
                    new_y = start_y + len(self.visual_data[layer_id])
                    new_i = new_y % DEFAULT_MAP_CHUNK_SIZE
                    new_chunk_i = (new_y - new_i) // DEFAULT_MAP_CHUNK_SIZE
                    self.visual_data[layer_id].append([])
                    for columns in range(len(self.visual_data[layer_id][0])):  # range(j)
                        current_x = start_x + columns
                        j = current_x % DEFAULT_MAP_CHUNK_SIZE
                        chunk_j = (current_x - j) // DEFAULT_MAP_CHUNK_SIZE
                        chunk_id = chunk_i * self.cwidth + chunk_j
                        id = self.visual_data[layer_id][0][columns]
                        data_to_save.append([layer_id, chunk_id, i, j, id])
                        # to load data:
                        new_j = current_x % DEFAULT_MAP_CHUNK_SIZE
                        new_chunk_j = (current_x - new_j) // DEFAULT_MAP_CHUNK_SIZE
                        new_chunk_id = new_chunk_i * self.cwidth + new_chunk_j
                        # print(new_chunk_i, new_chunk_j, new_chunk_id)
                        new_id = self.data[layer_id][new_chunk_id][1][new_i][new_j]
                        self.visual_data[layer_id][-1].append(new_id)
                        if new_id:
                            block = self.get_block_by_id(new_id)
                        else:
                            block = pygame.Surface((self.vtilesize, self.vtilesize), SRCALPHA)
                            block.fill(self.map.color if not layer_id else TRANSPARENT)
                        x = columns * self.vtilesize
                        y = (len(self.visual_data[layer_id]) - 2) * self.vtilesize
                        # -2 because we created new empty list
                        if not layer_id:
                            map.fill(self.background_color, (x, y, self.vtilesize, self.vtilesize))
                        map.blit(block, (x, y))
                    self.visual_data[layer_id].pop(0)
                start_y += 1
        elif tile_shift_height > 0:  # load top, save bottom
            for _ in range(tile_shift_height):
                for layer_id in range(len(self.visual_data)):
                    end_y = start_y + len(self.visual_data[layer_id]) - 1
                    i = end_y % DEFAULT_MAP_CHUNK_SIZE
                    chunk_i = (end_y - i) // DEFAULT_MAP_CHUNK_SIZE
                    # to load data :
                    new_y = start_y - 1  # -1 because start_y has not been incremented yet
                    new_i = new_y % DEFAULT_MAP_CHUNK_SIZE
                    new_chunk_i = (new_y - new_i) // DEFAULT_MAP_CHUNK_SIZE
                    self.visual_data[layer_id].insert(0, [])
                    for columns in range(len(self.visual_data[layer_id][1])):  # range(j)
                        current_x = start_x + columns
                        j = current_x % DEFAULT_MAP_CHUNK_SIZE
                        chunk_j = (current_x - j) // DEFAULT_MAP_CHUNK_SIZE
                        chunk_id = chunk_i * self.cwidth + chunk_j
                        id = self.visual_data[layer_id][-1][columns]
                        data_to_save.append([layer_id, chunk_id, i, j, id])
                        # to load data:
                        new_j = current_x % DEFAULT_MAP_CHUNK_SIZE
                        new_chunk_j = (current_x - new_j) // DEFAULT_MAP_CHUNK_SIZE
                        new_chunk_id = new_chunk_i * self.cwidth + new_chunk_j
                        new_id = self.data[layer_id][new_chunk_id][1][new_i][new_j]
                        self.visual_data[layer_id][0].append(new_id)
                        if new_id:
                            block = self.get_block_by_id(new_id)
                        else:
                            block = pygame.Surface((self.vtilesize, self.vtilesize), SRCALPHA)
                            block.fill(self.map.color if not layer_id else TRANSPARENT)
                        # y = row * self.vtilesize
                        x = columns * self.vtilesize
                        if not layer_id:
                            map.fill(self.background_color, (x, 0, self.vtilesize, self.vtilesize))
                        map.blit(block, (x, 0))
                    self.visual_data[layer_id].pop()
                start_y -= 1
        # print(data_to_save)
        self.save_data(data_to_save)
        self.map.surface = map
        self.map.topleft = ORIGIN
        self.visual_start = start_x, start_y
        # print(self.visual_start)
        # print(self.visual_data)
        self.draw_map()
        if self.mouse_tile:
            self.draw_alpha_mask_on_tile(self.mouse_tile[0], self.mouse_tile[1], False, draw_on_self)

    def save_data(self, data):
        for layer_id, chunk_id, i, j, id in data:
            self.data[layer_id][chunk_id][1][i][j] = id

    def update_mouse_tile(self, mouse_on_app, mcfx=None, mcfy=None, down=False, draw_on_self=True):
        if mouse_on_app and (swapcore.kernel.App.app_specs[0].id == self.id or down):
            mcmx, mcmy = mcfx - self.map.x, mcfy - self.map.y  # cm: converted (to) map (coord system)
            if self.is_mouse_on_map(mcmx, mcmy) and mcmx < self.map.width and mcmy < self.map.height:
                tile_x = mcmx - mcmx % self.vtilesize
                tile_y = mcmy - mcmy % self.vtilesize
                if not self.mouse_tile or (tile_x, tile_y) != (self.mouse_tile[0], self.mouse_tile[1]):
                    self.draw_alpha_mask_on_tile(tile_x, tile_y, True, draw_on_self)
                    j, i = tile_x // self.vtilesize, tile_y // self.vtilesize
                    is_placed = 1 if (self.block_id and self.visual_data[self.layer_id][i][j] == self.block_id[1]) else 0
                    self.mouse_tile = [tile_x, tile_y, self.vtilesize, is_placed]
            elif self.mouse_tile:
                self.clear_old_mouse_tile()
                self._surface.blit(self.foreground, self.foreground_topleft)
                self.mouse_tile = 0
        elif self.mouse_tile:
            self.clear_old_mouse_tile()
            self._surface.blit(self.foreground, self.foreground_topleft)
            self.mouse_tile = 0

    def clear_old_mouse_tile(self):
        if self.mouse_tile[2] == self.vtilesize:
            x, y = self.mouse_tile[0] + self.map.x, self.mouse_tile[1] + self.map.y
            j, i = self.mouse_tile[0] // self.vtilesize, self.mouse_tile[1] // self.vtilesize
            self.draw_block(i, j, self.foreground)
            if self.grid:
                x, y = self.mouse_tile[0] + self.map.x,self.mouse_tile[1] + self.map.y
                self.draw_grid_on_one_tile(x, y)

    def update_ptile(self, down=False):
        if self.mouse_tile:
            coords = (self.mouse_tile[0], self.mouse_tile[1])  # (x, y)
            if coords != self.ptile or down:
                self.clear_old_ptile()
                self.ptile = coords
                i, j = self.ptile[1] // self.vtilesize, self.ptile[0] // self.vtilesize
                x = j + self.visual_start[0]
                y = i + self.visual_start[1]
                id = self.visual_data[self.layer_id][i][j]
                # id = self.data[self.layer_id][chunk_id][1][i][j]
                chunk_id, k, l = self.convert_y_x_to_chunk_id(y, x)
                for name, value in zip(['x, y', 'id', 'layer id', 'chunk id', 'j, i'],
                                       [(x, y), id, self.layer_id, chunk_id, (l, k)]):
                    self.app_properties.add_row('{} : {}'.format(name, value))
                self.app_properties.scrollwidget.new_row_id = 1
                chunk_id, k, l = self.convert_y_x_to_chunk_id(y, x)
                key = '%d_%d' % (x, y)
                try:  # name: names of block's properties
                    for name in self.data[self.layer_id][chunk_id][0][key]:
                        mode, value = self.data[self.layer_id][chunk_id][0][key][name]
                        self.app_properties.add_row('{} : {} : {}'.format(name, mode, value))
                except KeyError:
                    pass

    def clear_old_ptile(self):
        while len(self.app_properties.scrollwidget.scrollarea.listing) > 3:
            self.app_properties.delete_row(0, True)
        self.app_properties.scrollwidget.new_row_id = 1

    def draw_alpha_mask_on_tile(self, tile_x, tile_y, clear_old=True, on_surface=True):
        alpha_mask = pygame.Surface((self.vtilesize, self.vtilesize), SRCALPHA)
        alpha_mask.fill(DEFAULT_MAP_ALPHA_MAK_COLOR)
        tcfx, tcfy = tile_x + self.map.x, tile_y + self.map.y  # tile converted to foreground
        self.foreground.blit(alpha_mask, (tcfx, tcfy))
        if self.grid:
            self.draw_grid_on_one_tile(tcfx, tcfy)
        if self.mouse_tile and clear_old:
            self.clear_old_mouse_tile()
        if on_surface:
            self._surface.blit(self.foreground, self.foreground_topleft)

    def is_mouse_on_map(self, mcmx, mcmy):  # cm: converted (to) map (coord system)
        return 0 <= mcmx <= self.map.width and 0 <= mcmy <= self.map.height

    def load_data(self, new=False):
        self.map, self.data, self.visual_data, self.visual_start = self.initialize_data(load_from_file=not new)
        self.grid = self.create_grid()
        self.draw_map()
        self._surface.blit(self.foreground, self.foreground_topleft)

    def initialize_data(self,
      chunk_width=DEFAULT_MAP_CHUNK_WIDTH,
      chunk_height=DEFAULT_MAP_CHUNK_HEIGHT,
      chunk_size=DEFAULT_MAP_CHUNK_SIZE, load_from_file=True, new_data=False):
        default_tw = chunk_width * chunk_size  # tw: tile width
        default_th = chunk_height * chunk_size  # th: tile height
        max_tw = self.foreground_width // self.tilesize + 1
        max_th = self.foreground_height // self.tilesize + 1
        tw, th = min(default_tw, max_tw), min(default_th, max_th)
        if load_from_file and not new_data:
            map = swapcore.kernel.Area(
                 tw*self.tilesize, th*self.tilesize, 0, 0, color=self.foreground_color)
            visual_start, visual_data, data = load_data_from_file(self.filename, index=3)
            for layer_id in range(len(data)):
                for chunk_id in range(len(data[layer_id])):
                    if not isinstance(data[layer_id][chunk_id][0], dict):
                        data[layer_id][chunk_id][0] = dict()  # initialize properties
            for i in range(len(visual_data[0])):
                for j in range(len(visual_data[0][i])):
                    self.draw_block(i, j, map.surface, visual_data)
            return map, data, visual_data, visual_start
        else:
            data = [[[], []] for _ in range(chunk_width*chunk_height)]
            for chunk_infos, block_data in data:
                for _ in range(chunk_size):
                    block_data.append([0 for _ in range(chunk_size)])
            visual_data = [[0 for _ in range(tw)] for _ in range(th)]
            if not new_data:
                visual_start = [0, 0]
                map = swapcore.kernel.Area(
                     tw*self.tilesize, th*self.tilesize, 0, 0, color=self.foreground_color)
                return map, [data], [visual_data], visual_start
            else:
                return data, visual_data

    def create_map(self):
        """deprecated"""
        if self.vtilesize % self.tilesize:
            if not self.lossless_map:
                # map is not proportional to original so save lossless original
                self.lossless_map = pygame.transform.scale(
                    self.map.surface, (self.twidth*self.tilesize, self.theight*self.tilesize))
        elif self.lossless_map:
            self.lossless_map = 0
        width = self.twidth * self.vtilesize
        height = self.theight * self.vtilesize
        self.map = swapcore.kernel.Area(
            width, height,
            round(self.map.x*(width/self.map.width)), round(self.map.y*(height/self.map.height)),
            pygame.transform.scale(
                self.map.surface,
                (self.twidth*self.vtilesize, self.theight*self.vtilesize)),
            self.foreground_color)
        if self.grid:
            self.grid = self.create_grid()

    def reduce_map(self):
        """
        should only be called in exceptional circumstances,
        and x1, y1, x2, y2 should be modified to fit the specific case
        """
        x1, y1, x2, y2 = 352, 352, 768, 608
        cwidth, cheight = (x2 - x1) // 32, (y2 - y1) // 32  # c: chunk
        twidth = cwidth * DEFAULT_MAP_CHUNK_SIZE  # c: chunk
        theight = cheight * DEFAULT_MAP_CHUNK_SIZE  # c: chunk
        map, data, visual_data, visual_start = \
            self.initialize_data(cwidth, cheight, DEFAULT_MAP_CHUNK_SIZE, False)
        for layer_id in range(len(data)):
            for chunk_id in range(len(data[layer_id])):
                data[layer_id][chunk_id][0] = dict()  # initialize properties
        for layer_id in range(len(self.data)-1):  # -1 because 1 layer already initialized
            d, v = self.initialize_data(cwidth, cheight, DEFAULT_MAP_CHUNK_SIZE, False, True)
            data.append(d)
            visual_data.append(v)
        for layer_id in range(len(self.data)):
            x = x1
            while x < x2:
                y = y1
                while y < y2:
                    chunk_id, i, j = self.convert_y_x_to_chunk_id(y, x)
                    id = self.data[layer_id][chunk_id][1][i][j]
                    cid, k, l = self.convert_y_x_to_chunk_id(y-y1, x-x1, cwidth=cwidth)
                    data[layer_id][cid][1][k][l] = id
                    y += 1
                x += 1
        self.load_visual_data_from_data(visual_data, visual_start, data, cwidth)
        self.load_map_from_visual_data(map.surface, visual_data)
        self.cwidth, self.cheight = cwidth, cheight
        self.twidth, self.theight = twidth, theight
        self.map, self.data, self.visual_data, self.visual_start = \
            map, data, visual_data, visual_start
        self.draw_map()
        if self.mouse_tile:
            self.draw_alpha_mask_on_tile(self.mouse_tile[0], self.mouse_tile[1], False)
        self.update_ptile(True)
        print('new cwidth: %d, new cheight: %d' % (cwidth, cheight))

    def load_visual_data_from_data(self, visual_data, visual_start, data, cwidth=None):
        width, height = len(visual_data[0][0]), len(visual_data[0])
        x1, y1 = visual_start
        x2, y2 = x1 + width, y1 + height
        for layer_id in range(len(data)):
            x = x1
            while x < x2:
                y = y1
                while y < y2:
                    chunk_id, i, j = self.convert_y_x_to_chunk_id(y, x, cwidth=cwidth)
                    id = data[layer_id][chunk_id][1][i][j]
                    visual_data[layer_id][y-y1][x-x1] = id
                    y += 1
                x += 1

    def load_map_from_visual_data(self, map, visual_data):
        for layer_id, layer in enumerate(visual_data):
            for i, row in enumerate(layer):
                for j, column in enumerate(row):
                    self.draw_block(i, j, map, visual_data)

    def draw_map(self, draw_on_self=True):
        self.foreground.fill(self.background_color)
        self.foreground.blit(self.map.surface, self.map.topleft)
        if self.grid:
            self.foreground.blit(self.grid, self.map.topleft)
        if draw_on_self:
            self._surface.blit(self.foreground, self.foreground_topleft)

    def create_grid(self):
        grid = pygame.Surface((self.map.width+1, self.map.height+1), SRCALPHA)  # +1 for last line
        for i in range(self.twidth+1):
            x = i * self.vtilesize
            pygame.draw.line(grid, DEFAULT_MAP_GRID_COLOR, (x, 0), (x, self.map.height))
        for j in range(self.theight+1):
            y = j * self.vtilesize
            pygame.draw.line(grid, DEFAULT_MAP_GRID_COLOR, (0, y), (self.map.width, y))
        return grid

    def draw_grid_on_one_tile(self, tcfx, tcfy):  # tile converted (to) foreground (coord system)
        x2 = tcfx + self.vtilesize
        y2 = tcfy + self.vtilesize
        pygame.draw.line(self.foreground, DEFAULT_MAP_GRID_COLOR, (tcfx, tcfy), (x2, tcfy))
        pygame.draw.line(self.foreground, DEFAULT_MAP_GRID_COLOR, (tcfx, y2), (x2, y2))
        pygame.draw.line(self.foreground, DEFAULT_MAP_GRID_COLOR, (tcfx, tcfy), (tcfx, y2))
        pygame.draw.line(self.foreground, DEFAULT_MAP_GRID_COLOR, (x2, tcfy), (x2, y2))

    def perform_undo(self, undo):
        self.save_data(undo)
        vx, vy = self.visual_start
        max_vi = len(self.visual_data[self.layer_id]) - 1  # v: visual
        max_vj = len(self.visual_data[self.layer_id][0]) - 1
        for layer_id, chunk_id, i, j, id in undo:
            chunk_i, chunk_j = self.get_chunk_i_j_from_id(chunk_id)
            vi = chunk_i * DEFAULT_MAP_CHUNK_SIZE + i - vy
            vj = chunk_j * DEFAULT_MAP_CHUNK_SIZE + j - vx
            if 0 <= vi <= max_vi and 0 <= vj <= max_vj:
                self.visual_data[layer_id][vi][vj] = id
                self.draw_block(vi, vj)
        self.draw_map()
        if self.mouse_tile:
            self.draw_alpha_mask_on_tile(self.mouse_tile[0], self.mouse_tile[1], False)
        self.undo_numbers -= 1

    def get_tile_x_y_from_visual(self, x, y):
        return (x // self.vtilesize + self.visual_start[0],
                y // self.vtilesize + self.visual_start[1])

    def convert_y_x_to_chunk_id(self, y, x, return_chunk_i_j=False, cwidth=None):
        i = y % DEFAULT_MAP_CHUNK_SIZE
        chunk_i = (y - i) // DEFAULT_MAP_CHUNK_SIZE
        j = x % DEFAULT_MAP_CHUNK_SIZE
        chunk_j = (x - j) // DEFAULT_MAP_CHUNK_SIZE
        chunk_id = chunk_i * (cwidth if cwidth else self.cwidth) + chunk_j
        if return_chunk_i_j:
            return chunk_id, chunk_i, chunk_j
        else:
            return chunk_id, i, j

    def get_chunk_i_j_from_id(self, chunk_id):
        return chunk_id // self.cwidth, chunk_id % self.cwidth

    @staticmethod
    def get_neighboring_tiles(i, j):
        return [(i, j - 1), (i - 1, j), (i, j + 1), (i + 1, j)]


class AppBlocks(swapcore.kernel.App):
    def __init__(self, font, appmanager):
        self.icon = draw_icon(
            'blocks', DEFAULT_APP_ICON_TILESIZE, DEFAULT_APP_ICON_LINESIZE,
            DEFAULT_ICON_BLOCKS_COLOR)
        self.dock_icon = draw_icon(
            'blocks', DEFAULT_DOCK_APP_ICON_TILESIZE,
            DEFAULT_DOCK_APP_ICON_LINESIZE,
            DEFAULT_ICON_BLOCKS_COLOR)
        self.borders = percent_border_to_px(
            appmanager.desk.width//4,
            int(appmanager.desk.height-2*appmanager.desk.width//128-DEFAULT_APP_TITLEBAR_HEIGHT),
            0, DEFAULT_APP_TITLEBAR_HEIGHT,
            DEFAULT_APP_BORDER_PERCENT, DEFAULT_APP_BORDER_REFERENCE)
        self.border_width = self.borders[2]
        super().__init__(
            self.icon,
            'blocks',
            DEFAULT_APP_NAME_COLOR,
            font,
            appmanager.desk.width//4,
            int(appmanager.desk.height-2*appmanager.desk.width//128-DEFAULT_APP_TITLEBAR_HEIGHT),
            appmanager.desk.right-appmanager.desk.width//4-appmanager.desk.width//128,
            appmanager.desk.top+DEFAULT_APP_TITLEBAR_HEIGHT+appmanager.desk.width//128,
            DEFAULT_APP_BACKGROUND_COLOR,
            0,
            DEFAULT_APP_TITLEBAR_HEIGHT,
            DEFAULT_APP_TITLEBAR_COLOR,
            DEFAULT_APP_TITLEBAR_BUTTON_RADIUS,
            *self.borders,
            DEFAULT_APP_FOREGROUND_COLOR,
            DEFAULT_MINIMIZE_BUTTON_COLOR,
            DEFAULT_MINIMIZE_BUTTON_OVER_COLOR,
            DEFAULT_MINIMIZE_BUTTON_DOWN_COLOR,
            DEFAULT_MAXIMIZE_BUTTON_COLOR,
            DEFAULT_MAXIMIZE_BUTTON_OVER_COLOR,
            DEFAULT_MAXIMIZE_BUTTON_DOWN_COLOR,
            DEFAULT_CLOSE_BUTTON_COLOR,
            DEFAULT_CLOSE_BUTTON_OVER_COLOR,
            DEFAULT_CLOSE_BUTTON_DOWN_COLOR,
            0, 0,
            PROGRAM_WIDTH,
            PROGRAM_HEIGHT,
            2)
        self.appmanager = appmanager
        self.filename = 'map.swptm'
        # must be initialized later with a linking function:
        self.app_map, self.app_layers, self.app_properties = None, None, None
        half = self.border_width // 2
        self.selection = ScrollArea(
            self.borders[0], self.borders[1]*3//4-half,
            *self.foreground_topleft,
            color=self.foreground_color)
        self.folders = ScrollArea(
            self.borders[0], self.borders[1]//4-half,
            self.foreground_left, self.selection.bottom+self.border_width,
            color=self.foreground_color)
        self.foreground.fill(self.background_color)
        self._surface.blit(self.foreground, self.foreground_topleft)
        self.tilesize = DEFAULT_TILESIZE
        self.path_to_id, self.id_to_path = self.initialize_path_id()
        self.update_folders()
        try:
            self.update_selection(self.folders.listing[3][2])
        except IndexError:
            print('There are no image folders')
            self.selection.listing = [[(1, 1), 0, 0, 0]]  # arbitrary value

    def additional_mouse_event(self, mx, my, action_type, actions, mouse_on_app,
                               on_titlebar_button, keystate):
        queries_folders = [0]  # index 0: redraw
        queries_selection = 0
        if mouse_on_app:
            mcx, mcy = mx - self._x, my - self._y  # c: converted (to app coord system)
            if action_type == MOUSEBUTTONDOWN:
                indexes = self.click_on_block_selection(mcx, mcy)
                if indexes is not None and self.path_to_id:
                    index, dex = indexes
                    path = self.selection.listing[index][dex][1]
                    self.app_map.block_id = (path, *self.path_to_id[path+'/0/0'])
            elif action_type == MOUSEWHEELUP or action_type == MOUSEWHEELDOWN:
                actions.append(1)  # request focus
            queries_folders = self.folders.mouse_event(mouse_on_app, action_type, mcx, mcy)
            queries_selection = self.selection.scrollbar.mouse_event(mouse_on_app, action_type, mcx, mcy)
        else:
            queries_folders = self.folders.mouse_event(mouse_on_app, action_type)
            queries_selection = self.selection.scrollbar.mouse_event(mouse_on_app, action_type)
        if queries_folders[0]:
            self._surface.blit(self.folders.surface, self.folders.topleft)
        if queries_selection:
            self._surface.blit(self.selection.surface, self.selection.topleft)
        self.perform_queries(queries_folders, 0)

    def perform_queries(self, queries, id):  # id: 0: folders, 1: selection
        if not id:  # folders
            for query in queries[1:]:  # [1:] because index 0 is redraw
                if query[0] == 2:  # request click action:
                    self.update_selection(self.folders.listing[query[1]][2])

    def click_on_block_selection(self, mcx, mcy):
        if self.selection.mouse_over_self(mcx, mcy) and not self.selection.scrollbar.old_mcsx \
          and not self.selection.scrollbar.old_mcsy:
            # get mouse converted to block selection coord system
            mcsx = mcx - self.selection.x - self.selection.scrollbar.shift_x  - self.border_width
            mcsy = mcy - self.selection.y - self.selection.scrollbar.shift_y - self.border_width
            if mcsx >= 0 and mcsy >= 0:
                index = 0
                length = len(self.selection.listing)
                while index < length and mcsy > self.selection.listing[index][3]:
                    index += 1
                if index < length:
                    multiplier = self.selection.listing[index][2]
                    width = self.selection.listing[index][0][0] * multiplier + self.border_width
                    height = self.selection.listing[index][0][1] * multiplier + self.border_width
                    on_border = mcsx % width > width - self.border_width or \
                        mcsy % height > height - self.border_width
                    if not on_border:
                        i = mcsx // width
                        max_per_line = self.selection.listing[index][1]
                        if i < max_per_line:
                            start_y = self.selection.listing[index][3] - (0 if not index \
                                else self.selection.listing[index-1][3])
                            j = mcsy % start_y // height
                            dex = i + j * max_per_line + 4
                            if dex < len(self.selection.listing[index]):
                                return (index, dex)
        return  # the click is not on a block

    def get_rows_columns_from_image(self, image):
        columns = image.get_width() / self.tilesize
        if columns != int(columns):
            columns = int(columns) + 1
        rows = image.get_height() / self.tilesize
        if rows != int(rows):
            rows = int(rows) + 1
        return int(rows), int(columns)

    def initialize_path_id(self, load_from_file=True):
        if load_from_file:
            path_to_id, id_to_path = load_data_from_file(self.filename, 2, 1)
            id = id_to_path[-1] + 1
        else:
            path_to_id, id_to_path = {}, {}
            id = 1  # id 0 is the null block
        path = '../../data/images'
        dirnames = [dir for dir in os.listdir(path) if os.path.isdir(os.path.join(path, dir))]
        for dir in dirnames:
            dir_path = os.path.join(path, dir)
            for img in os.listdir(dir_path):
                image_path = os.path.join(dir_path, img)
                image = pygame.image.load(image_path).convert()
                rows, columns = self.get_rows_columns_from_image(image)
                for i in range(rows):
                    for j in range(columns):
                        key = '%s/%d/%d' % ( image_path, i, j)
                        try:
                            path_to_id[key]
                            continue  # block already in database
                        except KeyError:  # block not in database
                            path_to_id[key] = (id, rows, columns)
                            id_to_path[id] = (image_path, i, j)
                            id += 1
        id_to_path[-1] = id - 1  # save max id
        return path_to_id, id_to_path

    def update_folders(self):
        self.folders.list.surface = pygame.Surface((self.folders.width, 1))
        self.folders.list.surface.fill(self.folders.list.color)
        path = '../../data/images'
        double = 2 * self.border_width
        max_width = 0
        height = DEFAULT_LIST_FONT_SIZE + double
        self.folders.listing = [height, None, None]  # None, None: over, down
        for dirname in [dir for dir in os.listdir(path) if os.path.isdir(os.path.join(path, dir))]:
            name = self.font.render(dirname, DEFAULT_LIST_FONT_SIZE, DEFAULT_LIST_NAME_COLOR)
            width = double + name.get_width()
            if width > max_width:
                max_width = width
            line = pygame.Surface((width, height), SRCALPHA)
            line.blit(name, (self.border_width, self.border_width))
            if width > self.folders.list.width:
                self.folders.list.width = width
            total_height = height * (len(self.folders.listing) - 2)  # -2: + 1 for new & -3 for height, over, down
            if total_height > self.folders.list.height:
                self.folders.list.height = total_height
            self.folders.list.surface.blit(line, (0, height*(len(self.folders.listing)-3)))
            self.folders.listing.append([line, width, dirname])
        self.folders.scrollbar.update_vertical()
        if self.folders.scrollbar.vertical:
            available = self.folders.width - self.folders.scrollbar.vertical.width
            if max_width <= available:
                self.folders.list.width = available
        self.folders.scrollbar.update_horizontal()
        if self.folders.scrollbar.vertical or self.folders.scrollbar.horizontal:
            self.folders.scrollbar.draw()
        else:
            self.folders.surface.fill(self.folders.color)
            self.folders.surface.blit(self.folders.list.surface, ORIGIN)
        # self.folders.draw_list()
        self._surface.blit(self.folders.surface, self.folders.topleft)

    def update_selection(self, dirname):
        self.selection.list.surface = pygame.Surface((1, 1))
        self.selection.list.surface.fill(self.selection.list.color)
        self.selection.listing = []
        path = os.path.join('../../data/images', dirname)
        double = 2 * self.border_width
        images = os.listdir(path)
        if images:
            multiplier = 2
            blocks = self.get_blocks_from_images(
                [[pygame.image.load(os.path.join(path, image)).convert_alpha(), \
                 os.path.join(path, image)] for image in images], multiplier)
            start_x = self.border_width
            start_y = self.border_width
            max_y = []
            for size, max_per_line, *block in blocks:
                width, height = size[0] * multiplier, size[1] * multiplier
                for index, (image, _) in enumerate(block):  # _: path
                    i, j = index % max_per_line, index // max_per_line
                    x = start_x + i * (self.border_width + width)
                    y = start_y + j * (self.border_width + height)
                    total_width = x + width + self.border_width
                    total_height = y + height + self.border_width
                    if total_width > self.selection.list.width:
                        self.selection.list.width = total_width
                    if total_height > self.selection.list.height:
                        self.selection.list.height = total_height
                    scaled = (image if multiplier == 1 else \
                        pygame.transform.scale(image, (width, height)))
                    self.selection.list.surface.blit(scaled, (x, y))
                start_y = self.selection.list.height
                max_y.append(self.selection.list.height-self.border_width)  # -: first border before first block
            for index, y in enumerate(max_y):
                blocks[index].insert(2, y)
                blocks[index].insert(2, multiplier)
            self.selection.listing = blocks
            # listing = [[(w, h), max_per_line, multiplier, max_y, *block_image], ...]
        self.selection.scrollbar.update()
        if self.selection.scrollbar.vertical or self.selection.scrollbar.horizontal:
            self.selection.scrollbar.draw()
        else:
            self.selection.surface.fill(self.selection.color)
            self.selection.surface.blit(self.selection.list.surface, ORIGIN)
        self._surface.blit(self.selection.surface, self.selection.topleft)

    @staticmethod
    def get_sizes_from_images(images):
        s = {(image.get_width(), image.get_height()) for image in images}  # s: sizes
        sizes = [s.pop()]
        for size in s:
            i = 0
            length = len(sizes)
            while (i < length and size[1] > sizes[i][1]) or \
              (i < length and size[0] > sizes[i][0] and size[1] == sizes[i][1]):
                i += 1
            if i == length:
                sizes.append(size)
            else:
                sizes.insert(i, size)
        return sizes

    def get_blocks_from_images(self, data, multiplier):  # data : [images, path]
        images = [d[0] for d in data]
        path = [d[1] for d in data]
        sizes = self.get_sizes_from_images(images)
        blocks = [[size] for size in sizes]
        for block, path in zip(images, path):
            i = 0
            length = len(sizes)
            while (block.get_width(), block.get_height()) != sizes[i]:
                i += 1
            if i == length:
                i -= 1
            blocks[i].append([block, path])
        for index, size in enumerate(sizes):  # add max_per_line:
            blocks[index].insert(1, max(1, self.selection.width//(size[0]*multiplier+self.border_width)))
        return blocks


class AppProperties(swapcore.kernel.App):
    def __init__(self, font, appmanager):
        self.icon = draw_icon(
            'properties', DEFAULT_APP_ICON_TILESIZE, DEFAULT_APP_ICON_LINESIZE,
            DEFAULT_ICON_PROPERTIES_COLOR)
        self.dock_icon = draw_icon(
            'properties', DEFAULT_DOCK_APP_ICON_TILESIZE,
            DEFAULT_DOCK_APP_ICON_LINESIZE,
            DEFAULT_ICON_PROPERTIES_COLOR)
        width = appmanager.desk.width * 3 // 8
        height = appmanager.desk.height // 3
        self.borders = percent_border_to_px(
            width, height, 0, DEFAULT_APP_TITLEBAR_HEIGHT,
            DEFAULT_APP_BORDER_PERCENT, DEFAULT_APP_BORDER_REFERENCE)
        # self.border_width = self.borders[2]
        self.border_width = DEFAULT_APP_BORDER_PERCENT * DEFAULT_APP_BORDER_REFERENCE // 100
        foreground_height = height - 2 * DEFAULT_APP_TITLEBAR_HEIGHT - 3 * self.border_width
        super().__init__(
            self.icon,
            'properties',
            DEFAULT_APP_NAME_COLOR,
            font,
            width,
            height,
            appmanager.desk.left+appmanager.desk.width//128,
            appmanager.desk.top+DEFAULT_APP_TITLEBAR_HEIGHT+2*appmanager.desk.width//128+appmanager.desk.height//3,
            DEFAULT_APP_BACKGROUND_COLOR,
            0,
            DEFAULT_APP_TITLEBAR_HEIGHT,
            DEFAULT_APP_TITLEBAR_COLOR,
            DEFAULT_APP_TITLEBAR_BUTTON_RADIUS,
            *self.borders,
            DEFAULT_APP_FOREGROUND_COLOR,
            DEFAULT_MINIMIZE_BUTTON_COLOR,
            DEFAULT_MINIMIZE_BUTTON_OVER_COLOR,
            DEFAULT_MINIMIZE_BUTTON_DOWN_COLOR,
            DEFAULT_MAXIMIZE_BUTTON_COLOR,
            DEFAULT_MAXIMIZE_BUTTON_OVER_COLOR,
            DEFAULT_MAXIMIZE_BUTTON_DOWN_COLOR,
            DEFAULT_CLOSE_BUTTON_COLOR,
            DEFAULT_CLOSE_BUTTON_OVER_COLOR,
            DEFAULT_CLOSE_BUTTON_DOWN_COLOR,
            0, 0,
            PROGRAM_WIDTH,
            PROGRAM_HEIGHT,
            2)
        self.appmanager = appmanager
        # must be initialized later with a linking function:
        self.app_map, self.app_blocks, self.app_layers = None, None, None
        # ===== scroll widget =====
        scrollarea = ScrollArea(
            self.foreground_width, foreground_height,
            self.rx+self.border_width, self.ry+self.border_width,
            self.foreground, self.foreground_color)
        toolbar = swapcore.kernel.Area(
            self.width-2*self.border_width, self.titlebar_height+self.border_width,
            self.border_width, scrollarea.bottom,
            color=self.background_color)
        self.scrollwidget = ScrollWidget(self, scrollarea, toolbar, 'property')
        self._surface.blit(self.scrollwidget.scrollarea.surface, self.scrollwidget.scrollarea.topleft)
        self._surface.blit(self.scrollwidget.toolbar.surface, self.scrollwidget.toolbar.topleft)
        self.spreads = []

    def additional_mouse_event(self, mx, my, action_type, actions, mouse_on_app,
                               on_titlebar_button, keystate):
        if mouse_on_app:
            mcx, mcy = mx - self._x, my - self._y  # c: converted (to app coord system)
            if action_type == MOUSEWHEELUP or action_type == MOUSEWHEELDOWN:
                actions.append(1)  # request focus
            self.scrollwidget.mouse_event(mouse_on_app, action_type, mcx=mcx, mcy=mcy)
        else:
            self.scrollwidget.mouse_event(False, action_type, mx, my)

    def keyboard_event(self, event, keystate, mx, my):
        self.scrollwidget.keyboard_event(event, keystate, mx, my)

    def perform_queries(self, *arg):
        return

    def add_row(self, name=' ', surface=None, x=None):
        if self.app_map.ptile:
            width = self.scrollwidget.add_row(name)
            self.scrollwidget.scrollarea.listing[-1] += [name, width]

    def delete_row(self, y, resetting=False):
        """
        resetting is a boolean needed to delete x, y, id, layer id rows
        when we have to load the properties of a new tile
        """
        index = y // self.scrollwidget.scrollarea.listing[0]
        if y is not None and index > 6 or resetting:
            # called if index > 6, because can't delete x, y, id, layer id rows
            if not resetting:
                string = self.scrollwidget.scrollarea.listing[index+3][1]
                self.delete_property(string.split(':')[0].strip())
            self.scrollwidget.delete_row(y)

    def perform_row_creation(self, string):
        property = [s.strip() for s in string.split(':')]
        if property[2].isdigit():
            property[2] = int(property[2])
        self.spread_property(property)

    def spread_property(self, property):
        """
        should only be called if name, mode, value are valid (through is_focus_string_valid)
        property: [name, mode, value]
        mode list: default (no letter: same id), p (same Path), d (same Dir), i (Identical)
        spread list: o (Only), b (Bucket), a (All visible), v (oVerhaul)
        """
        print("property %s is spreading" % property)
        spreading = PropertySpreadingThread(self.app_map, property)
        spreading.start()
        self.spreads.append(spreading)

    def delete_property(self, name):
        x, y = self.app_map.get_tile_x_y_from_visual(*self.app_map.ptile)
        chunk_id, *_ = self.app_map.convert_y_x_to_chunk_id(y, x)
        key = '%d_%d' % (x, y)
        del self.app_map.data[self.app_map.layer_id][chunk_id][0][key][name]
        if not self.app_map.data[self.app_map.layer_id][chunk_id][0][key]:
            # the tile no longer has properties, so delete empty dict
            del self.app_map.data[self.app_map.layer_id][chunk_id][0][key]

    @staticmethod
    def is_focus_string_valid(string):
        decomposed = [s.strip() for s in string.split(':')]  # s: string
        if len(decomposed) == 3 and decomposed[1] in \
          ['o', 'b', 'bp', 'bd', 'bi', 'a', 'ap', 'ad', 'ai', 'v', 'vp', 'vd', 'vi']:
            return True
        return False


class AppLayers(swapcore.kernel.App):
    def __init__(self, font, appmanager):
        self.icon = draw_icon(
            'layers', DEFAULT_APP_ICON_TILESIZE, DEFAULT_APP_ICON_LINESIZE,
            DEFAULT_ICON_LAYERS_COLOR)
        self.dock_icon = draw_icon(
            'layers', DEFAULT_DOCK_APP_ICON_TILESIZE,
            DEFAULT_DOCK_APP_ICON_LINESIZE,
            DEFAULT_ICON_LAYERS_COLOR)
        self.border_width = DEFAULT_APP_BORDER_PERCENT * DEFAULT_APP_BORDER_REFERENCE // 100
        width = appmanager.desk.width * 3 // 8
        height = appmanager.desk.height // 3
        foreground_width = (width - 3 * self.border_width) // 2
        foreground_height = height - 2 * DEFAULT_APP_TITLEBAR_HEIGHT - 3 * self.border_width
        self.borders = (foreground_width, foreground_height,
                        self.border_width, self.border_width)
        super().__init__(
            self.icon,
            'layers',
            DEFAULT_APP_NAME_COLOR,
            font,
            width,
            height,
            appmanager.desk.left+appmanager.desk.width//128,
            appmanager.desk.top+DEFAULT_APP_TITLEBAR_HEIGHT+appmanager.desk.width//128,
            DEFAULT_APP_BACKGROUND_COLOR,
            0,
            DEFAULT_APP_TITLEBAR_HEIGHT,
            DEFAULT_APP_TITLEBAR_COLOR,
            DEFAULT_APP_TITLEBAR_BUTTON_RADIUS,
            *self.borders,
            DEFAULT_APP_FOREGROUND_COLOR,
            DEFAULT_MINIMIZE_BUTTON_COLOR,
            DEFAULT_MINIMIZE_BUTTON_OVER_COLOR,
            DEFAULT_MINIMIZE_BUTTON_DOWN_COLOR,
            DEFAULT_MAXIMIZE_BUTTON_COLOR,
            DEFAULT_MAXIMIZE_BUTTON_OVER_COLOR,
            DEFAULT_MAXIMIZE_BUTTON_DOWN_COLOR,
            DEFAULT_CLOSE_BUTTON_COLOR,
            DEFAULT_CLOSE_BUTTON_OVER_COLOR,
            DEFAULT_CLOSE_BUTTON_DOWN_COLOR,
            0, 0,
            PROGRAM_WIDTH,
            PROGRAM_HEIGHT,
            2)
        self.appmanager = appmanager
        self.filename = 'map.swptm'
        # must be initialized later with a linking function:
        self.app_map, self.app_blocks, self.app_properties = None, None, None
        # ===== scroll widget =====
        scrollarea = ScrollArea(
            foreground_width, foreground_height,
            self.rx+self.border_width, self.ry+self.border_width,
            self.foreground, self.foreground_color)
        toolbar = swapcore.kernel.Area(
            self.width-2*self.border_width, self.titlebar_height,
            self.border_width, scrollarea.bottom+self.border_width,
            color=self.background_color)
        self.scrollwidget = ScrollWidget(self, scrollarea, toolbar, 'layer')
        # self.scrollwidget.scrollarea.listing:
        # list of layers' eye & padlock state, width, height, name
        # ===== infos =====
        self.infos = swapcore.kernel.Area(
            self.scrollwidget.scrollarea.width, self.scrollwidget.scrollarea.height,
            self.scrollwidget.scrollarea.right+self.border_width, self.scrollwidget.scrollarea.top,
            self.foreground)
        # ===== drawings =====
        self._surface.blit(self.infos.surface, self.infos.topleft)
        # self.add_row('ground')
        layers_name = load_data_from_file(self.filename, amount=1)
        for name in layers_name:
            self.add_row(name, add_layer_to_map=False)

    def additional_mouse_event(self, mx, my, action_type, actions, mouse_on_app,
                               on_titlebar_button, keystate):
        if mouse_on_app:
            mcx, mcy = mx - self._x, my - self._y  # c: converted (to app coord system)
            if action_type == MOUSEWHEELUP or action_type == MOUSEWHEELDOWN:
                actions.append(1)  # request focus
            self.scrollwidget.mouse_event(mouse_on_app, action_type, mcx=mcx, mcy=mcy)
        else:
            self.scrollwidget.mouse_event(False, action_type, mx, my)

    def keyboard_event(self, event, keystate, mx, my):
        self.scrollwidget.keyboard_event(event, keystate, mx, my)

    def perform_queries(self, queries, old_selected_row):
        if old_selected_row != self.scrollwidget.scrollarea.listing[2]:
            self.app_map.layer_id = \
                self.scrollwidget.scrollarea.listing[2] // self.scrollwidget.scrollarea.listing[0]

    def add_row(self, name=' ', eye_state=1, padlock_state=1, add_layer_to_map=True):
        noun = self.font.render(name, DEFAULT_LAYERS_LIST_FONT_SIZE,
                                DEFAULT_LAYERS_LIST_NAME_COLOR)
        eye_type = 'opened_eye' if eye_state else 'closed_eye'
        eye_color = DEFAULT_GREEN if eye_state else DEFAULT_RED
        padlock_type = 'opened_padlock' if padlock_state else 'closed_padlock'
        padlock_color = DEFAULT_GREEN if padlock_state else DEFAULT_RED
        eye = draw_icon(
            eye_type,
            DEFAULT_LAYERS_LIST_ICON_TILESIZE,
            DEFAULT_LAYERS_LIST_ICON_LINESIZE,
            eye_color)
        padlock = draw_icon(
            padlock_type,
            DEFAULT_LAYERS_LIST_ICON_TILESIZE,
            DEFAULT_LAYERS_LIST_ICON_LINESIZE,
            padlock_color)
        width = 2 * self.border_width + 14 * DEFAULT_LAYERS_LIST_ICON_TILESIZE + noun.get_width()
        height = DEFAULT_LAYERS_LIST_FONT_SIZE + 2 * self.border_width
        layer = pygame.Surface((width, height), SRCALPHA)
        layer.blit(padlock, (self.border_width+6*DEFAULT_LAYERS_LIST_ICON_TILESIZE, self.border_width))
        layer.blit(eye, (self.border_width, self.border_width))
        x = self.border_width + 14 * DEFAULT_LAYERS_LIST_ICON_TILESIZE
        layer.blit(noun, (x, self.border_width))
        self.scrollwidget.add_row(name, layer, x)
        self.scrollwidget.scrollarea.listing[-1] += [name, width, eye_state, padlock_state]
        if self.app_map is not None and add_layer_to_map:
            data, visual_data = self.app_map.initialize_data(new_data=True)
            self.app_map.data.append(data)
            self.app_map.visual_data.append(visual_data)

    def delete_row(self, *arg):
        return

    def perform_row_creation(self, string):
        return

    @staticmethod
    def is_focus_string_valid(string):
        return True
