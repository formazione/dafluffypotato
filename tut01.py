import pygame, sys, os, random
from pygame.locals import *



def load_animation(path: str, frame_durations: list) -> list:
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations: # frame_duration = [7,7]
        animation_frame_id = animation_name + '_' + str(n) # ....run\run_0
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc).convert()
        animation_image.set_colorkey((255,255,255))
        animation_frames[animation_frame_id] = animation_image.copy()
        # animation_frames["idle"] = 
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
            # animation_frame_data = ["run_0", "run_0", "run_0"... "run_1", "run_2"...]
        n += 1
    return animation_frame_data


global animation_frames
animation_frames = {}
animation_database = {}

class Animation:
	def __init__(self, action, time):
		animation_database[action] = load_animation(f"player_animations/{action}",[7,7])


pygame.init() # initiates pygame
pygame.mixer.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Exploring Newland')
WINDOW_SIZE = (600, 400)
screen = pygame.display.set_mode(WINDOW_SIZE,0 , 32)
display = pygame.Surface((600, 400))
# Variables to control the player movements
moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
true_scroll = [0,0] # control camera
CHUNK_SIZE = 8

Animation("run", [7,7])
Animation("idle", [7,7,40])

game_map = {}


#       SOUNDS
jump_sound = pygame.mixer.Sound('jump.wav')
grass_sounds = [pygame.mixer.Sound('grass_0.wav'), pygame.mixer.Sound('grass_1.wav')]
grass_sounds[0].set_volume(0.2)
grass_sounds[1].set_volume(0.2)

# SOUNDTRACK LOOP
pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1) # loop = -1

player_action = 'idle'
player_frame = 0
player_flip = False

grass_sound_timer = 0

player_rect = pygame.Rect(100, 100, 5, 13)
# player_rect.x = 100

background_objects = [
        [0.25,[120,10,70,400]], # obj 1 parallax 
        [0.25,[280,30,40,400]], # obj 2 ...
        [0.5,[30,40,40,400]],
        [0.5,[130,90,100,400]],
        [0.5,[300,80,120,400]]
        ]

def parallax():
    # horizontal scroll
    true_scroll[0] += (player_rect.x - true_scroll[0] - 152) / 20
    true_scroll[0] += (player_rect.x-true_scroll[0]-152)//20
    true_scroll[1] += (player_rect.y-true_scroll[1]-106)//20
    scroll = true_scroll.copy()
    # scroll[0] = int(scroll[0])
    # scroll[1] = int(scroll[1])

    # the parallax farest object
    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect( # this is slow, it's farer
            background_object[1][0]-scroll[0]*background_object[0],
            background_object[1][1]-scroll[1]*background_object[0],
            background_object[1][2],
            background_object[1][3])
        if background_object[0] == 0.5:
            # lighter and nearer - faster
            pygame.draw.rect(display,(20,170,150),obj_rect)
        else:
            # darker and farer - slower
            pygame.draw.rect(display,(15,76,73),obj_rect)


while True: # game loop
    display.fill((146,244,255))

    if grass_sound_timer > 0:
        grass_sound_timer -= 1
    parallax()

    for event in pygame.event.get(): # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE),(0,0))
    pygame.display.update()
    clock.tick(60)