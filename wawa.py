import pygame
import random
import math

window_width = h = 1280
window_height = v = 720
hv = (h,v)
screen = pygame.display.set_mode(hv)
clock = pygame.time.Clock()

#troop event flags
troop_event_flag = False
troop_list = list()
troop_count = 10

#waypoint test event flags
waypoint_event_flag = False
waypoint_list = list()

#barrier test event flag
barrier_ef = False
barrier_count = 10
barrier_list = list()
#troop class
class troop():
    def __init__(self,x,y) -> None:
        self.position = pygame.Vector2(x,y)
        self.jitter = 1
        self.speed = 6
        pass
    def render(self): 
        pygame.draw.circle(screen,'red',(self.position),5)
    #
    def move_to_waypoint(self,target_position) -> None:

        self.position.move_towards_ip(target_position,1)

        pass

#class barrier
class barrier():
    def __init__(self, rect) -> None:
        self.rect = rect
        pass
    def render(self):
        pygame.draw.rect(screen,'white',self.rect)
        pass
#create waypoint class
class waypoint():
    def __init__(self,position,ID) -> None:
        self.position = position
        self.ID = ID
        pass
    def render(self):
        pygame.draw.circle(screen,'green',(self.position),5) #waypoints are displayed as green circles

#running while loop
running = True
while running:
    #quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pass
        pass
    pass

    #troop test event
    if troop_event_flag == False:
        troop_event_flag = True
        for i in range(troop_count):
            tx,ty = random.randint(0,h),random.randint(0,v)
            troop_list.append(troop(tx,ty))
            pass
        pass

    #waypoint test event
        if waypoint_event_flag == False:
            waypoint_event_flag = True
            wp_position = pygame.Vector2(random.randint(0,h),random.randint(0,v))
            waypoint_list.append(waypoint(wp_position,5))
    #barrier test event
        if barrier_ef == False:
            barrier_ef = True
            for i in range(barrier_count):
                rect = pygame.Rect(random.randint(0,h),random.randint(0,v),10,100)
                barrier_list.append(barrier(rect))
    #screen refresh event
    screen.fill('black')

    #render events under here

    # render waypoints
    for i in waypoint_list:
        i.render()
        pass
    # render troops
    for unit in troop_list:
        unit.render()
        for i in waypoint_list:
            unit.move_to_waypoint(i.position)
            pass
        pass
    #render barriers
    for i in barrier_list:
        i.render()
        pass
    #flip screen event
    pygame.display.flip()

    #clock frame event
    clock.tick(60)

pygame.quit()