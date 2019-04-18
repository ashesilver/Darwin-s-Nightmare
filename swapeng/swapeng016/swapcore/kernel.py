import swapcore.constants as constants
import pygame
import pygame.gfxdraw


class Rect:
    def __init__(self, width, height, x, y):
        self._width = width
        self._height = height
        self._x = x
        self._y = y

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def left(self):
        return self._x

    @left.setter
    def left(self, value):
        self._x = value

    @property
    def right(self):
        return self._x + self._width

    @right.setter
    def right(self, value):
        self._x = value - self._width

    @property
    def top(self):
        return self._y

    @top.setter
    def top(self, value):
        self._y = value

    @property
    def topleft(self):
        return (self._x, self._y)

    @topleft.setter
    def topleft(self, value):
        self._x, self._y = value

    @property
    def topright(self):
        return (self._x + self._width, self._y)

    @topright.setter
    def topright(self, value):
        self._x = value[0] - self._width
        self._y = value[1]

    @property
    def bottom(self):
        return self._y + self._height

    @bottom.setter
    def bottom(self, value):
        self._y = value - self._height

    @property
    def bottomleft(self):
        return (self._x, self._y + self._height)

    @bottomleft.setter
    def bottomleft(self, value):
        self._x = value[0]
        self._y = value[1] - self._height

    @property
    def bottomright(self):
        return (self._x + self._width, self._y + self._height)

    @bottomright.setter
    def bottomright(self, value):
        self._x = value[0] - self._width
        self._y = value[1] - self._height

    @property
    def centerx(self):
        return self._x + self._width // 2

    @centerx.setter
    def centerx(self, value):
        self._x = value - self._width // 2

    @property
    def centery(self):
        return self._y + self._height // 2

    @centery.setter
    def centery(self, value):
        self._y = value - self._height // 2

    @property
    def center(self):
        return (self._x + self._width // 2, self._y + self._height // 2)

    @center.setter
    def center(self, value):
        self._x = value[0] - self._width // 2
        self._y = value[1] - self._height // 2


class Area(Rect):
    def __init__(self, width, height, x, y, surface=0, color=0):
        super().__init__(width, height, x, y)
        self._surface = pygame.Surface((width, height))
        self._color = color if color else constants.BLACK
        self._surface.fill(self._color)
        if surface:
            self._surface.blit(surface, constants.ORIGIN)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        surface = pygame.Surface((value, self._height))
        surface.fill(self._color)
        surface.blit(self._surface, constants.ORIGIN)
        self._surface = surface

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        surface = pygame.Surface((self._width, value))
        surface.fill(self._color)
        surface.blit(self._surface, constants.ORIGIN)
        self._surface = surface

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, value):
        self._width = value.get_width()
        self._height = value.get_height()
        self._surface = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    def draw_on(self, surface):
        surface.blit(self._surface, self.topleft)


class Font:
    def __init__(self, sketch_file, height=9):
        self.chars = {}
        self.infos = {}
        self.max_width = 0
        self.height = height
        self.decode_sketch_file(sketch_file, False)  # init attributes

    def render(self, text, size, color=constants.BLACK, background=constants.TRANSPARENT):
        scale = size / self.height
        max_scaled_width = round(self.max_width*scale)
        spacing = round(scale)  # 1px * scale = scale
        surface = pygame.Surface(((max_scaled_width+spacing)*len(text), size), pygame.SRCALPHA)
        surface.fill(background)
        color_mask = pygame.Surface((max_scaled_width, size))
        color_mask.fill(color)
        total_width = 0
        for char in text:
            try:
                char_width = round(self.infos[char]*scale)
            except KeyError:
                continue  # char is unknown so skip it and go to the next one
            char = pygame.transform.scale(self.chars[char], (char_width, size))
            char.blit(color_mask, constants.ORIGIN, None, pygame.BLEND_ADD)
            surface.blit(char, (total_width, 0))
            total_width += char_width + spacing
        final = pygame.Surface((max(spacing, total_width-spacing), size), pygame.SRCALPHA)
        final.blit(surface, constants.ORIGIN)
        return final

    def decode_sketch_file(self, sketch_file, reset):
        if reset:
            self.chars = {}
            self.infos = {}
            self.max_width = 0
        with open(sketch_file, 'r') as file:
            for line in file:
                char = line[0]
                char_width = int(line[1])
                if char_width > self.max_width:
                    self.max_width = char_width
                surface = pygame.Surface((char_width, self.height), pygame.SRCALPHA)
                # w: width h: height; create list from line with only shape & coords infos: [(1,2,3,4),(5,6,7,8),...]
                for w, h, x, y in [(int(a), int(b), int(c), int(d)) for a, b, c, d in line.rstrip()[2:].split()]:
                    pygame.draw.line(surface, constants.BLACK, (x, y), (x+w, y+h))
                self.chars[char] = surface
                self.infos[char] = char_width


