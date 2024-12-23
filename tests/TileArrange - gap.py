import pygame
from random import randrange, seed, choice

GAME_FPS = 60
MENU_FPS = 60
PAUSE_FPS = 5

GAME_BORDER = 0.1 #Game Border as percent of screen size

ANMTN_DRAG_DUR = 10
ANMTN_DRAG_FUNC = lambda frac : frac**(0.8)

ANMTN_INIT_DUR = 120
ANMTN_INIT_ENABLED = True

NEIGHBOURS = [(1,0),(0,1),(-1,0),(0,-1)]


pygame.init()
screen = pygame.display.set_mode((600,600))
dw,dh = pygame.display.get_surface().get_size()
display_width, display_height = dw,dh
pygame.display.set_caption("Tile Arrange")
clock = pygame.time.Clock()

pygame.font.init()
myFont = pygame.font.SysFont("monospace", 50)
fancyFont = pygame.font.SysFont("calibri", 22)

black = (0,0,0); lightgray = (150,150,150); darklightgray = (100,100,100); white = (255,255,255); red = (255,0,0); green = (0,255,0); blue = (0,0,255); darkgray = (50,50,50); brown = (101,67,33); darkorange = (255,100,0); darkgreen = (0,100,0); darkred = (139,0,0); yellow = (255,255,0); whiteskin = (255,195, 170); yellow = (255,255,0); darkyellow = (204,204,0); purple = (128,0,128); lightblue = (50,50,255)



PDU = pygame.display.update

def text_objects(text,font,colour=white):
    textSurface = font.render(text,True,colour)
    return(textSurface, textSurface.get_rect())
def simple_text(inputText,co=(0,0),colour=white,simpleFont = fancyFont):
    text = simpleFont.render(inputText, True, colour)
    screen.blit(text,co)
def cent_text(inputText,center,colour=white,font=myFont):#draws text to the screen anchored on the centre of the given position
    textSurf, textRect = text_objects(inputText,font,colour)#generates the text surface and rectangle
    textRect.center = center#centres the text
    screen.blit(textSurf,textRect)#blits the text to the screen
def in_rect(co,rect): return co[0] >= rect[0] and co[1] >= rect[1] and co[0] < rect[0]+rect[2] and co[1] < rect[1]+rect[3]

def dA(d1,d2): return (d1[0]+d2[0], d1[1]+d2[1])
def dS(d1,d2): return (d1[0]-d2[0], d1[1]-d2[1])

def between_point(co1,co2,n=0.5): return [ (co1[c]*(1-n) + co2[c]*n) for c in range(2) ]

class Tile:
    def __init__(self, parent_level, pos):
        self.parent_level, self.pos = parent_level, pos
        self.colour = self.parent_level.col_formula(*pos)
        self.original_pos = pos
        self.is_pivot = self.original_pos in self.parent_level.pivot_pos_list
        self.sync_graphics()
    def sync_graphics(self):
        self.draw_pos = self.parent_level.calculate_tile_pos(self.pos)
        self.cent = [self.draw_pos[n]+self.parent_level.tile_size//2 for n in range(2)]
    def move(self,new_pos):
        self.pos = new_pos
        self.draw_pos = self.parent_level.calculate_tile_pos(new_pos)
        self.sync_graphics()
    def draw(self,force_pos=None):
        pygame.draw.rect(screen, self.colour, (*(self.draw_pos if force_pos == None else force_pos), self.parent_level.tile_size, self.parent_level.tile_size))
        if self.is_pivot:
            pygame.draw.circle(screen, black, self.cent, 3)
    def check_correct(self):
        return self.original_pos == self.pos

class TileLevel:
    def __init__(self, settings):
        if settings == None:
            self.width = self.height = 5
            self.col_formula = lambda x,y : (255-40*x, 255-40*y, 128)
            self.pivot_pos_list = [(0,0),(self.width-1,0),(self.width-1,self.height-1),(0,self.height-1)]
            self.randomize_seed = 0
        else:
            self.width, self.height, self.col_formula, self.pivot_pos_list = settings
        
        self.grid_rect = (0,0,self.width,self.height)
        self.resize_update()
        self.tiles = [[Tile(self, (x,y)) for x in range(self.width)] for y in range(self.height)]
        self.empty_pos = (3,3)
        self.tiles[self.empty_pos[1]][self.empty_pos[0]] = None

        self.randomize_tiles()      
        self.animations = [] # [ [(tile obj, old_pos, new_pos, total_life), ticks_alive], ... ]
    def resize_update(self):
        self.map_margin = int(dw*GAME_BORDER)
        self.tile_size = int(min( (dw - self.map_margin*2)/self.width, (dh - self.map_margin*2)/self.height ))
        self.map_rect = (self.map_margin, self.map_margin, self.tile_size*self.width, self.tile_size*self.height)
    def calculate_tile_pos(self, t_pos):
        return ( self.map_margin + t_pos[0]*self.tile_size, self.map_margin + t_pos[1]*self.tile_size )
    def move_tile(self, t, show_animation=False):
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
    def randomize_tiles(self, n=1000):
        for _ in range(n):
            em_nes = [pos for pos in [dA(ne, self.empty_pos) for ne in NEIGHBOURS] if in_rect(pos, self.grid_rect)]
            chosen = choice(em_nes)
            self.move_tile(self.tiles[chosen[1]][chosen[0]])
    def check_won(self):
        return all([all([self.tiles[y][x] == None or self.tiles[y][x].check_correct() for x in range(self.width)]) for y in range(self.height)])
    def draw(self,held_tile=None,held_draw_pos=None):
        animated_tiles = [i[0][2] for i in self.animations]
        for y,row in enumerate(self.tiles):
            for x,item in enumerate(row):
                if (item != None) and ((x,y) != held_tile) and (not (x,y) in animated_tiles): item.draw()
        pygame.draw.rect(screen, white, self.map_rect, 2)

        for a in self.animations:
            ticks_alive = a[1]
            tile_obj, old_pos, new_pos, total_life = a[0]
            alive_frac = ticks_alive/total_life

            tile_obj.draw(self.calculate_tile_pos(between_point(old_pos, new_pos, ANMTN_DRAG_FUNC(alive_frac))))
            


        if held_tile != None: self.tiles[held_tile[1]][held_tile[0]].draw(held_draw_pos)
    def d_to_r(self, d_pos):
        return tuple([(d_pos[n]-self.map_margin)//self.tile_size for n in range(2)])
    def get_grid_pos(self, d_pos):
        r_pos = self.d_to_r(d_pos)
        return r_pos if in_rect(r_pos,self.grid_rect) else None
    def try_move(self, t, show_animation=False):
        if self.tiles[t[1]][t[0]] == None: return False
        else: return self.move_tile(self.tiles[t[1]][t[0]], show_animation)
    def update_animations(self):
        to_del = []
        for c,item in enumerate(self.animations):
            item[1] += 1
            if item[1] >= item[0][3]: to_del.append(c)
        for c in to_del[::-1]: del self.animations[c]
    def update(self):
        self.update_animations()





def run_level(settings=None):
    game_exit = False
    level = TileLevel(settings)
    won = False
    while not game_exit:
        m_co = pygame.mouse.get_pos()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); quit()
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1: #Left Click Down
                    mouse_down_pos = level.get_grid_pos(m_co)
                    level.try_move(mouse_down_pos, True)


        level.update()

        screen.fill(black)
        level.draw()
        
        if won:
            simple_text("Won!")

        PDU()

        clock.tick(GAME_FPS)

run_level(None)