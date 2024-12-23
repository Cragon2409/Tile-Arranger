import pygame, os
from random import randrange, seed, choice
from datetime import datetime
from pathlib import Path

###================================================================
###                           Constants
###================================================================
DEFAULT_DW,DEFAULT_DH = 1600, 1200
GAME_FPS = 60
MENU_FPS = 60
PAUSE_FPS = 20

GAME_BORDER = 0.1 #Game Border as percent of screen size

ANMTN_DRAG_DUR = 10
ANMTN_DRAG_FUNC = lambda frac : frac**(0.8)

ANMTN_INIT_DUR = 120
ANMTN_INIT_ENABLED = True

NEIGHBOURS = [(1,0),(0,1),(-1,0),(0,-1)]

CODE_GMDE_DRAG = 0
CODE_GMDE_GAPS = 1

ALLOWED_IMAGE_TYPES = [".webp",".png",".jpg"]

COL_FORMULAS = [
    lambda x,y,w,h : (255-(200//w)*x, 255-(200//h)*y, 128), #yellow - green - purple - red
    lambda x,y,w,h : ()
]

LEVEL_SETTINGS = [
    #NAME,                          GAMEMODE        PICTURE_SOURCE,    WIDTH       HEIGHT      FORMULA             RANDOM SEED     SHUFFLE_NUM     PIVOT_POS_LIST
    ("Level 1",                     CODE_GMDE_DRAG, None,              10,         10,         COL_FORMULAS[0],    0,             1000,           [(0,0),(9,0),(9,9),(0,9)]),
    ("Level 2",                     CODE_GMDE_DRAG, None,              5,          5,          COL_FORMULAS[0],    0,             1000,           [(0,0),(4,0),(4,4),(0,4)]),

    ("Level 3",                     CODE_GMDE_GAPS, None,              10,         10,         COL_FORMULAS[0],    0,             1000,           [(0,0),(9,0),(9,9),(0,9)]),
    ("Shitty Mode",                 CODE_GMDE_GAPS, None,              5,          5,          COL_FORMULAS[0],    0,             1000,           []),#(0,0),(4,0),(4,4),(0,4)
    
    ("Level 5",                     CODE_GMDE_DRAG, "Minions",         10,         10,         None,               0,             1000,           [(0,0),(9,0),(9,9),(0,9)]),
    ("Level 6",                     CODE_GMDE_GAPS, "Minions",         5,          5,          None,               0,             20,             []), #(0,0),(4,0),(4,4),(0,4)
]

INBUILT_LEVELS = len(LEVEL_SETTINGS)
CHAPTERS = [
    ("Pretty Colours",  4),
    ("Minions",         2)
]

CHAPTER_LEVELS = {}

def sync_levels(show=True):
    if show: print("Syncing Levels")
    cur_ind = 0
    for ch_name, le in CHAPTERS[:-1]:
        CHAPTER_LEVELS[ch_name] = LEVEL_SETTINGS[cur_ind:cur_ind+le]
        if show:
            print(ch_name)
            for l in CHAPTER_LEVELS[ch_name]:
                print("\t",l)
        cur_ind += le
    CHAPTER_LEVELS[CHAPTERS[-1][0]] = LEVEL_SETTINGS[cur_ind:]
    if show:
        print(CHAPTERS[-1][0])
        for l in CHAPTER_LEVELS[CHAPTERS[-1][0]]:
            print("\t",l)

CREDIT_MENU_DESCR = """
These are credits! Amazing
Next line
wooohooo
"""[1:]

HELP_MENU_DESC = """
This is a help menu! Amazing
"""[1:]

black = (0,0,0); lightgray = (150,150,150); darklightgray = (100,100,100); white = (255,255,255); red = (255,0,0); green = (0,255,0); blue = (0,0,255); darkgray = (50,50,50); brown = (101,67,33); darkorange = (255,100,0); darkgreen = (0,100,0); darkred = (139,0,0); yellow = (255,255,0); whiteskin = (255,195, 170); yellow = (255,255,0); darkyellow = (204,204,0); purple = (128,0,128); lightblue = (50,50,255)
teal = (40,170,130); dark_teal = tuple([i*0.2 for i in teal])
dark_purple = (49,21,74)
magenta = (170,50,170)
navy_blue = (2,7,93)
baby_blue = (137,207,240)
pastel_pink = (255,197,211)
peach_red = (255,177,173)
title_blue = (20, 51, 117)


###================================================================
###                           Pygame Init
###================================================================

pygame.init()
screen = pygame.display.set_mode((DEFAULT_DW,DEFAULT_DH))
dw,dh = pygame.display.get_surface().get_size()
display_width, display_height = dw,dh
pygame.display.set_caption("Tile Arranger")
clock = pygame.time.Clock()

pygame.font.init()
my_font = pygame.font.SysFont("monospace", 50)
my_font_smaller = pygame.font.SysFont("monospace", 40)
big_font = pygame.font.SysFont("calibri", 50)
big_font_bold = pygame.font.SysFont("calibri", 50, bold=True)
fancy_font_bigger = pygame.font.SysFont("calibri", 30)
fancy_font_underline = pygame.font.SysFont("calibri", 50); fancy_font_underline.set_underline(True)
fancy_font_bigger_bold = pygame.font.SysFont("calibri", 30,bold=True)
fancy_font = pygame.font.SysFont("calibri", 22)
fancy_font_bold = pygame.font.SysFont("calibri", 22, bold=True)
fancy_font_smaller = pygame.font.SysFont("calibri", 20)
title_font = pygame.font.SysFont("elephant",70,bold=True)
impact_font_big = pygame.font.SysFont("impact",70)
gab_font_big = pygame.font.SysFont("gabriola",100, bold=False)
hel_bold_font = pygame.font.Font("source/fonts/Helvetica-Bold.ttf",100)
arial_bigger = pygame.font.SysFont("arial",30)
helvetica_med = pygame.font.Font("source/fonts/Helvetica.ttf", 30)
helvetica_big = pygame.font.Font("source/fonts/Helvetica.ttf", 45)

TITLE_FONT = gab_font_big

TITLE_COL = title_blue

PAUSE_BUTTON_FONT = fancy_font_smaller
SMALL_BUTTON_SHADOW_OFFSET = (3,3)
SMALL_BUTTON_SHADOW_COL = dark_purple
BUTTON_OUTLINE_COLOUR = (50,50,50)

PLAY_BUTTON_FONT = helvetica_big#big_font

MENU_BUTTON_FONT = helvetica_med#fancy_font_bigger_bold
MENU_SHADOW_OFFSET = (5,5)
MENU_SHADOW_COL = dark_purple

BUTTON_HOVER_COL = peach_red
BUTTON_BACKGROUND_COL = white

GAME_BORDER_COL = (50,50,50)

MAIN_BACKGROUND_COL = teal

TEXT_BOX_OFFSET = (5,5)
LEVEL_LIST_GAP = 2
LEVEL_LIST_FONT = fancy_font_bigger
LEVEL_LIST_TEXT_OFFSET = (5,5)

def sync_graphics():
    global QUIT_BUTTON_RECT, PAUSE_BUTTON_RECT, PLAY_BUTTON_RECT, LEVEL_BUTTON_RECT, SHOP_BUTTON_RECT, CREDIT_BUTTON_RECT, HELP_BUTTON_RECT, MENU_TEXT_POS, HINT_BUTTON_RECT, BIG_TEXT_RECT, LEVEL_LIST_RECT, LEVEL_LIST_ITEM_RECT, LEVEL_LIST_BUTTON_RECT, LEVEL_CREATE_RECT, IMAGE_PREVIEW_SIZE,LEVEL_PREVIEW_RECT,LEVEL_PREVIEW_RSET_RECT, LEVEL_PREVIEW_PLAY_RECT, LEVEL_PREVIEW_TEXT_RECT
    QUIT_BUTTON_RECT        = [dw-35,5,30,30]
    PAUSE_BUTTON_RECT       = [dw-70,5,30,30]
    HINT_BUTTON_RECT        = [dw-105,5,30,30]
    PLAY_BUTTON_RECT        = [dw//2-200,150+30,400,70]
    LEVEL_BUTTON_RECT       = [dw//2-200,230+30,190,50]
    SHOP_BUTTON_RECT        = [dw//2+10,230+30,190,50]
    CREDIT_BUTTON_RECT      = [dw//2-200,290+30,190,50]
    HELP_BUTTON_RECT        = [dw//2+10,290+30,190,50]
    BIG_TEXT_RECT           = [dw//6, dh//6, 4*dw//6, 4*dh//6]

    LEVEL_LIST_RECT         = [3*dw//12, dh//6, 4*dw//6, 4*dh//6]
    LEVEL_LIST_ITEM_RECT    = [5,5, LEVEL_LIST_RECT[2] - 10, 40]
    LEVEL_LIST_BUTTON_RECT  = [10,LEVEL_LIST_RECT[1], (3*dw//12)-15, 40]
    LEVEL_CREATE_RECT       = [LEVEL_LIST_RECT[0], LEVEL_LIST_RECT[1]+LEVEL_LIST_RECT[3]+5, LEVEL_LIST_RECT[2], 40]

    LEVEL_PREVIEW_RECT      = [dw//6, dh//6, 4*dw//6, 4*dh//6]
    LEVEL_PREVIEW_TEXT_RECT = [LEVEL_PREVIEW_RECT[0]+5, LEVEL_PREVIEW_RECT[1]+5, LEVEL_PREVIEW_RECT[2]//2-10, 40]
    LEVEL_PREVIEW_PLAY_RECT = [LEVEL_PREVIEW_RECT[0]+5, LEVEL_PREVIEW_RECT[1]+LEVEL_PREVIEW_RECT[3]//2+5, LEVEL_PREVIEW_RECT[2]-10, 40]
    LEVEL_PREVIEW_RSET_RECT = [LEVEL_PREVIEW_RECT[0]+5, LEVEL_PREVIEW_RECT[1]+LEVEL_PREVIEW_RECT[3]//2+5+45, LEVEL_PREVIEW_RECT[2]-10, 40]
    
    MENU_TEXT_POS           = [dw//2,100]
    IMAGE_PREVIEW_SIZE = (200,200)

sync_graphics()




###================================================================
###                           Helpers
###================================================================


PDU = pygame.display.update
def quit_all(): pygame.quit(); quit()

def text_objects(text,font,colour=white):
    textSurface = font.render(text,True,colour)
    return(textSurface, textSurface.get_rect())
def simple_text(input_text,co=(0,0),colour=white, font = fancy_font):
    text = font.render(input_text, True, colour)
    screen.blit(text,co)
def simple_text_lines(input_text_lines, co=(0,0), colour=white, font= fancy_font):
    line_height = font.size('A')[1]
    for n,line in enumerate(input_text_lines):
        simple_text(line, dA(co,(0,n*line_height)),colour,font)
def cent_text(input_text,center,colour=white,font=my_font):#draws text to the screen anchored on the centre of the given position
    textSurf, textRect = text_objects(input_text,font,colour)#generates the text surface and rectangle
    textRect.center = center#centres the text
    screen.blit(textSurf,textRect)#blits the text to the screen
def in_rect(co,rect): return co[0] >= rect[0] and co[1] >= rect[1] and co[0] < rect[0]+rect[2] and co[1] < rect[1]+rect[3]
def rect_cent(rect): return dA(rect[:2],dSM(0.5,rect[2:]))

def dA(d1,d2): return (d1[0]+d2[0], d1[1]+d2[1])
def dS(d1,d2): return (d1[0]-d2[0], d1[1]-d2[1])
def dSM(s,d1): return (s*d1[0],s*d1[1])

def between_point(co1,co2,n=0.5): return [ (co1[c]*(1-n) + co2[c]*n) for c in range(2) ]

def decide_img_square_size(img_dims, grid_dims):
    return min([img_dims[n]//grid_dims[n] for n in range(2)])

def cut_image(image, grid_dims, square_size):
    crop_dim = [square_size, square_size]
    table = []
    for y in range(grid_dims[1]):
        rows = []
        for x in range(grid_dims[0]):
            img_pos = [x*square_size, y*square_size]
            item = pygame.Surface(crop_dim)
            item.blit(image, (0,0), img_pos + crop_dim)

            rows.append(item)
        table.append(rows)
    return table

###================================================================
###                           Class Definitions
###================================================================

# Menu Items
class MenuItem:
    def __init__(self,rect,rounding=-1,shadow=(0,0),shadow_col=SMALL_BUTTON_SHADOW_COL,background_col=BUTTON_BACKGROUND_COL):
        self.rect, self.rounding, self.shadow, self.shadow_col, self.background_col = rect, rounding, shadow, shadow_col, background_col
        if self.shadow != (0,0): self.shadow_rect = list(dA(self.rect[:2],self.shadow)) + list(self.rect[2:])
        self.syncCent()
    def inButton(self,m_co):
        return in_rect(m_co, self.rect)
    def syncCent(self):
        self.cent = rect_cent(self.rect)
    def onPressDown(self,m_co=None):
        self.pressed = True
    def onPressUp(self,m_co=None):
        self.pressed = False
    def onPressRelease(self):
        self.pressed = False
    def onScroll(self,s_di):
        pass
    def draw(self, m_co=None):
        if self.shadow != (0,0):
            pygame.draw.rect(screen, self.shadow_col, self.shadow_rect, border_radius = self.rounding)
        pygame.draw.rect(screen,self.background_col,self.rect, border_radius = self.rounding)
        pygame.draw.rect(screen,BUTTON_OUTLINE_COLOUR,self.rect,2, border_radius = self.rounding)

class MenuButton(MenuItem):
    def __init__(self,rect,text,func,font=fancy_font,rounding=-1,shadow=(0,0),shadow_col=SMALL_BUTTON_SHADOW_COL):
        super().__init__(rect, rounding, shadow, shadow_col)
        self.text, self.func, self.font = text, func, font
        self.pressed = False
    def onPressUp(self,m_co=None):
        self.pressed = False
        if self.func != None: self.func()
        return True
    def draw(self, m_co):
        selCol = BUTTON_HOVER_COL if in_rect(m_co,self.rect) else BUTTON_BACKGROUND_COL
        if self.pressed:
            pygame.draw.rect(screen,selCol,self.shadow_rect, border_radius = self.rounding)
            pygame.draw.rect(screen,BUTTON_OUTLINE_COLOUR,self.shadow_rect, 2, border_radius = self.rounding)
            cent_text(self.text,dA(self.cent,self.shadow), black,font=self.font)
        else:
            if self.shadow != (0,0):
                pygame.draw.rect(screen, self.shadow_col, self.shadow_rect, border_radius = self.rounding)
            pygame.draw.rect(screen,selCol,self.rect, border_radius = self.rounding)
            pygame.draw.rect(screen,BUTTON_OUTLINE_COLOUR,self.rect,2, border_radius = self.rounding)
            cent_text(self.text,self.cent, black,font=self.font)

class SelectionButton(MenuItem):
    def __init__(self,rect,text,func,font=fancy_font,rounding=-1,shadow=(0,0),shadow_col=SMALL_BUTTON_SHADOW_COL):
        super().__init__(rect, rounding, shadow, shadow_col)
        self.text, self.func, self.font = text, func, font
        self.pressed = False
        #self.other_buttons needs to be set externally
    def set_other_buttons(self,other_buttons):
        self.other_buttons = other_buttons
    def onPressUp(self,m_co=None):
        pass
    def onPressRelease(self):
        pass
    def onPressDown(self,m_co=None):
        self.pressed = True
        for b in self.other_buttons: b.pressed = False
        if self.func != None: self.func(self)
    def draw(self, m_co):
        selCol = BUTTON_HOVER_COL if in_rect(m_co,self.rect) else BUTTON_BACKGROUND_COL
        if self.pressed:
            pygame.draw.rect(screen,selCol,self.shadow_rect, border_radius = self.rounding)
            pygame.draw.rect(screen,BUTTON_OUTLINE_COLOUR,self.shadow_rect, 2, border_radius = self.rounding)
            cent_text(self.text,dA(self.cent,self.shadow), black,font=self.font)
        else:
            if self.shadow != (0,0):
                pygame.draw.rect(screen, self.shadow_col, self.shadow_rect, border_radius = self.rounding)
            pygame.draw.rect(screen,selCol,self.rect, border_radius = self.rounding)
            pygame.draw.rect(screen,BUTTON_OUTLINE_COLOUR,self.rect,2, border_radius = self.rounding)
            cent_text(self.text,self.cent, black,font=self.font)


class TextBox(MenuItem):
    def __init__(self,rect,text,font=fancy_font,rounding=-1,shadow=(0,0),shadow_col=SMALL_BUTTON_SHADOW_COL):
        super().__init__(rect, rounding, shadow, shadow_col)
        self.text, self.font = text, font
        self.text_pos = dA(self.rect[:2],TEXT_BOX_OFFSET)
        self.text_lines = text.splitlines()
    def draw(self, m_co=None):
        if self.shadow != (0,0):
            pygame.draw.rect(screen, self.shadow_col, self.shadow_rect, border_radius = self.rounding)
        pygame.draw.rect(screen,BUTTON_BACKGROUND_COL,self.rect, border_radius = self.rounding)
        pygame.draw.rect(screen,BUTTON_OUTLINE_COLOUR,self.rect,2, border_radius = self.rounding)
        simple_text_lines(self.text_lines, self.text_pos,black)

class LevelList(MenuItem):
    def __init__(self):
        super().__init__(LEVEL_LIST_RECT,background_col=dark_teal)
        self.switch_list(LEVEL_SETTINGS)
    def switch_list(self,ch_level_settings):
        self.ch_level_settings = ch_level_settings
        self.items = [(settings[0], settings[1]) for settings in ch_level_settings] # (name, mode)
    def draw(self,m_co):
        super().draw()
        for c,item in enumerate(self.items):
            pos = dA(dA(self.rect[:2], LEVEL_LIST_ITEM_RECT), dSM(c, (0, LEVEL_LIST_GAP+LEVEL_LIST_ITEM_RECT[3])))
            rect = list(pos) + LEVEL_LIST_ITEM_RECT[2:]
            sel_col = BUTTON_HOVER_COL if in_rect(m_co, rect) else BUTTON_BACKGROUND_COL
            pygame.draw.rect(screen, sel_col, rect)
            pygame.draw.rect(screen, black, rect, 2)
            simple_text(item[0], dA(pos,LEVEL_LIST_TEXT_OFFSET), black, font=LEVEL_LIST_FONT)
    def onPressDown(self,m_co):
        for c,item in enumerate(self.items):
            pos = dA(dA(self.rect[:2], LEVEL_LIST_ITEM_RECT), dSM(c, (0, LEVEL_LIST_GAP+LEVEL_LIST_ITEM_RECT[3])))
            rect = list(pos) + LEVEL_LIST_ITEM_RECT[2:]
            if in_rect(m_co, rect):
                level_preview_menu(self.ch_level_settings[c])
        
class LevelPreview(MenuItem):
    def __init__(self,settings,quit_func):
        def comp_quit_func(): run_level(settings); quit_func()
        def reset_seed_func(): 
            copy = list(settings)
            copy[6] = randrange(0,100000)
            level_ind = [s[0] for s in LEVEL_SETTINGS].index(settings[0])
            LEVEL_SETTINGS[level_ind] = tuple(copy)
            self.name, self.gamemode, _, self.width, self.height, _, _, _, _ = LEVEL_SETTINGS[level_ind]
            sync_levels()

        super().__init__(LEVEL_PREVIEW_RECT,background_col=dark_teal)
        self.name, self.gamemode, _, self.width, self.height, _, _, _, _ = settings
        self.preview = level_previews[self.name]
        self.preview_pos = dA(self.rect[:2],(200,0))
        self.preview_rect = list(self.preview_pos) + list(IMAGE_PREVIEW_SIZE)
        self.sub_buttons = [
            MenuButton(LEVEL_PREVIEW_PLAY_RECT, "Play", comp_quit_func, shadow=(3,3), rounding=3, font=fancy_font_bigger),
            MenuButton(LEVEL_PREVIEW_RSET_RECT, "Reset Seed", reset_seed_func, shadow=(3,3), rounding=3, font=fancy_font_bigger)
        ]
        self.pressed_button = None
        self.pressed = False
        self.text_lines = [["Mode: Drag","Mode: Magic"][self.gamemode], "Size: "+str(self.width)+"x"+str(self.height)]
    def draw(self,m_co):
        screen.blit(self.preview,self.preview_pos)
        pygame.draw.rect(screen, GAME_BORDER_COL, self.preview_rect, 2)
        simple_text(self.name, LEVEL_PREVIEW_TEXT_RECT, font=fancy_font_underline, colour=black)
        simple_text_lines(self.text_lines, dA(LEVEL_PREVIEW_TEXT_RECT,[0,50]),font=fancy_font_bigger, colour=black)
        for b in self.sub_buttons: b.draw(m_co)
    def onPressDown(self,m_co):
        for b in self.sub_buttons:
            if b.inButton(m_co):
                self.pressed = True
                self.pressed_button = b
                b.onPressDown()
    def onPressUp(self,m_co):
        for b in self.sub_buttons:
            if b.inButton(m_co):
                if self.pressed_button == b: b.onPressUp()
        if self.pressed_button != None: self.pressed_button.onPressRelease()
        self.pressed_button = None
        self.pressed = False
    def onPressRelease(self):
        if self.pressed_button != None: self.pressed_button.onPressRelease()
        self.pressed_button = None
        self.pressed = False

# Game Classes
class Tile:
    def __init__(self, parent_level, pos):
        self.parent_level, self.pos = parent_level, pos
        self.original_pos = pos
        self.is_pivot = self.original_pos in self.parent_level.pivot_pos_list
        self.sync_graphics()
    def sync_graphics(self):
        self.draw_pos = self.parent_level.calculate_tile_pos(self.pos)
        self.cent = [self.draw_pos[n]+self.parent_level.tile_size//2 for n in range(2)]
        self.surf = pygame.Surface([self.parent_level.tile_size]*2)
        if self.parent_level.picture_source == None: #colour mode
            self.colour = self.parent_level.col_formula(*self.original_pos, self.parent_level.width, self.parent_level.height)
            self.surf.fill(self.colour)
        else:
            self.surf = pygame.transform.scale(self.parent_level.crop_imgs[self.original_pos[1]][self.original_pos[0]], [self.parent_level.tile_size]*2)
        if self.is_pivot: pygame.draw.circle(self.surf, black, [self.parent_level.tile_size//2]*2, 3)
    def move(self,new_pos):
        self.pos = new_pos
        self.draw_pos = self.parent_level.calculate_tile_pos(new_pos)
        self.sync_graphics()
    def draw(self,force_pos=None):
        screen.blit(self.surf, (self.draw_pos if force_pos == None else force_pos))
    def check_correct(self):
        return self.original_pos == self.pos

class TileLevel:
    def __init__(self, settings):
        self.level_name, self.gamemode,self.picture_source, self.width, self.height, self.col_formula, self.randomize_seed, self.shuffle_n, self.pivot_pos_list = settings
        
        if self.picture_source != None: self.crop_imgs = cropped_images['_'.join([picture_source,str(self.width),str(self.height)])]

        self.grid_rect = (0,0,self.width,self.height)
        self.resize_update()
        self.tiles = [[Tile(self, (x,y)) for x in range(self.width)] for y in range(self.height)]
        self.animations = [] # [ [(tile obj, old_pos, new_pos, total_life), ticks_alive], ... ]


        if self.gamemode == CODE_GMDE_GAPS:
            self.empty_pos = (3,3)
            self.tiles[self.empty_pos[1]][self.empty_pos[0]] = None
            self.gap_randomize_tiles()
        elif self.gamemode == CODE_GMDE_DRAG:
            self.drag_randomize_tiles()
            if ANMTN_INIT_ENABLED:
                for row in self.tiles:
                    for tile in row:
                        if not tile.check_correct():
                            self.animations.append([(tile, tile.original_pos, tile.pos, ANMTN_INIT_DUR),0])
        self.draw_preview()
    def resize_update(self):
        self.map_margin = int(dw*GAME_BORDER)
        self.tile_size = int(min( (dw - self.map_margin*2)/self.width, (dh - self.map_margin*2)/self.height ))
        self.map_rect = (self.map_margin, self.map_margin, self.tile_size*self.width, self.tile_size*self.height)
    def calculate_tile_pos(self, t_pos):
        return ( self.map_margin + t_pos[0]*self.tile_size, self.map_margin + t_pos[1]*self.tile_size )
    def check_won(self):
        return all([all([self.tiles[y][x] == None or self.tiles[y][x].check_correct() for x in range(self.width)]) for y in range(self.height)])
    def draw(self,held_tile=None,held_draw_pos=None):
        pygame.draw.rect(screen, dark_teal, self.map_rect, border_radius=1)
        animated_tiles = [i[0][2] for i in self.animations]
        for y,row in enumerate(self.tiles):
            for x,item in enumerate(row):
                if (item != None) and ((x,y) != held_tile) and (not (x,y) in animated_tiles): item.draw()
        pygame.draw.rect(screen, GAME_BORDER_COL, self.map_rect, 2, border_radius=1)

        for a in self.animations:
            ticks_alive = a[1]
            tile_obj, old_pos, new_pos, total_life = a[0]
            alive_frac = ticks_alive/total_life

            tile_obj.draw(self.calculate_tile_pos(between_point(old_pos, new_pos, ANMTN_DRAG_FUNC(alive_frac))))
        if held_tile != None: self.tiles[held_tile[1]][held_tile[0]].draw(held_draw_pos)
    def draw_preview(self):
        self.preview_surf = pygame.Surface(self.map_rect[2:])
        for _,row in enumerate(self.tiles):
            for _,item in enumerate(row):
                if item != None: self.preview_surf.blit(item.surf, dSM(self.tile_size, item.original_pos))
        pygame.draw.rect(self.preview_surf, GAME_BORDER_COL, [0,0]+list(self.map_rect[2:]),2)
        return self.preview_surf
    def d_to_r(self, d_pos):
        return tuple([(d_pos[n]-self.map_margin)//self.tile_size for n in range(2)])
    def get_grid_pos(self, d_pos):
        r_pos = self.d_to_r(d_pos)
        return r_pos if in_rect(r_pos,self.grid_rect) else None
    def update_animations(self):
        to_del = []
        for c,item in enumerate(self.animations):
            item[1] += 1
            if item[1] >= item[0][3]: to_del.append(c)
        for c in to_del[::-1]: del self.animations[c]
    def update(self):
        self.update_animations()
    ### Gap Mode Functions
    def gap_move_tile(self, t, show_animation=False):
        t_pos = t.pos
        nes = [dA(t_pos, ne) for ne in NEIGHBOURS]
        if self.empty_pos in nes and not t.pos in self.pivot_pos_list:
            e_pos = self.empty_pos
            t.move(e_pos)
            self.empty_pos = t_pos
            
            self.tiles[e_pos[1]][e_pos[0]] = t
            self.tiles[t_pos[1]][t_pos[0]] = None

            if show_animation: self.animations.append([(t, t_pos, e_pos, ANMTN_DRAG_DUR),0])
            return True
        else:
            return False
    def gap_randomize_tiles(self):
        seed(self.randomize_seed)
        for _ in range(self.shuffle_n):
            em_nes = [pos for pos in [dA(ne, self.empty_pos) for ne in NEIGHBOURS] if in_rect(pos, self.grid_rect)]
            chosen = choice(em_nes)
            self.gap_move_tile(self.tiles[chosen[1]][chosen[0]])
        seed(datetime.now().second)#fix randomness
    def gap_try_move(self, t, show_animation=False):
        if t == None or self.tiles[t[1]][t[0]] == None: return False
        else: return self.gap_move_tile(self.tiles[t[1]][t[0]], show_animation)
    ### Drag Mode Functions
    def drag_swap_tiles(self, t_1, t_2, show_animations=(False,False)):
        t_1_pos = t_1.pos
        t_2_pos = t_2.pos

        t_1.move(t_2_pos)
        self.tiles[t_2_pos[1]][t_2_pos[0]] = t_1
        if show_animations[0]: #animiation for t_1 moving to t_2_pos
            self.animations.append( [(t_1,t_1_pos,t_2_pos,ANMTN_DRAG_DUR),0])

        t_2.move(t_1_pos)
        self.tiles[t_1_pos[1]][t_1_pos[0]] = t_2
        if show_animations[1]: #animation for t_2 moving to t_1_pos
            self.animations.append( [(t_2,t_2_pos,t_1_pos,ANMTN_DRAG_DUR),0])
    def drag_randomize_tiles(self):
        seed(self.randomize_seed)
        for _ in range(self.shuffle_n):
            p_1 = (randrange(0,self.width), randrange(0,self.height))
            p_2 = (randrange(0,self.width), randrange(0,self.height))
            while (p_1 in self.pivot_pos_list) or (p_2 in self.pivot_pos_list):
                p_1 = (randrange(0,self.width), randrange(0,self.height))
                p_2 = (randrange(0,self.width), randrange(0,self.height))
            self.drag_swap_tiles(self.tiles[p_1[1]][p_1[0]], self.tiles[p_2[1]][p_2[0]])
        seed(datetime.now().second)#fix randomness
    def drag_try_swap(self, t_1, t_2, show_animations=(False,False)):
        if t_1 in self.pivot_pos_list or t_2 in self.pivot_pos_list or None in [t_1,t_2]: 
            return False
        else:
            self.drag_swap_tiles(self.tiles[t_1[1]][t_1[0]], self.tiles[t_2[1]][t_2[0]], show_animations)
            return True

###================================================================
###                           Main Loops
###================================================================

def pause_menu(quit_func=quit_all,show_img=None): #show_img = (img, pos)
    pause_exit = [False]
    def unpause(): pause_exit[0] = True
    def comp_quit_func():
        quit_func()
        unpause()
    
    buttons = [
        MenuButton(PAUSE_BUTTON_RECT, ">", unpause, rounding=6, shadow=SMALL_BUTTON_SHADOW_OFFSET, shadow_col=SMALL_BUTTON_SHADOW_COL),
        MenuButton(QUIT_BUTTON_RECT, "X", comp_quit_func, rounding=6, shadow=SMALL_BUTTON_SHADOW_OFFSET, shadow_col=SMALL_BUTTON_SHADOW_COL)
    ]

    prev_screen = pygame.Surface((dw,dh), pygame.SRCALPHA)
    prev_screen.blit(screen,(0,0))
    
    #Draw Background colour around menu buttons (Manual override for edge case with hint menu)
    pygame.draw.rect(prev_screen, MAIN_BACKGROUND_COL, PAUSE_BUTTON_RECT)
    pygame.draw.rect(prev_screen, MAIN_BACKGROUND_COL, QUIT_BUTTON_RECT)

    fill_surf = pygame.Surface((dw,dh), pygame.SRCALPHA)
    fill_surf.fill((0,0,0,128))
    prev_screen.blit(fill_surf,(0,0))
    if show_img != None: prev_screen.blit(*show_img)



    down_press_button = None
    while not pause_exit[0]:
        m_co = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); quit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pause_exit[0] = True
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressDown()
                            down_press_button = b
                            break
            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressUp()
                            break
                    if down_press_button != None:
                        down_press_button.onPressRelease()
                        down_press_button = None
        
        screen.fill(MAIN_BACKGROUND_COL)
        screen.blit(prev_screen,(0,0))
        for b in buttons: b.draw(m_co)
        PDU()

        clock.tick(PAUSE_FPS)

def text_menu(text):
    menu_exit = [False]
    def unpause(): menu_exit[0] = True

    menu_items = [
        MenuButton(QUIT_BUTTON_RECT, "X", unpause, rounding=6, shadow=SMALL_BUTTON_SHADOW_OFFSET, shadow_col=SMALL_BUTTON_SHADOW_COL),
        TextBox(BIG_TEXT_RECT, text, fancy_font)
    ]
    down_press_button = None
    while not menu_exit[0]:
        m_co = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); quit()
            elif ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    menu_exit[0] = True
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    for b in menu_items:
                        if b.inButton(m_co): 
                            b.onPressDown()
                            down_press_button = b
                            break
            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    for b in menu_items:
                        if b.inButton(m_co): 
                            b.onPressUp()
                            break
                    if down_press_button != None:
                        down_press_button.onPressRelease()
                        down_press_button = None
        screen.fill(MAIN_BACKGROUND_COL)
        for b in menu_items: b.draw(m_co)
        PDU()

        clock.tick(PAUSE_FPS)

def preview_menu(quit_func, level):
    pause_menu(quit_func, (level.preview_surf, level.map_rect[:2]))

def level_select():
    menu_exit = [False]
    def quit_func(): menu_exit[0] = True
    buttons = [
        MenuButton(QUIT_BUTTON_RECT, "X", quit_func, rounding=6, shadow=SMALL_BUTTON_SHADOW_OFFSET, shadow_col=SMALL_BUTTON_SHADOW_COL),
        LevelList(),
        MenuButton(LEVEL_CREATE_RECT, "Create Level", level_create_menu, rounding=6,shadow=(4,4), shadow_col=SMALL_BUTTON_SHADOW_COL)
    ]

    # Make New Buttons for chapters
    level_list_b = buttons[1]
    other_buttons = len(buttons)
    ch_num = 0
    for ch_name, ch_len in CHAPTERS:
        rect = list(dA(LEVEL_LIST_BUTTON_RECT[:2], (0,45*ch_num))) + LEVEL_LIST_BUTTON_RECT[2:]
        new_button = SelectionButton(rect,ch_name,lambda s: level_list_b.switch_list(CHAPTER_LEVELS[s.text]), font=fancy_font,rounding=2,shadow=(3,3))
        buttons.append(new_button)
        ch_num += 1
    
    # Assign Selection Buttons to Each Other
    for b in buttons[other_buttons:]:
        others = buttons[other_buttons:][:]
        others.remove(b)
        b.set_other_buttons(others)
    
    buttons[other_buttons].onPressDown() #select first chapter
    

    ticks = 0
    down_press_button = None
    while not menu_exit[0]:
        # keys_pressed = pygame.key.get_pressed()
        m_co = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressDown(m_co)
                            down_press_button = b
                            break
            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressUp()
                            break
                    if down_press_button != None:
                        down_press_button.onPressRelease()
                        down_press_button = None
        
        screen.fill(MAIN_BACKGROUND_COL)
        for b in buttons: b.draw(m_co)
        
        PDU()

        clock.tick(MENU_FPS)
        ticks += 1

def level_preview_menu(settings):
    menu_exit = [False]
    def quit_func(): menu_exit[0] = True
    buttons = [
        MenuButton(QUIT_BUTTON_RECT, "X", quit_func, rounding=6, shadow=SMALL_BUTTON_SHADOW_OFFSET, shadow_col=SMALL_BUTTON_SHADOW_COL),
        LevelPreview(settings, quit_func)
    ]

    ticks = 0
    down_press_button = None
    while not menu_exit[0]:
        # keys_pressed = pygame.key.get_pressed()
        m_co = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressDown(m_co)
                            down_press_button = b
                            break
            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressUp(m_co)
                            break
                    if down_press_button != None:
                        down_press_button.onPressRelease()
                        down_press_button = None
        
        screen.fill(MAIN_BACKGROUND_COL)
        for b in buttons: b.draw(m_co)
        
        PDU()

        clock.tick(MENU_FPS)
        ticks += 1

def shop_menu():
    menu_exit = [False]
    def quit_func(): menu_exit[0] = True
    buttons = [
        MenuButton(QUIT_BUTTON_RECT, "X", quit_func, rounding=6, shadow=SMALL_BUTTON_SHADOW_OFFSET, shadow_col=SMALL_BUTTON_SHADOW_COL),
    ]
    ticks = 0
    down_press_button = None
    while not menu_exit[0]:
        # keys_pressed = pygame.key.get_pressed()
        m_co = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressDown()
                            down_press_button = b
                            break
            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressUp()
                            break
                    if down_press_button != None:
                        down_press_button.onPressRelease()
                        down_press_button = None
        
        screen.fill(MAIN_BACKGROUND_COL)
        for b in buttons: b.draw(m_co)
        
        PDU()

        clock.tick(MENU_FPS)
        ticks += 1

def level_create_menu():
    menu_exit = [False]
    def quit_func(): menu_exit[0] = True
    buttons = [
        MenuButton(QUIT_BUTTON_RECT, "X", quit_func, rounding=6, shadow=SMALL_BUTTON_SHADOW_OFFSET, shadow_col=SMALL_BUTTON_SHADOW_COL),
    ]
    ticks = 0
    down_press_button = None
    while not menu_exit[0]:
        m_co = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressDown()
                            down_press_button = b
                            break
            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressUp()
                            break
                    if down_press_button != None:
                        down_press_button.onPressRelease()
                        down_press_button = None
        
        screen.fill(MAIN_BACKGROUND_COL)
        for b in buttons: b.draw(m_co)
        
        PDU()

        clock.tick(MENU_FPS)
        ticks += 1

def run_level(settings):
    game_exit = [False]
    def quit_level(): game_exit[0] = True
    def pmenu_quit_func():
        quit_level()

    level = TileLevel(settings)
    gamemode = level.gamemode
    drag_mouse_down = False
    down_press_button = None
    won = False
    buttons = [
        MenuButton(PAUSE_BUTTON_RECT, "||", lambda : pause_menu(pmenu_quit_func), rounding=6, font=PAUSE_BUTTON_FONT, shadow=SMALL_BUTTON_SHADOW_OFFSET, shadow_col=SMALL_BUTTON_SHADOW_COL),
        MenuButton(QUIT_BUTTON_RECT, "X", quit_level, rounding=6, shadow=SMALL_BUTTON_SHADOW_OFFSET, shadow_col=SMALL_BUTTON_SHADOW_COL),
        MenuButton(HINT_BUTTON_RECT, "?", lambda : preview_menu(pmenu_quit_func, level), rounding=6, shadow=SMALL_BUTTON_SHADOW_OFFSET, shadow_col=SMALL_BUTTON_SHADOW_COL)
    ]
    while not game_exit[0]:
        m_co = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1: #Left Click Down
                    pressed = False
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressDown()
                            down_press_button = b
                            pressed = True
                            break
                    if not pressed:
                        if gamemode == CODE_GMDE_GAPS:
                            drag_mouse_down_pos = level.get_grid_pos(m_co)
                            level.gap_try_move(drag_mouse_down_pos, True)
                            won = level.check_won()
                        elif gamemode == CODE_GMDE_DRAG:
                            drag_mouse_down = True
                            drag_mouse_down_pos = level.get_grid_pos(m_co)
                            if drag_mouse_down_pos in level.pivot_pos_list: drag_mouse_down_pos = None
                            if drag_mouse_down_pos != None: mouse_offset = dS(level.calculate_tile_pos(drag_mouse_down_pos), m_co)
            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1: #Left Click Up
                    if down_press_button != None:
                        for b in buttons:
                            if b.inButton(m_co): 
                                b.onPressUp()
                                break
                        down_press_button.onPressRelease()
                        down_press_button = None
                    elif drag_mouse_down:
                        if gamemode == CODE_GMDE_DRAG:
                            drag_mouse_down = False
                            mouse_up_pos = level.get_grid_pos(m_co)
                            level.drag_try_swap(drag_mouse_down_pos, mouse_up_pos, (False, True))
                            won = level.check_won()

        if not game_exit[0]:
            level.update()

            screen.fill(MAIN_BACKGROUND_COL)
            if gamemode == CODE_GMDE_GAPS:
                level.draw()
            elif gamemode == CODE_GMDE_DRAG:
                if drag_mouse_down and drag_mouse_down_pos != None: level.draw(drag_mouse_down_pos, dA(m_co, mouse_offset))
                else: level.draw()
            
            for b in buttons: b.draw(m_co)

            if won:
                simple_text("Won!")

            PDU()

        clock.tick(GAME_FPS)

def main_menu():
    menu_exit = [False]
    buttons = [
        MenuButton(QUIT_BUTTON_RECT,    "X",            quit_all,                                   rounding=6, shadow=SMALL_BUTTON_SHADOW_OFFSET, shadow_col=SMALL_BUTTON_SHADOW_COL),
        MenuButton(PLAY_BUTTON_RECT,    "Play Random",  lambda : run_level(choice(LEVEL_SETTINGS)), rounding=10, font=PLAY_BUTTON_FONT, shadow=MENU_SHADOW_OFFSET, shadow_col=MENU_SHADOW_COL),
        MenuButton(LEVEL_BUTTON_RECT,   "Levels",       level_select,                               rounding=6, font=MENU_BUTTON_FONT, shadow=MENU_SHADOW_OFFSET, shadow_col=MENU_SHADOW_COL),
        MenuButton(SHOP_BUTTON_RECT,    "Shop",         shop_menu,                                  rounding=6, font=MENU_BUTTON_FONT, shadow=MENU_SHADOW_OFFSET, shadow_col=MENU_SHADOW_COL),
        MenuButton(CREDIT_BUTTON_RECT,  "Credit",       lambda : text_menu(CREDIT_MENU_DESCR),      rounding=6, font=MENU_BUTTON_FONT, shadow=MENU_SHADOW_OFFSET, shadow_col=MENU_SHADOW_COL),
        MenuButton(HELP_BUTTON_RECT,    "Help",         lambda : text_menu(HELP_MENU_DESC),         rounding=6, font=MENU_BUTTON_FONT, shadow=MENU_SHADOW_OFFSET, shadow_col=MENU_SHADOW_COL)
    ]
    ticks = 0
    down_press_button = None
    while not menu_exit[0]:
        # keys_pressed = pygame.key.get_pressed()
        m_co = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressDown()
                            down_press_button = b
                            break
            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    for b in buttons:
                        if b.inButton(m_co): 
                            b.onPressUp()
                            break
                    if down_press_button != None:
                        down_press_button.onPressRelease()
                        down_press_button = None
        
        screen.fill(MAIN_BACKGROUND_COL)
        cent_text("Tile Arranger",MENU_TEXT_POS, TITLE_COL, TITLE_FONT)
        for b in buttons: b.draw(m_co)
        
        PDU()

        clock.tick(MENU_FPS)
        ticks += 1


###================================================================
###                                Main
###================================================================


# Import Pictures
image_files = [file for file in Path("source/images/").glob("**/*") if file.is_file() and any([file.name.endswith(f_type) for f_type in ALLOWED_IMAGE_TYPES])] #Import files with only allowed file types
raw_images = {}
for path in image_files:
    print("Importing",str(path))
    file_name = path.name.split('.')[0]
    raw_images[file_name] = pygame.image.load(str(path))

# Set Up Image Cuts and Image Previews
cropped_images = {}
level_previews = {}
level_num = 0
for level_name, _, picture_source, width, height, _, _, _, _ in LEVEL_SETTINGS:
    # Image Cuts
    if picture_source != None:
        image_name = '_'.join([picture_source, str(width), str(height)])
        image = raw_images[picture_source]
        img_width, img_height = image.get_width(), image.get_height()

        square_size = decide_img_square_size((img_width,img_height),(width,height))
        cropped_images[image_name] = cut_image(image, (width,height), square_size)
    
    # Image Previews
    temp_level = TileLevel(LEVEL_SETTINGS[level_num])
    level_previews[level_name] = pygame.transform.scale(temp_level.preview_surf, IMAGE_PREVIEW_SIZE)

    # Increment
    level_num += 1

del temp_level #clean up

# Import Custom Levels
CHAPTERS.append( ("Custom", 0)) #FIXME toimplement

sync_levels()

main_menu()