class Toolbar(Area):
    def __init__(self, width, height, x, y,
                 background_color,
                 over_parameter_color,
                 demarcation_height, demarcation_color):
        super().__init__(width, height, x, y)
        self.background_color = background_color
        self.over_parameter_color = over_parameter_color
        self.demarcation_height = demarcation_height
        self.demarcation_color = demarcation_color
        self.demarcation = pygame.Surface((width, demarcation_height))
        self.demarcation.fill(demarcation_color)
        self._surface.fill(background_color)
        self._surface.blit(self.demarcation, (0, height-self.demarcation_height))


class Dock(Area):
    def __init__(self, width, height, x, y,
                 background_color,
                 focus_app_color, over_app_color, down_app_color,
                 open_line_app_color,
                 *app_icon_pack):
        super().__init__(width, height, x, y)
        self.background_color = background_color
        self.focus_app_color = focus_app_color
        self.over_app_color = over_app_color
        self.down_app_color = down_app_color
        self.open_line_app_color = open_line_app_color
        self._surface.fill(background_color)
        self.max_x = 0
        self.apps = []
        self.icons = []  # list like that: [[non-scaled icon, scaled icon], ...]
        if app_icon_pack:
            self.add_apps(app_icon_pack)
        self.line_slight_shift = 0
        self.line_shift = max(int(self._height*0.08), 1)
        self.line_height = max(int(self._height*0.08), 1)
        self.mouse_over_icon = -1  # index of the app where the mouse is over its icon

    def add_apps(self, *app_icon_pack):
        width = max(int(self._height*0.6), 1)
        y = max(int(self._height*0.2), 1)
        for i, (app, icon) in enumerate(app_icon_pack):
            x = self.max_x + self._height * i
            ic = (pygame.transform.scale(icon, (width, width))  # ic: icon
                  if icon.get_width() != width else icon)
            self._surface.blit(ic, (x+y, y))
            self.apps.append(app)
            self.icons.append([icon, ic])
            app.dock = self  # set a pointer to self as a link between dock & app
            dock_index = len(self.apps) - 1
            app.dock_index = dock_index  # allow the app to know where it is on the dock
            if app.state:  # if the app is open
                self.update_dock_state_color(dock_index)
        self.max_x = self._height * len(self.apps)

    def check_for_mouse_event(self, mx, my, action_type):
        mouse_on_dock = self.is_mouse_on_dock(mx, my)
        if mouse_on_dock:
            mcx, mcy = mx - self._x, my - self._y  # c: converted (to dock coord system)
        if action_type == pygame.MOUSEBUTTONDOWN:
            if mouse_on_dock and mcx < self.max_x:  # click on an icon
                self.update_app_dock_state(2, mcx//self._height)
        elif action_type == pygame.MOUSEMOTION:
            if mouse_on_dock and mcx < self.max_x:  # mouse over an icon
                index = mcx // self._height
                if self.mouse_over_icon > -1:
                    if self.mouse_over_icon != index:
                        state = 4 if App.app_specs[0].id == self.apps[self.mouse_over_icon].id else 0
                        self.update_app_dock_state(state, self.mouse_over_icon)
                        self.mouse_over_icon = index
                        self.update_app_dock_state(1, index)
                else:
                    self.mouse_over_icon = index
                    self.update_app_dock_state(1, index)
            elif self.mouse_over_icon > -1:
                state = 4 if App.app_specs[0].id == self.apps[self.mouse_over_icon].id else 0
                self.update_app_dock_state(state, self.mouse_over_icon)
                self.mouse_over_icon = -1
        elif action_type == pygame.MOUSEBUTTONUP:
            if mouse_on_dock and mcx < self.max_x:  # release mouse click on an icon
                index = mcx // self._height
                app = self.apps[index]
                if app.dock_state == 2:  # if we clicked before
                    self.update_app_dock_state(1, index)
                    if app.state:  # the app is open
                        if app.is_minimized:
                            app.is_minimized = False
                        # app was minimized or not on top so put it on top
                        if app.is_minimized or App.app_specs[0].id != app.id:
                            # appmanager necessarily exists because app is open
                            app.appmanager.put_app_on_top_by_id(app.id)
                        else:  # app is on top
                            app.is_minimized = True
                            App.app_specs[0] = AppNull()  # app loses keyboard focus
                    else:  # the app is not open
                        try:
                            app.appmanager.add_apps_to_queue(app)  # so open it
                            focus = App.app_specs[0]  # the app that currently have the focus
                            if focus.dock:
                                focus.dock.update_app_dock_state(0, focus.dock_index)
                            App.app_specs[0] = app  # give to the app the keyboard focus
                            self.update_app_dock_state(3, app.dock_index)
                        except AttributeError:
                            print('The app is not linked to an appmanager so it can not be opened')

    def is_mouse_on_dock(self, mx, my):
        return self.left <= mx <= self.right and self.top <= my <= self.bottom

    def update_app_dock_state(self, state, *index):
        """
        state:
        0: nothing
        1: mouse over icon
        2: mouse click on icon
        3: app has keyboard focus and mouse over icon
        4: app has keyboard focus and mouse is not over icon
        """
        iterator = index if index else range(len(self.apps))
        for i in iterator:
            self.apps[i].dock_state = state
        self.update_dock_state_color(*index)

    def update_dock_state_color(self, *index):
        """
        must be called if the state of an app linked to the dock changes
        - if index is empty that means that we don't know which app is
        concerned so the function update all app of the dock
        """
        iterator = index if index else range(len(self.apps))
        for i in iterator:
            app = self.apps[i]
            x = self._height * app.dock_index
            y = max(int(self._height*0.2), 1)
            if app.dock_state:  # there are interactions between app's icon and mouse
                if app.dock_state == 1 or app.dock_state == 3:  # mouse over icon
                    # the app may be the app that has the keyboard focus
                    self._surface.fill(self.over_app_color, (x, 0, self._height, self._height))
                elif app.dock_state == 2: # mouse click
                    self._surface.fill(self.down_app_color, (x, 0, self._height, self._height))
                else:  # dock_state = 4, app has keyboard focus and mouse not over icon
                    self._surface.fill(self.focus_app_color, (x, 0, self._height, self._height))
            else:  # no interactions between app's icon and mouse
                self._surface.fill(self.background_color, (x, 0, self._height, self._height))
            self._surface.blit(self.icons[i][1], (x+y, y))  # draw scaled icon
            if app.state:  # app is open
                shift = self.line_slight_shift if 0 < app.dock_state < 4 else self.line_shift
                self._surface.fill(self.open_line_app_color, (x+shift, 0, self._height-2*shift, self.line_height))


class AppNull:
    def __init__(self):
        self.id = 0
        self.dock = 0


class App(Area):
    app_events = [0]  # value: 0: not yet triggered, non-zero (1 by default): event already triggered
    # index: 0: if the mouse is on an app
    app_specs = [AppNull()]
    # index: 0: app that has keyboard focus, value (type: App): the app object
    app_number = 0

    def __init__(self, icon, name, name_color, font,
                 width, height, x, y,
                 background_color,
                 titlebar_width, titlebar_height,
                 titlebar_color, titlebar_button_radius,
                 foreground_width, foreground_height,
                 foreground_x, foreground_y, foreground_color,
                 minimize_button_color, minimize_button_over_color, minimize_button_down_color,
                 maximize_button_color, maximize_button_over_color, maximize_button_down_color,
                 close_button_color, close_button_over_color, close_button_down_color,
                 min_x=0, min_y=0,
                 max_x=constants.DEFAULT_PROGRAM_WIDTH,
                 max_y=constants.DEFAULT_PROGRAM_HEIGHT,
                priority=1):
        super().__init__(width, height, x, y)
        App.increment_app_number(1)
        self.id = App.app_number
        self.icon = icon
        self.icon_width = 0
        self.icon_x = 2 * foreground_x if self.icon else 0
        self.dock = 0  # initialized later in the dock
        self.dock_index = 0  # initialized later in the dock
        self.dock_state = 0  # initialized later in the dock
        self.appmanager = 0  # initialized later in the appmanager
        self.name = name
        self.name_color = name_color
        self.font = font
        self.rx = titlebar_width
        self.ry = titlebar_height
        # r: real ; facilite les calculs de positions en creant une nouvelle origine
        # pour ne pas prendre en compte la titlebar
        self.background_color = background_color
        self.titlebar_height = titlebar_height
        self.titlebar_color = titlebar_color
        self.titlebar_button_radius = titlebar_button_radius
        self.titlebar_button_y = titlebar_height // 2
        self.foreground_width = foreground_width
        self.foreground_height = foreground_height
        self.foreground_x = foreground_x
        self.foreground_y = foreground_y
        self.foreground_color = foreground_color
        self.minimize_button_color = minimize_button_color
        self.minimize_button_up_color = minimize_button_color
        self.minimize_button_over_color = minimize_button_over_color
        self.minimize_button_down_color = minimize_button_down_color
        self.minimize_button_x = width - 8 * titlebar_button_radius
        self.maximize_button_color = maximize_button_color
        self.maximize_button_up_color = maximize_button_color
        self.maximize_button_over_color = maximize_button_over_color
        self.maximize_button_down_color = maximize_button_down_color
        self.maximize_button_x = width - 5 * titlebar_button_radius
        self.close_button_color = close_button_color
        self.close_button_up_color = close_button_color
        self.close_button_over_color = close_button_over_color
        self.close_button_down_color = close_button_down_color
        self.close_button_x = width - 2 * titlebar_button_radius
        self.titlebar = pygame.Surface((width, titlebar_height))
        self.titlebar.fill(titlebar_color)
        self.draw_icon()
        self.draw_name()
        self.draw_titlebar_button(2, 3, 4)
        self.foreground = pygame.Surface((foreground_width, foreground_height))
        self.foreground.fill(foreground_color)
        self._surface.fill(background_color)
        self.draw_titlebar(self.titlebar, constants.ORIGIN)
        self._surface.blit(self.foreground, (self.rx+foreground_x, self.ry+foreground_y))
        # end of input attributs
        self.are_titlebar_buttons_upped = True
        self.titlebar_button_state = [0, 0, 0]
        self.old_pos, self.old_mcx, self.old_mcy = 0, 0, 0
        self.min_x, self.min_y = min_x, min_y
        self.max_x, self.max_y = max_x - width, max_y - height
        self.priority = priority
        self.state = 0  # when created, the app is considered as closed
        self.is_minimized = False  # app is closed so not minimized

    def mouse_event(self, mx, my, action_type, keystate):
        """methode appelee par l'AppManager lors d'une action de la souris sur l'app"""
        mouse_on_app = self.is_mouse_on_app(mx, my)
        actions = []
        if mouse_on_app:
            App.app_events[0] = 1  # mouse is on an app
            mcx, mcy = mx - self._x, my - self._y  # c: converted (to app coord system)
        on_titlebar_button = self.is_mouse_on_titlebar_button(mcx, mcy) if mouse_on_app else 0
        self.update_titlebar_button_state(action_type, on_titlebar_button)
        if action_type == pygame.MOUSEBUTTONDOWN:  # app is visible
            if mouse_on_app:
                actions.append(1)  # request focus
                if mcy < self.ry and not on_titlebar_button:  # mouse on taskbar (and no app has been moved)
                    self.old_mcx, self.old_mcy = mcx, mcy
        elif action_type == pygame.MOUSEMOTION:
            if self.old_mcx:  # app is being moved
                self.topleft = (min(self.max_x, max(self.min_x, mx - self.old_mcx)), min(self.max_y,max(self.min_y, my - self.old_mcy)))
        elif action_type == pygame.MOUSEBUTTONUP:
            # if button is down and we up it
            if on_titlebar_button and self.titlebar_button_state[on_titlebar_button-2] == 2:
                actions.append(on_titlebar_button)  # request button action
            if self.old_mcx:
                self.old_mcx, self.old_mcy = 0, 0  # stop moving the app
        self.additional_mouse_event(mx, my, action_type, actions,
                                    mouse_on_app, on_titlebar_button, keystate)
        return actions

    def additional_mouse_event(self, *args):
        return

    def mouse_state(self, *args):
        return

    def keyboard_event(self, *args):
        return

    def keyboard_state(self, *args):
        return

    def is_mouse_on_app(self, mx, my):
        # app is visible and mouse on app
        return not App.app_events[0] and self.left <= mx <= self.right and self.top <= my <= self.bottom

    def is_mouse_on_titlebar_button(self, mcx, mcy):  # c: converted (to app coord system)
        if mcy >= self.ry or mcx < self.minimize_button_x - self.titlebar_button_radius:
            return 0  # mouse not on button area
        else:  # mouse is on button area, now check if mouse is on a button
            y = (mcy - self.titlebar_button_y) ** 2  # y to refer to the y coord
            r = self.titlebar_button_radius ** 2  # r: radius^2
            if (mcx - self.minimize_button_x) ** 2 + y <= r:
                return 2  # mouse on minimize button
            elif (mcx - self.maximize_button_x) ** 2 + y <= r:
                return 3  # mouse on maximize button
            elif (mcx - self.close_button_x) ** 2 + y <= r:
                return 4  # mouse on close button
            return 0  # mouse is not on a button

    def update_titlebar_button_state(self, action_type, *button):
        # button: list of buttons where the mouse is
        # is practice *button is only 1 button (mouse can only be on one place)
        # but in special cases, this function is built to allow multiple button update
        # ex: if a button is linked to another
        if not button or not button[0]:
            if self.are_titlebar_buttons_upped:
                return  # all buttons are already upped
            # button_state are store like that:
            # [minimize_button_state, maximize_button_state, close_button_state]
            # so the respective indexes are 0, 1, 2
            # but the update system understands these indexes: 2, 3, 4
            # so we have to do +2 to have a correspondence
            update = [index+2 for index, state in enumerate(self.titlebar_button_state) if state]
            self.minimize_button_color = self.minimize_button_up_color
            self.maximize_button_color = self.maximize_button_up_color
            self.close_button_color = self.close_button_up_color
            self.draw_titlebar_button(*update)
            self.draw_titlebar(self.titlebar, constants.ORIGIN)
            self.titlebar_button_state = [0, 0, 0]
            self.are_titlebar_buttons_upped = True
        else:
            for b in button:  # b: button
                if action_type == pygame.MOUSEMOTION and not self.titlebar_button_state[b-2]:
                    if b == 2:  # minimize button
                        self.minimize_button_color = self.minimize_button_over_color
                    elif b == 3:  # maximize button
                        self.maximize_button_color = self.maximize_button_over_color
                    elif b == 4:  # close button
                        self.close_button_color = self.close_button_over_color
                    self.titlebar_button_state[b-2] = 1
                elif action_type == pygame.MOUSEBUTTONDOWN and self.titlebar_button_state[b-2] != 2:
                    if b == 2:
                        self.minimize_button_color = self.minimize_button_down_color
                    elif b == 3:
                        self.maximize_button_color = self.maximize_button_down_color
                    elif b == 4:
                        self.close_button_color = self.close_button_down_color
                    self.titlebar_button_state[b-2] = 2
                elif action_type == pygame.MOUSEBUTTONUP and self.titlebar_button_state[b-2] == 2:
                    # if button is down and we up it
                    if b == 2:
                        self.minimize_button_color = self.minimize_button_up_color
                    elif b == 3:
                        # TODO: it is possible that the coords of the buttons are the same
                        # after maximize the app so an additional condition must be added
                        self.maximize_button_color = self.maximize_button_over_color
                        self.titlebar_button_state[1] = 1
                    elif b == 4:
                        self.close_button_color = self.close_button_up_color
            self.are_titlebar_buttons_upped = True if self.titlebar_button_state == [0, 0, 0] else False
            self.draw_titlebar_button(*button)
            self.draw_titlebar(self.titlebar, constants.ORIGIN)

    def draw_titlebar_button(self, *button):
        for b in button:
            y = self.titlebar_button_y - self.titlebar_button_radius
            width = 2 * self.titlebar_button_radius + 2  # +2 because aacircle
            if b == 2:  # minimize button
                x = self.minimize_button_x - self.titlebar_button_radius
                self.titlebar.fill(self.titlebar_color, (x, y, width, width))
                pygame.gfxdraw.filled_circle(
                    self.titlebar, self.minimize_button_x, self.titlebar_button_y,
                    self.titlebar_button_radius, self.minimize_button_color)
                pygame.gfxdraw.aacircle(
                    self.titlebar, self.minimize_button_x, self.titlebar_button_y,
                    self.titlebar_button_radius, self.minimize_button_color)
            elif b == 3:  # maximize button
                x = self.maximize_button_x - self.titlebar_button_radius
                self.titlebar.fill(self.titlebar_color, (x, y, width, width))
                pygame.gfxdraw.filled_circle(
                    self.titlebar, self.maximize_button_x, self.titlebar_button_y,
                    self.titlebar_button_radius, self.maximize_button_color)
                pygame.gfxdraw.aacircle(
                    self.titlebar, self.maximize_button_x, self.titlebar_button_y,
                    self.titlebar_button_radius, self.maximize_button_color)
            elif b == 4:  # close button
                x = self.close_button_x - self.titlebar_button_radius
                self.titlebar.fill(self.titlebar_color, (x, y, width, width))
                pygame.gfxdraw.filled_circle(
                    self.titlebar, self.close_button_x, self.titlebar_button_y,
                    self.titlebar_button_radius, self.close_button_color)
                pygame.gfxdraw.aacircle(
                    self.titlebar, self.close_button_x, self.titlebar_button_y,
                    self.titlebar_button_radius, self.close_button_color)

    def draw_titlebar(self, titlebar, coords):
        self._surface.blit(titlebar, coords)

    def draw_icon(self):
        if self.icon:
            width = int(self.titlebar_height*0.9)
            y = self.titlebar_height // 2 - width // 2
            icon = (pygame.transform.scale(self.icon, (width, width))
                if self.icon.get_width() != width else self.icon)
            self.icon_width = icon.get_width()
            self.titlebar.blit(icon, (self.icon_x, y))

    def draw_name(self):
        size = int(self.titlebar_height*0.9)
        y = self.titlebar_height // 2 - size // 2
        name = self.font.render(self.name, size, self.name_color)
        self.titlebar.blit(name, (self.icon_x+self.icon_width+2*self.foreground_x, y))

    @property
    def foreground_topleft(self):
        return (self.rx + self.foreground_x, self.ry + self.foreground_y)

    @property
    def foreground_left(self):
        return self.rx + self.foreground_x

    @property
    def foreground_top(self):
        return self.ry + self.foreground_y

    @classmethod
    def clear_app_events(cls):
        cls.app_events = [0] * len(cls.app_events)  # reset all event values

    @classmethod
    def increment_app_number(cls, value):
        cls.app_number += value


class AppManager:
    def __init__(self):
        self._app_queue = []  # index 0 is the lowest priority
        self._max_index = -1  # to init
        self._priorities_indexes = {0: -1}  # to init
        self._existing_priorities = [0]  # index 0 is the highest priority
        self._max_priority = 0  # to init
        self.min_x, self.min_y, self.max_x, self.max_y = 0, 0, 0, 0
        self.desk = Rect(0, 0, 0, 0)

    def add_apps_to_queue(self, *app):
        for a in app:  # a: app
            if a.priority > self._max_priority:
                self._app_queue.append(a)  # append because 'a' has the highest priority
                self._priorities_indexes[a.priority] = self._max_index + 1
                # +1 because 'a' is being added
                self._existing_priorities.insert(0, a.priority)  # index 0 : highest priority
                self._max_priority = a.priority
            else:
                i = a.priority  # i: index
                is_alone = False
                while True:  # while 'a' is not added
                    try:
                        index = self._priorities_indexes[i] # check if index exists
                        # the following code is executed only if no error has occurred
                        if i != a.priority:  # an error has occurred at least once
                            is_only = True  # so priority of 'a' is a new priority
                        self._app_queue.insert(index+1, a) # +1 to be first
                        self.modify_priorities_indexes(a.priority, index+1, is_alone)
                        break  # quit the while loop because 'a' has been added
                    except KeyError:  # index does not exist
                        i -= 1
            a.state = 1  # set app state to opened
            if a.dock:  # if app is linked to a dock, informs it that the app is opened
                a.dock.update_dock_state_color(a.dock_index)
            a.appmanager = self
            self._max_index += 1
        if app:
            self.apply_possible_coords(*app)

    def remove_apps_from_queue(self, *index):  # apps' index
        for i in index:
            try:
                if not isinstance(i, int):
                    raise TypeError('TypeError : wrong type for the app index, int expected instead of %s' % type(i))
                elif self._max_index < 0:
                    raise IndexError('IndexError : trying to delete an app but the app queue is empty')
                elif i > self._max_index:
                    raise IndexError('IndexError : index of the app is out of range : %d (maximum index allowed: %d)' % (i, self._max_index))
            except (TypeError, IndexError) as error:
                print(error)
            else:
                app = self._app_queue[i]
                priority = app.priority
                is_alone = self.is_app_alone(i, priority)
                self.modify_priorities_indexes(priority, i, is_alone, 1)
                app.state = 0  # set app state to closed
                app.is_minimized = False
                if App.app_specs[0].id == app.id:  # remove the keyboard focus if it has
                    App.app_specs[0] = AppNull()
                    if app.dock:
                        app.dock.update_app_dock_state(0, app.dock_index)
                elif app.dock:  # if linked to a dock, informs it that the app is closed
                    app.dock.update_dock_state_color(app.dock_index)
                self._app_queue.pop(i) # remove the app
                self._max_index -= 1
                if not self._app_queue:  # app queue is empty
                    self._max_priority = 0
                elif is_alone and priority == self._max_priority:
                    self._max_priority = self._app_queue[self._max_index].priority

    def is_app_alone(self, index, priority):
        if not self._max_index:
            return True
        try:
            return self._app_queue[index+1].priority != priority and \
                   self._app_queue[index-1].priority != priority
        except IndexError:
            return self._app_queue[index-1].priority != priority

    def draw_apps_on(self, surface):
        for app in self._app_queue:
            if not app.is_minimized:
                app.draw_on(surface)

    def check_for_mouse_event(self, mx, my, action_type, keystate):
        actions = []
        for dex, app in enumerate(reversed(self._app_queue)):  # dex: index
            if app.is_minimized:
                continue  # app is minimized so it should not receive mouse events
            index = self._max_index - dex  # get real index, not inversed one
            acts = app.mouse_event(mx, my, action_type, keystate)
            for act in acts:
                if act == 1:
                    # check if the app already has the focus
                    # if index == self._priorities_indexes[app.priority]:
                    if app.id == App.app_specs[0].id:
                        continue  # if so, check the next act
                if act == 2:
                    if not app.dock:
                        print('App is not linked to a dock so it can not be minimized')
                        app.titlebar_button_state[0] = 1
                        app.minimize_button_color = app.minimize_button_over_color
                        app.draw_titlebar_button(act)
                        app.draw_titlebar(app.titlebar, constants.ORIGIN)
                        continue
                actions.append((index, act))  # save index & action to reorganize the queue later
        for index, action in actions:
            # 1: request focus
            # 2: request minimize
            # 3: request maximize
            # 4: request close
            if action == 1:  # request focus
                app = self._app_queue.pop(index)
                self._app_queue.insert(self._priorities_indexes[app.priority], app)
                if app.dock:
                    app.dock.update_app_dock_state(4, app.dock_index)
                focus = App.app_specs[0]  # the app that currently have the focus
                if focus.dock:
                    focus.dock.update_app_dock_state(0, focus.dock_index)
                App.app_specs[0] = app
            elif action == 2:  # request minimize
                app = self._app_queue[index]
                app.is_minimized = True
                if App.app_specs[0].id == app.id:  # remove the keyboard focus if it has
                    App.app_specs[0] = AppNull()
                    if app.dock:
                        app.dock.update_app_dock_state(0, app.dock_index)
            elif action == 4:  # request close
                self.remove_apps_from_queue(index)
        if action_type == pygame.MOUSEBUTTONDOWN and not App.app_events[0] \
            and self.desk.left <= mx <= self.desk.right \
            and self.desk.top <= my <= self.desk.bottom:
            # if we click on the desk, the app that has the focus lose it
            focus = App.app_specs[0]
            if focus.dock:
                focus.dock.update_app_dock_state(0, focus.dock_index)
            App.app_specs[0] = AppNull()
        App.clear_app_events()  # reset all event values

    def set_possible_coords(self, min_x=0, min_y=0, max_x=0, max_y=0):
        # 0 to not overwrite the default min / max of the app
        self.min_x, self.min_y = min_x, min_y
        self.max_x, self.max_y = max_x, max_y

    def apply_possible_coords(self, *app):
        # 0 to not overwrite the default min / max of the app
        iterator = app if app else self._app_queue
        for a in iterator:  # a: app
            if self.min_x:  # overwrite min x
                a.min_x = self.min_x
                if a.min_x > a.x:
                    a.x = a.min_x
            if self.min_y:  # overwrite min y
                a.min_y = self.min_y
                if a.min_y > a.y:
                    a.y = a.min_y
            if self.max_x:  # overwrite max x
                a.max_x = self.max_x
                if a.max_x < a.x:
                    a.x = a.max_x
            if self.max_y:  # overwrite max y
                a.max_y = self.max_y
                if a.max_y < a.y:
                    a.y = a.max_y

    def set_desk(self, width, height, x, y):
        self.desk.width = width
        self.desk.height = height
        self.desk.x = x
        self.desk.y = y
        # self.desk_width = right - left
        # self.desk_height = bottom - top

    def modify_priorities_indexes(self, priority, index, is_alone, mode=0):
        # is_only: 0: not only, else: only
        # mode: 0 add, 1: remove
        i = 0  # i: index
        for dex, p in enumerate(self._existing_priorities):  # dex: index, p: priority
            if p > priority:
                # shift index to the right or left, depends on the chosen mode
                # mode: 0: right, 1: left
                self._priorities_indexes[p] += -1 if mode else 1
            else:
                i = dex  # save dex, dex: index where the priority will be inserted / removed
                break  # time to add / remove the priority
        if mode:
            if self._priorities_indexes[priority] == index and not is_alone:  # app is the top app of its priority
                self._priorities_indexes[priority] = index - 1
            elif is_alone:
                self._priorities_indexes.pop(priority)
                self._existing_priorities.pop(i)
        else:
            self._priorities_indexes[priority] = index
            if is_alone:
                self._existing_priorities.insert(i, priority)

    def put_app_on_top_by_id(self, id):
        """
        This function can give the focus to an app by its unique ID
        This function should be called from an external object (external to self)
        From self, you should call check_for_mouse_event instead to request focus
        whenever possible
        """
        index = -1
        for i, app in enumerate(self._app_queue):  # i: index
            if app.id == id:
                index = i
                break
        if index > -1:  # if the app has been found
            app = self._app_queue.pop(index)
            self._app_queue.insert(self._priorities_indexes[app.priority], app)
            focus = App.app_specs[0]  # the app that currently have the focus
            if focus.dock:
                focus.dock.update_app_dock_state(0, focus.dock_index)
            App.app_specs[0] = app
            if app.dock:
                app.dock.update_app_dock_state(3, app.dock_index)
