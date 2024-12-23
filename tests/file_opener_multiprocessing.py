import pygame
from random import randrange, seed, choice
import multiprocessing

import easygui


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

ALLOWED_FILE_TYPES = [".png",".svg",".jpeg",".webp"]
opened_files = []
def pick_file(dest=opened_files):
     # we don't want a full GUI, so keep the root window from appearing
    filename = easygui.fileopenbox()
    print("Selected",filename)
    dest.append(filename)
    exit() #exit once thread is complete

current_threads = []
thread_num = 0 #when converting code, check scope #FIXME


game_exit = False
ticks = 0
won = False
fps = 0
while not game_exit:
    m_co = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit(); quit()
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            pass
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_o:
                if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                    new_thread = multiprocessing.Process(target=pick_file, name="Open"+str(thread_num), daemon=True)
                    new_thread.start()
                    thread_num += 1
                    current_threads.append(new_thread)
            elif ev.key == pygame.K_ESCAPE:
                print("escaping!")
                n_thr = len(current_threads)
                for c in range(n_thr):
                    ind = n_thr-c-1
                    current_threads[c].terminate()
                    current_threads.remove(current_threads[c])
                    
                # current_threads = []
    
    #delete dead threads
    to_del = []
    for c,thread in enumerate(current_threads):
        if not thread.is_alive(): to_del.append(c)
    for c in to_del[::-1]: current_threads.remove(current_threads[c])


    screen.fill((0,255-(ticks%256), ticks%256))
    
    for c,i in enumerate(["Files:"]+opened_files):
        simple_text(i, (5,5+c*30))

    simple_text(str(round(fps,2)), (dw-50,5))
    PDU()

    clock.tick(30)
    fps = clock.get_fps()
    ticks += 1